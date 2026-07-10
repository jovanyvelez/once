# Soluciones — Capítulo 10: Crear las tablas (DDL)

[Volver al capítulo 10](../capitulos/10-crear-tablas.md)

---

## Ejercicio 10.1

**`echo=True` vs `echo=False`**

```python
engine_con = create_engine("sqlite:///:memory:", echo=True)
Base.metadata.create_all(engine_con)   # Imprime TODO el SQL en consola

engine_sin = create_engine("sqlite:///:memory:", echo=False)
Base.metadata.create_all(engine_sin)   # Silencio total
```

Con `echo=True` ves líneas como:

```
INFO sqlalchemy.engine.Engine CREATE TABLE productos (...)
INFO sqlalchemy.engine.Engine COMMIT
```

Con `echo=False` no se imprime nada (útil en producción para no ensuciar los logs).

[Volver al ejercicio ↑](../capitulos/10-crear-tablas.md#%C2%B0-ejercicio-101)

---

## Ejercicio 10.2

**Inspección de tablas**

```python
print("Tablas que se crearán:")
for tabla in Base.metadata.sorted_tables:
    print(f"- {tabla.name}")
    for col in tabla.columns:
        print(f"    {col.name} ({col.type})")
```

Salida esperada:

```
Tablas que se crearán:
- categorias
    id (INTEGER)
    nombre (VARCHAR(50))
    descripcion (VARCHAR)
    creado_en (DATETIME)
- productos
    id (INTEGER)
    nombre (VARCHAR(100))
    ...
```

[Volver al ejercicio ↑](../capitulos/10-crear-tablas.md#%C2%B1-ejercicio-102)

---

## Ejercicio 10.3

**Patrón de tests**

```python
import pytest
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool


@pytest.fixture
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
    
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()
    
    yield session
    
    session.close()
    engine.dispose()


def test_crear_categoria(db_session):
    cat = Categoria(nombre="Test")
    db_session.add(cat)
    db_session.commit()
    
    assert cat.id is not None
    assert cat.nombre == "Test"
```

[Volver al ejercicio ↑](../capitulos/10-crear-tablas.md#%C2%B1-ejercicio-103)

---

## Ejercicio 10.4

**`checkfirst`**

```python
engine = create_engine("sqlite:///:memory:")

print("=== Primera ejecución ===")
Base.metadata.create_all(engine)  # Crea las tablas

print("\n=== Segunda ejecución (con checkfirst=True, default) ===")
Base.metadata.create_all(engine)  # No hace nada, ya existen

print("\n=== Tercera ejecución con checkfirst=False ===")
Base.metadata.create_all(engine, checkfirst=False)  # 💥 Error: tabla ya existe
```

Salida esperada:

```
=== Primera ejecución ===
[SQL emitido]

=== Segunda ejecución (con checkfirst=True, default) ===
[Silencio]

=== Tercera ejecución con checkfirst=False ===
sqlalchemy.exc.ProgrammingError: (sqlite3.ProgrammingError) table ... already exists
```

[Volver al ejercicio ↑](../capitulos/10-crear-tablas.md#%C2%B1-ejercicio-104)

---

## Ejercicio 10.5

**Schema versionado**

⚠️ **NO usar en producción**. Solo para entender cómo Alembic funciona por dentro.

```python
from sqlalchemy import text


def verificar_y_actualizar(engine):
    """Verifica la versión del schema y aplica cambios manuales."""
    Base.metadata.create_all(engine)  # Por si es la primera vez
    
    with engine.connect() as conn:
        # Ver si ya existe la tabla de versiones
        try:
            version = conn.execute(
                text("SELECT version FROM schema_version LIMIT 1")
            ).scalar()
        except Exception:
            version = 0
        
        if version < 1:
            # Necesitamos agregar la columna `stock`
            conn.execute(text("ALTER TABLE productos ADD COLUMN stock INTEGER DEFAULT 0"))
            conn.execute(text("UPDATE schema_version SET version = 1"))
            conn.commit()
            print("✅ Schema actualizado a versión 1")


# En tu app:
verificar_y_actualizar(engine)
```

**Conclusión**: este enfoque es frágil y propenso a errores. **Usá Alembic** (cap. 23).

[Volver al ejercicio ↑](../capitulos/10-crear-tablas.md#%F0%9F%94%B4-ejercicio-105)