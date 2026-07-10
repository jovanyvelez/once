# Capítulo 12: Consultas (`SELECT`, `WHERE`, `JOIN`)

> La nueva forma de hacer consultas en SQLAlchemy 2.0: con `select()`, **no** con `query()`.

---

## 12.1 El nuevo `select()`

En SQLAlchemy 2.0, todas las consultas arrancan con la función `select()` del módulo `sqlalchemy`:

```python
from sqlalchemy import select

stmt = select(Producto)         # SELECT * FROM productos
resultados = session.scalars(stmt).all()
```

Comparado con 1.x:

```python
# ❌ SQLAlchemy 1.x (antiguo)
session.query(Producto).all()
```

> ⚠️ Si ves `query()` en un tutorial de 2024, **es viejo**. Siempre usá `select()`.

---

## 12.2 Anatomía de una consulta moderna

```python
stmt = (
    select(Producto)                          # 1. qué columnas / modelo
    .where(Producto.precio > 1000)           # 2. filtros
    .where(Producto.sku.like("CF-%"))         #    se encadenan con AND
    .order_by(Producto.precio.desc())         # 3. ordenamiento
    .limit(10)                                # 4. límite
    .offset(20)                               # 5. salto inicial
)
```

Esto se traduce a:

```sql
SELECT *
FROM productos
WHERE precio > 1000 AND sku LIKE 'CF-%'
ORDER BY precio DESC
LIMIT 10 OFFSET 20
```

---

## 12.3 Filtros con `where()`

### Filtrado por igualdad

```python
# WHERE nombre = 'Cafetera'
stmt = select(Producto).where(Producto.nombre == "Cafetera")
```

### Encadenar varios `where()` es AND automático

```python
# WHERE precio > 5000 AND sku LIKE 'CF-%'
stmt = (
    select(Producto)
    .where(Producto.precio > 5000)
    .where(Producto.sku.like("CF-%"))
)
```

### OR con `or_()`

```python
from sqlalchemy import or_

# WHERE nombre = 'Cafetera' OR sku LIKE 'CF-%'
stmt = select(Producto).where(
    or_(
        Producto.nombre == "Cafetera",
        Producto.sku.like("CF-%"),
    )
)
```

### AND explícito con `and_()`

```python
from sqlalchemy import and_

# WHERE (nombre = 'Cafetera' AND precio > 1000) OR sku LIKE 'CF-%'
stmt = select(Producto).where(
    or_(
        and_(Producto.nombre == "Cafetera", Producto.precio > 1000),
        Producto.sku.like("CF-%"),
    )
)
```

---

## 12.4 Operadores comunes

| Python | SQL | Ejemplo |
|---|---|---|
| `==` | `=` | `Producto.nombre == "Ana"` |
| `!=` / `<>` | `<>` | `Producto.nombre != "Ana"` |
| `>`, `>=`, `<`, `<=` | igual | `Producto.precio > 100` |
| `.in_([1, 2, 3])` | `IN (...)` | `Producto.id.in_([1, 2, 3])` |
| `.not_in([...])` | `NOT IN (...)` | `Producto.id.not_in([1, 2])` |
| `.like("%texto%")` | `LIKE` | `Producto.nombre.like("%café%")` |
| `.ilike("%texto%")` | `ILIKE` (case-insensitive) | `Producto.nombre.ilike("café")` |
| `.is_(None)` / `.is_not(None)` | `IS NULL` / `IS NOT NULL` | `Producto.descripcion.is_(None)` |
| `.between(10, 100)` | `BETWEEN` | `Producto.precio.between(10, 100)` |
| `.contains("texto")` | `LIKE '%texto%'` | `Producto.nombre.contains("Cafetera")` |
| `.startswith("texto")` | `LIKE 'texto%'` | `Producto.nombre.startswith("Cafetera")` |

> 🎓 **Convenciones**: `like` y `ilike` con `%texto%`. El símbolo `%` significa "cualquier texto".

---

## 12.5 Seleccionar columnas específicas

Por defecto, `select(Producto)` trae **todas** las columnas. Si querés un subset:

```python
# SELECT id, nombre FROM productos
stmt = select(Producto.id, Producto.nombre)
```

Para iterar como tuplas:

```python
with Session(engine) as session:
    for id, nombre in session.execute(stmt):
        print(f"{id}: {nombre}")
```

### Alias para columnas calculadas

```python
from sqlalchemy import func

# SELECT nombre, LENGTH(descripcion) AS largo
stmt = select(
    Producto.nombre,
    func.length(Producto.descripcion).label("largo"),
)
```

---

## 12.6 Orden, límite y offset

```python
# ORDER BY nombre ASC
stmt = select(Producto).order_by(Producto.nombre)

# ORDER BY precio DESC, nombre ASC
stmt = select(Producto).order_by(Producto.precio.desc(), Producto.nombre)

# TOP 10
stmt = select(Producto).limit(10)

# Paginado (página 3 de 20)
stmt = select(Producto).offset(40).limit(20)
```

---

## 12.7 JOIN — unir tablas

### JOIN explícito

```python
# SELECT productos.* FROM productos
# JOIN categorias ON categorias.id = productos.categoria_id
# WHERE categorias.nombre = 'Electrónica'
stmt = (
    select(Producto)
    .join(Categoria, Categoria.id == Producto.categoria_id)
    .where(Categoria.nombre == "Electrónica")
)
```

### JOIN usando la relación directa

```python
# SQLAlchemy sabe que Producto.categoria es Categoria
stmt = (
    select(Producto)
    .join(Producto.categoria)
    .where(Categoria.nombre == "Electrónica")
)
```

### LEFT OUTER JOIN

```python
# Trae productos SIN categoría también
stmt = (
    select(Producto)
    .join(Producto.categoria, isouter=True)
)
```

