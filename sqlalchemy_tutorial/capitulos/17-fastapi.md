# Capítulo 17: FastAPI + SQLAlchemy (patrón moderno)

> Toda la teoría cobra sentido: armar una API REST moderna con FastAPI y SQLAlchemy 2.0.

Este capítulo es la integración de todo: vas a ver el patrón canónico moderno, igual al que vas a usar en producción.

---

## 17.1 El patrón canónico: `get_db()` con `yield` + `SessionDep`

Este es **el patrón más importante** para usar SQLAlchemy con FastAPI. Se resume en tres pasos:

### Paso 1: El generador `get_db()` con `yield`

```python
from typing import Generator
from sqlalchemy.orm import Session
from src.database import engine

def get_db() -> Generator[Session, None, None]:
    """Abre una sesión por request y la cierra al terminar."""
    with Session(engine) as session:
        yield session
        # Cuando el request termina, el bloque `with` cierra la sesión
```

#### ¿Por qué `yield` y no un `return` simple?

Con `return`, la sesión se crea al inicio de la request y nunca la cerraríamos. Con `yield`, Python **pausa** la función hasta que la request termine, ejecuta el código antes (crear sesión, abrirla) **y** el código después (cerrarla). Es un patrón seguro: pase lo que pase, la sesión se cierra.

> 🎓 **Analogía del profesor**: `yield` es como decir: "tomá esta sesión, usala, y cuando termines **te la devuelvo** para que la limpie yo mismo".

#### ¿Por qué con `with Session()`?

Porque `Session` ya implementa el protocolo `__enter__`/`__exit__`. Eso significa que **si el endpoint falla** con una excepción, el `with` cierra la sesión automáticamente. Sin pérdida de conexiones.

> 🎓 **Pregunta clásica**: ¿hace falta `try/finally`? En este caso **no**, porque `Session(engine) as session` ya garantiza el cierre. Pero si tu generador hace más cosas (como cachear o loggear), entonces sí.

---

### Paso 2: El alias `SessionDep`

```python
from typing import Annotated
from fastapi import Depends

SessionDep = Annotated[Session, Depends(get_db)]
```

Este es **uno de los patrones más importantes** de FastAPI moderno. Vamos a compararlo con la alternativa sin alias:

```python
# ❌ Sin alias: repetís código
@app.get("/productos/")
def listar_productos(
    session: Annotated[Session, Depends(get_db)]
):
    ...

# ✅ Con alias: tu código es elegante
@app.get("/productos/")
def listar_productos(session: SessionDep):
    ...
```

#### ¿Por qué `Annotated` y no el valor por defecto?

| Aspecto | `Depends(...)` por defecto 🟠 | `Annotated[..., Depends(...)]` ✅ |
|---|---|---|
| Autocompletado en IDE | 🟠 confunde tipos | 🟢 claro: es `Session` |
| MyPy | 🟠 se pierde la info | 🟢 retiene la info |
| Legibilidad | 🟠 hay que adivinar | 🟢 se ve explícito |
| Reutilización | 🟠 repetir el `Annotated` | 🟢 alias `SessionDep` |

> 🎓 **Consejo del profesor**: usá siempre `Annotated` + alias. Es una vez y te ahorrás meses de confusión.

---

### Paso 3: Pydantic Schemas

**Pydantic** valida y documenta los datos que entran y salen de tu API. La mejor práctica es tener **un modelo por caso de uso**:

| Schema | Para qué sirve | Campos |
|---|---|---|
| `Base` | Heredar lo común | Compartidos |
| `Create` | Endpoint POST (input) | Datos requeridos |
| `Public` | Respuesta al cliente | Lo que se puede mostrar |
| `Update` | Endpoint PATCH (input parcial) | Todos opcionales |

