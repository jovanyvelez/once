# Capítulo 14: Subconsultas y operadores avanzados

> Lo que necesitás cuando `SELECT * FROM tabla WHERE ...` ya no alcanza.

---

## 14.1 Funciones agregadas (`COUNT`, `AVG`, `SUM`, `MIN`, `MAX`)

```python
from sqlalchemy import func, select

with Session(engine) as session:
    # COUNT
    total = session.scalar(select(func.count(Producto.id)))
    print(f"Total: {total}")

    # AVG
    promedio = session.scalar(select(func.avg(Producto.precio)))
    print(f"Promedio: {promedio}")

    # SUM
    suma = session.scalar(select(func.sum(Producto.precio)))
    print(f"Suma: {suma}")

    # MIN y MAX
    mas_barato = session.scalar(select(func.min(Producto.precio)))
    mas_caro = session.scalar(select(func.max(Producto.precio)))
```

### Usar en una columna calculada

```python
stmt = select(
    Producto.nombre,
    (Producto.precio * 0.9).label("precio_con_descuento"),  # 10% off
)
```

---

## 14.2 `GROUP BY` con `group_by()` y `having()`

```python
from sqlalchemy import func

# Para cada categoría: nombre y cantidad de productos
stmt = (
    select(
        Categoria.nombre,
        func.count(Producto.id).label("cantidad"),
    )
    .join(Producto, Producto.categoria_id == Categoria.id)
    .group_by(Categoria.nombre)
    .having(func.count(Producto.id) > 0)   # HAVING count > 0
    .order_by(func.count(Producto.id).desc())
)

for nombre, cantidad in session.execute(stmt):
    print(f"{nombre}: {cantidad}")
```

---

## 14.3 Subconsultas en `WHERE`

### `IN` con subquery

```python
# Productos cuya categoría tiene al menos un producto
stmt = (
    select(Producto)
    .where(Producto.categoria_id.in_(
        select(Producto.categoria_id)
        .where(Producto.precio > 10000)
        .distinct()
    ))
)
```

### Comparación con subquery

```python
# Productos más caros que el promedio
stmt = (
    select(Producto)
    .where(Producto.precio > select(func.avg(Producto.precio)).scalar_subquery())
)
```

### `EXISTS` y `NOT EXISTS`

```python
from sqlalchemy import exists, not_

# Usuarios que tienen al menos una dirección
subq = exists().where(Direccion.usuario_id == Usuario.id)
stmt = select(Usuario).where(subq)

# Usuarios SIN direcciones
stmt = select(Usuario).where(~subq)  # ~ es NOT
```

---

## 14.4 Subqueries en `FROM`

```python
# Subquery como tabla virtual
precio_promedio_categoria = (
    select(
        Producto.categoria_id,
        func.avg(Producto.precio).label("promedio"),
    )
    .group_by(Producto.categoria_id)
    .subquery()
)

# Úsalo como una tabla más
stmt = (
    select(Categoria.nombre, precio_promedio_categoria.c.promedio)
    .join(precio_promedio_categoria, precio_promedio_categoria.c.categoria_id == Categoria.id)
)
```

---

## 14.5 CTE — Common Table Expressions

Las CTEs son como subqueries pero **más legibles**, especialmente para queries complejas.

```python
# WITH productos_caros AS (SELECT * FROM productos WHERE precio > 10000)
productos_caros = (
    select(Producto)
    .where(Producto.precio > 10000)
    .cte("productos_caros")
)

# SELECT * FROM productos_caros WHERE categoria_id = 1
stmt = select(productos_caros).where(productos_caros.c.categoria_id == 1)
```

### CTE con varios usos

```python
from sqlalchemy import case

# CTE: productos vendidos este mes
ventas_mes = (
    select(
        Pedido.producto_id,
        func.count(Pedido.id).label("total"),
    )
    .where(Pedido.fecha >= "2026-01-01")
    .group_by(Pedido.producto_id)
    .cte("ventas_mes")
)

# Uso en query principal
stmt = (
    select(Producto.nombre, ventas_mes.c.total)
    .join(ventas_mes, ventas_mes.c.producto_id == Producto.id)
    .order_by(ventas_mes.c.total.desc())
)
```

