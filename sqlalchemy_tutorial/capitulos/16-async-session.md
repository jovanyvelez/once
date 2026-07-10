# Capítulo 16: AsyncSession — SQLAlchemy con `async/await`

> Para aplicaciones que ya son asíncronas (ej: `aiohttp`, FastAPI async, asyncio puro).

---

## 16.1 ¿Por qué async?

El `Session` tradicional es **sincrónico** y **bloqueante**. Esto significa que cuando hace una query, el thread queda esperando la respuesta. En aplicaciones con mucha concurrencia (millares de conexiones, websockets, etc.), esto es un problema.

**AsyncSession** soluciona esto: usa `await` para liberar el event loop mientras espera la base de datos.

### ¿Cuándo usar AsyncSession?

| Caso | Recomendación |
|---|---|
| App FastAPI con CRUD normal | 🟢 `Session` sync es suficiente |
| FastAPI con muchas requests concurrentes y queries lentas | 🔵 `AsyncSession` vale la pena |
| App con websockets / streaming | 🔵 `AsyncSession` |
| Scripts, ETL, batch jobs | 🟢 `Session` sync |
| Async puro (aiohttp, starlette, etc.) | 🔵 `AsyncSession` |

> 🎓 **Consejo del profesor**: empezá con sync. Si medís y necesitás async, migrás después. Sync es más simple.

---

## 16.2 Requisitos previos

Necesitás un driver de base de datos **async**:

| Base de datos | Driver async |
|---|---|
| PostgreSQL | `asyncpg` o `psycopg[binary]` (psycopg3) |
| MySQL | `aiomysql` o `asyncmy` |
| SQLite | `aiosqlite` |
| SQL Server | `aioodbc` |

```bash
pip install "sqlalchemy[asyncio]" asyncpg     # para PostgreSQL
pip install aiosqlite                          # para SQLite
```

---

## 16.3 Engine asíncrono

```python
from sqlalchemy.ext.asyncio import create_async_engine

# SQLite async
engine = create_async_engine("sqlite+aiosqlite:///./tienda.db", echo=True)

# PostgreSQL async
engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost:5432/db",
    echo=False,
    pool_size=5,
    max_overflow=10,
)
```

> 💡 **Diferencia clave**: la URL tiene el driver async (`sqlite+aiosqlite`, `postgresql+asyncpg`).

---

## 16.4 Tu primera query async

```python
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession

async def listar_productos():
    async with AsyncSession(engine) as session:
        result = await session.scalars(select(Producto))
        for producto in result:
            print(producto.nombre)

# Para ejecutar:
asyncio.run(listar_productos())
```

> ⚠️ **Importante**: las operaciones de sesión son **awaitable**. Tenés que poner `await` antes.

---

## 16.5 Operaciones CRUD async

### CREATE

```python
async def crear_producto():
    async with AsyncSession(engine) as session:
        nuevo = Producto(nombre="Tablet", sku="TAB-001", precio=35000)
        session.add(nuevo)
        await session.commit()
        await session.refresh(nuevo)
        return nuevo
```

### READ

```python
async def obtener_producto(id: int):
    async with AsyncSession(engine) as session:
        stmt = select(Producto).where(Producto.id == id)
        return await session.scalar(stmt)


async def listar_productos(skip: int = 0, limit: int = 100):
    async with AsyncSession(engine) as session:
        stmt = select(Producto).offset(skip).limit(limit)
        result = await session.scalars(stmt)
        return result.all()
```

### UPDATE

```python
async def actualizar_producto(id: int, **kwargs):
    async with AsyncSession(engine) as session:
        p = await session.get(Producto, id)
        if not p:
            return None
        for key, value in kwargs.items():
            setattr(p, key, value)
        await session.commit()
        await session.refresh(p)
        return p
```

### DELETE

```python
async def eliminar_producto(id: int):
    async with AsyncSession(engine) as session:
        p = await session.get(Producto, id)
        if not p:
            return False
        await session.delete(p)
        await session.commit()
        return True
```

---

## 16.6 `AsyncSession` no es thread-safe

Como **cualquier** recurso async, una `AsyncSession` está atada al event loop. No la compartas entre corutinas que se ejecutan en eventos diferentes.

```python
# ❌ Mal: session creada fuera, usada por muchas corutinas
async def handler_compartida():
    session = AsyncSession(engine)
    await asyncio.gather(
        usar_session(session),
        usar_session(session),  # 💥 problemas
    )

# ✅ Bien: cada corutina con su propia sesión
async def handler_independiente():
    async def una_op():
        async with AsyncSession(engine) as session:
            # ...
            pass

    await asyncio.gather(una_op(), una_op())
```

---

## 16.7 Patrón `get_db()` async (para FastAPI)

```python
from typing import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

engine = create_async_engine("sqlite+aiosqlite:///./tienda.db", echo=True)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with AsyncSession(engine) as session:
        yield session
```

Y el alias:

```python
from typing import Annotated
from fastapi import Depends

SessionDep = Annotated[AsyncSession, Depends(get_db)]


@app.get("/productos/")
async def listar_productos(session: SessionDep):
    stmt = select(Producto)
    result = await session.scalars(stmt)
    return result.all()
```

> 💡 **Detalle clave**: las funciones del endpoint deben ser `async def` cuando usan `AsyncSession`.

---

## 16.8 Usar con asyncpg (PostgreSQL)

```bash
pip install asyncpg
```

```python
from sqlalchemy.ext.asyncio import create_async_engine

engine = create_async_engine(
    "postgresql+asyncpg://user:pass@localhost:5432/db",
    echo=False,
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
)
```

### Configuración avanzada

```python
from sqlalchemy.ext.asyncio import async_sessionmaker

# Creamos una factory de sesiones
async_session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,    # <- importante en async
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_factory() as session:
        yield session
```

