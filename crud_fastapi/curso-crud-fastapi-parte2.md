# CURSO CRUD FASTAPI - PARTE 2 (SESIONES 11-20)

---

# SESIÓN 11: Consultas Avanzadas y Agregaciones

## Duración: 2 horas

## Objetivos de Aprendizaje

- Dominar consultas SQL complejas en SQLModel
- Implementar agregaciones (COUNT, SUM, AVG, MAX, MIN)
- Usar subconsultas y CTEs
- Implementar búsqueda full-text

## 11.1 Aggregaciones Básicas

```python
from sqlalchemy import select, func, and_, or_, case
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.producto import Producto
from app.models.orden import Orden, OrdenItem
from app.models.vendedor import Vendedor

# Contar productos
async def contar_productos(session: AsyncSession) -> int:
    result = await session.execute(
        select(func.count(Producto.id))
    )
    return result.scalar()

# SUM - Valor total del inventario
async def valor_inventario(session: AsyncSession):
    result = await session.execute(
        select(
            func.sum(Producto.precio * Producto.stock).label("valor_total")
        )
        .where(Producto.is_active == True)
    )
    return result.scalar()

# AVG - Precio promedio
async def precio_promedio(session: AsyncSession):
    result = await session.execute(
        select(
            func.avg(Producto.precio).label("precio_promedio")
        )
        .where(Producto.is_active == True)
    )
    return result.scalar()

# MIN/MAX - Productos más barato y caro
async def rango_precios(session: AsyncSession):
    result = await session.execute(
        select(
            func.min(Producto.precio).label("minimo"),
            func.max(Producto.precio).label("maximo")
        )
        .where(Producto.is_active == True)
    )
    row = result.one()
    return {"minimo": row.minimo, "maximo": row.maximo}
```

## 11.2 Group By y Having

```python
# Productos por categoría
async def productos_por_categoria(session: AsyncSession):
    result = await session.execute(
        select(
            Producto.categoria_id,
            func.count(Producto.id).label("total"),
            func.avg(Producto.precio).label("precio_promedio")
        )
        .where(Producto.is_active == True)
        .group_by(Producto.categoria_id)
        .order_by(func.count(Producto.id).desc())
    )
    return [
        {
            "categoria_id": row.categoria_id,
            "total_productos": row.total,
            "precio_promedio": float(row.precio_promedio) if row.precio_promedio else 0
        }
        for row in result.all()
    ]


# Vendedores con más productos (HAVING)
async def vendedores_con_mas_productos(session: AsyncSession, min_productos: int = 5):
    result = await session.execute(
        select(
            Vendedor.id,
            Vendedor.nombre_tienda,
            func.count(Producto.id).label("total_productos"),
            func.sum(Producto.stock).label("stock_total")
        )
        .join(Producto, Vendedor.id == Producto.vendedor_id)
        .where(Producto.is_active == True)
        .group_by(Vendedor.id, Vendedor.nombre_tienda)
        .having(func.count(Producto.id) >= min_productos)
        .order_by(func.count(Producto.id).desc())
    )
    return list(result.all())


# Productos con stock bajo
async def productos_stock_bajo(session: AsyncSession, umbral: int = 5):
    result = await session.execute(
        select(Producto)
        .where(
            and_(
                Producto.is_active == True,
                Producto.stock <= umbral
            )
        )
        .order_by(Producto.stock.asc())
    )
    return list(result.scalars().all())
```

## 11.3 Case y Condicionales

```python
# Clasificar productos por stock
async def clasificar_stock(session: AsyncSession):
    result = await session.execute(
        select(
            Producto.id,
            Producto.nombre,
            Producto.stock,
            case(
                (Producto.stock == 0, "Sin stock"),
                (Producto.stock <= 5, "Stock bajo"),
                (Producto.stock <= 20, "Stock medio"),
                else_="Stock alto"
            ).label("clasificacion")
        )
        .where(Producto.is_active == True)
    )
    return [
        {"id": row.id, "nombre": row.nombre, "stock": row.stock, "clasificacion": row.clasificacion}
        for row in result.all()
    ]


# Descuentos según cantidad
async def calcular_precio_con_descuento(session: AsyncSession):
    result = await session.execute(
        select(
            Producto.id,
            Producto.nombre,
            Producto.precio,
            case(
                (Producto.precio >= 1000, Producto.precio * Decimal("0.9")),   # 10% off
                (Producto.precio >= 500, Producto.precio * Decimal("0.95")),   # 5% off
                else_=Producto.precio
            ).label("precio_final")
        )
        .where(Producto.is_active == True)
    )
    return list(result.all())
```

## 11.4 Subconsultas

```python
# Productos cuyo precio es mayor al promedio
async def productos_precio_superior_promedio(session: AsyncSession):
    # Subconsulta para el promedio
    subquery = (
        select(func.avg(Producto.precio))
        .where(Producto.is_active == True)
        .scalar_subquery()
    )

    result = await session.execute(
        select(Producto)
        .where(
            and_(
                Producto.is_active == True,
                Producto.precio > subquery
            )
        )
        .order_by(Producto.precio.desc())
    )
    return list(result.scalars().all())


# Top 3 productos más vendidos por vendedor
async def top_productos_por_vendedor(session: AsyncSession):
    # Subconsulta: productos ordenados por cantidad vendida
    subquery = (
        select(
            OrdenItem.producto_id,
            func.sum(OrdenItem.cantidad).label("total_vendido")
        )
        .group_by(OrdenItem.producto_id)
        .subquery()
    )

    result = await session.execute(
        select(
            Producto.id,
            Producto.nombre,
            Producto.vendedor_id,
            subquery.c.total_vendido
        )
        .join(subquery, Producto.id == subquery.c.producto_id)
        .order_by(subquery.c.total_vendido.desc())
        .limit(3)
    )
    return list(result.all())


# Usuarios que han gastado más que el promedio
async def top_compradores(session: AsyncSession):
    subquery = (
        select(func.avg(Orden.total))
        .where(Orden.status != "cancelado")
        .scalar_subquery()
    )

    result = await session.execute(
        select(
            Orden.usuario_id,
            func.sum(Orden.total).label("total_gastado")
        )
        .where(
            and_(
                Orden.status != "cancelado",
                Orden.total > subquery
            )
        )
        .group_by(Orden.usuario_id)
        .order_by(func.sum(Orden.total).desc())
    )
    return list(result.all())
```

## 11.5 Búsqueda Full-Text

```python
from sqlalchemy import func, to_tsvector, to_tsquery, rank

# Búsqueda full-text en PostgreSQL
async def buscar_productos_fulltext(session: AsyncSession, query: str):
    """Búsqueda usando índice tsvector de PostgreSQL."""
    # Convertir query a tsquery
    ts_query = func.plainto_tsquery("spanish", query)

    result = await session.execute(
        select(
            Producto.id,
            Producto.nombre,
            Producto.descripcion,
            func.rank().label("rank")
        )
        .where(
            or_(
                func.to_tsvector("spanish", Producto.nombre).op("@@")(ts_query),
                func.to_tsvector("spanish", Producto.descripcion).op("@@")(ts_query)
            )
        )
        .order_by(rank.desc())
        .limit(20)
    )
    return list(result.all())


# Configurar índice tsvector en el modelo
# En la migración o directamente:
"""
ALTER TABLE productos ADD COLUMN busqueda_vector tsvector
GENERATED ALWAYS AS (
    setweight(to_tsvector('spanish', coalesce(nombre, '')), 'A') ||
    setweight(to_tsvector('spanish', coalesce(descripcion, '')), 'B')
) STORED;

CREATE INDEX idx_productos_busqueda ON productos USING GIN(busqueda_vector);

-- Búsqueda:
SELECT * FROM productos
WHERE busqueda_vector @@ plainto_tsquery('spanish', 'laptop gaming')
ORDER BY ts_rank(busqueda_vector, plainto_tsquery('spanish', 'laptop gaming')) DESC;
"""
```

## 11.6 Common Table Expressions (CTEs)

```python
from sqlalchemy import cte

# Análisis de ventas con CTE
async def analisis_ventas(session: AsyncSession):
    # CTE: Total de ventas por producto
    ventas_por_producto = (
        select(
            OrdenItem.producto_id,
            func.sum(OrdenItem.cantidad).label("unidades_vendidas"),
            func.sum(OrdenItem.cantidad * OrdenItem.precio_unitario).label("ingresos")
        )
        .join(Orden, Orden.id == OrdenItem.orden_id)
        .where(Orden.status == "entregado")
        .group_by(OrdenItem.producto_id)
        .cte("ventas_por_producto")
    )

    # Query principal usando el CTE
    result = await session.execute(
        select(
            Producto.id,
            Producto.nombre,
            ventas_por_producto.c.unidades_vendidas,
            ventas_por_producto.c.ingresos
        )
        .outerjoin(ventas_por_producto, Producto.id == ventas_por_producto.c.producto_id)
        .order_by(ventas_por_producto.c.ingresos.desc().nulls_last())
    )
    return list(result.all())


# CTE Recursivo para jerarquía de categorías
async def jerarquia_categoria(session: AsyncSession, categoria_id: int):
    # CTE base: categoría raíz
    base = (
        select(Categoria.id, Categoria.nombre, Categoria.parent_id)
        .where(Categoria.id == categoria_id)
        .cte("categoria_jerarquia", recursive=True)
    )

    # Parte recursiva: subcategorías
    recursivo = select(Categoria).join(base, Categoria.parent_id == base.c.id)
    jerarquia = base.union_all(recursivo)

    result = await session.execute(
        select(jerarquia)
    )
    return list(result.scalars().all())
```

## 11.7 Window Functions

```python
# Productos ordenados por precio con ranking
async def ranking_productos_por_precio(session: AsyncSession):
    result = await session.execute(
        select(
            Producto.id,
            Producto.nombre,
            Producto.precio,
            func.rank().over(
                order_by=Producto.precio.desc()
            ).label("rank_precio"),
            func.row_number().over(
                partition_by=Producto.categoria_id,
                order_by=Producto.precio.desc()
            ).label("row_num_categoria")
        )
        .where(Producto.is_active == True)
    )
    return [
        {
            "id": row.id,
            "nombre": row.nombre,
            "precio": row.precio,
            "rank_precio": row.rank_precio,
            "row_num_categoria": row.row_num_categoria
        }
        for row in result.all()
    ]


# Suma acumulada de ventas
async def ventas_acumuladas(session: AsyncSession):
    # Primero obtener ventas diarias
    ventas_diarias = (
        select(
            func.date(Orden.fecha_creacion).label("dia"),
            func.sum(Orden.total).label("ventas_dia")
        )
        .where(Orden.status == "pagado")
        .group_by(func.date(Orden.fecha_creacion))
        .order_by(func.date(Orden.fecha_creacion))
        .cte("ventas_diarias")
    )

    result = await session.execute(
        select(
            ventas_diarias.c.dia,
            ventas_diarias.c.ventas_dia,
            func.sum(ventas_diarias.c.ventas_dia)
            .over(order_by=ventas_diarias.c.dia)
            .label("ventas_acumuladas")
        )
        .select_from(ventas_diarias)
    )
    return list(result.all())
```

## Ejercicios Prácticos

**Ejercicio 1**: Implementa `GET /reportes/ventas` que retorne ventas totales, promedio por orden, y número de órdenes.

