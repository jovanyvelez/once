# Soluciones — Capítulo 14: Subconsultas y operadores avanzados

[Volver al capítulo 14](../capitulos/14-subconsultas.md)

---

## Ejercicio 14.1

**Funciones agregadas**

```python
from sqlalchemy import select, func


with Session(engine) as session:
    promedio = session.scalar(select(func.avg(Producto.precio)))
    total = session.scalar(select(func.sum(Producto.precio)))
    mas_caro = session.scalar(select(func.max(Producto.precio)))
    
    print(f"Promedio: {promedio}, Total: {total}, Más caro: {mas_caro}")
```

[Volver al ejercicio ↑](../capitulos/14-subconsultas.md#%C2%B0-ejercicio-141)

---

## Ejercicio 14.2

**GROUP BY con HAVING**

```python
stmt = (
    select(
        Categoria.nombre,
        func.count(Producto.id).label("cantidad"),
        func.avg(Producto.precio).label("promedio"),
    )
    .join(Producto, Producto.categoria_id == Categoria.id)
    .group_by(Categoria.nombre)
    .having(func.count(Producto.id) > 1)
)
```

[Volver al ejercicio ↑](../capitulos/14-subconsultas.md#%C2%B1-ejercicio-142)

---

## Ejercicio 14.3

**EXISTS**

```python
from sqlalchemy import exists


class Venta(Base):
    __tablename__ = "ventas"
    id: Mapped[int] = mapped_column(primary_key=True)
    producto_id: Mapped[int] = mapped_column(ForeignKey("productos.id"))
    fecha: Mapped[datetime] = mapped_column(DateTime)
    monto: Mapped[float]


stmt = select(Producto).where(
    exists().where(Venta.producto_id == Producto.id)
)
```

[Volver al ejercicio ↑](../capitulos/14-subconsultas.md#%C2%B1-ejercicio-143)

---

## Ejercicio 14.4

**CASE**

```python
from sqlalchemy import case


stmt = select(
    Producto.nombre,
    Producto.precio,
    case(
        (Producto.precio < 100, "Económico"),
        (Producto.precio < 1000, "Medio"),
        else_="Premium",
    ).label("categoria_precio"),
)
for nombre, precio, categoria in session.execute(stmt):
    print(f"{nombre} (${precio}) → {categoria}")
```

[Volver al ejercicio ↑](../capitulos/14-subconsultas.md#%C2%B1-ejercicio-144)

---

## Ejercicio 14.5

**CTE con ranking**

```python
from sqlalchemy import over


# CTE con ranking por categoría
ranking_cte = (
    select(
        Producto.id,
        Producto.nombre,
        Producto.categoria_id,
        Producto.precio,
        func.row_number()
        .over(partition_by=Producto.categoria_id, order_by=Producto.precio.desc())
        .label("ranking"),
    )
    .cte("ranking_categoria")
)

# Query final
stmt = select(
    ranking_cte.c.nombre,
    ranking_cte.c.categoria_id,
    ranking_cte.c.precio,
    ranking_cte.c.ranking,
).order_by(ranking_cte.c.categoria_id, ranking_cte.c.ranking)

for nombre, cat, precio, ranking in session.execute(stmt):
    print(f"#{ranking} en cat {cat}: {nombre} (${precio})")
```

[Volver al ejercicio ↑](../capitulos/14-subconsultas.md#%F0%9F%94%B4-ejercicio-145)