# Soluciones — Capítulo 17: FastAPI + SQLAlchemy

[Volver al capítulo 17](../capitulos/17-fastapi.md)

---

## Ejercicio 17.1

**Tu primer endpoint**

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/saludo/{nombre}")
def saludar(nombre: str):
    return {"saludo": f"Hola {nombre}!"}
```

Probá en: `http://127.0.0.1:8000/saludo/Mundo` → `{"saludo": "Hola Mundo!"}`

[Volver al ejercicio ↑](../capitulos/17-fastapi.md#%C2%B0-ejercicio-171)

---

## Ejercicio 17.2

**Schemas completos**

```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ComentarioBase(BaseModel):
    texto: str = Field(..., min_length=1, max_length=1000)
    autor: str = Field(..., min_length=1, max_length=100)


class ComentarioCreate(ComentarioBase):
    pass


class ComentarioPublic(ComentarioBase):
    id: int
    fecha: datetime
    model_config = ConfigDict(from_attributes=True)


class ComentarioUpdate(BaseModel):
    texto: Optional[str] = Field(default=None, min_length=1, max_length=1000)
```

[Volver al ejercicio ↑](../capitulos/17-fastapi.md#%C2%B1-ejercicio-172)

---

## Ejercicio 17.3

**Endpoint con filtros**

```python
from typing import Optional
from fastapi import Query
from decimal import Decimal


@router.get("/", response_model=List[ProductoPublic])
def listar(
    session: SessionDep,
    search: Optional[str] = Query(None, description="Buscar en nombre"),
    min_precio: Optional[Decimal] = Query(None, ge=0),
    max_precio: Optional[Decimal] = Query(None, ge=0),
    categoria_id: Optional[int] = Query(None, ge=1),
    offset: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=500),
) -> List[ProductoPublic]:
    stmt = select(Producto)

    if search:
        stmt = stmt.where(Producto.nombre.ilike(f"%{search}%"))
    if min_precio is not None:
        stmt = stmt.where(Producto.precio >= min_precio)
    if max_precio is not None:
        stmt = stmt.where(Producto.precio <= max_precio)
    if categoria_id is not None:
        stmt = stmt.where(Producto.categoria_id == categoria_id)

    stmt = stmt.offset(offset).limit(limit)
    return list(session.scalars(stmt))
```

[Volver al ejercicio ↑](../capitulos/17-fastapi.md#%C2%B1-ejercicio-173)

---

## Ejercicio 17.4

**PATCH robusto**

```python
from fastapi import HTTPException
from sqlalchemy.exc import IntegrityError


@router.patch("/{producto_id}", response_model=ProductoPublic)
def actualizar(
    producto_id: int,
    data: ProductoUpdate,
    session: SessionDep,
) -> ProductoPublic:
    # 1. Verificar que venga al menos un campo
    cambios = data.model_dump(exclude_unset=True)
    if not cambios:
        raise HTTPException(400, "Debe enviar al menos un campo")

    # 2. Verificar que el producto existe
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(404, "Producto no encontrado")

    # 3. Aplicar cambios
    for campo, valor in cambios.items():
        setattr(producto, campo, valor)

    # 4. Intentar guardar, manejando IntegrityError
    try:
        session.commit()
        session.refresh(producto)
    except IntegrityError:
        session.rollback()
        raise HTTPException(400, "Conflicto: SKU duplicado")

    return producto
```

[Volver al ejercicio ↑](../capitulos/17-fastapi.md#%C2%B1-ejercicio-174)

---

## Ejercicio 17.5

**Auth + DB**

```python
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy import select


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def get_current_user(
    session: SessionDep,
    token: str = Depends(oauth2_scheme),
) -> "Usuario":
    """Lee el token y devuelve el usuario autenticado."""
    usuario = session.scalar(
        select(Usuario).where(Usuario.token == token)
    )
    if not usuario:
        raise HTTPException(status_code=401, detail="Token inválido")
    return usuario


UsuarioDep = Annotated[Usuario, Depends(get_current_user)]


@router.get("/perfil")
def ver_perfil(usuario: UsuarioDep) -> dict:
    return {
        "id": usuario.id,
        "email": usuario.email,
        "nombre": usuario.nombre,
    }
```

[Volver al ejercicio ↑](../capitulos/17-fastapi.md#%F0%9F%94%B4-ejercicio-175)