```python
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    sku: str = Field(..., min_length=1, max_length=20)
    precio: float = Field(..., gt=0)
    descripcion: Optional[str] = None


class ProductoCreate(ProductoBase):
    pass


class ProductoPublic(ProductoBase):
    id: int
    creado_en: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductoUpdate(BaseModel):
    """PATCH: todos los campos son opcionales."""
    nombre: Optional[str] = None
    sku: Optional[str] = None
    precio: Optional[float] = Field(default=None, gt=0)
    descripcion: Optional[str] = None
```

> 🎓 **Por qué tres schemas**: nunca expongas `password`, `token` o cualquier dato secreto. `ProductoPublic` define tu **contrato** con el cliente.

---

## 17.2 Proyecto completo CRUD

### 🗂️ Estructura del proyecto

```
mi_api/
├── src/
│   ├── __init__.py
│   ├── database.py        # engine + get_db + Base
│   ├── models.py          # modelos SQLAlchemy (ORM)
│   ├── schemas.py         # schemas Pydantic
│   ├── routers/
│   │   ├── __init__.py
│   │   └── productos.py   # endpoints
│   └── main.py
├── tests/
├── requirements.txt
└── README.md
```

---

### 📄 `src/database.py`

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

SQLALCHEMY_DATABASE_URL = "sqlite:///./tienda.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=False,                # True para debug
)


def get_db():
    """Generador de sesión por request."""
    with Session(engine) as session:
        yield session


class Base(DeclarativeBase):
    pass
```

---

### 📄 `src/models.py`

```python
from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Numeric, ForeignKey, func, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.database import Base


class Producto(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    sku: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    precio: Mapped[float] = mapped_column(Numeric(10, 2))
    descripcion: Mapped[Optional[str]] = mapped_column(default=None)
    creado_en: Mapped[datetime] = mapped_column(server_default=func.now())
    actualizado_en: Mapped[datetime] = mapped_column(
        server_default=func.now(), onupdate=func.now()
    )

    # relación: cada producto pertenece a una categoría
    categoria_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("categorias.id"), default=None
    )
    categoria: Mapped[Optional["Categoria"]] = relationship(
        back_populates="productos"
    )

    def __repr__(self):
        return f"Producto(id={self.id}, nombre={self.nombre!r})"


class Categoria(Base):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), unique=True)
    descripcion: Mapped[Optional[str]] = mapped_column(default=None)

    productos: Mapped[List["Producto"]] = relationship(
        back_populates="categoria", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"Categoria(id={self.id}, nombre={self.nombre!r})"
```

---

### 📄 `src/schemas.py`

```python
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict, Field


class CategoriaBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=50)


class CategoriaCreate(CategoriaBase):
    pass


class CategoriaPublic(CategoriaBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class ProductoBase(BaseModel):
    nombre: str = Field(..., min_length=1, max_length=100)
    sku: str = Field(..., min_length=1, max_length=20)
    precio: float = Field(..., gt=0)
    descripcion: Optional[str] = None
    categoria_id: Optional[int] = None


class ProductoCreate(ProductoBase):
    pass


class ProductoPublic(ProductoBase):
    id: int
    creado_en: datetime
    actualizado_en: datetime
    model_config = ConfigDict(from_attributes=True)


class ProductoUpdate(BaseModel):
    """PATCH: todos opcionales."""
    nombre: Optional[str] = None
    sku: Optional[str] = None
    precio: Optional[float] = Field(default=None, gt=0)
    descripcion: Optional[str] = None
    categoria_id: Optional[int] = None
```

---

### 📄 `src/routers/categorias.py`

```python
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Categoria
from src.schemas import CategoriaCreate, CategoriaPublic

SessionDep = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/categorias", tags=["categorias"])


@router.post("/", response_model=CategoriaPublic, status_code=status.HTTP_201_CREATED)
def crear(data: CategoriaCreate, session: SessionDep) -> CategoriaPublic:
    nueva = Categoria(**data.model_dump())
    session.add(nueva)
    session.commit()
    session.refresh(nueva)
    return nueva


@router.get("/", response_model=List[CategoriaPublic])
def listar(session: SessionDep) -> List[CategoriaPublic]:
    return list(session.scalars(select(Categoria)))
```

---

### 📄 `src/routers/productos.py`

```python
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.database import get_db
from src.models import Producto
from src.schemas import ProductoCreate, ProductoPublic, ProductoUpdate

SessionDep = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/productos", tags=["productos"])


@router.post("/", response_model=ProductoPublic, status_code=status.HTTP_201_CREATED)
def crear(data: ProductoCreate, session: SessionDep) -> ProductoPublic:
    nuevo = Producto(**data.model_dump())
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo


@router.get("/", response_model=List[ProductoPublic])
def listar(
    session: SessionDep,
    offset: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=500),
) -> List[ProductoPublic]:
    stmt = select(Producto).offset(offset).limit(limit)
    return list(session.scalars(stmt))


