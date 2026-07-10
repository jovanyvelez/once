# Soluciones — Capítulo 6: Anotaciones `Mapped[T]`

[Volver al capítulo 6](../capitulos/06-anotaciones-mapped.md)

---

## Ejercicio 6.1

**Mapeo de tipos**

| Columna SQL | Anotación Python |
|---|---|
| `nombre VARCHAR(100)` | `Mapped[str] = mapped_column(String(100))` |
| `descripcion TEXT` | `Mapped[str] = mapped_column(Text)` |
| `precio NUMERIC(12, 2)` | `Mapped[float] = mapped_column(Numeric(12, 2))` |
| `cantidad INTEGER NOT NULL DEFAULT 0` | `Mapped[int] = mapped_column(Integer, default=0)` |
| `activo BOOLEAN DEFAULT true` | `Mapped[bool] = mapped_column(Boolean, default=True)` |
| `creado_en DATETIME DEFAULT CURRENT_TIMESTAMP` | `Mapped[datetime] = mapped_column(DateTime, server_default=func.now())` |
| `tags JSON` | `Mapped[dict] = mapped_column(JSON)` |
| `foto BLOB` | `Mapped[bytes] = mapped_column(LargeBinary)` |

[Volver al ejercicio ↑](../capitulos/06-anotaciones-mapped.md#%C2%B0-ejercicio-61)

---

## Ejercicio 6.2

**Optionales vs requeridos**

```python
from datetime import datetime
from decimal import Decimal
from typing import Optional
from sqlalchemy import String, Numeric, Integer, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Pedido(Base):
    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(primary_key=True)

    # NO nullable (no son Optional)
    cliente_email: Mapped[str] = mapped_column(String(120))
    monto: Mapped[Decimal] = mapped_column(Numeric(12, 2))

    # SÍ nullable (tienen Optional)
    direccion_envio: Mapped[Optional[str]] = mapped_column(default=None)
    notas: Mapped[Optional[str]] = mapped_column(default=None)

    fecha_pedido: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
```

[Volver al ejercicio ↑](../capitulos/06-anotaciones-mapped.md#%C2%B0-ejercicio-62)

---

## Ejercicio 6.3

**El error del `Float` para plata**

```python
# El problema
>>> 0.1 + 0.2
0.30000000000000004   # 💥 No es exactamente 0.3
```

Con `Mapped[float]`, los precios se acumulan en una columna `FLOAT` que tiene este mismo problema:

```python
# ❌ Con Float
producto = Producto(precio=19.99)
# En la base: 19.99
# ... alguien lo cambia, se hacen cálculos ...
# En la base: 19.989999999999998  # 💥 no es exactamente lo que esperabas
```

```python
# ✅ Con Numeric
from decimal import Decimal
from sqlalchemy import Numeric

producto = Producto(precio=Decimal("19.99"))   # exacto
# Cálculos exactos, redondeo predecible.
```

**Regla**: nunca `float` para dinero. Usá `Decimal` (que en SQLAlchemy se mapea a `NUMERIC`).

[Volver al ejercicio ↑](../capitulos/06-anotaciones-mapped.md#%C2%B1-ejercicio-63)

---

## Ejercicio 6.4

**Elegí el default correcto**

| Caso | Default apropiado | Razón |
|---|---|---|
| 1. UUID en Python | `default=` con `uuid.uuid4` | La DB no tiene cómo generar un UUID. |
| 2. Timestamp al insertar | `server_default=func.now()` | Lo pone la DB; consistente entre Python y la DB. |
| 3. Estado inicial `"pendiente"` | `default="pendiente"` | Es un valor de Python determinista. |
| 4. Slug del título | `default=` con una función que calcule | Lógica Python; la DB no sabe. |

[Volver al ejercicio ↑](../capitulos/06-anotaciones-mapped.md#%C2%B1-ejercicio-64)

---

## Ejercicio 6.5

**Diagnóstico**

```python
expiracion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
```

**Problema**: `datetime.now()` **se ejecuta cuando se define la clase**, no cuando se crean las instancias. Resultado: **todas las sesiones tendrían la misma fecha de expiración** (el momento en que arrancó el proceso).

**Solución 1**: pasar la función sin llamarla:

```python
expiracion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
#                                                              ^ sin paréntesis
```

**Solución 2** (mejor): que la DB ponga la fecha:

```python
from sqlalchemy import func

expiracion: Mapped[datetime] = mapped_column(
    DateTime, default=datetime.now, onupdate=datetime.now
)
# o todavía mejor:
expiracion: Mapped[datetime] = mapped_column(
    DateTime, server_default=func.now()
)
```

[Volver al ejercicio ↑](../capitulos/06-anotaciones-mapped.md#%C2%B1-ejercicio-65)