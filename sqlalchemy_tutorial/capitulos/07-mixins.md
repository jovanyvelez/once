# Capítulo 7: Mixins — reutilizá columnas entre modelos

> _"DRY" — Don't Repeat Yourself. La regla de oro de cualquier programador senior._

---

## 7.1 ¿Qué es un Mixin?

Un **Mixin** es una clase que define columnas comunes para que varios modelos las hereden. No es un modelo completo: **no tiene `__tablename__`**, solo atributos y métodos.

> 🎓 **Analogía del profesor**: un Mixin es una **"plantilla reutilizable"** 📋. Si todos tus modelos tienen `id`, `creado_en` y `actualizado_en`, no los escribís tres veces: los metés en un Mixin y cada modelo los hereda.

### Mixin vs Herencia vs Interfaz

| Concepto | Qué hace | Tiene tabla propia? |
|---|---|---|
| **Mixin** | Comparte columnas y métodos | ❌ No |
| **Herencia de modelos** | Comparte estructura pero crea una jerarquía | ✅ Depende |
| **Interfaz / Protocolo** | Define un contrato (tipos) sin implementación | ❌ No |

> 💡 Si tenés dudas entre Mixin y herencia de modelos, mirá el [capítulo 8](./08-herencia-modelos.md).

---

## 7.2 El Mixin más común: fechas de auditoría

Una columna `creado_en` y otra `actualizado_en` aparecen en casi toda tabla. Son el ejemplo canónico de Mixin.

```python
# src/mixins.py
from datetime import datetime
from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column

class TimestampMixin:
    """Campos de auditoría de fecha automáticos."""
    
    creado_en: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        nullable=False,
    )
    actualizado_en: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
```

Y se usa así:

```python
# src/models.py
from src.database import Base
from src.mixins import TimestampMixin

class Usuario(Base, TimestampMixin):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]

class Producto(Base, TimestampMixin):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(primary_key=True)
    sku: Mapped[str]
```

Ambos modelos tendrán automáticamente `creado_en` y `actualizado_en`.

```python
# SQL generado:
CREATE TABLE usuarios (
    id INTEGER NOT NULL PRIMARY KEY,
    nombre VARCHAR NOT NULL,
    creado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    actualizado_en DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);
```

---

## 7.3 Mixin de Soft Delete

¿Querés marcar como borrado sin eliminar el registro? Mixin al rescate:

```python
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Mapped, mapped_column

class SoftDeleteMixin:
    """Permite borrado lógico."""
    
    eliminado_en: Mapped[Optional[datetime]] = mapped_column(default=None, nullable=True)

    @property
    def esta_eliminado(self) -> bool:
        return self.eliminado_en is not None

    def marcar_eliminado(self) -> None:
        """Marca el registro como eliminado."""
        self.eliminado_en = datetime.utcnow()

    def restaurar(self) -> None:
        """Recupera un registro eliminado."""
        self.eliminado_en = None
```

Uso:

```python
class Articulo(Base, SoftDeleteMixin):
    __tablename__ = "articulos"
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str]

articulo = Articulo(titulo="Mi primer post")
session.add(articulo)
session.commit()

articulo.marcar_eliminado()   # soft delete
session.commit()

# Para listar solo los no eliminados:
stmt = select(Articulo).where(Articulo.eliminado_en.is_(None))
```

---

## 7.4 Mixin de PK autoincremental

Otro clásico: predefinir una PK estándar en todos los modelos:

```python
class IdIntMixin:
    """PK entera autoincremental."""
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

class IdStrMixin:
    """PK alfanumérica (ej. UUID)."""
    id: Mapped[str] = mapped_column(String(36), primary_key=True)
```

```python
class Cliente(Base, IdIntMixin, TimestampMixin):
    __tablename__ = "clientes"
    nombre: Mapped[str]
```

---

## 7.5 Mixin con métodos de instancia

Los Mixins pueden traer **métodos además de columnas**. Esto permite agrupar lógica común:

```python
class AuditoriaMixin:
    """Columnas + métodos de auditoría."""
    
    creado_por: Mapped[Optional[str]] = mapped_column(default=None)
    actualizado_por: Mapped[Optional[str]] = mapped_column(default=None)

    def registrar_creacion(self, usuario: str) -> None:
        self.creado_por = usuario

    def registrar_actualizacion(self, usuario: str) -> None:
        self.actualizado_por = usuario
```

Uso:

```python
class Documento(Base, AuditoriaMixin):
    __tablename__ = "documentos"
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str]

doc = Documento(titulo="Contrato")
doc.registrar_creacion("juan@empresa.com")
session.add(doc)
session.commit()
```

---

## 7.6 Mixin con relaciones

También es perfectamente válido que un Mixin defina relaciones comunes. Útil cuando muchos modelos comparten una estructura similar.

```python
from typing import List
from sqlalchemy.orm import Mapped, relationship

class AuditLogMixin:
    """Relación con un log de auditoría."""
    
    logs: Mapped[List["AuditLog"]] = relationship(
        back_populates="entidad",
        cascade="all, delete-orphan",
    )
```

> 💡 Si usás esto, asegurate de importar bien las clases cuando las necesites (no es trivial — mejor usar `string forward references`).

---

## 7.7 Caso de uso realista: un CRUD con varios Mixins