@router.get("/{producto_id}", response_model=ProductoPublic)
def obtener(producto_id: int, session: SessionDep) -> ProductoPublic:
    p = session.get(Producto, producto_id)
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return p


@router.patch("/{producto_id}", response_model=ProductoPublic)
def actualizar(
    producto_id: int,
    data: ProductoUpdate,
    session: SessionDep,
) -> ProductoPublic:
    p = session.get(Producto, producto_id)
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    # Solo actualiza los campos que vinieron en el body
    cambios = data.model_dump(exclude_unset=True)
    for campo, valor in cambios.items():
        setattr(p, campo, valor)

    session.commit()
    session.refresh(p)
    return p


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def borrar(producto_id: int, session: SessionDep) -> None:
    p = session.get(Producto, producto_id)
    if not p:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    session.delete(p)
    session.commit()
```

---

### 📄 `src/main.py`

```python
from fastapi import FastAPI
from src.database import engine, Base
from src.routers import productos, categorias
import src.models  # registra modelos

# 🌟 Crea todas las tablas al iniciar (solo dev)
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mi API de Productos",
    version="1.0",
    description="API REST con FastAPI + SQLAlchemy 2.0",
)

app.include_router(productos.router)
app.include_router(categorias.router)


@app.get("/")
def raiz():
    return {"mensaje": "API funcionando"}
```

---

### ▶️ Ejecutarlo

```bash
pip install "fastapi[standard]" "sqlalchemy>=2.0"
uvicorn src.main:app --reload
```

Luego abrí `http://127.0.0.1:8000/docs` y verás la **documentación interactiva de Swagger**. ¡Toda generada automáticamente!

> 🎓 **Demo mental**: probá crear una categoría y un producto asociado. Verás en `session.refresh(nuevo)` cómo SQLAlchemy regresa a la base para traer los campos autogenerados (`id`, `creado_en`).

---

## 17.3 PATCH parcial con `exclude_unset=True`

La magia de `model_dump(exclude_unset=True)` es que solo devuelve los campos que el cliente **realmente envió**, no los que Pydantic rellenó con `None`.

```python
class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None

# Si el cliente PATCH envía {"precio": 200} (sin nombre):
data = ProductoUpdate(nombre=None, precio=200)
print(data.model_dump())
# {"nombre": None, "precio": 200}

print(data.model_dump(exclude_unset=True))
# {"precio": 200}    👈 solo lo enviado
```

Así, en la query solo actualizás el campo que el cliente explícitamente envió.

---

## 17.4 Usar `AsyncSession` con FastAPI

```python
# src/database.py (versión async)
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase

engine = create_async_engine("sqlite+aiosqlite:///./tienda.db", echo=False)
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session


class Base(DeclarativeBase):
    pass
```

```python
# src/routers/productos.py (async)
from typing import Annotated, List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

SessionDep = Annotated[AsyncSession, Depends(get_db)]


@router.get("/")
async def listar(session: SessionDep) -> List[dict]:
    stmt = select(Producto)
    result = await session.scalars(stmt)
    return [{"id": p.id, "nombre": p.nombre} for p in result.all()]


@router.post("/")
async def crear(data: ProductoCreate, session: SessionDep) -> dict:
    nuevo = Producto(**data.model_dump())
    session.add(nuevo)
    await session.commit()
    await session.refresh(nuevo)
    return {"id": nuevo.id}
```