> 💡 **`expire_on_commit=False`**: por default, SQLAlchemy "expira" los objetos después del commit (es decir, los invalida para que se traigan de nuevo). En async esto puede ser problemático porque rompe el tipado. Con `False`, mantenés los atributos vivos hasta la próxima query.

---

## 16.9 Contexto transaccional explícito

```python
async with async_session_factory() as session:
    async with session.begin():
        # todas estas operaciones dentro de UNA transacción
        session.add(Producto(nombre="A", sku="A-001", precio=100))
        session.add(Producto(nombre="B", sku="B-001", precio=200))
    # commit automático al salir del bloque begin
```

Para tener **savepoints** (sub-transacciones):

```python
async with async_session_factory() as session:
    async with session.begin():
        # operación riesgosa
        try:
            async with session.begin_nested():  # SAVEPOINT
                # si falla, vuelve al estado anterior al savepoint
                session.add(...)
        except IntegrityError:
            pass  # continúa con la transacción principal
```

---

## 16.10 Manejo de errores async

```python
from sqlalchemy.exc import IntegrityError, NoResultFound

async def crear_o_error(data):
    async with async_session_factory() as session:
        try:
            nuevo = Producto(**data.model_dump())
            session.add(nuevo)
            await session.commit()
            return nuevo
        except IntegrityError:
            await session.rollback()
            return None
```

---

## 16.11 Ejecución en tests (pytest-asyncio)

```python
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from src.models import Base


@pytest.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSession(engine) as session:
        yield session

    await engine.dispose()


@pytest.mark.asyncio
async def test_crear_producto(db_session):
    nuevo = Producto(nombre="Test", sku="TST-001", precio=100)
    db_session.add(nuevo)
    await db_session.commit()
    await db_session.refresh(nuevo)

    assert nuevo.id is not None
    assert nuevo.nombre == "Test"
```

---

## 16.12 Comparación rápida: Sync vs Async

| Operación | Sync | Async |
|---|---|---|
| Crear engine | `create_engine(...)` | `create_async_engine(...)` |
| Crear sesión | `Session(engine)` | `AsyncSession(engine)` |
| Ejecutar query | `session.scalars(stmt)` | `await session.scalars(stmt)` |
| Commit | `session.commit()` | `await session.commit()` |
| Get por PK | `session.get(M, id)` | `await session.get(M, id)` |
| Refresh | `session.refresh(obj)` | `await session.refresh(obj)` |
| Delete | `session.delete(obj)` | `await session.delete(obj)` |
| Session factory | `sessionmaker(...)` | `async_sessionmaker(...)` |
| Context manager | `with Session(...) as s:` | `async with AsyncSession(...) as s:` |
| Generador | `def get_db(): yield` | `async def get_db(): yield` |

---

## 16.13 Reglas de oro para Async SQLAlchemy

1. ✅ Usá `expire_on_commit=False` para evitar surprises con atributos expirados.
2. ✅ No mezcles operaciones sync y async en la misma sesión.
3. ✅ Cada request / corutina principal debe tener su propia sesión.
4. ✅ Cerrá la sesión siempre (el `async with` lo hace por vos).
5. ❌ No uses `await` dentro de un constructor (los `__init__` no son awaitable).
6. ❌ No hagas `await session.add(...)`: `add` es **sync** (solo la I/O es async).

> ⚠️ Cuidado con esto último: `session.add()` y `session.delete()` son **sincrónicos** (no llevan await). Solo las operaciones de I/O (`commit`, `refresh`, `scalars`, `execute`) son async.

---

## 🛠️ Ejercicios prácticos

### 🟢 Ejercicio 16.1: Engine async básico

Creá un script async que cree un `AsyncEngine` apuntando a SQLite (con `aiosqlite`) y ejecute un `SELECT 1`.

**Solución**: [soluciones/16-async-session.md](../soluciones/16-async-session.md#ejercicio-161)

---

### 🟡 Ejercicio 16.2: CRUD async

Convertí los CRUD operations del [ejercicio 11.5](#%F0%9F%94%B4-ejercicio-115-transferir-stock) a la versión `async` con `AsyncSession`.

**Solución**: [soluciones/16-async-session.md](../soluciones/16-async-session.md#ejercicio-162)

---

### 🟡 Ejercicio 16.3: `expire_on_commit=False`

Investigá qué pasa si no ponés `expire_on_commit=False`. Demostralo con un test que lea un atributo **después** del commit.

**Solución**: [soluciones/16-async-session.md](../soluciones/16-async-session.md#ejercicio-163)

---

### 🟡 Ejercicio 16.4: `asyncio.gather`

Escribí una función que cree 3 productos en **paralelo** (con `asyncio.gather`), cada uno en su propia sesión. Verificá que los 3 quedan en la DB.

**Solución**: [soluciones/16-async-session.md](../soluciones/16-async-session.md#ejercicio-164)

---

### 🔴 Ejercicio 16.5: Tests con `pytest-asyncio`

Escribí un test que verifique una operación CRUD async. Usá `pytest-asyncio` y una fixture que cree una DB en memoria.

**Solución**: [soluciones/16-async-session.md](../soluciones/16-async-session.md#ejercicio-165)

---

## 🎓 Lo que aprendiste

- `AsyncSession` permite I/O no bloqueante contra la base de datos.
- Necesitás drivers async (`aiosqlite`, `asyncpg`, etc.).
- Las operaciones de I/O van con `await`; `add()` y `delete()` no.
- `expire_on_commit=False` evita sorpresas con objetos expirados.
- Cada request / corutina debe tener su propia sesión.

## 📖 Siguiente

[Capítulo 17: FastAPI + SQLAlchemy (patrón moderno) →](./17-fastapi.md)