### Múltiples JOINs

```python
# productos → categorías → proveedores
stmt = (
    select(Producto)
    .join(Producto.categoria)
    .join(Categoria.proveedor)
    .where(Proveedor.pais == "Argentina")
)
```

---

## 12.8 Ejecución de la consulta

```python
stmt = select(Producto).where(Producto.precio > 1000)

# Devuelve todos en una lista
resultados = session.scalars(stmt).all()

# Devuelve el primero o None
primero = session.scalars(stmt).first()

# Devuelve uno o falla
unico = session.scalars(stmt).one()

# Itera uno a uno (útil para grandes volúmenes)
for producto in session.scalars(stmt):
    print(producto)
```

> 💡 **Para datasets grandes**, iterar directamente es más eficiente que `.all()` (no carga todo en memoria).

---

## 12.9 DISTINCT

```python
# SELECT DISTINCT categoria_id FROM productos
stmt = select(Producto.categoria_id).distinct()
```

---

## 12.10 Alias (cuando necesitás la misma tabla dos veces)

```python
from sqlalchemy.orm import aliased

# Self-join: empleados con su jefe
EmpleadoJefe = aliased(Empleado)

stmt = (
    select(Empleado, EmpleadoJefe)
    .join(EmpleadoJefe, Empleado.jefe_id == EmpleadoJefe.id)
)
```

> 🎓 **Útil cuando**: una tabla se referencia a sí misma (empleados con su jefe, comentarios con su respuesta).

---

## 12.11 UNION, INTERSECT, EXCEPT

```python
from sqlalchemy import union, union_all

q1 = select(Producto.id).where(Producto.precio < 100)
q2 = select(Producto.id).where(Producto.sku.like("DESC-%"))

# Todos los IDs únicos
stmt = union(q1, q2)

# Todos, incluyendo duplicados
stmt = union_all(q1, q2)
```

---

## 12.12 Subconsultas

```python
# IDs de categorías con productos
subq = select(Producto.categoria_id).distinct().subquery()

# Productos cuyas categorías tienen al menos un producto
stmt = select(Producto).where(Producto.categoria_id.in_(subq))
```

---

## 12.13 CTE — Common Table Expressions (WITH ... AS)

```python
from sqlalchemy import select

# Productos caros por categoría
stmt_caros = (
    select(Producto.categoria_id, Producto.precio)
    .where(Producto.precio > 10000)
    .cte("productos_caros")
)

stmt = (
    select(Categoria.nombre, stmt_caros.c.precio)
    .join(stmt_caros, stmt_caros.c.categoria_id == Categoria.id)
)
```

> 🎓 **CTE vs subquery**: las CTEs son más legibles en SQL, especialmente para queries complejas.

---

## 12.14 Resumen del flujo

```python
stmt = (
    select(Modelo)                          # FROM
    .join(Otra, ...)                        # JOIN
    .where(Modelo.campo > valor)            # WHERE
    .group_by(Modelo.campo)                 # GROUP BY
    .having(func.count(...) > 1)            # HAVING
    .order_by(Modelo.campo.desc())          # ORDER BY
    .limit(10)                              # LIMIT
    .offset(0)                              # OFFSET
)

resultado = session.scalars(stmt).all()
```

---

## 🛠️ Ejercicios prácticos

### 🟢 Ejercicio 12.1: Filtros básicos

Usando el modelo `Producto` (con precio y stock), escribí queries para:

1. Traer productos con precio > 500.
2. Traer productos cuyo nombre contiene `"café"` (case-insensitive).
3. Traer productos con stock entre 10 y 50.

**Solución**: [soluciones/12-consultas.md](../soluciones/12-consultas.md#ejercicio-121)

---

### 🟡 Ejercicio 12.2: Orden y paginación

Escribí una query que devuelva la **segunda página** de productos (asumiendo 20 por página), ordenados por precio descendente.

**Solución**: [soluciones/12-consultas.md](../soluciones/12-consultas.md#ejercicio-122)

---

### 🟡 Ejercicio 12.3: Substring con regex

Traé todos los productos cuyo `sku` termina con `"001"`. ¿Qué método usaste?

**Solución**: [soluciones/12-consultas.md](../soluciones/12-consultas.md#ejercicio-123)

---

### 🟡 Ejercicio 12.4: JOIN con filtro

Traé todos los productos de la categoría `"Electrónica"` mostrando nombre del producto y nombre de la categoría.

**Solución**: [soluciones/12-consultas.md](../soluciones/12-consultas.md#ejercicio-124)

---

### 🟡 Ejercicio 12.5: Alias

Modelá `Empleado(jefe_id)` con autorreferencia. Escribí una query que traiga cada empleado con el nombre de su jefe (o `None` si no tiene).

**Solución**: [soluciones/12-consultas.md](../soluciones/12-consultas.md#ejercicio-125)

---

### 🔴 Ejercicio 12.6: Top N por categoría

Escribí una query que devuelva el **producto más caro** de cada categoría. (Pista: subquery con `ROW_NUMBER()` o CTE).

**Solución**: [soluciones/12-consultas.md](../soluciones/12-consultas.md#ejercicio-126)

---

## 🎓 Lo que aprendiste

- `select()` es la única forma de armar consultas en SQLAlchemy 2.0.
- `.where()` se encadena con AND automáticamente; usá `or_()` y `and_()` para más control.
- Operadores como `.in_()`, `.like()`, `.between()` cubren la mayoría de los casos.
- `.join()` puede recibir una relación o una expresión manual.
- `.scalars()` devuelve objetos ORM; `.execute()` devuelve tuplas.

## 📖 Siguiente

[Capítulo 13: Relaciones entre tablas (lo que nadie te explica bien) →](./13-relaciones.md)