> 💡 Para usar async todo el camino, instalá `aiosqlite` (o `asyncpg`).
>
> ```bash
> pip install aiosqlite
> ```

---

## 17.5 Sub-dependencias (auth + DB)

```python
SessionDep = Annotated[Session, Depends(get_db)]


def get_current_user(
    session: SessionDep,
    token: str = Depends(oauth2_scheme),
) -> Usuario:
    user = session.scalar(select(Usuario).where(Usuario.token == token))
    if not user:
        raise HTTPException(401, "Token inválido")
    return user


# 👈 dependencia compuesta
UsuarioDep = Annotated[Usuario, Depends(get_current_user)]


@app.get("/perfil/")
def ver_perfil(usuario: UsuarioDep):
    return {"nombre": usuario.nombre}
```

---

## 17.6 Buenas prácticas combinadas

1. **Schemas separados**: uno para crear, otro para responder, otro para actualizar.
2. **`response_model` siempre**: evita exponer campos sensibles.
3. **`exclude_unset=True`** en PATCH.
4. **`SessionDep` global**: definilo una vez y reusá.
5. **HTTPException** para errores.
6. **Manejá errores con `try/except`** en operaciones riesgosas (ej: `IntegrityError`).
7. **`session.refresh()` después de insertar** para tener datos generados.

---

## 🛠️ Ejercicios prácticos

### 🟢 Ejercicio 17.1: Tu primer endpoint

Implementá un endpoint `GET /saludo/{nombre}` que devuelva `{"saludo": "Hola {nombre}!"}`. No necesita DB.

**Solución**: [soluciones/17-fastapi.md](../soluciones/17-fastapi.md#ejercicio-171)

---

### 🟡 Ejercicio 17.2: Schemas completos

Implementá los schemas (`Base`, `Create`, `Public`, `Update`) para un modelo `Comentario(texto, autor, fecha)`.

**Solución**: [soluciones/17-fastapi.md](../soluciones/17-fastapi.md#ejercicio-172)

---

### 🟡 Ejercicio 17.3: Endpoint con filtros

Mejorá el endpoint `GET /productos/` para que acepte query params:

- `?search=texto`: buscar en `nombre`.
- `?min_precio=100&max_precio=500`: filtrar por rango.
- `?categoria_id=1`: filtrar por categoría.

**Solución**: [soluciones/17-fastapi.md](../soluciones/17-fastapi.md#ejercicio-173)

---

### 🟡 Ejercicio 17.4: PATCH robusto

Implementá un PATCH que:

- Use `model_dump(exclude_unset=True)`.
- Valide que al menos un campo venga.
- Devuelva `404` si el producto no existe.
- Devuelva `400` si hay `IntegrityError`.

**Solución**: [soluciones/17-fastapi.md](../soluciones/17-fastapi.md#ejercicio-174)

---

### 🔴 Ejercicio 17.5: Auth + DB

Implementá un endpoint `GET /perfil` que:

- Lea el usuario desde una `Dependencia` que consulta la DB.
- Devuelva 401 si el token no es válido.
- Devuelva 200 con los datos del usuario si todo va bien.

**Solución**: [soluciones/17-fastapi.md](../soluciones/17-fastapi.md#ejercicio-175)

---

## 🎓 Lo que aprendiste

- `get_db()` con `yield` da una sesión por request, segura y limpia.
- `SessionDep = Annotated[Session, Depends(get_db)]` simplifica y tipa los endpoints.
- Pydantic schemas separados (Base, Create, Public, Update) definen tu contrato con el cliente.
- `model_dump(exclude_unset=True)` permite PATCH parcial sin tocar campos no enviados.
- `session.refresh()` después del commit asegura tener los datos autogenerados.
- La misma estructura sirve para sync y async.

## 📖 Siguiente

[Capítulo 18: Buenas prácticas →](./18-buenas-practicas.md)