**Ejercicio 2**: Crea `GET /reportes/productos-populares` que retorne los 10 productos más vendidos.

**Ejercicio 3**: Implementa `GET /reportes/vendedores` con estadísticas: total productos, valor inventario, órdenes recibidas.

---

# SESIÓN 12: Validación y Serialización

## Duración: 2 horas

## Objetivos de Aprendizaje

- Crear validadores Pydantic personalizados
- Implementar serialización condicional
- Validar datos relacionados entre campos
- Manejar tipos personalizados

## 12.1 Validadores Personalizados

```python
from pydantic import BaseModel, Field, validator, model_validator, field_validator
from typing import Optional, List
from datetime import datetime, date
from decimal import Decimal
import re

class ProductoCreate(BaseModel):
    nombre: str = Field(min_length=3, max_length=200)
    descripcion: Optional[str] = Field(None, max_length=2000)
    precio: Decimal = Field(ge=0, decimal_places=2)
    stock: int = Field(ge=0)
    categoria_id: Optional[int] = None
    sku: Optional[str] = None

    @field_validator("nombre")
    @classmethod
    def nombre_no_invalido(cls, v: str) -> str:
        """El nombre no puede contener ciertas palabras."""
        palabras_bloqueadas = ["spam", "test", "fake"]
        v_lower = v.lower()
        for palabra in palabras_bloqueadas:
            if palabra in v_lower:
                raise ValueError(f"El nombre no puede contener '{palabra}'")
        return v.strip()

    @field_validator("sku")
    @classmethod
    def sku_formato(cls, v: Optional[str]) -> Optional[str]:
        """SKU debe tener formato: XXX-YYYY-NNN."""
        if v is None:
            return v
        if not re.match(r"^[A-Z]{3}-[A-Z]{4}-\d{3}$", v):
            raise ValueError("SKU debe tener formato: XXX-YYYY-NNN (ej: ELE-COMP-001)")
        return v.upper()

    @field_validator("precio")
    @classmethod
    def precio_decimal_places(cls, v: Decimal) -> Decimal:
        """Redondear a 2 decimales."""
        return round(v, 2)

    @model_validator(mode="after")
    def validar_producto(self):
        """Validaciones entre múltiples campos."""
        if self.stock > 0 and self.precio == 0:
            raise ValueError("Un producto con stock debe tener precio mayor a 0")

        if self.categoria_id and self.categoria_id < 0:
            raise ValueError("ID de categoría inválido")

        return self


class OrdenCreate(BaseModel):
    usuario_id: int = Field(gt=0)
    items: List[dict] = Field(min_length=1)

    @field_validator("items")
    @classmethod
    def items_validos(cls, v: List[dict]) -> List[dict]:
        if not v:
            raise ValueError("La orden debe tener al menos un item")

        producto_ids = []
        for i, item in enumerate(v):
            if "producto_id" not in item:
                raise ValueError(f"Item {i}: falta producto_id")
            if "cantidad" not in item:
                raise ValueError(f"Item {i}: falta cantidad")
            if item["cantidad"] <= 0:
                raise ValueError(f"Item {i}: cantidad debe ser mayor a 0")
            if item["producto_id"] in producto_ids:
                raise ValueError(f"Item {i}: producto duplicado")
            producto_ids.append(item["producto_id"])

        return v
```

## 12.2 Serialización Condicional

```python
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime

class UsuarioResponse(BaseModel):
    """Response que oculta datos sensibles según contexto."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    email: str
    nombre: str
    rol: str
    is_active: bool
    created_at: datetime

    # Ocultar password_hash en respuesta por defecto
    # (no se incluye en el modelo)


class UsuarioAdminResponse(UsuarioResponse):
    """Response completa solo para admins."""
    password_hash: str


class ProductoResponse(BaseModel):
    """Producto para usuarios normales."""
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    descripcion: Optional[str]
    precio: Decimal
    stock: int
    is_active: bool
    categoria_id: Optional[int]
    created_at: datetime

    # Ocultar información interna
    vendedor_id: int = Field exclude=True  # No mostrar en response


class ProductoVendedorResponse(ProductoResponse):
    """Producto para el propio vendedor (muestra todo)."""
    vendedor_id: int
    margen: Optional[Decimal] = None  # Calculado


# Schema con campos calculados
class ProductoConStats(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    precio: Decimal
    stock: int

    # Campos calculados (no existen en el modelo BD)
    valor_inventario: Decimal = Field(
        default=Decimal("0.00"),
        description="precio * stock"
    )
    esta_en_stock: bool = Field(
        default=False,
        description="stock > 0"
    )
    clasificacion: str = Field(
        default="sin_clasificar",
        description="Según cantidad en stock"
    )

    @field_validator("valor_inventario", mode="before")
    @classmethod
    def calcular_valor_inventario(cls, v, info):
        if v is not None:
            return v
        # Se calcula desde el values dict
        values = info.data
        precio = values.get("precio", Decimal("0"))
        stock = values.get("stock", 0)
        return Decimal(str(precio)) * Decimal(str(stock))

    @field_validator("clasificacion", mode="before")
    @classmethod
    def clasificar_stock(cls, v, info):
        if v is not None:
            return v
        stock = info.data.get("stock", 0)
        if stock == 0:
            return "sin_stock"
        elif stock < 5:
            return "stock_bajo"
        elif stock < 20:
            return "stock_medio"
        return "stock_adecuado"
```

## 12.3 Tipos Personalizados

```python
from pydantic import BaseModel, field_validator
from typing import Optional
from decimal import Decimal
import re

class PositiveDecimal(Decimal):
    """Decimal que solo permite valores positivos."""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info=None):
        if v is None:
            return v
        decimal_v = Decimal(str(v))
        if decimal_v < 0:
            raise ValueError("Debe ser un valor positivo")
        return decimal_v


class EmailStr(str):
    """String que valid que sea un email válido."""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info=None):
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", v):
            raise ValueError("Email inválido")
        return v.lower()


class Telefono(str):
    """String que valida formato de teléfono."""
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, info=None):
        if not v:
            return v
        # Eliminar caracteres no numéricos
        cleaned = re.sub(r"[^\d+]", "", v)
        if len(cleaned) < 10:
            raise ValueError("Teléfono debe tener al menos 10 dígitos")
        return cleaned


class ProductoConTiposPersonalizados(BaseModel):
    nombre: str
    precio: PositiveDecimal
    telefono_vendedor: Optional[Telefono] = None
    email_contacto: Optional[EmailStr] = None
```

## 12.4 Transformación de Datos

```python
from pydantic import BaseModel, field_serializer, computed_field
from typing import List, Optional
from datetime import datetime
from decimal import Decimal

class OrdenItemResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    producto_id: int
    cantidad: int
    precio_unitario: Decimal

    # Serializador personalizado
    @field_serializer("precio_unitario")
    def serialize_precio(self, v: Decimal) -> float:
        return float(round(v, 2))

    @computed_field
    @property
    def subtotal(self) -> float:
        return float(self.cantidad * self.precio_unitario)


class OrdenConTotales(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    usuario_id: int
    status: str
    fecha_creacion: datetime

    items: List[OrdenItemResponse]

    @computed_field
    @property
    def total(self) -> float:
        return sum(item.subtotal for item in self.items)

    @computed_field
    @property
    def total_items(self) -> int:
        return sum(item.cantidad for item in self.items)

    @computed_field
    @property
    def estado_legible(self) -> str:
        estados = {
            "pendiente": "Pendiente de pago",
            "pagado": "Pagado",
            "enviado": "Enviado",
            "entregado": "Entregado",
            "cancelado": "Cancelado"
        }
        return estados.get(self.status, self.status)


# Serialización de fechas
class ProductoResponseFechas(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nombre: str
    precio: Decimal
    created_at: datetime

    @field_serializer("created_at")
    def serialize_fecha(self, v: datetime) -> str:
        return v.strftime("%Y-%m-%d %H:%M:%S")
```

## 12.5 Validación Asíncrona

```python
from fastapi import Depends, HTTPException, status
from pydantic import BaseModel, field_validator
from sqlalchemy.ext.asyncio import AsyncSession

# Validación que requiere acceso a BD
async def validar_vendedor_existe(
    vendedor_id: int,
    session: AsyncSession = Depends(get_session)
) -> Vendedor:
    """Validador que verifica que el vendedor existe."""
    result = await session.execute(
        select(Vendedor).where(Vendedor.id == vendedor_id)
    )
    vendedor = result.scalar_one_or_none()
    if not vendedor:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Vendedor {vendedor_id} no encontrado"
        )
    return vendedor


async def validar_stock_suficiente(
    producto_id: int,
    cantidad: int,
    session: AsyncSession
) -> Producto:
    """Verifica que hay stock suficiente."""
    result = await session.execute(
        select(Producto).where(Producto.id == producto_id)
    )
    producto = result.scalar_one_or_none()

    if not producto:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Producto {producto_id} no encontrado"
        )

    if producto.stock < cantidad:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Stock insuficiente para {producto.nombre}. "
                   f"Solicitado: {cantidad}, Disponible: {producto.stock}"
        )

    return producto


# Usar en el endpoint
@router.post("/ordenes")
async def crear_orden(
    orden_data: OrdenCreate,
    session: AsyncSession = Depends(get_session)
):
    # Validar que todos los productos tienen stock
    for item_data in orden_data.items:
        await validar_stock_suficiente(
            item_data["producto_id"],
            item_data["cantidad"],
            session
        )
    # Continuar con la creación...
```

## 12.6 Schemas Complejos

```python
from typing import Union

class VarianteCreate(BaseModel):
    nombre: str
    sku: str
    atributos: dict  # {"color": "rojo", "talla": "M"}

class ProductoConVariantes(BaseModel):
    id: int
    nombre: str
    precio_base: Decimal
    variantes: List[VarianteCreate]
    precio_minimo: Decimal
    precio_maximo: Decimal


class FiltrosProducto(BaseModel):
    """Schema para filtros de búsqueda."""
    categoria_id: Optional[int] = None
    vendedor_id: Optional[int] = None
    precio_min: Optional[Decimal] = Field(None, ge=0)
    precio_max: Optional[Decimal] = Field(None, ge=0)
    stock_min: Optional[int] = Field(None, ge=0)
    etiquetas: Optional[List[int]] = None
    buscar: Optional[str] = Field(None, min_length=2)

    @model_validator(mode="after")
    def validar_rango_precio(self):
        if self.precio_min and self.precio_max:
            if self.precio_min > self.precio_max:
                raise ValueError("precio_min no puede ser mayor a precio_max")
        return self


class OrdenBulkCreate(BaseModel):
    """Crear múltiples órdenes a la vez."""
    usuario_id: int = Field(gt=0)
    ordenes: List[OrdenCreate] = Field(min_length=1, max_length=10)

    @field_validator("ordenes")
    @classmethod
    def validar_ordenes(cls, v):
        for i, orden in enumerate(v):
            if not orden.get("items"):
                raise ValueError(f"Orden {i}: debe tener items")
        return v
```

## Ejercicios Prácticos

**Ejercicio 1**: Crea un validador que verifique que el slug de una categoría sea único antes de crear.

**Ejercicio 2**: Implementa un schema `ProductoImport` que acepte precio como string "$1,234.56" y lo convierta a Decimal.

**Ejercicio 3**: Crea un validador asíncrono que verifique que todos los IDs de etiquetas en un producto existan.

---

# SESIÓN 13: Manejo de Errores y Excepciones

