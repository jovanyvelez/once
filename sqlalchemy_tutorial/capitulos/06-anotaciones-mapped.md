# Capítulo 6: Anotaciones `Mapped[T]` — el "truco mágico" de la versión 2.0

> Antes, escribir un modelo era verboso. Ahora, **la clase es la fuente de verdad**.

---

## 6.1 El antes y el después

```python
# ❌ SQLAlchemy 1.x (antiguo)
class Usuario(Base):
    __tablename__ = "usuarios"
    id = Column(Integer, primary_key=True)
    nombre = Column(String(50))
```

```python
# ✅ SQLAlchemy 2.0 (moderno, recomendado)
class Usuario(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50))
```

### ¿Qué cambió?

1. **`Mapped[T]`** declara el tipo con *anotaciones* de Python (PEP 484).
2. **`mapped_column(...)`** reúne la configuración en una sola expresión.
3. Tu IDE sabe qué tipo es `usuario.nombre` (es `str`, no `Any`).
4. `mypy` valida tu código de forma precisa.

---

## 6.2 ¿Cómo funciona la "magia"?

| Lo que escribís en Python | Lo que SQLAlchemy deduce para SQL |
|---|---|
| `Mapped[int]` | columna `INTEGER` |
| `Mapped[str]` | columna `VARCHAR` (sin límite) |
| `Mapped[Optional[str]]` (o `Mapped[str \| None]`) | columna `VARCHAR` que **acepta NULL** |
| `Mapped[datetime]` | columna `DATETIME` |
| `Mapped[date]` | columna `DATE` |
| `Mapped[bool]` | columna `BOOLEAN` |
| `Mapped[float]` | columna `FLOAT` |
| `Mapped[bytes]` | columna `BLOB` |
| `Mapped[Decimal]` | columna `NUMERIC` (decimales exactos) |
| `Mapped[UUID]` | columna `UUID` (o `CHAR(32)` en MySQL) |

> 🎓 **Mental model**: la anotación `Mapped[T]` es como una **"pista"** que le dejás a SQLAlchemy sobre el tipo y la nulabilidad. A partir de eso, arma el SQL apropiado.

---

## 6.3 Reglas de nulabilidad

La **presencia o ausencia de `Optional`** define si la columna acepta `NULL` en SQL.

```python
from typing import Optional

class Perfil(Base):
    __tablename__ = "perfiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    # ✅ NOT NULL (no es Optional)
    nombre: Mapped[str] = mapped_column(String(50))

    # ✅ nullable (puede ser NULL)
    bio: Mapped[Optional[str]] = mapped_column(default=None)

    # ✅ equivalente con sintaxis moderna (Python 3.10+)
    sitio_web: Mapped[str | None] = mapped_column(default=None)
```

| Sintaxis | Equivale a |
|---|---|
| `Mapped[str]` | columna NOT NULL |
| `Mapped[Optional[str]]` | columna NULLABLE |
| `Mapped[str \| None]` | columna NULLABLE (Python 3.10+) |
| `Mapped[str] = mapped_column(nullable=False)` | explícito NOT NULL |
| `Mapped[str] = mapped_column(nullable=True)` | explícito NULLABLE |

---

## 6.4 Cuándo usar `mapped_column(...)` y cuándo no

```python
# Sin necesidad de configuración extra
id: Mapped[int] = mapped_column(primary_key=True)
apellido: Mapped[str]                  # → columna VARCHAR simple

# Cuando querés detalles
nombre: Mapped[str] = mapped_column(String(30), unique=True)
precio: Mapped[float] = mapped_column(Numeric(10, 2))
creado_en: Mapped[datetime] = mapped_column(server_default=func.now())
```

### Regla de oro

- Si necesitás `primary_key`, `nullable`, `unique`, `ForeignKey`, etc. → usás `mapped_column(...)`.
- Si solo necesitás el tipo básico → podés poner `Mapped[T]` **a secas**.

---

## 6.5 Opcionales y defaults

```python
from typing import Optional
from datetime import datetime
from sqlalchemy import func

class Persona(Base):
    __tablename__ = "personas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    email: Mapped[Optional[str]] = mapped_column(default=None)
    
    # La base pone el timestamp al insertar
    fecha_alta: Mapped[datetime] = mapped_column(server_default=func.now())

    # La base actualiza el timestamp en cada UPDATE
    fecha_actualizacion: Mapped[datetime] = mapped_column(
        server_default=func.now(),
        onupdate=func.now(),
    )
```

### Tipos de defaults

| Tipo | Cuándo se aplica | Ejemplo |
|---|---|---|
| `default=` | Cuando **Python** crea la instancia. | `default=uuid.uuid4` |
| `server_default=` | Cuando la **base** hace el INSERT. | `server_default=func.now()` |

> 💡 **Consejo**: para campos calculados por la base (timestamps, valores autoincrementales), preferí `server_default`. Para valores en Python, `default`.

---

## 6.6 Tipos de columnas: equivalencias SQL