```python
# src/mixins.py
from datetime import datetime
from typing import Optional
from sqlalchemy import func, String
from sqlalchemy.orm import Mapped, mapped_column


class IdMixin:
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)


class TimestampMixin:
    creado_en: Mapped[datetime] = mapped_column(
        server_default=func.now(), nullable=False
    )
    actualizado_en: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class SoftDeleteMixin:
    eliminado_en: Mapped[Optional[datetime]] = mapped_column(default=None)

    @property
    def activo(self) -> bool:
        return self.eliminado_en is None

    def eliminar(self) -> None:
        self.eliminado_en = datetime.utcnow()
```

```python
# src/models.py
from src.database import Base
from src.mixins import IdMixin, TimestampMixin, SoftDeleteMixin


class Producto(Base, IdMixin, TimestampMixin, SoftDeleteMixin):
    __tablename__ = "productos"
    nombre: Mapped[str] = mapped_column(String(100))
    sku: Mapped[str] = mapped_column(String(20), unique=True)


class Cliente(Base, IdMixin, TimestampMixin):
    __tablename__ = "clientes"
    nombre: Mapped[str]
    email: Mapped[str]
```

Ambos modelos tienen `id`, `creado_en`, `actualizado_en`. `Producto` además tiene `eliminado_en`.

> 🎓 **Magia**: el Mixin evita duplicación sin sacrificar tipado ni claridad. Cada modelo queda con **solo lo propio**.

---

## 7.8 Errores comunes con Mixins

### ❌ Error 1: Olvidarse de poner `Base` en la herencia

```python
class Producto(TimestampMixin):  # ❌ HEREDA SOLO DEL MIXIN, no de Base
    __tablename__ = "productos"
    ...
```

Resultado: SQLAlchemy no lo trata como modelo ORM y no genera tabla.

### ✅ Correcto

```python
class Producto(Base, TimestampMixin):  # ✅ Base PRIMERO, después Mixins
    __tablename__ = "productos"
    ...
```

> ⚠️ **Orden importante**: `Base` primero en la lista de herencia.

### ❌ Error 2: Conflicto de nombres

```python
class TimestampMixin:
    id: Mapped[int] = mapped_column(primary_key=True)

class IdMixin:
    id: Mapped[int] = mapped_column(primary_key=True)

class Producto(Base, IdMixin, TimestampMixin):  # 💥 ¡dos veces id!
    ...
```

Resultado: error de columna duplicada. ¡Revisá siempre que no haya nombres repetidos!

### ❌ Error 3: Mixin abstracto que no se entiende

```python
# Un mixin con __tablename__ NO es un mixin, es un modelo
class MalMixin(Base):  # ❌ Base + __tablename__ = modelo, no mixin
    __tablename__ = "algo"
    id: Mapped[int] = mapped_column(primary_key=True)
```

> 🎓 **Regla clara**: un Mixin **NUNCA** hereda de `Base` y **NUNCA** tiene `__tablename__`.

---

## 🛠️ Ejercicios prácticos

### 🟢 Ejercicio 7.1: Tu primer Mixin

Creá un `NombreMixin` que tenga solo `nombre: Mapped[str]`. Usalo en dos modelos: `Pais` y `Ciudad`.

**Pista**: el mixin NO hereda de `Base`.

**Solución**: [soluciones/07-mixins.md](../soluciones/07-mixins.md#ejercicio-71)

---

### 🟢 Ejercicio 7.2: `IdMixin` con UUID

Creá un `UuidIdMixin` que use `UUID` como primary key, generado por Python.

**Pista**: `import uuid` y `Mapped[str] = mapped_column(String(36), default=lambda: str(uuid.uuid4()))`.

**Solución**: [soluciones/07-mixins.md](../soluciones/07-mixins.md#ejercicio-72)

---

### 🟡 Ejercicio 7.3: Mixin con método

Creá un `SlugMixin` que:

- Tenga un campo `slug: Mapped[str]` (único, indexado).
- Tenga un método `generar_slug()` que reciba un `titulo: str` y devuelva `titulo.lower().replace(" ", "-")`.

Usalo en un modelo `Articulo`.

**Solución**: [soluciones/07-mixins.md](../soluciones/07-mixins.md#ejercicio-73)

---

### 🟡 Ejercicio 7.4: Diagnóstico

Este Mixin tiene **dos** errores que harán fallar `create_all`. Encontrá ambos:

```python
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, DateTime, func


class MixinAuditable:
    creado_en: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now(), nullable=False
    )
    actualizado_en: Mapped[DateTime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now(), nullable=False
    )


class Usuario(MixinAuditable):  # ❌
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80))
```

**Solución**: [soluciones/07-mixins.md](../soluciones/07-mixins.md#ejercicio-74)

---

### 🔴 Ejercicio 7.5: Combinación de Mixins

Tomá los modelos `Producto` y `Cliente` del manual (capítulo 9). Aplicá:

- `TimestampMixin` a ambos.
- `IdMixin` a ambos.
- `SoftDeleteMixin` solo a `Producto`.

Escribí un test que cree un `Producto`, lo "elimine" (soft), y verifique que `activo == False`.

**Solución**: [soluciones/07-mixins.md](../soluciones/07-mixins.md#ejercicio-75)

---

## 🎓 Lo que aprendiste

- **Mixin** = clase con columnas/métodos reutilizables.
- Se usa cuando varios modelos **comparten columnas** (típico: timestamps, soft delete).
- Se aplica con herencia múltiple: `class Modelo(Base, Mixin):`.
- El orden de herencia importa: `Base` primero.
- Podés combinar varios Mixins en un mismo modelo.

## 📖 Siguiente

[Capítulo 8: Herencia de modelos →](./08-herencia-modelos.md)