## Duración: 2 horas

## Objetivos de Aprendizaje

- Crear excepciones personalizadas
- Configurar handlers globales de errores
- Implementar logging
- Manejar errores de forma consistente

## 13.1 Excepciones Personalizadas

```python
# app/exceptions/base.py
from fastapi import HTTPException, status

class AppException(HTTPException):
    """Excepción base de la aplicación."""
    def __init__(
        self,
        status_code: int,
        detail: str,
        error_code: str = None,
        headers: dict = None
    ):
        super().__init__(status_code=status_code, detail=detail, headers=headers)
        self.error_code = error_code or f"ERR_{status_code}"


class NotFoundException(AppException):
    """Recurso no encontrado."""
    def __init__(self, resource: str, resource_id: any):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{resource} con ID {resource_id} no encontrado",
            error_code=f"NOT_FOUND_{resource.upper()}"
        )


class DuplicateException(AppException):
    """Recurso duplicado."""
    def __init__(self, resource: str, field: str, value: any):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"{resource} con {field}='{value}' ya existe",
            error_code=f"DUPLICATE_{resource.upper()}"
        )


class ValidationException(AppException):
    """Error de validación."""
    def __init__(self, detail: str, errors: list = None):
        super().__init__(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=detail,
            error_code="VALIDATION_ERROR"
        )
        self.errors = errors or []


class InsufficientStockException(AppException):
    """Stock insuficiente."""
    def __init__(self, producto_nombre: str, solicitado: int, disponible: int):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Stock insuficiente para '{producto_nombre}'. "
                   f"Solicitado: {solicitado}, Disponible: {disponible}",
            error_code="INSUFFICIENT_STOCK"
        )


class UnauthorizedException(AppException):
    """No autenticado."""
    def __init__(self, detail: str = "No autenticado"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            error_code="UNAUTHORIZED"
        )


class ForbiddenException(AppException):
    """No autorizado."""
    def __init__(self, detail: str = "No tienes permiso para esta acción"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
            error_code="FORBIDDEN"
        )


class BusinessRuleException(AppException):
    """Violación de regla de negocio."""
    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=detail,
            error_code="BUSINESS_RULE_VIOLATION"
        )
```

## 13.2 Handlers Globales

```python
# app/exceptions/handlers.py
from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
import logging

logger = logging.getLogger(__name__)


async def http_exception_handler(request: Request, exc: HTTPException):
    """Handler para HTTPException."""
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": {
                "code": getattr(exc, "error_code", f"ERR_{exc.status_code}"),
                "message": exc.detail,
                "path": str(request.url)
            }
        },
        headers=exc.headers
    )


async def validation_exception_handler(request: Request, exc: RequestValidationError):
    """Handler para errores de validación de FastAPI/Pydantic."""
    errors = []
    for error in exc.errors():
        errors.append({
            "field": ".".join(str(loc) for loc in error["loc"]),
            "message": error["msg"],
            "type": error["type"]
        })

    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": {
                "code": "VALIDATION_ERROR",
                "message": "Error de validación",
                "details": errors,
                "path": str(request.url)
            }
        }
    )


async def sqlalchemy_integrity_handler(request: Request, exc: IntegrityError):
    """Handler para errores de integridad de BD."""
    logger.error(f"Integrity error: {exc}")

    # Extraer mensaje amigable
    detail = "Error de integridad de datos"
    if "unique" in str(exc.orig).lower():
        detail = "Ya existe un registro con estos datos"
    elif "foreign key" in str(exc.orig).lower():
        detail = "Referencia a otro registro inválida"

    return JSONResponse(
        status_code=status.HTTP_400_BAD_REQUEST,
        content={
            "error": {
                "code": "INTEGRITY_ERROR",
                "message": detail,
                "path": str(request.url)
            }
        }
    )


async def sqlalchemy_handler(request: Request, exc: SQLAlchemyError):
    """Handler genérico para errores de SQLAlchemy."""
    logger.error(f"Database error: {exc}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "DATABASE_ERROR",
                "message": "Error interno de base de datos",
                "path": str(request.url)
            }
        }
    )


async def generic_exception_handler(request: Request, exc: Exception):
    """Handler genérico para cualquier excepción."""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": "INTERNAL_ERROR",
                "message": "Error interno del servidor",
                "path": str(request.url)
            }
        }
    )
```

## 13.3 Registrar Handlers en Main

```python
# app/main.py
from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from app.exceptions.handlers import (
    http_exception_handler,
    validation_exception_handler,
    sqlalchemy_handler,
    sqlalchemy_integrity_handler,
    generic_exception_handler
)
from app.exceptions.base import AppException

app = FastAPI()

# Registrar handlers
app.add_exception_handler(HTTPException, http_exception_handler)
app.add_exception_handler(RequestValidationError, validation_exception_handler)
app.add_exception_handler(IntegrityError, sqlalchemy_integrity_handler)
app.add_exception_handler(SQLAlchemyError, sqlalchemy_handler)
app.add_exception_handler(AppException, http_exception_handler)
app.add_exception_handler(Exception, generic_exception_handler)
```

## 13.4 Uso en Rutas

```python
# app/routes/productos.py
from app.exceptions.base import (
    NotFoundException,
    DuplicateException,
    InsufficientStockException,
    BusinessRuleException
)

@router.post("/", response_model=ProductoResponse, status_code=201)
async def crear_producto(
    producto_data: ProductoCreate,
    session: AsyncSession = Depends(get_session)
):
    # Validar vendedor
    result = await session.execute(
        select(Vendedor).where(Vendedor.id == producto_data.vendedor_id)
    )
    vendedor = result.scalar_one_or_none()
    if not vendedor:
        raise NotFoundException("Vendedor", producto_data.vendedor_id)

    # Verificar duplicado
    if producto_data.sku:
        result = await session.execute(
            select(Producto).where(Producto.sku == producto_data.sku)
        )
        if result.scalar_one_or_none():
            raise DuplicateException("Producto", "sku", producto_data.sku)

    # Crear producto
    db_producto = Producto(**producto_data.model_dump())
    session.add(db_producto)
    await session.flush()
    await session.refresh(db_producto)

    return db_producto


@router.patch("/{producto_id}/stock")
async def actualizar_stock(
    producto_id: int,
    delta: int = Query(..., description="Cambio en stock (+/-)"),
    session: AsyncSession = Depends(get_session)
):
    producto = await session.get(Producto, producto_id)
    if not producto:
        raise NotFoundException("Producto", producto_id)

    nuevo_stock = producto.stock + delta
    if nuevo_stock < 0:
        raise InsufficientStockException(
            producto.nombre,
            abs(delta),
            producto.stock
        )

    producto.stock = nuevo_stock
    await session.flush()
    await session.refresh(producto)

    return producto
```

## 13.5 Logging

```python
# app/logging.py
import logging
import sys
from datetime import datetime

# Configuración de logging
def setup_logging(debug: bool = False):
    level = logging.DEBUG if debug else logging.INFO

    # Formato
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)

    # Logger root
    root_logger = logging.getLogger()
    root_logger.setLevel(level)
    root_logger.addHandler(console_handler)

    # Logger de SQL (solo en debug)
    if debug:
        logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
    else:
        logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    return root_logger


# Uso en repositories
class BaseRepository:
    async def create(self, session, obj):
        try:
            session.add(obj)
            await session.flush()
            await session.refresh(obj)
            logging.info(f"Created {self.model.__name__} id={obj.id}")
            return obj
        except Exception as e:
            logging.error(f"Error creating {self.model.__name__}: {e}")
            raise


# Log de requests
from fastapi import Request

@app.middleware("http")
async def log_requests(request: Request, call_next):
    start_time = datetime.now()

    logger.info(f"Request: {request.method} {request.url}")

    response = await call_next(request)

    duration = (datetime.now() - start_time).total_seconds()
    logger.info(
        f"Response: {request.method} {request.url} "
        f"status={response.status_code} duration={duration:.3f}s"
    )

    return response
```

## 13.6 Respuestas de Error Consistencia

```python
# app/schemas/responses.py
from pydantic import BaseModel
from typing import Optional, Any

class ErrorResponse(BaseModel):
    error: "ErrorDetail"

class ErrorDetail(BaseModel):
    code: str
    message: str
    details: Optional[Any] = None
    path: Optional[str] = None


class SuccessResponse(BaseModel):
    success: bool = True
    data: Any
    message: Optional[str] = None


class PaginatedResponse(BaseModel):
    success: bool = True
    data: list
    pagination: "PaginationInfo"

class PaginationInfo(BaseModel):
    total: int
    skip: int
    limit: int
    has_more: bool
```

## Ejercicios Prácticos

**Ejercicio 1**: Crea una excepción `CategoryHasProductsException` que se lance cuando se intente eliminar una categoría que tiene productos.

**Ejercicio 2**: Implementa un middleware que registre todas las excepciones no manejadas a un archivo de log.

**Ejercicio 3**: Crea un handler para `IntegrityError` que extraiga el nombre del campo que violate la constraint única.

---

# SESIÓN 14: Paginación y Ordenamiento

## Duración: 2 horas

## Objetivos de Aprendizaje

- Implementar paginación offset-based
- Implementar cursor-based pagination
- Ordenamiento multi-campo
- Headers de paginación

## 14.1 Offset-Based Pagination

```python
# Schema de paginación
class PaginationParams:
    """Params de paginación para usar en rutas."""
    def __init__(
        self,
        skip: int = Query(0, ge=0, description="Registros a omitir"),
        limit: int = Query(10, ge=1, le=100, description="Registros a devolver")
    ):
        self.skip = skip
        self.limit = limit


class PaginatedResponse(BaseModel):
    items: list
    total: int
    skip: int
    limit: int
    has_more: bool

    @classmethod
    def create(cls, items: list, total: int, skip: int, limit: int):
        return cls(
            items=items,
            total=total,
            skip=skip,
            limit=limit,
            has_more=(skip + len(items)) < total
        )


# Repository con paginación
class ProductoRepository(BaseRepository[Producto]):
    async def get_paginated(
        self,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 10,
        categoria_id: int = None,
        ordenar_por: str = "created_at",
        orden: str = "desc"
    ) -> tuple[list[Producto], int]:
        # Query base
        query = select(Producto)
        count_query = select(func.count(Producto.id))

        # Filtros
        if categoria_id:
            query = query.where(Producto.categoria_id == categoria_id)
            count_query = count_query.where(Producto.categoria_id == categoria_id)

        # Total
        total_result = await session.execute(count_query)
        total = total_result.scalar()

        # Ordenamiento
        columna = getattr(Producto, ordenar_por, Producto.created_at)
        if orden.lower() == "desc":
            columna = columna.desc()

        # Query paginada
        query = query.order_by(columna).offset(skip).limit(limit)

        result = await session.execute(query)
        items = list(result.scalars().all())

        return items, total


# Endpoint con paginación
@router.get("/productos", response_model=PaginatedResponse)
async def listar_productos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    categoria_id: int = Query(None),
    ordenar_por: str = Query("created_at", regex="^(created_at|precio|nombre|stock)$"),
    orden: str = Query("desc", regex="^(asc|desc)$"),
    session: AsyncSession = Depends(get_session)
):
    productos, total = await producto_repo.get_paginated(
        session,
        skip=skip,
        limit=limit,
        categoria_id=categoria_id,
        ordenar_por=ordenar_por,
        orden=orden
    )

    return PaginatedResponse.create(
        items=productos,
        total=total,
        skip=skip,
        limit=limit
    )
```