```python
from sqlalchemy import (
    String, Integer, BigInteger, SmallInteger,
    Numeric, Float, Boolean, Date, DateTime, Time,
    Text, LargeBinary, JSON, Enum,
)

class Tipos(Base):
    __tablename__ = "tipos"

    id: Mapped[int] = mapped_column(primary_key=True)

    # Texto
    nombre: Mapped[str] = mapped_column(String(100))      # VARCHAR(100)
    descripcion_corta: Mapped[str] = mapped_column(String(50))
    resumen_largo: Mapped[str] = mapped_column(Text)      # TEXT sin límite

    # Números
    cantidad: Mapped[int] = mapped_column(Integer)        # INTEGER
    visitas: Mapped[int] = mapped_column(BigInteger)      # BIGINT
    pequeño: Mapped[int] = mapped_column(SmallInteger)    # SMALLINT
    precio: Mapped[float] = mapped_column(Numeric(10, 2)) # NUMERIC exacto
    promedio: Mapped[float] = mapped_column(Float)        # FLOAT aproximado

    # Booleano
    activo: Mapped[bool] = mapped_column(Boolean, default=True)

    # Fechas
    fecha: Mapped[date] = mapped_column(Date)
    momento: Mapped[datetime] = mapped_column(DateTime)

    # Bytes / archivos
    archivo: Mapped[bytes] = mapped_column(LargeBinary)

    # JSON
    configuracion: Mapped[dict] = mapped_column(JSON)

    # Enum
    estado: Mapped[str] = mapped_column(Enum("borrador", "publicado", name="estado_enum"))
```

> ⚠️ **Para dinero, usá `Numeric(10, 2)`**, no `Float`. El float tiene errores de redondeo que se notan en plata.

---

## 6.7 Desactivar anotaciones con `MappedAsDataclass`

Si venís del mundo de `dataclasses`, podés combinar ambas cosas:

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, MappedAsDataclass

class Base(MappedAsDataclass, DeclarativeBase):
    pass

class Producto(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    precio: Mapped[float]
```

✅ Ganas `__init__`, `__repr__` y `__eq__` automáticos. Pero perdés el control fino de los defaults.

> 🎓 **Consejo**: para la mayoría de proyectos, no lo uses. Mantenelo explícito.

---

## 🛠️ Ejercicios prácticos

### 🟢 Ejercicio 6.1: Mapeo de tipos

Para cada fila de la tabla, escribí la anotación `Mapped[T]` y `mapped_column(...)` que corresponda:

| Columna SQL | Anotación Python |
|---|---|
| `nombre VARCHAR(100)` | ? |
| `descripcion TEXT` | ? |
| `precio NUMERIC(12, 2)` | ? |
| `cantidad INTEGER NOT NULL DEFAULT 0` | ? |
| `activo BOOLEAN DEFAULT true` | ? |
| `creado_en DATETIME DEFAULT CURRENT_TIMESTAMP` | ? |
| `tags JSON` | ? |
| `foto BLOB` | ? |

**Solución**: [soluciones/06-anotaciones-mapped.md](../soluciones/06-anotaciones-mapped.md#ejercicio-61)

---

### 🟢 Ejercicio 6.2: Optionales vs requeridos

Definí el modelo `Pedido` con estas reglas:

- `id` (PK entero).
- `cliente_email` (NO nullable).
- `monto` (decimal, NO nullable).
- `direccion_envio` (puede ser NULL al inicio).
- `notas` (puede ser NULL).
- `fecha_pedido` (datetime, con server_default `now()`).

**Solución**: [soluciones/06-anotaciones-mapped.md](../soluciones/06-anotaciones-mapped.md#ejercicio-62)

---

### 🟡 Ejercicio 6.3: El error del `Float` para plata

Imaginá que un junior usa `Mapped[float]` para `precio`. Mostrá con un ejemplo de código por qué `Float` puede dar problemas con plata, y por qué `Numeric(10, 2)` lo arregla.

**Pista**: `0.1 + 0.2 != 0.3` en float.

**Solución**: [soluciones/06-anotaciones-mapped.md](../soluciones/06-anotaciones-mapped.md#ejercicio-63)

---

### 🟡 Ejercicio 6.4: Elegí el default correcto

Para cada caso, decidí si usás `default=` o `server_default=`:

1. UUID generado por Python al crear.
2. Timestamp al insertar.
3. Estado inicial `"pendiente"`.
4. Slug generado a partir del título.

**Solución**: [soluciones/06-anotaciones-mapped.md](../soluciones/06-anotaciones-mapped.md#ejercicio-64)

---

### 🟡 Ejercicio 6.5: Diagnóstico

Este modelo compila pero genera un SQL **incorrecto**. Encontrá el problema:

```python
from sqlalchemy import String, DateTime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from datetime import datetime

class Base(DeclarativeBase):
    pass

class Sesion(Base):
    __tablename__ = "sesiones"
    id: Mapped[str] = mapped_column(primary_key=True)
    expiracion: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
```

**Pista**: ¿qué pasa con las sesiones que se crean el 31 de diciembre de 2026 a las 23:59?

**Solución**: [soluciones/06-anotaciones-mapped.md](../soluciones/06-anotaciones-mapped.md#ejercicio-65)

---

## 🎓 Lo que aprendiste

- `Mapped[T]` es la forma moderna de declarar columnas.
- `Optional[T]` define nulabilidad (PK y campos requeridos no son `Optional`).
- `mapped_column(...)` recibe los mismos argumentos que `Column(...)`.
- Para Python 3.10+: `Mapped[str | None]` es lo mismo que `Mapped[Optional[str]]`.

## 📖 Siguiente

[Capítulo 7: Mixins — reutilizá columnas entre modelos →](./07-mixins.md)
