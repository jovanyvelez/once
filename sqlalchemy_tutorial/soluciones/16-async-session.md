# Soluciones — Capítulo 16: AsyncSession

[Volver al capítulo 16](../capitulos/16-async-session.md)

---

## Ejercicio 16.1

**Engine async básico**

```python
import asyncio
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy import text


async def main():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    
    async with engine.connect() as conn:
        result = await conn.execute(text("SELECT 1 + 1"))
        print(result.scalar())  # 2
    
    await engine.dispose()


asyncio.run(main())
```

> ⚠️ Para que funcione, instalá `aiosqlite`: `pip install aiosqlite`.

[Volver al ejercicio ↑](../capitulos/16-async-session.md#%C2%B0-ejercicio-161)

---

## Ejercicio 16.2

**CRUD async**

```python
from sqlalchemy.ext.asyncio import AsyncSession


async def transferir_stock(
    session: AsyncSession,
    origen_id: int,
    destino_id: int,
    cantidad: int,
) -> bool:
    """Versión async de transferir_stock."""
    try:
        origen = await session.get(Producto, origen_id)
        destino = await session.get(Producto, destino_id)
        
        if not origen or not destino or origen.stock < cantidad:
            return False
        
        origen.stock -= cantidad
        destino.stock += cantidad
        
        await session.commit()
        return True
    except Exception:
        await session.rollback()
        return False
```

[Volver al ejercicio ↑](../capitulos/16-async-session.md#%C2%B1-ejercicio-162)

---

## Ejercicio 16.3

**`expire_on_commit=False`**

```python
async def test_sin_expire_on_commit():
    factory = async_sessionmaker(engine, class_=AsyncSession)  # SIN expire_on_commit
    
    async with factory() as session:
        p = Producto(nombre="Test", sku="TST-1", precio=100)
        session.add(p)
        await session.commit()
        
        # Después del commit, los atributos están EXPIRADOS
        # Acceder a p.nombre dispara una nueva query
        print(p.nombre)  # <- necesitas await session.refresh(p) primero


async def test_con_expire_on_commit_false():
    factory = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    
    async with factory() as session:
        p = Producto(nombre="Test", sku="TST-2", precio=100)
        session.add(p)
        await session.commit()
        
        # Después del commit, los atributos SIGUEN VIVOS
        print(p.nombre)  # "Test", sin queries extra
```

[Volver al ejercicio ↑](../capitulos/16-async-session.md#%C2%B1-ejercicio-163)

---

## Ejercicio 16.4

**`asyncio.gather`**

```python
async def crear_producto(nombre: str, precio: float) -> int:
    factory = async_sessionmaker(engine, expire_on_commit=False)
    
    async with factory() as session:
        p = Producto(nombre=nombre, sku=f"SKU-{nombre}", precio=precio)
        session.add(p)
        await session.commit()
        return p.id


async def main():
    # Crear 3 productos en paralelo
    ids = await asyncio.gather(
        crear_producto("A", 100),
        crear_producto("B", 200),
        crear_producto("C", 300),
    )
    print(f"IDs creados: {ids}")
```

[Volver al ejercicio ↑](../capitulos/16-async-session.md#%C2%B1-ejercicio-164)

---

## Ejercicio 16.5

**Tests con `pytest-asyncio`**

```python
import pytest
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker


@pytest.fixture
async def db_session():
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    
    factory = async_sessionmaker(engine, expire_on_commit=False)
    async with factory() as session:
        yield session
    
    await engine.dispose()


@pytest.mark.asyncio
async def test_crear_producto(db_session):
    p = Producto(nombre="Test", sku="TST-1", precio=100)
    db_session.add(p)
    await db_session.commit()
    
    assert p.id is not None
    
    # Verificar que se persistió
    resultado = await db_session.get(Producto, p.id)
    assert resultado is not None
    assert resultado.nombre == "Test"
```

Instalación:

```bash
pip install pytest-asyncio aiosqlite
```

[Volver al ejercicio ↑](../capitulos/16-async-session.md#%F0%9F%94%B4-ejercicio-165)