## 14.2 Cursor-Based Pagination

```python
# Cursor pagination - más eficiente para datasets grandes
class CursorParams:
    def __init__(
        self,
        cursor: int = Query(None, description="ID del último item visto"),
        limit: int = Query(10, ge=1, le=100)
    ):
        self.cursor = cursor
        self.limit = limit


async def get_productos_cursor(
    session: AsyncSession,
    cursor: int = None,
    limit: int = 10,
    ordenar_por: str = "id",
    orden: str = "asc"
) -> list[Producto]:
    """
    Cursor pagination usando el ID del último item.

    Ventajas sobre offset:
    - No se desplaza por todos los registros anteriores
    - Consistente incluso si se insertan nuevos registros
    - Más rápido en datasets grandes
    """
    query = select(Producto).where(Producto.is_active == True)

    # Aplicar cursor
    if cursor is not None:
        columna = getattr(Producto, ordenar_por)
        if orden == "asc":
            query = query.where(columna > cursor)
        else:
            query = query.where(columna < cursor)

    # Orden y límite
    columna = getattr(Producto, ordenar_por, Producto.id)
    if orden == "desc":
        columna = columna.desc()

    query = query.order_by(columna).limit(limit + 1)  # +1 para saber si hay más

    result = await session.execute(query)
    items = list(result.scalars().all())

    # Verificar si hay más
    has_more = len(items) > limit
    if has_more:
        items = items[:limit]

    return items, has_more


@router.get("/productos/cursor")
async def listar_productos_cursor(
    cursor: int = Query(None),
    limit: int = Query(10, ge=1, le=100),
    ordenar_por: str = Query("id", regex="^(id|precio|created_at)$"),
    orden: str = Query("asc", regex="^(asc|desc)$"),
    session: AsyncSession = Depends(get_session)
):
    productos, has_more = await get_productos_cursor(
        session,
        cursor=cursor,
        limit=limit,
        ordenar_por=ordenar_por,
        orden=orden
    )

    # siguiente cursor = último ID
    next_cursor = productos[-1].id if productos and has_more else None

    return {
        "items": productos,
        "next_cursor": next_cursor,
        "has_more": has_more
    }
```

## 14.3 Headers de Paginación

```python
from fastapi import Response

@router.get("/productos/headers")
async def listar_productos_headers(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_session)
):
    productos, total = await producto_repo.get_paginated(
        session, skip=skip, limit=limit
    )

    # Headers de paginación
    response = JSONResponse(
        content={"items": [p.model_dump() for p in productos]}
    )

    response.headers["X-Total-Count"] = str(total)
    response.headers["X-Total-Pages"] = str((total + limit - 1) // limit)
    response.headers["X-Current-Page"] = str(skip // limit + 1)
    response.headers["X-Per-Page"] = str(limit)
    response.headers["Content-Range"] = f"items {skip}-{skip + len(productos) - 1}/{total}"

    return response
```

## 14.4 Ordenamiento Múltiple

```python
from typing import List
from sqlalchemy import desc, asc

def parse_sort_params(
    sort: str = Query(None, description="Formato: campo:asc,campo:desc")
) -> List[tuple]:
    """Parsea parámetro sort tipo 'precio:desc,nombre:asc'."""
    if not sort:
        return []

    ordenes = []
    for campo_direccion in sort.split(","):
        campo_direccion = campo_direccion.strip()
        if not campo_direccion:
            continue

        if ":" in campo_direccion:
            campo, direccion = campo_direccion.split(":", 1)
        else:
            campo = campo_direccion
            direccion = "asc"

        ordenes.append((campo.strip(), direccion.strip().lower()))

    return ordenes


async def get_productos_multi_sort(
    session: AsyncSession,
    skip: int = 0,
    limit: int = 10,
    sort: str = None
) -> list[Producto]:
    ordenes = parse_sort_params(sort)

    query = select(Producto).where(Producto.is_active == True)

    # Aplicar ordenamiento
    for campo, direccion in ordenes:
        if hasattr(Producto, campo):
            columna = getattr(Producto, campo)
            if direccion == "desc":
                columna = columna.desc()
            query = query.order_by(columna)

    # Default order si no hay sort
    if not ordenes:
        query = query.order_by(Producto.created_at.desc())

    query = query.offset(skip).limit(limit)

    result = await session.execute(query)
    return list(result.scalars().all())


@router.get("/productos")
async def listar_productos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    sort: str = Query(None, description="Ordenamiento: campo:direccion"),
    session: AsyncSession = Depends(get_session)
):
    productos = await get_productos_multi_sort(
        session, skip=skip, limit=limit, sort=sort
    )

    return productos
```

## 14.5 Paginación de Relaciones

```python
# Obtener órdenes de un usuario con paginación
@router.get("/usuarios/{usuario_id}/ordenes")
async def obtener_ordenes_usuario(
    usuario_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_session)
):
    # Verificar usuario
    usuario = await session.get(Usuario, usuario_id)
    if not usuario:
        raise NotFoundException("Usuario", usuario_id)

    # Órdenes paginadas
    count_result = await session.execute(
        select(func.count(Orden.id)).where(Orden.usuario_id == usuario_id)
    )
    total = count_result.scalar()

    result = await session.execute(
        select(Orden)
        .where(Orden.usuario_id == usuario_id)
        .order_by(Orden.fecha_creacion.desc())
        .offset(skip)
        .limit(limit)
    )
    ordenes = list(result.scalars().all())

    return PaginatedResponse.create(
        items=ordenes,
        total=total,
        skip=skip,
        limit=limit
    )


# Productos de una categoría con paginación
@router.get("/categorias/{categoria_id}/productos")
async def productos_categoria(
    categoria_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_session)
):
    categoria = await session.get(Categoria, categoria_id)
    if not categoria:
        raise NotFoundException("Categoría", categoria_id)

    # Incluir subcategorías
    subcategorias_ids = [categoria_id]
    result = await session.execute(
        select(Categoria.id).where(Categoria.parent_id == categoria_id)
    )
    subcategorias_ids.extend([row[0] for row in result.all()])

    # Count
    count_result = await session.execute(
        select(func.count(Producto.id))
        .where(Producto.categoria_id.in_(subcategorias_ids))
        .where(Producto.is_active == True)
    )
    total = count_result.scalar()

    # Productos
    result = await session.execute(
        select(Producto)
        .where(Producto.categoria_id.in_(subcategorias_ids))
        .where(Producto.is_active == True)
        .order_by(Producto.created_at.desc())
        .offset(skip)
        .limit(limit)
    )
    productos = list(result.scalars().all())

    return PaginatedResponse.create(
        items=productos,
        total=total,
        skip=skip,
        limit=limit
    )
```

## Ejercicios Prácticos

**Ejercicio 1**: Implementa cursor-based pagination para la lista de órdenes.

**Ejercicio 2**: Crea un endpoint `/productos` que acepte ordenamiento multi-campo como query param `sort=nombre:asc,precio:desc`.

**Ejercicio 3**: Implementa paginación con headers estilo REST (`Content-Range`, `X-Total-Count`).

---

# SESIÓN 15: Transacciones y Concurrencia

## Duración: 2 horas

## Objetivos de Aprendizaje

- Entender ACID y transacciones
- Manejar transacciones con SQLModel async
- Implementar optimistic locking
- Evitar condiciones de carrera

## 15.1 Conceptos de Transacciones

```python
"""
ACID:
- Atomicity: Todo o nada
- Consistency: La BD siempre está en estado válido
- Isolation: Transacciones concurrentes no se interfieren
- Durability: Lo escrito persiste

Niveles de aislamiento:
- READ UNCOMMITTED: Puede leer datos noCommit de otras transacciones
- READ COMMITTED: Solo lee datos commiteados
- REPEATABLE READ: Datos leídos no cambian durante la transacción
- SERIALIZABLE: Transacciones se ejecutan secuencialmente
"""
```

## 15.2 Transacciones Básicas

```python
async def crear_orden_transaccional(
    usuario_id: int,
    items: list[dict],
    session: AsyncSession
) -> Orden:
    """
    Crea una orden de forma atómica.
    Si algo falla, todo se revierte.
    """
    try:
        # 1. Validar usuario existe
        usuario = await session.get(Usuario, usuario_id)
        if not usuario:
            raise NotFoundException("Usuario", usuario_id)

        # 2. Crear orden (sin commit aún)
        orden = Orden(
            usuario_id=usuario_id,
            status="pendiente",
            total=Decimal("0.00")
        )
        session.add(orden)
        await session.flush()  # Obtiene ID

        total = Decimal("0.00")

        # 3. Procesar cada item
        for item_data in items:
            producto = await session.get(Producto, item_data["producto_id"])
            if not producto:
                raise NotFoundException("Producto", item_data["producto_id"])

            if producto.stock < item_data["cantidad"]:
                raise InsufficientStockException(
                    producto.nombre,
                    item_data["cantidad"],
                    producto.stock
                )

            cantidad = item_data["cantidad"]
            precio = producto.precio

            # Crear orden item
            orden_item = OrdenItem(
                orden_id=orden.id,
                producto_id=producto.id,
                cantidad=cantidad,
                precio_unitario=precio
            )
            session.add(orden_item)

            # Reducir stock
            producto.stock -= cantidad

            total += precio * cantidad

        # 4. Actualizar total
        orden.total = total

        # 5. Commit automático al salir del context manager
        # (o con await session.commit() explícito)
        await session.flush()

        logger.info(f"Orden {orden.id} creada exitosamente")
        return orden

    except Exception as e:
        # Rollback automático por el context manager de session
        logger.error(f"Error creando orden: {e}")
        raise
```

## 15.3 Savepoints

```python
async def operacion_con_savepoint(session: AsyncSession):
    """
    Usa savepoint para rollback parcial.
    """
    # Crear savepoint
    async with session.begin_nested():
        # Primera operación
        producto1 = await session.get(Producto, 1)
        producto1.stock -= 1

        # Segunda operación (puede fallar)
        try:
            async with session.begin_nested():
                producto2 = await session.get(Producto, 2)
                producto2.stock -= 1
                if producto2.stock < 0:
                    raise ValueError("Stock negativo")
        except ValueError:
            # Rollback solo de la segunda operación
            pass

    # Commit de la primera operación aunque la segunda haya fallado
    await session.commit()
```

## 15.4 Optimistic Locking

```python
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

class VersionedModel(SQLModel):
    """Modelo base con versionamiento para optimistic locking."""
    __abstract__ = True

    version: int = Field(default=1, nullable=False)


class ProductoConVersion(VersionedModel, table=True):
    __tablename__ = "productos_versioned"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=200)
    precio: Decimal
    stock: int
    version: int = Field(default=1)


async def actualizar_con_optimistic_lock(
    session: AsyncSession,
    producto_id: int,
    nuevo_precio: Decimal,
    expected_version: int
) -> ProductoConVersion:
    """
    Actualiza solo si la versión es la esperada.
    Previene lost updates en concurrencia.
    """
    producto = await session.get(ProductoConVersion, producto_id)
    if not producto:
        raise NotFoundException("Producto", producto_id)

    # Verificar versión
    if producto.version != expected_version:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"El producto fue modificado por otro proceso. "
                   f"Versión esperada: {expected_version}, "
                   f"Versión actual: {producto.version}"
        )

    # Actualizar con nueva versión
    producto.precio = nuevo_precio
    producto.version += 1
    producto.updated_at = datetime.utcnow()

    await session.flush()
    await session.refresh(producto)

    return producto


# En el endpoint
@router.patch("/{producto_id}/precio")
async def actualizar_precio(
    producto_id: int,
    precio: Decimal,
    version: int = Query(..., description="Versión actual del producto"),
    session: AsyncSession = Depends(get_session)
):
    try:
        producto = await actualizar_con_optimistic_lock(
            session, producto_id, precio, version
        )
        return producto
    except HTTPException as e:
        if e.status_code == 409:
            raise e  # Conflict - el cliente debe reintentar
        raise
```