---

## 14.6 Funciones de fecha

```python
from sqlalchemy import func

# Fecha actual
hoy = func.current_date()
ahora = func.now()

# Extraer partes
stmt = select(
    Producto.nombre,
    func.year(Producto.creado_en).label("año"),
    func.month(Producto.creado_en).label("mes"),
)

# Diferencia entre fechas
dias_desde_alta = func.date_diff(func.current_date(), Producto.creado_en)
```

---

## 14.7 `CASE` condicional

```python
from sqlalchemy import case

# Clasificar productos por precio
stmt = select(
    Producto.nombre,
    case(
        (Producto.precio < 100, "Barato"),
        (Producto.precio < 1000, "Medio"),
        (Producto.precio < 10000, "Caro"),
        else_="Premium",
    ).label("clasificacion"),
)
```

---

## 14.8 Full-text search (PostgreSQL)

```python
from sqlalchemy.dialects.postgresql import TSVECTOR

# Para Postgres (no funciona en SQLite directamente)
class Articulo(Base):
    __tablename__ = "articulos"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str]
    contenido: Mapped[str]
    busqueda: Mapped[str] = mapped_column(TSVECTOR)
```

---

## 14.9 Tips de performance para queries avanzadas

| Tip | Explicación |
|---|---|
| **Indexá columnas de `WHERE` y `ORDER BY`** | Reduce escaneo lineal. |
| **Usá `EXISTS` en vez de `COUNT(*)`** | `EXISTS` corta la búsqueda al primer match. |
| **Evitá `SELECT *`** | Traé solo las columnas necesarias. |
| **`LIMIT` siempre** | Si solo necesitás 10, decilo. |
| **`EXPLAIN ANALYZE`** | Usá esta query para ver el plan de ejecución. |

```sql
EXPLAIN ANALYZE SELECT * FROM productos WHERE precio > 100;
```

---

## 🛠️ Ejercicios prácticos

### 🟢 Ejercicio 14.1: Funciones agregadas

Para el modelo `Producto`:

1. Calculá el precio promedio.
2. Calculá el precio total (suma).
3. Encontrá el producto más caro.

**Solución**: [soluciones/14-subconsultas.md](../soluciones/14-subconsultas.md#ejercicio-141)

---

### 🟡 Ejercicio 14.2: GROUP BY

Para cada categoría, calculá la cantidad de productos y el precio promedio. Mostrá solo las categorías con más de 1 producto.

**Solución**: [soluciones/14-subconsultas.md](../soluciones/14-subconsultas.md#ejercicio-142)

---

### 🟡 Ejercicio 14.3: EXISTS

Listá los productos que tienen al menos una venta registrada. Modelá una tabla `Venta(producto_id, fecha, monto)` y resolvélo con `EXISTS`.

**Solución**: [soluciones/14-subconsultas.md](../soluciones/14-subconsultas.md#ejercicio-143)

---

### 🟡 Ejercicio 14.4: CASE

Listá productos con una columna calculada `categoria_precio`:

- `"Económico"` si precio < 100.
- `"Medio"` si 100 <= precio < 1000.
- `"Premium"` si precio >= 1000.

**Solución**: [soluciones/14-subconsultas.md](../soluciones/14-subconsultas.md#ejercicio-144)

---

### 🔴 Ejercicio 14.5: CTE con ranking

Usá un CTE para listar los productos ordenados por precio descendente dentro de cada categoría, con un ranking `1, 2, 3...`.

**Solución**: [soluciones/14-subconsultas.md](../soluciones/14-subconsultas.md#ejercicio-145)

---

## 🎓 Lo que aprendiste

- Funciones agregadas con `func.count()`, `func.avg()`, etc.
- `GROUP BY` y `HAVING` para agrupar y filtrar agregaciones.
- Subqueries con `.in_()`, `EXISTS`, `scalar_subquery()`.
- CTEs para queries complejas y legibles.
- `CASE` para lógica condicional.

## 📖 Siguiente

[Capítulo 15: Eventos SQLAlchemy →](./15-eventos.md)