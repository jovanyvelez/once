# Soluciones — Capítulo 19: Errores comunes

[Volver al capítulo 19](../capitulos/19-errores-comunes.md)

---

## Ejercicio 19.1

**DetachedInstanceError**

```python
# ❌ Versión rota
def procesar():
    with Session(engine) as session:
        u = session.get(Usuario, 1)
    print(u.direcciones)   # 💥 DetachedInstanceError
```

**Solución 1**: usar `selectinload` para traer las direcciones dentro del `with`:

```python
from sqlalchemy.orm import selectinload
from sqlalchemy import select


def procesar():
    with Session(engine) as session:
        stmt = select(Usuario).options(selectinload(Usuario.direcciones))
        u = session.scalars(stmt).one()
        print(u.direcciones)  # ✅ dentro del with
```

**Solución 2**: usar la relación **dentro** del `with`:

```python
def procesar():
    with Session(engine) as session:
        u = session.get(Usuario, 1)
        print(u.direcciones)  # ✅ dentro del with
```

[Volver al ejercicio ↑](../capitulos/19-errores-comunes.md#%C2%B0-ejercicio-191)

---

## Ejercicio 19.2

**`IntegrityError` en endpoint**

```python
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException


@router.post("/", response_model=ProductoPublic)
def crear(data: ProductoCreate, session: SessionDep) -> ProductoPublic:
    try:
        nuevo = Producto(**data.model_dump())
        session.add(nuevo)
        session.commit()
        session.refresh(nuevo)
        return nuevo
    except IntegrityError:
        session.rollback()
        raise HTTPException(
            status_code=400,
            detail="Ya existe un producto con ese SKU",
        )
```

[Volver al ejercicio ↑](../capitulos/19-errores-comunes.md#%C2%B1-ejercicio-192)

---

## Ejercicio 19.3

**Foreign Key mal escrita**

```python
# ❌ Mal
post_id: Mapped[int] = mapped_column(ForeignKey("Post.id"))
```

**Problemas**:

1. La tabla se llama `posts` (plural, minúscula), no `Post`.
2. La columna es `id` (correcto, no es el problema).

**Versión corregida**:

```python
post_id: Mapped[int] = mapped_column(ForeignKey("posts.id"))  # ✅
```

> 🎓 **Regla**: el nombre en `ForeignKey` tiene que coincidir **exactamente** con `__tablename__` y el nombre de la columna.

[Volver al ejercicio ↑](../capitulos/19-errores-comunes.md#%C2%B1-ejercicio-193)

---

## Ejercicio 19.4

**Depurá N+1**

```python
# ❌ Código problemático
@app.get("/api/reports/")
def reports(session: SessionDep):
    productos = session.scalars(select(Producto)).all()
    resultado = []
    for p in productos:
        # 💥 Cada acceso a p.categoria dispara un SELECT
        categoria_nombre = p.categoria.nombre
        resultado.append({
            "producto": p.nombre,
            "categoria": categoria_nombre,
        })
    return resultado
```

**Diagnóstico**: 1 + N queries (N+1).

**Solución**:

```python
from sqlalchemy.orm import selectinload


@app.get("/api/reports/")
def reports(session: SessionDep):
    # 1 sola query extra con IN(...)
    stmt = select(Producto).options(selectinload(Producto.categoria))
    productos = session.scalars(stmt).all()
    
    return [
        {
            "producto": p.nombre,
            "categoria": p.categoria.nombre,
        }
        for p in productos
    ]
```

**Resultado**: 2 queries totales (en vez de 1 + N). Para 1000 productos, pasás de 1001 a 2 queries.

[Volver al ejercicio ↑](../capitulos/19-errores-comunes.md#%F0%9F%94%B4-ejercicio-194)