## 15.5 Control de Concurrencia con SELECT FOR UPDATE

```python
# Bloquear filas durante una transacción
async def comprar_producto_con_lock(
    session: AsyncSession,
    producto_id: int,
    cantidad: int
) -> OrdenItem:
    """
    SELECT FOR UPDATE bloquea la fila hasta fin de transacción.
    Otros procesos esperan hasta que liberemos el lock.
    """
    async with session.begin():
        # Bloquear el producto (no permite otros SELECT FOR UPDATE)
        result = await session.execute(
            select(Producto)
            .where(Producto.id == producto_id)
            .with_for_update()  # Bloqueo exclusivo
        )
        producto = result.scalar_one_or_none()

        if not producto:
            raise NotFoundException("Producto", producto_id)

        if producto.stock < cantidad:
            raise InsufficientStockException(
                producto.nombre,
                cantidad,
                producto.stock
            )

        # Reducir stock (bloqueado, nadie más puede leer el stock real)
        producto.stock -= cantidad

        # Crear registro de compra
        orden_item = OrdenItem(
            producto_id=producto_id,
            cantidad=cantidad,
            precio_unitario=producto.precio
        )
        session.add(orden_item)

        await session.flush()
        return orden_item

# Si dos personas intentan comprar el mismo producto simultáneamente:
# - Primera transacción: adquiere el lock, procesa, libera lock
# - Segunda transacción: espera el lock, luego procede con stock ya reducido
```

## 15.6 Patrones de Reintento

```python
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

async def operacion_con_reintento(session: AsyncSession, max_intentos: int = 3):
    """
    Reintenta operaciones que fallan por conflictos de concurrencia.
    Útil para optimistic locking cuando hay alta contención.
    """
    for intento in range(max_intentos):
        try:
            # Tu operación aquí
            await session.flush()
            return True
        except SQLAlchemyError as e:
            if intento == max_intentos - 1:
                raise
            if "could not serialize" in str(e):
                # Retry en error de serialización
                await session.rollback()
                await asyncio.sleep(0.1 * (2 ** intento))  # Backoff exponencial
            else:
                raise

    return False


# Decorador con tenacity
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_result

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=0.1, min=0.1, max=1.0),
    retry=retry_if_result(lambda x: x is False)
)
async def operacion_con_reintento_decorada(session: AsyncSession):
    try:
        await session.flush()
        return True
    except Exception:
        await session.rollback()
        return False
```

## 15.7 Transacciones Distribuidas

```python
# Cuando necesitas actualizar múltiples bases de datos
from sqlalchemy.ext.asyncio import create_async_engine

async def operacion_distribuida(
    orden_data: dict,
    db1_url: str,
    db2_url: str
):
    """
    Simulación de transacción distribuida.
    En producción usar: SAGA pattern, 2PC, o Message Queues.
    """
    engine1 = create_async_engine(db1_url)
    engine2 = create_async_engine(db2_url)

    async with async_session(engine1) as session1, \
               async_session(engine2) as session2:

        try:
            # 1. Reservar stock en BD1
            # ...

            # 2. Registrar pago en BD2
            # ...

            # 3. Commit ambos
            await session1.commit()
            await session2.commit()

        except Exception as e:
            # Rollback ambos
            await session1.rollback()
            await session2.rollback()
            raise

    # WARNING: Esto NO garantiza atomicidad real entre BD distintas
    # Para eso se necesita 2PC o SAGA
```

## Ejercicios Prácticos

**Ejercicio 1**: Implementa una función `transferir_stock(producto_origen_id, producto_destino_id, cantidad)` que use transacciones.

**Ejercicio 2**: Implementa optimistic locking en el modelo Orden para actualizar el status.

**Ejercicio 3**: Crea un endpoint de "reserva de stock" que bloquee el producto mientras se completa el checkout.

---

# SESIÓN 16: Migraciones con Alembic

## Duración: 2 horas

## Objetivos de Aprendizaje

- Configurar Alembic para migraciones
- Crear y ejecutar migraciones
- Modificar esquemas existentes
- Hacer rollback de migraciones

## 16.1 Instalación y Configuración

```bash
pip install alembic asyncpg
```

```bash
# Inicializar Alembic
alembic init alembic
```

```ini
# alembic.ini
[alembic]
script_location = alembic
prepend_sys_path = .
version_path_separator = os

# Usar async
sqlalchemy.url = postgresql+asyncpg://postgres:password@localhost:5432/marketdb

[post_write_hooks]

[loggers]
keys = root,sqlalchemy,alembic

[handlers]

[formatters]

[logger_root]
level = WARN
handlers =
qualname =

[logger_sqlalchemy]
level = WARN
handlers =
qualname = sqlalchemy.engine

[logger_alembic]
level = INFO
handlers =
qualname = alembic
```

```python
# alembic/env.py
import asyncio
from logging.config import fileConfig

from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config

from alembic import context

from app.config import settings
from app.models import *  # Importar todos los modelos
from sqlmodel import SQLModel

config = context.config

# Config de log
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = SQLModel.metadata


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = settings.database_url
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)

    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    """In this scenario we need to create an Engine
    and associate a connection with the context."""

    connectable = async_engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)

    await connectable.dispose()


def run_migrations_online() -> None:
    """Run migrations in 'online' mode."""
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

## 16.2 Crear Migración Inicial

```bash
# Generar migración inicial desde modelos
alembic revision --autogenerate -m "Initial migration"

# Ver estructura
# alembic/
# ├── env.py
# ├── script.py.mako
# └── versions/
#     └── 2024_01_01_initial_migration.py
```

```python
# alembic/versions/2024_01_01_initial_migration.py
"""Initial migration

Revision ID: 001
Revises:
Create Date: 2024-01-01 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Crear tabla usuarios
    op.create_table(
        'usuarios',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('email', sa.String(length=255), nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('password_hash', sa.String(length=255), nullable=False),
        sa.Column('rol', sa.String(length=20), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_usuarios_email'), 'usuarios', ['email'], unique=True)

    # Crear tabla categorias
    op.create_table(
        'categorias',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('nombre', sa.String(length=100), nullable=False),
        sa.Column('slug', sa.String(length=100), nullable=False),
        sa.Column('descripcion', sa.Text(), nullable=True),
        sa.Column('parent_id', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['parent_id'], ['categorias.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_categorias_slug'), 'categorias', ['slug'], unique=True)

    # ... más tablas
```

## 16.3 Migraciones Posteriores

```bash
# Crear nueva migración
alembic revision --autogenerate -m "Add is_verified to vendedores"
```

```python
# alembic/versions/2024_01_02_add_is_verified.py
"""Add is_verified to vendedores

Revision ID: 002
Revises: 001
Create Date: 2024-01-02 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa

revision = '002'
down_revision = '001'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column(
        'vendedores',
        sa.Column('is_verified', sa.Boolean(), nullable=False, server_default='false')
    )


def downgrade() -> None:
    op.drop_column('vendedores', 'is_verified')
```

## 16.4 Ejecutar Migraciones

```bash
# Upgrade a la última migración
alembic upgrade head

# Upgrade a una migración específica
alembic upgrade 001

# Downgrade una migración
alembic downgrade -1

# Downgrade a una migración específica
alembic downgrade 001

# Ver historial
alembic history

# Ver estado actual
alembic current

# Marcar como aplicada sin ejecutar (para datos existentes)
alembic stamp head
```

## 16.5 Modificar Columnas

```python
# Renombrar columna
def upgrade() -> None:
    op.alter_column('productos', 'nombre',
                    new_column_name='titulo',
                    existing_type=sa.String(length=200))


# Cambiar tipo de columna
def upgrade() -> None:
    op.alter_column('productos', 'precio',
                    existing_type=sa.Numeric(precision=10, scale=2),
                    new_type=sa.Numeric(precision=12, scale=2))


# Añadir constraint
def upgrade() -> None:
    op.create_check_constraint(
        'ck_productos_precio_positivo',
        'productos',
        'precio >= 0'
    )
```

## 16.6 Datos de Semilla (Seed Data)

```python
# alembic/seeds.py
"""Seed data para desarrollo"""

async def seed_categorias(session):
    from app.models.categoria import Categoria

    categorias = [
        Categoria(nombre="Electrónica", slug="electronica", descripcion="Devices and gadgets"),
        Categoria(nombre="Ropa", slug="ropa", descripcion="Fashion and apparel"),
        Categoria(nombre="Hogar", slug="hogar", descripcion="Home and garden"),
    ]

    for cat in categorias:
        session.add(cat)

    await session.commit()


# Ejecutar seeds después de migrar
# En env.py:
def run_migrations_online() -> None:
    # ... después de migraciones
    if context.get_context().run_modules_hooks:
        from alembic.seeds import seed_categorias
```

## 16.7 Multi-Schemas

```python
# Para multi-tenant o separar tablas
def upgrade() -> None:
    # Crear en schema específico
    op.create_table(
        'productos',
        sa.Column('id', sa.Integer(), nullable=False),
        # ...
        schema='vendedor_1'
    )

    # Mover tabla a otro schema
    op.move_table('productos', schema='public', new_schema='archived')
```

## Ejercicios Prácticos

**Ejercicio 1**: Crea una migración que añada un campo `deleted_at` para soft delete.

**Ejercicio 2**: Crea una migración que cree una tabla de auditoría para tracking de cambios.

**Ejercicio 3**: Implementa una seed migration con 5 categorías y 10 productos de ejemplo.

---

# SESIÓN 17: Autenticación y Autorización

## Duración: 2 horas

## Objetivos de Aprendizaje

- Implementar autenticación con JWT
- Hashear contraseñas con bcrypt
- Crear dependencias de autenticación
- Implementar autorización por roles

## 17.1 Seguridad Básica

```python
# app/security/utils.py
from passlib.context import CryptContext

