# Soluciones — Capítulo 12: Consultas

[Volver al capítulo 12](../capitulos/12-consultas.md)

---

## Ejercicio 12.1

**Filtros básicos**

```python
# 1. Precio > 500
stmt1 = select(Producto).where(Producto.precio > 500)

# 2. Nombre contiene "café" (case-insensitive)
stmt2 = select(Producto).where(Producto.nombre.ilike("%café%"))

# 3. Stock entre 10 y 50
stmt3 = select(Producto).where(Producto.stock.between(10, 50))
```

[Volver al ejercicio ↑](../capitulos/12-consultas.md#%C2%B0-ejercicio-121)

---

## Ejercicio 12.2

**Orden y paginación**

```python
# Segunda página = offset (página - 1) * limit
# Página 2, 20 por página → offset=20

stmt = (
    select(Producto)
    .order_by(Producto.precio.desc())
    .limit(20)
    .offset(20)
)
```

[Volver al ejercicio ↑](../capitulos/12-consultas.md#%C2%B1-ejercicio-122)

---

## Ejercicio 12.3

**Substring con regex**

```python
# sku que termina con "001"
stmt = select(Producto).where(Producto.sku.like("%001"))
```

Alternativas:
- `Producto.sku.endswith("001")` (más explícito en Python).

[Volver al ejercicio ↑](../capitulos/12-consultas.md#%C2%B1-ejercicio-123)

---

## Ejercicio 12.4

**JOIN con filtro**

```python
stmt = (
    select(Producto.nombre, Categoria.nombre)
    .join(Producto.categoria)
    .where(Categoria.nombre == "Electrónica")
)
for producto, categoria in session.execute(stmt):
    print(f"{producto} → {categoria}")
```

[Volver al ejercicio ↑](../capitulos/12-consultas.md#%C2%B1-ejercicio-124)

---

## Ejercicio 12.5

**Alias (self-join)**

```python
from sqlalchemy.orm import aliased


EmpleadoJefe = aliased(Empleado)

stmt = (
    select(Empleado.nombre, EmpleadoJefe.nombre)
    .join(EmpleadoJefe, Empleado.jefe_id == EmpleadoJefe.id, isouter=True)
)
```

El `isouter=True` hace LEFT JOIN, así empleados sin jefe también aparecen (con `None` como jefe).

[Volver al ejercicio ↑](../capitulos/12-consultas.md#%C2%B1-ejercicio-125)

---

## Ejercicio 12.6

**Top N por categoría**

```python
from sqlalchemy import func, over


# Subquery: precio máximo por categoría
stmt_max = (
    select(
        Producto.categoria_id,
        func.max(Producto.precio).label("max_precio"),
    )
    .group_by(Producto.categoria_id)
    .subquery()
)

stmt = (
    select(Producto.nombre, Categoria.nombre, Producto.precio)
    .join(Producto.categoria)
    .join(
        stmt_max,
        (Producto.categoria_id == stmt_max.c.categoria_id)
        & (Producto.precio == stmt_max.c.max_precio),
    )
)
```

**Alternativa con `ROW_NUMBER()`**:

```python
# CTE
productos_ranqueados = (
    select(
        Producto,
        func.row_number()
        .over(partition_by=Producto.categoria_id, order_by=Producto.precio.desc())
        .label("rn")
    )
    .cte("ranked")
)

stmt = (
    select(productos_ranqueados)
    .where(productos_ranqueados.c.rn == 1)
)
```

[Volver al ejercicio ↑](../capitulos/12-consultas.md#%F0%9F%94%B4-ejercicio-126)