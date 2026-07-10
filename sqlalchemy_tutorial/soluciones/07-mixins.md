# Soluciones — Capítulo 7: Mixins

[Volver al capítulo 7](../capitulos/07-mixins.md)

---

## Ejercicio 7.1

**Tu primer Mixin**

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String


class Base(DeclarativeBase):
    pass


# ⚠️ NO hereda de Base
class NombreMixin:
    nombre: Mapped[str] = mapped_column(String(80))


class Pais(Base, NombreMixin):
    __tablename__ = "paises"
    id: Mapped[int] = mapped_column(primary_key=True)


class Ciudad(Base, NombreMixin):
    __tablename__ = "ciudades"
    id: Mapped[int] = mapped_column(primary_key=True)
```

Ambas tablas tendrán su propia columna `nombre`.

[Volver al ejercicio ↑](../capitulos/07-mixins.md#%C2%B0-ejercicio-71)

---

## Ejercicio 7.2

**`IdMixin` con UUID**

```python
import uuid
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class UuidIdMixin:
    id: Mapped[str] = mapped_column(
        String(36),
        primary_key=True,
        default=lambda: str(uuid.uuid4()),
    )


class Documento(Base, UuidIdMixin):
    __tablename__ = "documentos"
    titulo: Mapped[str]
```

Cada documento creado tendrá un UUID distinto como id.

[Volver al ejercicio ↑](../capitulos/07-mixins.md#%C2%B0-ejercicio-72)

---

## Ejercicio 7.3

**Mixin con método**

```python
import re
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column


class SlugMixin:
    slug: Mapped[str] = mapped_column(String(120), unique=True, index=True)

    @staticmethod
    def generar_slug(titulo: str) -> str:
        slug = titulo.lower()
        slug = re.sub(r"[^a-z0-9\s-]", "", slug)
        slug = re.sub(r"\s+", "-", slug)
        return slug


class Articulo(Base, SlugMixin):
    __tablename__ = "articulos"
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str]


# Uso
art = Articulo(
    titulo="Mi Primer Artículo!",
    slug=Articulo.generar_slug("Mi Primer Artículo!"),
)
print(art.slug)  # "mi-primer-articulo"
```

[Volver al ejercicio ↑](../capitulos/07-mixins.md#%C2%B1-ejercicio-73)

---

## Ejercicio 7.4

**Diagnóstico**

```python
class MixinAuditable:
    creado_en: Mapped[DateTime] = mapped_column(  # 1️⃣ Faltó import
        ...
    )
```

**Errores encontrados**:

1. **`from datetime import datetime` falta** y se usa `DateTime` como tipo en vez de `Mapped[datetime]`.
2. **`class Usuario(MixinAuditable)`** falta heredar de `Base`. SQLAlchemy no lo reconoce.

**Versión corregida**:

```python
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, DateTime, func


class Base(DeclarativeBase):
    pass


class MixinAuditable:
    creado_en: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )


class Usuario(Base, MixinAuditable):  # ✅
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80))
```

[Volver al ejercicio ↑](../capitulos/07-mixins.md#%C2%B1-ejercicio-74)

---

## Ejercicio 7.5

**Combinación de Mixins**

```python
from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, func, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class IdMixin:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class TimestampMixin:
    creado_en: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )


class SoftDeleteMixin:
    eliminado_en: Mapped[Optional[datetime]] = mapped_column(default=None)

    @property
    def activo(self) -> bool:
        return self.eliminado_en is None

    def eliminar(self):
        self.eliminado_en = datetime.utcnow()


class Producto(Base, IdMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "productos"
    nombre: Mapped[str] = mapped_column(String(80))
    precio: Mapped[float]


class Cliente(Base, IdMixin, TimestampMixin):
    __tablename__ = "clientes"
    nombre: Mapped[str] = mapped_column(String(80))
    email: Mapped[str]


# Test
from sqlalchemy.orm import Session
from sqlalchemy import create_engine

engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)

with Session(engine) as session:
    p = Producto(nombre="Mouse", precio=2000)
    session.add(p)
    session.commit()

    print(f"Activo: {p.activo}")  # True
    p.eliminar()
    session.commit()
    print(f"Activo después: {p.activo}")  # False
```

[Volver al ejercicio ↑](../capitulos/07-mixins.md#%F0%9F%94%B4-ejercicio-75)