# Contexto de hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """Hashea una contraseña usando bcrypt."""
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica una contraseña contra su hash."""
    return pwd_context.verify(plain_password, hashed_password)


# Ejemplo de uso:
# Hash: $2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4gGrxgPI01dTMK0K
# Bcrypt genera un salt automático, así que el mismo password
# genera hashes diferentes cada vez (más seguro)
```

## 17.2 JWT

```python
# app/security/jwt.py
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from pydantic import BaseModel

# Config (de settings)
SECRET_KEY = "tu-secret-key-super-secreta-mínimo-32-caracteres"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


class TokenData(BaseModel):
    user_id: Optional[int] = None
    email: Optional[str] = None
    rol: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crea un JWT token.

    El token contiene:
    - sub: subject (user_id)
    - email: email del usuario
    - rol: rol del usuario
    - exp: expiración
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> TokenData:
    """Decodifica y valida un JWT token."""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        email: str = payload.get("email")
        rol: str = payload.get("rol")

        if user_id is None:
            raise JWTError()

        return TokenData(user_id=user_id, email=email, rol=rol)
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
```

## 17.3 Dependencias de Autenticación

```python
# app/security/deps.py
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.connection import get_session
from app.models.usuario import Usuario
from app.security.jwt import decode_access_token, TokenData
from app.security.utils import verify_password

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    session: AsyncSession = Depends(get_session)
) -> Usuario:
    """
    Dependencia que obtiene el usuario actual desde el JWT.

    Uso:
    @router.get("/perfil")
    async def mi_perfil(usuario: Usuario = Depends(get_current_user)):
    """
    token = credentials.credentials
    token_data = decode_access_token(token)

    result = await session.execute(
        select(Usuario).where(Usuario.id == token_data.user_id)
    )
    user = result.scalar_one_or_none()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no encontrado"
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )

    return user


async def get_current_active_user(
    current_user: Usuario = Depends(get_current_user)
) -> Usuario:
    """Verifica que el usuario esté activo."""
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )
    return current_user


def require_role(roles: list[str]):
    """
    Factory de dependencia para requerir roles específicos.

    Uso:
    @router.delete("/usuarios/{id}")
    async def eliminar_usuario(
        usuario: Usuario = Depends(require_role(["admin"]))
    ):
    """
    async def role_checker(
        current_user: Usuario = Depends(get_current_user)
    ) -> Usuario:
        if current_user.rol not in roles:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Rol requerido: {', '.join(roles)}"
            )
        return current_user

    return role_checker
```

## 17.4 Endpoints de Auth

```python
# app/routes/auth.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from app.database.connection import get_session
from app.models.usuario import Usuario
from app.schemas.usuario import UsuarioResponse, UsuarioCreate
from app.schemas.auth import Token, LoginRequest
from app.security.jwt import create_access_token, TokenData
from app.security.utils import hash_password, verify_password
from datetime import timedelta

router = APIRouter(prefix="/auth", tags=["Autenticación"])


@router.post("/register", response_model=UsuarioResponse, status_code=201)
async def registrar_usuario(
    usuario_data: UsuarioCreate,
    session: AsyncSession = Depends(get_session)
):
    """Registra un nuevo usuario."""
    # Verificar email único
    result = await session.execute(
        select(Usuario).where(Usuario.email == usuario_data.email)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El email ya está registrado"
        )

    # Crear usuario con contraseña hasheada
    db_usuario = Usuario(
        email=usuario_data.email,
        nombre=usuario_data.nombre,
        password_hash=hash_password(usuario_data.password),
        rol=usuario_data.rol or "cliente",
        is_active=True
    )

    session.add(db_usuario)
    await session.commit()
    await session.refresh(db_usuario)

    return db_usuario


@router.post("/login", response_model=Token)
async def login(
    login_data: LoginRequest,
    session: AsyncSession = Depends(get_session)
):
    """
    Inicia sesión y retorna JWT token.

    Requiere email y password en el body.
    """
    # Buscar usuario
    result = await session.execute(
        select(Usuario).where(Usuario.email == login_data.email)
    )
    usuario = result.scalar_one_or_none()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

    # Verificar contraseña
    if not verify_password(login_data.password, usuario.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )

    # Verificar estado
    if not usuario.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuario inactivo"
        )

    # Crear token
    access_token = create_access_token(
        data={
            "sub": usuario.id,
            "email": usuario.email,
            "rol": usuario.rol
        },
        expires_delta=timedelta(minutes=60 * 24)  # 24 horas
    )

    return Token(access_token=access_token)


@router.get("/me", response_model=UsuarioResponse)
async def get_current_user_info(
    current_user: Usuario = Depends(get_current_user)
):
    """Obtiene información del usuario autenticado."""
    return current_user
```

## 17.5 Protección de Rutas

```python
# app/routes/usuarios.py
from app.security.deps import get_current_user, require_role

# Rutas públicas
@router.get("/usuarios")
async def listar_usuarios(
    session: AsyncSession = Depends(get_session)
):
    """Ruta pública - cualquiera puede ver usuarios."""
    ...

# Rutas protegidas
@router.get("/usuarios/perfil")
async def mi_perfil(
    current_user: Usuario = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    """Ruta protegida - requiere autenticación."""
    return current_user


# Rutas de admin
@router.delete("/usuarios/{usuario_id}")
async def eliminar_usuario(
    usuario_id: int,
    current_user: Usuario = Depends(require_role(["admin"])),
    session: AsyncSession = Depends(get_session)
):
    """Ruta solo para admins."""
    ...


# Rutas de vendedor
@router.post("/productos")
async def crear_producto_vendedor(
    producto_data: ProductoCreate,
    current_user: Usuario = Depends(require_role(["vendedor", "admin"])),
    session: AsyncSession = Depends(get_session)
):
    """Ruta para vendedores o admins."""
    ...
```

## 17.6 Refresh Tokens

```python
# app/routes/auth.py (continuación)

REFRESH_TOKEN_EXPIRE_DAYS = 7

class RefreshToken(BaseModel):
    refresh_token: str


@router.post("/refresh", response_model=Token)
async def refresh_token(
    current_user: Usuario = Depends(get_current_user)
):
    """
    Genera un nuevo access token sin necesidad de login.
    """
    access_token = create_access_token(
        data={
            "sub": current_user.id,
            "email": current_user.email,
            "rol": current_user.rol
        }
    )
    return Token(access_token=access_token)


@router.post("/logout")
async def logout(
    current_user: Usuario = Depends(get_current_user)
):
    """
    Logout (en JWT stateless, el cliente descarta el token).
    Para blacklist, necesitarías guardar tokens en BD/Redis.
    """
    return {"message": "Sesión cerrada"}
```

## 17.7 Hash de Password en Registro

```python
# Actualizar schema
class UsuarioCreate(BaseModel):
    email: EmailStr
    nombre: str = Field(min_length=2)
    password: str = Field(min_length=8)
    rol: str = Field(default="cliente")

    @field_validator("password")
    @classmethod
    def password_fuerte(cls, v: str) -> str:
        if not re.match(r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d).{8,}$", v):
            raise ValueError(
                "La contraseña debe tener al menos 8 caracteres, "
                "una mayúscula, una minúscula y un número"
            )
        return v
```

## Ejercicios Prácticos

**Ejercicio 1**: Implementa el endpoint POST `/auth/password-reset` que genere un token de recuperación.

**Ejercicio 2**: Crea una dependencia `require_vendedor_o_admin` que permita acceso a vendedores y admins.

**Ejercicio 3**: Implementa un middleware que registre intentos de login fallidos y bloquee después de 5 intentos.

---

# SESIÓN 18: Testing

## Duración: 2 horas

## Objetivos de Aprendizaje

- Configurar pytest con async
- Crear fixtures para tests
- Testear endpoints API
- Testear repository con BD real o en memoria

## 18.1 Configuración

```bash
pip install pytest pytest-asyncio httpx faker
```

```ini
# pytest.ini
[pytest]
asyncio_mode = auto
testpaths = tests
python_files = test_*.py
python_functions = test_*
python_classes = Test*
addopts = -v --tb=short
```

```python
# tests/conftest.py
import pytest
import asyncio
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from httpx import AsyncClient, ASGITransport
from sqlmodel import SQLModel

from app.main import app
from app.database.connection import get_session
from app.models import *

# BD en memoria para tests
TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"

test_engine = create_async_engine(
    TEST_DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False}
)

test_async_session = sessionmaker(
    test_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


@pytest.fixture(scope="session")
def event_loop():
    """Crea event loop para tests."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="function")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    """Crea sesión de BD limpia para cada test."""
    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with test_async_session() as session:
        yield session

    async with test_engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.drop_all)


@pytest.fixture
async def client(db_session: AsyncSession) -> AsyncGenerator[AsyncClient, None]:
    """Cliente HTTP con sesión de BD override."""

    async def override_get_session():
        yield db_session

    app.dependency_overrides[get_session] = override_get_session

    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test"
    ) as ac:
        yield ac

    app.dependency_overrides.clear()


@pytest.fixture
async def usuario_test(db_session: AsyncSession):
    """Crea usuario de prueba."""
    from app.models.usuario import Usuario
    from app.security.utils import hash_password

    usuario = Usuario(
        email="test@example.com",
        nombre="Usuario Test",
        password_hash=hash_password("Password123"),
        rol="cliente",
        is_active=True
    )
    db_session.add(usuario)
    await db_session.commit()
    await db_session.refresh(usuario)
    return usuario


@pytest.fixture
async def vendedor_test(db_session: AsyncSession, usuario_test):
    """Crea vendedor de prueba."""
    from app.models.vendedor import Vendedor

    vendedor = Vendedor(
        usuario_id=usuario_test.id,
        nombre_tienda="Tienda Test"
    )
    db_session.add(vendedor)
    await db_session.commit()
    await db_session.refresh(vendedor)
    return vendedor
```

## 18.2 Tests de Repositorio

```python
# tests/test_repositories.py
import pytest
from sqlalchemy import select
from app.models.usuario import Usuario
from app.models.producto import Producto
from app.repositories.usuario import usuario_repo
from app.repositories.producto import producto_repo


@pytest.mark.asyncio
async def test_create_usuario(db_session):
    """Test crear usuario."""
    usuario = Usuario(
        email="nuevo@test.com",
        nombre="Nuevo Usuario",
        password_hash="hash123",
        rol="cliente"
    )

    created = await usuario_repo.create(db_session, usuario)
    await db_session.commit()

    assert created.id is not None
    assert created.email == "nuevo@test.com"


@pytest.mark.asyncio
async def test_get_usuario_por_email(db_session, usuario_test):
    """Test buscar por email."""
    found = await usuario_repo.get_by_email(db_session, "test@example.com")
    assert found is not None
    assert found.email == "test@example.com"


@pytest.mark.asyncio
async def test_get_usuario_no_existe(db_session):
    """Test buscar email inexistente."""
    found = await usuario_repo.get_by_email(db_session, "noexiste@test.com")
    assert found is None


@pytest.mark.asyncio
async def test_update_usuario(db_session, usuario_test):
    """Test actualizar usuario."""
    updates = {"nombre": "Nombre Actualizado"}
    updated = await usuario_repo.update(db_session, usuario_test, updates)

    assert updated.nombre == "Nombre Actualizado"


@pytest.mark.asyncio
async def test_delete_usuario(db_session, usuario_test):
    """Test eliminar usuario."""
    deleted = await usuario_repo.delete(db_session, usuario_test.id)
    assert deleted is True

    found = await usuario_repo.get(db_session, usuario_test.id)
    assert found is None
```

## 18.3 Tests de Endpoints

```python
# tests/test_usuarios.py
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_crear_usuario(client: AsyncClient):
    """Test crear usuario via API."""
    response = await client.post(
        "/usuarios/",
        json={
            "email": "nuevo@ejemplo.com",
            "nombre": "Nuevo Usuario",
            "password": "Password123",
            "rol": "cliente"
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == "nuevo@ejemplo.com"
    assert "id" in data
    assert "password" not in data  # No expuesta


@pytest.mark.asyncio
async def test_crear_usuario_email_duplicado(client: AsyncClient, usuario_test):
    """Test error al crear usuario con email duplicado."""
    response = await client.post(
        "/usuarios/",
        json={
            "email": "test@example.com",
            "nombre": "Otro Usuario",
            "password": "Password123"
        }
    )

    assert response.status_code == 400
    assert "ya registrado" in response.json()["detail"]


@pytest.mark.asyncio
async def test_listar_usuarios(client: AsyncClient, usuario_test):
    """Test listar usuarios."""
    response = await client.get("/usuarios/")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


@pytest.mark.asyncio
async def test_obtener_usuario(client: AsyncClient, usuario_test):
    """Test obtener usuario por ID."""
    response = await client.get(f"/usuarios/{usuario_test.id}")

    assert response.status_code == 200
    data = response.json()
    assert data["id"] == usuario_test.id
    assert data["email"] == usuario_test.email


@pytest.mark.asyncio
async def test_obtener_usuario_no_existe(client: AsyncClient):
    """Test obtener usuario inexistente."""
    response = await client.get("/usuarios/9999")

    assert response.status_code == 404


@pytest.mark.asyncio
async def test_actualizar_usuario(client: AsyncClient, usuario_test):
    """Test actualizar usuario."""
    response = await client.patch(
        f"/usuarios/{usuario_test.id}",
        json={"nombre": "Nombre Actualizado"}
    )

    assert response.status_code == 200
    data = response.json()
    assert data["nombre"] == "Nombre Actualizado"


@pytest.mark.asyncio
async def test_eliminar_usuario(client: AsyncClient, usuario_test):
    """Test eliminar usuario."""
    response = await client.delete(f"/usuarios/{usuario_test.id}")

    assert response.status_code == 204

    # Verificar eliminado
    response = await client.get(f"/usuarios/{usuario_test.id}")
    assert response.status_code == 404
```

## 18.4 Tests de Productos con Relaciones

```python
# tests/test_productos.py

@pytest.mark.asyncio
async def test_crear_producto_con_vendedor(client: AsyncClient, vendedor_test):
    """Test crear producto asociado a vendedor."""
    response = await client.post(
        "/productos/",
        json={
            "nombre": "Producto Test",
            "precio": "99.99",
            "stock": 10,
            "vendedor_id": vendedor_test.id
        }
    )

    assert response.status_code == 201
    data = response.json()
    assert data["nombre"] == "Producto Test"
    assert data["vendedor_id"] == vendedor_test.id


@pytest.mark.asyncio
async def test_crear_producto_vendedor_invalido(client: AsyncClient):
    """Test crear producto con vendedor inexistente."""
    response = await client.post(
        "/productos/",
        json={
            "nombre": "Producto Test",
            "precio": "99.99",
            "stock": 10,
            "vendedor_id": 9999
        }
    )

    assert response.status_code == 400


@pytest.mark.asyncio
async def test_filtro_por_categoria(client: AsyncClient, categoria_test):
    """Test filtrar productos por categoría."""
    # Crear producto con categoría
    response = await client.post(
        "/productos/",
        json={
            "nombre": "Producto Electrónica",
            "precio": "299.99",
            "stock": 5,
            "vendedor_id": 1,
            "categoria_id": categoria_test.id
        }
    )

    assert response.status_code == 201

    # Filtrar por categoría
    response = await client.get(f"/productos/?categoria_id={categoria_test.id}")
    assert response.status_code == 200
    data = response.json()
    assert all(p["categoria_id"] == categoria_test.id for p in data)
```

## 18.5 Tests con Autenticación

```python
# tests/test_auth.py

@pytest.mark.asyncio
async def test_register(client: AsyncClient):
    """Test registro de usuario."""
    response = await client.post(
        "/auth/register",
        json={
            "email": "nuevo@test.com",
            "nombre": "Nuevo Usuario",
            "password": "Password123"
        }
    )

    assert response.status_code == 201
    assert "access_token" in response.json()


@pytest.mark.asyncio
async def test_login_exitoso(client: AsyncClient, usuario_test):
    """Test login con credenciales válidas."""
    response = await client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "Password123"
        }
    )

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_password_invalido(client: AsyncClient, usuario_test):
    """Test login con password incorrecto."""
    response = await client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "WrongPassword"
        }
    )

    assert response.status_code == 401


@pytest.mark.asyncio
async def test_ruta_protegida_sin_token(client: AsyncClient):
    """Test acceder a ruta protegida sin token."""
    response = await client.get("/auth/me")
    assert response.status_code == 403  # Forbidden sin token


@pytest.mark.asyncio
async def test_ruta_protegida_con_token(client: AsyncClient, usuario_test):
    """Test acceder a ruta protegida con token válido."""
    # Login primero
    login_response = await client.post(
        "/auth/login",
        json={
            "email": "test@example.com",
            "password": "Password123"
        }
    )
    token = login_response.json()["access_token"]

    # Acceder a ruta protegida
    response = await client.get(
        "/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )

    assert response.status_code == 200
    assert response.json()["email"] == "test@example.com"
```

## 18.6 Fixtures para Datos de Prueba

```python
# tests/fixtures.py
import pytest
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import *

@pytest.fixture
async def categoria_test(db_session: AsyncSession) -> Categoria:
    categoria = Categoria(
        nombre="Electrónica",
        slug="electronica",
        descripcion="Productos electrónicos"
    )
    db_session.add(categoria)
    await db_session.commit()
    await db_session.refresh(categoria)
    return categoria


@pytest.fixture
async def producto_test(db_session: AsyncSession, vendedor_test, categoria_test) -> Producto:
    producto = Producto(
        nombre="Laptop Test",
        descripcion="Laptop para testing",
        precio=Decimal("999.99"),
        stock=10,
        vendedor_id=vendedor_test.id,
        categoria_id=categoria_test.id,
        is_active=True
    )
    db_session.add(producto)
    await db_session.commit()
    await db_session.refresh(producto)
    return producto


@pytest.fixture
async def orden_test(db_session: AsyncSession, usuario_test, producto_test) -> Orden:
    orden = Orden(
        usuario_id=usuario_test.id,
        status="pendiente",
        total=producto_test.precio
    )
    db_session.add(orden)
    await db_session.flush()

    item = OrdenItem(
        orden_id=orden.id,
        producto_id=producto_test.id,
        cantidad=1,
        precio_unitario=producto_test.precio
    )
    db_session.add(item)
    await db_session.commit()
    await db_session.refresh(orden)
    return orden
```

## Ejercicios Prácticos

**Ejercicio 1**: Escribe tests para el endpoint `PATCH /productos/{id}/stock` verificando que no允许 stock negativo.

**Ejercicio 2**: Crea un test de integración completo: crear usuario → login → crear producto → crear orden.

**Ejercicio 3**: Implementa un test que verifique el conteo de paginación con múltiples productos.

---

# SESIÓN 19: Optimización

## Duración: 2 horas

## Objetivos de Aprendizaje

- Crear y usar índices effectively
- Evitar N+1 queries
- Implementar caching
- Optimizar queries complejas

## 19.1 Índices

```python
# app/models/producto.py
from sqlalchemy import Index

class Producto(SQLModel, table=True):
    __tablename__ = "productos"
    __table_args__ = (
        # Índice compuesto para búsqueda común
        Index("idx_productos_categoria_precio", "categoria_id", "precio"),
        # Índice para ordenamiento por fecha
        Index("idx_productos_created_at", "created_at"),
        # Índice para búsqueda de texto
        Index("idx_productos_nombre", "nombre", postgresql_using="gin",
              postgresql_ops={"nombre": "gin_trgm"}),
    )

    # ...
```

```sql
-- Índices en SQL directo
CREATE INDEX idx_productos_nombre_gin ON productos USING gin (nombre gin_trgm_ops);

CREATE INDEX idx_ordenes_usuario_fecha ON ordenes (usuario_id, fecha_creacion DESC);

CREATE INDEX idx_productos_stock ON productos (stock) WHERE is_active = true;

-- Índice parcial: solo para productos activos
CREATE INDEX idx_productos_activos ON productos (created_at DESC)
WHERE is_active = true;
```

## 19.2 Evitar N+1 Queries

```python
# PROBLEMA: N+1 queries
async def get_ordenes_con_usuarios_n_plus_1(session: AsyncSession):
    ordenes = await session.execute(select(Orden).limit(10))
    ordenes = ordenes.scalars().all()

    # N+1: 1 query para órdenes + N queries para cada usuario
    for orden in ordenes:
        user = await session.execute(
            select(Usuario).where(Usuario.id == orden.usuario_id)
        )
        orden.usuario = user.scalar_one()

    return ordenes


# SOLUCIÓN 1: joinedload
async def get_ordenes_con_usuarios_optimizado(session: AsyncSession):
    result = await session.execute(
        select(Orden)
        .options(joinedload(Orden.usuario))  # JOIN en la misma query
        .limit(10)
    )
    return result.unique().scalars().all()


# SOLUCIÓN 2: selectinload (mejor para 1:N)
async def get_ordenes_con_items_optimizado(session: AsyncSession):
    result = await session.execute(
        select(Orden)
        .options(selectinload(Orden.items).selectinload(OrdenItem.producto))
        .limit(10)
    )
    return result.unique().scalars().all()


# SOLUCIÓN 3: subqueryload (similar a selectinload)
from sqlalchemy.orm import subqueryload

result = await session.execute(
    select(Orden)
    .options(subqueryload(Orden.items))
    .limit(10)
)
```

## 19.3 Caching

```python
# app/cache.py
from functools import lru_cache
import redis.asyncio as redis
from typing import Optional
import json

# Cache simple en memoria (para desarrollo)
@lru_cache(maxsize=1000)
def get_cached(key: str):
    """Cache simple con lru_cache."""
    return None


class CacheService:
    def __init__(self):
        self.redis: Optional[redis.Redis] = None

    async def connect(self):
        self.redis = await redis.from_url("redis://localhost")

    async def get(self, key: str):
        if not self.redis:
            return None
        value = await self.redis.get(key)
        return json.loads(value) if value else None

    async def set(self, key: str, value: any, ttl: int = 300):
        if self.redis:
            await self.redis.set(key, json.dumps(value), ex=ttl)

    async def delete(self, key: str):
        if self.redis:
            await self.redis.delete(key)

    async def invalidate_pattern(self, pattern: str):
        if self.redis:
            async for key in self.redis.scan_iter(pattern):
                await self.redis.delete(key)


cache = CacheService()


# Uso en endpoints
@router.get("/productos/{producto_id}")
async def obtener_producto(
    producto_id: int,
    session: AsyncSession = Depends(get_session)
):
    cache_key = f"producto:{producto_id}"

    # Intentar cache primero
    cached = await cache.get(cache_key)
    if cached:
        return cached

    # Query BD
    producto = await session.get(Producto, producto_id)
    if not producto:
        raise NotFoundException("Producto", producto_id)

    # Guardar en cache
    await cache.set(cache_key, producto.model_dump(), ttl=60)

    return producto
```

## 19.4 Optimización de Queries

```python
# Usar columnas específicas en vez de SELECT *
async def get_productos_optimizado(session: AsyncSession):
    # ❌ SELECT * (trae todas las columnas)
    result = await session.execute(select(Producto))

    # ✅ Solo columnas necesarias
    result = await session.execute(
        select(Producto.id, Producto.nombre, Producto.precio)
        .where(Producto.is_active == True)
    )


# Usar WHERE en vez de filter en memoria
async def filtrar_productos(session: AsyncSession, categoria: str):
    # ❌ Trae todo y filtra en Python
    result = await session.execute(select(Producto))
    productos = result.scalars().all()
    return [p for p in productos if p.categoria == categoria]

    # ✅ Filtra en SQL
    result = await session.execute(
        select(Producto).where(Producto.categoria == categoria)
    )
    return list(result.scalars().all())


# Batch inserts
async def bulk_insert_productos(session: AsyncSession, productos_data: list):
    # ❌ Inserciones una por una
    for data in productos_data:
        producto = Producto(**data)
        session.add(producto)
        await session.flush()

    # ✅ Bulk insert
    productos = [Producto(**data) for data in productos_data]
    session.add_all(productos)
    await session.flush()
```

## 19.5 Count Eficiente

```python
# count() puede ser lento en tablas grandes
# Alternativas:

# 1. Subquery con exists (más rápido si solo necesitas saber si existe)
async def producto_existe(session: AsyncSession, categoria_id: int) -> bool:
    from sqlalchemy import exists
    result = await session.execute(
        exists(select(Producto.id)).where(Producto.categoria_id == categoria_id).select()
    )
    return result.scalar()


# 2. COUNT con índice covering
async def count_con_index(session: AsyncSession):
    # Asegúrate de tener índice en la columna de filtrado
    result = await session.execute(
        select(func.count(Producto.id))
        .where(Producto.is_active == True)
    )
    return result.scalar()


# 3. Cachear el count (si no cambia frecuentemente)
async def get_total_productos(session: AsyncSession) -> int:
    cache_key = "stats:total_productos"
    cached = await cache.get(cache_key)
    if cached:
        return cached["total"]

    result = await session.execute(
        select(func.count(Producto.id)).where(Producto.is_active == True)
    )
    total = result.scalar()

    await cache.set(cache_key, {"total": total}, ttl=300)
    return total
```

## 19.6 Query Compilation Caching

```python
# SQLAlchemy compila queries - podemos cachear la compilación
from sqlalchemy.orm import Query

# Configure engine con pool de conexiones
engine = create_async_engine(
    DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True,
    pool_recycle=3600,  # Reciclar conexiones cada hora
    echo=False
)

# Queries compiladas se cachean automáticamente
# Pero podemos optimizar más:
from sqlalchemy.pool import QueuePool

engine = create_async_engine(
    DATABASE_URL,
    poolclass=QueuePool,
    pool_size=10,
    max_overflow=20,
    pool_timeout=30,
    pool_recycle=1800
)
```

## 19.7 Profiling

```python
# Medir tiempo de queries
import time
from functools import wraps

def time_query(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = await func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        logger.info(f"{func.__name__} took {elapsed:.3f}s")
        return result
    return wrapper


# En desarrollo: SQL echo
engine = create_async_engine(DATABASE_URL, echo=True)


# Query stats middleware
@app.middleware("http")
async def log_slow_requests(request: Request, call_next):
    start = time.perf_counter()
    response = await call_next(request)
    duration = time.perf_counter() - start

    if duration > 1.0:  # Log requests > 1s
        logger.warning(f"Slow request: {request.method} {request.url} took {duration:.2f}s")

    return response
```

## Ejercicios Prácticos

**Ejercicio 1**: Implementa cacheo de categoría con productos usando Redis.

**Ejercicio 2**: Optimiza el endpoint `GET /productos` para que use selectinload en relaciones.

**Ejercicio 3**: Crea un índice covering para la query de productos por categoría.

---

# SESIÓN 20: Proyecto Final Integrador

## Duración: 2 horas

## Objetivos

- Integrar todos los conceptos del curso
- Construir una API REST completa
- Implementar testing básico
- Documentar la API

## 20.1 Especificación del Proyecto

### API REST Completa de E-Commerce "TechStore"

**Entidades:**
- Usuarios (con roles: cliente, vendedor, admin)
- Vendedores (asociados a usuarios)
- Productos (asociados a vendedores y categorías)
- Categorías (jerárquicas)
- Etiquetas (N:M con productos)
- Órdenes (asociadas a usuarios)
- OrdenItems (productos en órdenes)

**Funcionalidades Requeridas:**

1. **Autenticación**
   - Registro y login con JWT
   - Refresh tokens
   - Roles: cliente, vendedor, admin

2. **Usuarios**
   - CRUD completo
   - Perfil propio
   - Solo admins pueden ver todos

3. **Vendedores**
   - Registro de vendedor (asociado a usuario)
   - Dashboard con estadísticas
   - Gestión de productos

4. **Productos**
   - CRUD completo
   - Búsqueda con filtros
   - Etiquetas
   - Imágenes (URL)
   - Paginación y ordenamiento

5. **Categorías**
   - Jerarquía (padre/hijo)
   - Productos por categoría

6. **Órdenes**
   - Crear orden con items
   - Actualizar status
   - Historial de compras
   - Cancelación (restaurando stock)

7. **Reportes**
   - Top productos
   - Ventas por período
   - Stats de vendedor

## 20.2 Estructura del Proyecto

```
techstore/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI app
│   ├── config.py               # Settings
│   ├── database/
│   │   ├── __init__.py
│   │   └── connection.py       # Async engine
│   ├── models/
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── vendedor.py
│   │   ├── producto.py
│   │   ├── categoria.py
│   │   ├── etiqueta.py
│   │   └── orden.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── usuario.py
│   │   ├── vendedor.py
│   │   ├── producto.py
│   │   ├── categoria.py
│   │   ├── etiqueta.py
│   │   └── orden.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   └── base.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── usuarios.py
│   │   ├── vendedores.py
│   │   ├── productos.py
│   │   ├── categorias.py
│   │   ├── etiquetas.py
│   │   └── ordenes.py
│   ├── security/
│   │   ├── __init__.py
│   │   ├── jwt.py
│   │   ├── utils.py
│   │   └── deps.py
│   ├── exceptions/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   └── handlers.py
│   └── cache.py
├── tests/
│   ├── conftest.py
│   ├── test_auth.py
│   ├── test_productos.py
│   └── test_ordenes.py
├── alembic/
│   ├── env.py
│   └── versions/
├── requirements.txt
├── .env.example
└── README.md
```

## 20.3 Implementación paso a paso

### Paso 1: Configuración Base
```python
# config.py
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    database_url: str = "postgresql+asyncpg://postgres:password@localhost:5432/techstore"
    secret_key: str
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings():
    return Settings()
```

### Paso 2: Modelos
```python
# models/producto.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class Producto(SQLModel, table=True):
    __tablename__ = "productos"

    id: Optional[int] = Field(default=None, primary_key=True)
    vendedor_id: int = Field(foreign_key="vendedores.id", index=True)
    categoria_id: Optional[int] = Field(default=None, foreign_key="categorias.id")

    nombre: str = Field(max_length=200, index=True)
    descripcion: Optional[str] = None
    precio: Decimal = Field(decimal_places=2, index=True)
    stock: int = Field(ge=0, default=0)
    imagen_url: Optional[str] = None
    is_active: bool = Field(default=True)

    vendedor: "Vendedor" = Relationship(back_populates="productos")
    categoria: Optional["Categoria"] = Relationship(back_populates="productos")
    etiquetas: List["Etiqueta"] = Relationship(
        back_populates="productos",
        link_model="ProductoEtiqueta"
    )
```

### Paso 3: Rutas con Todo
```python
# routes/productos.py
@router.get("/", response_model=List[ProductoResponse])
async def listar_productos(
    skip: int = 0,
    limit: int = 10,
    categoria_id: int = None,
    min_precio: float = None,
    max_precio: float = None,
    buscar: str = None,
    ordenar_por: str = "created_at",
    orden: str = "desc",
    session: AsyncSession = Depends(get_session)
):
    query = select(Producto).where(Producto.is_active == True)

    if categoria_id:
        query = query.where(Producto.categoria_id == categoria_id)
    if min_precio:
        query = query.where(Producto.precio >= min_precio)
    if max_precio:
        query = query.where(Producto.precio <= max_precio)
    if buscar:
        query = query.where(Producto.nombre.ilike(f"%{buscar}%"))

    columna = getattr(Producto, ordenar_por, Producto.created_at)
    if orden == "desc":
        columna = columna.desc()

    query = query.order_by(columna).offset(skip).limit(limit)
    result = await session.execute(query)

    return list(result.scalars().all())
```

## 20.4 Testing Required

```python
# tests/test_productos.py
@pytest.mark.asyncio
async def test_crud_producto(client: AsyncClient, vendedor_test):
    """Test flujo completo CRUD."""
    # Create
    response = await client.post("/productos/", json={
        "nombre": "Laptop Gaming",
        "precio": "1299.99",
        "stock": 5,
        "vendedor_id": vendedor_test.id
    })
    assert response.status_code == 201
    producto_id = response.json()["id"]

    # Read
    response = await client.get(f"/productos/{producto_id}")
    assert response.status_code == 200

    # Update
    response = await client.patch(f"/productos/{producto_id}", json={
        "stock": 10
    })
    assert response.status_code == 200
    assert response.json()["stock"] == 10

    # Delete
    response = await client.delete(f"/productos/{producto_id}")
    assert response.status_code == 204


@pytest.mark.asyncio
async def test_busqueda_con_filtros(client: AsyncClient, producto_test):
    """Test búsqueda con múltiples filtros."""
    response = await client.get(
        f"/productos/?min_precio=100&max_precio=2000&ordenar_por=precio&orden=asc"
    )
    assert response.status_code == 200
    data = response.json()
    assert all(100 <= p["precio"] <= 2000 for p in data)
```

## 20.5 Documentación README

```markdown
# TechStore API

API REST completa de e-commerce construida con FastAPI, SQLModel y AsyncPG.

## Características

- Autenticación JWT con roles
- CRUD completo de productos
- Órdenes con validación de stock
- Relaciones 1:N y N:M
- Paginación y ordenamiento
- Tests con pytest

## Quick Start

```bash
# Instalar dependencias
pip install -r requirements.txt

# Configurar .env
cp .env.example .env

# Migraciones
alembic upgrade head

# Ejecutar
uvicorn app.main:app --reload
```

## Documentación

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Endpoints Principales

### Autenticación
- POST /auth/register
- POST /auth/login
- GET /auth/me

### Productos
- GET /productos
- POST /productos
- GET /productos/{id}
- PATCH /productos/{id}
- DELETE /productos/{id}

### Órdenes
- POST /ordenes
- GET /ordenes
- PATCH /ordenes/{id}/status
```

---

# FIN DEL CURSO

## Resumen de Conceptos Cubiertos

Sesiones 11-20 completaron:
- Consultas avanzadas y agregaciones
- Validación y serialización
- Manejo de errores centralizado
- Paginación (offset y cursor)
- Transacciones y concurrencia
- Migraciones con Alembic
- Autenticación JWT
- Testing con pytest
- Optimización de queries
- Proyecto integrador final

## Próximos Pasos

1. Profundizar en deployment (Docker, Kubernetes)
2. Explorar WebSockets para tiempo real
3. Implementar background jobs (Celery)
4. Aprendiendo sobre GraphQL
5. Explorar microservicios

## Recursos Adicionales

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [AsyncPG Documentation](https://magicstack.github.io/asyncpg/)
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [Alembic Documentation](https://alembic.sqlalchemy.org/)
- [Pytest Documentation](https://docs.pytest.org/)

---

*Curso creado en Marzo 2026*
*Versión 1.0*
