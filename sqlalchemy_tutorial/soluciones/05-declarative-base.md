# Soluciones — Capítulo 5: Declarative Base

[Volver al capítulo 5](../capitulos/05-declarative-base.md)

---

## Ejercicio 5.1

**Tu primer modelo**

```python
from datetime import datetime
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True)
    nombre: Mapped[str] = mapped_column(String(80))
    fecha_registro: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now()
    )
```

[Volver al ejercicio ↑](../capitulos/05-declarative-base.md#%C2%B0-ejercicio-51)

---

## Ejercicio 5.2

**`__repr__` útil**

```python
class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(120), unique=True)
    nombre: Mapped[str] = mapped_column(String(80))

    def __repr__(self) -> str:
        return f"Cliente(id={self.id}, email={self.email!r}, nombre={self.nombre!r})"
```

```python
c = Cliente(id=1, email="ana@ejemplo.com", nombre="Ana")
print(c)
# -> Cliente(id=1, email='ana@ejemplo.com', nombre='Ana')
```

[Volver al ejercicio ↑](../capitulos/05-declarative-base.md#%C2%B0-ejercicio-52)

---

## Ejercicio 5.3

**`__table_args__` con índice único compuesto**

```python
from sqlalchemy import UniqueConstraint, Date
from datetime import date


class Matriculacion(Base):
    __tablename__ = "matriculaciones"

    id: Mapped[int] = mapped_column(primary_key=True)
    estudiante_id: Mapped[int]
    curso_id: Mapped[int]
    fecha: Mapped[date] = mapped_column(Date)

    __table_args__ = (
        UniqueConstraint(
            "estudiante_id",
            "curso_id",
            name="uq_estudiante_curso",
        ),
    )
```

Esto genera:

```sql
CREATE TABLE matriculaciones (
    id INTEGER NOT NULL PRIMARY KEY,
    estudiante_id INTEGER NOT NULL,
    curso_id INTEGER NOT NULL,
    fecha DATE NOT NULL,
    UNIQUE (estudiante_id, curso_id)
);
```

[Volver al ejercicio ↑](../capitulos/05-declarative-base.md#%C2%B1-ejercicio-53)

---

## Ejercicio 5.4

**Diagnóstico**

```python
# ❌ ERRORES
class Libro():  # 1️⃣ Falta heredar de Base
    __tablename__ = "libros"
    ...
```

**Errores**:

1. **`class Libro():`** no hereda de `Base`. SQLAlchemy no lo reconoce como modelo ORM.
2. Le falta el paréntesis en la herencia correcta: `class Libro(Base):`.

**Versión corregida**:

```python
class Libro(Base):  # ✅ Correcto
    __tablename__ = "libros"
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(200))
    isbn: Mapped[str] = mapped_column(String(13), unique=True)
```

[Volver al ejercicio ↑](../capitulos/05-declarative-base.md#%C2%B1-ejercicio-54)

---

## Ejercicio 5.5

**Múltiples `Base`**

```python
from sqlalchemy.orm import DeclarativeBase


class BaseAuth(DeclarativeBase):
    pass


class BaseBiblioteca(DeclarativeBase):
    pass
```

Cada `Base` tiene su propio `metadata`. Esto te permite:

1. **Evitar que se toquen tablas**: `BaseBiblioteca.metadata.create_all(engine)` solo crea las tablas de biblioteca, no las de auth.
2. **Separar migraciones con Alembic**: cada `Base` puede tener su propia carpeta `migrations/auth/` y `migrations/biblioteca/`.

```python
class UsuarioAuth(BaseAuth):
    __tablename__ = "usuarios"
    ...


class Libro(BaseBiblioteca):
    __tablename__ = "libros"
    ...


# Crear solo las de biblioteca
BaseBiblioteca.metadata.create_all(engine)
```

2. **¿Tiene sentido múltiples `Base` en una app monolítica?** Generalmente **no**. Es complejidad innecesaria. Usá `Base` única salvo que tengas dominios **verdaderamente independientes** que pueda que se separen a futuro.

[Volver al ejercicio ↑](../capitulos/05-declarative-base.md#%F0%9F%94%B4-ejercicio-55)