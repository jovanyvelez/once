# Capítulo 24: SQLAlchemy-Utils y extensiones útiles

> Lo que SQLAlchemy no trae de fábrica, pero te va a hacer la vida más fácil.

[SQLAlchemy-Utils](https://sqlalchemy-utils.readthedocs.io/) es una librería de extensión que añade **tipos de columna, helpers, mixins y funciones** que SQLAlchemy core no trae. Es como un kit de herramientas extra para el ORM.

---

## 24.1 Instalación

```bash
pip install sqlalchemy-utils
```

Para algunos tipos puede requerir extras:

```bash
pip install "sqlalchemy-utils[arrow]"      # soporte Arrow
pip install "sqlalchemy-utils[encrypted]"  # EncryptedType
pip install "sqlalchemy-utils[password]"   # PasswordType
```

---

## 24.2 Tipos de columna listos para usar

### `EmailType` — validar emails en la DB

```python
from sqlalchemy_utils import EmailType


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(EmailType, unique=True)
    nombre: Mapped[str]
```

> 💡 Internamente es un `VARCHAR`, pero valida al asignar: si no es un email válido, tira `AssertionError`.

### `URLType` — URLs

```python
from sqlalchemy_utils import URLType


class Empresa(Base):
    __tablename__ = "empresas"

    id: Mapped[int] = mapped_column(primary_key=True)
    sitio_web: Mapped[str | None] = mapped_column(URLType)
    api_url: Mapped[str | None] = mapped_column(URLType)
```

### `ColorType` — Colores

```python
from sqlalchemy_utils import ColorType


class Perfil(Base):
    __tablename__ = "perfiles"

    id: Mapped[int] = mapped_column(primary_key=True)
    color_favorito: Mapped[str] = mapped_column(ColorType)   # "#FF0000"
```

Lectura/escritura automática como string:

```python
p = Perfil(color_favorito="#FF0000")
print(p.color_favorito)  # "#ff0000"
```

### `CurrencyType` — Moneda con tipo de cambio

```python
from sqlalchemy_utils import CurrencyType


class Producto(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(primary_key=True)
    precio: Mapped[str] = mapped_column(CurrencyType)   # "USD", "ARS", etc.
```

### `UUIDType` — UUIDs nativos

```python
from sqlalchemy_utils import UUIDType
import uuid


class Sesion(Base):
    __tablename__ = "sesiones"

    id: Mapped[uuid.UUID] = mapped_column(
        UUIDType(binary=False),   # string legible
        primary_key=True,
        default=uuid.uuid4,
    )
```

```python
s = Sesion()
print(s.id)   # UUID('3f2504e0-4f89-11d3-9a0c-0305e82c3301')
```

### `ArrowType` — datetime con timezone

```python
from sqlalchemy_utils import ArrowType


class Evento(Base):
    __tablename__ = "eventos"

    id: Mapped[int] = mapped_column(primary_key=True)
    fecha: Mapped[arrow.Arrow] = mapped_column(ArrowType)
```

> 🎓 **Arrow** es una mejora sobre `datetime`: tiene métodos más prácticos para sumas, restas, timezones.

```python
import arrow
e = Evento(fecha=arrow.utcnow())
e.fecha.shift(days=7)
e.fecha.humanize()   # "an hour ago"
```

### `ChoiceType` — Enum en la DB

```python
from sqlalchemy_utils import ChoiceType


class Pedido(Base):
    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(primary_key=True)
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("pagado", "Pagado"),
        ("enviado", "Enviado"),
        ("entregado", "Entregado"),
        ("cancelado", "Cancelado"),
    ]
    estado: Mapped[str] = mapped_column(
        ChoiceType(choices=ESTADOS),
        default="pendiente",
    )
```

```python
p = Pedido()
p.estado = "pagado"   # acepta el código o la descripción
print(p.estado)        # ("pagado", "Pagado")
print(p.estado.code)   # "pagado"
print(p.estado.value)  # "Pagado"
```

> 🎓 **ChoiceType vs Enum**: ChoiceType es más flexible si los valores están en la DB y se cargan dinámicamente.

### `JSONType` — JSON nativo

```python
from sqlalchemy_utils import JSONType


class Configuracion(Base):
    __tablename__ = "configuraciones"

    id: Mapped[int] = mapped_column(primary_key=True)
    datos: Mapped[dict] = mapped_column(JSONType)
```

```python
c = Configuracion(datos={"tema": "oscuro", "notif": True})
c.datos["idioma"] = "es"
```

### `ScalarListType` — Lista como texto

Útil cuando tu DB no soporta arrays (PostgreSQL sí, pero SQLite/MySQL no):

```python
from sqlalchemy_utils import ScalarListType


class Articulo(Base):
    __tablename__ = "articulos"

    id: Mapped[int] = mapped_column(primary_key=True)
    tags: Mapped[list[str]] = mapped_column(ScalarListType(separator="|"))
```

```python
a = Articulo(tags=["python", "sqlalchemy", "fastapi"])
print(a.tags)  # ['python', 'sqlalchemy', 'fastapi']
# En la DB se guarda: "python|sqlalchemy|fastapi"
```

### `PasswordType` — hash automático

```python
from sqlalchemy_utils import PasswordType


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(EmailType, unique=True)
    password: Mapped[str] = mapped_column(PasswordType(schemes=["pbkdf2_sha512"]))
```

```python
u = Usuario(email="ana@ejemplo.com", password="secreto123")
session.add(u)
session.commit()

# En la DB, `password` está hasheado
# Para verificar:
u.check_password("secreto123")  # True
u.check_password("otro")        # False
```

> ⚠️ **Mejores prácticas**: para password hashing, usá `passlib` o `bcrypt` directamente. `PasswordType` está bien para prototipos.

### `EncryptedType` — cifrado a nivel columna

```python
from sqlalchemy_utils import EncryptedType


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    telefono: Mapped[str] = mapped_column(EncryptedType(str, key="mi-clave-secreta"))
```

> 🎓 **Para casos legales (datos personales sensibles)**: el cifrado a nivel columna cumple con GDPR, HIPAA, etc.

---

## 24.3 Mixins de SQLAlchemy-Utils

### `Timestamp` — columnas de auditoría

```python
from sqlalchemy_utils import Timestamp


class Producto(Base, Timestamp):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
```

Esto agrega automáticamente `created` y `updated` (con trigger en la DB).

### `SoftDeleteMixin` — borrado lógico

```python
from sqlalchemy_utils import SoftDeleteMixin


class Articulo(Base, SoftDeleteMixin):
    __tablename__ = "articulos"

    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str]
```

```python
a = session.get(Articulo, 1)
session.delete(a)   # hace UPDATE articulos SET deleted_at = now() WHERE id=1
session.commit()
```

Para excluir los eliminados de las queries, usá el **QueryClass** customizado.

### `ForceIDMixin` — para tablas sin ID explícito

No recomendado, pero existe.

---

## 24.4 Helpers para queries

### `database_exists` y `create_database`

```python
from sqlalchemy_utils import database_exists, create_database, drop_database

engine = create_engine("postgresql://user:pass@localhost/mydb")

if not database_exists(engine.url):
    create_database(engine.url)
    print("✅ DB creada")
else:
    print("Ya existe")

# Si querés borrarla
# drop_database(engine.url)
```

### `create_all` con tipos especiales

SQLAlchemy-Utils provee un `create_all` mejorado que reconoce los tipos extendidos:

```python
from sqlalchemy_utils import create_database, database_exists

if not database_exists(engine.url):
    create_database(engine.url)

# crea todas las tablas (incluyendo tipos especiales)
Base.metadata.create_all(engine)
```

### Helpers para relaciones

```python
from sqlalchemy_utils import (
    foreign_keys,
    has_unique_index,
    primary_keys,
    indexes,
    tables,
    get_columns,
    getdotattr,
)
```

> 💡 Menos frecuentes en la práctica diaria, pero útiles para scripts de introspección.

---

## 24.5 Funciones de polimorfismo

### `polymorphic_identity` helpers

```python
from sqlalchemy_utils import get_polymorphic_base_class, get_polymorphic_class


class Vehiculo(Base):
    __tablename__ = "vehiculos"
    id: Mapped[int] = mapped_column(primary_key=True)
    __mapper_args__ = {
        "polymorphic_identity": "vehiculo",
        "polymorphic_on": "tipo",
    }


# En runtime:
tipo = get_polymorphic_class(Vehiculo, "auto")   # la clase Auto
```

---

## 24.6 Generadores de datos para tests

```python
from sqlalchemy_utils import (
    Ltree,
    Locale,
    Country,
    Currency,
    TimezoneType,
)
```

`Locale`, `Country`, `Currency` son enumeraciones que te dan valores predefinidos:

```python
from sqlalchemy_utils import Country


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    pais: Mapped[Country] = mapped_column()  # ISO 3166


u = Usuario(pais="AR")
print(u.pais)  # Country(name='Argentina', alpha2='AR', alpha3='ARG', numeric='032', ...)
```

---

## 24.7 `RangeType` y `DateRangeType` (PostgreSQL)

```python
from sqlalchemy_utils import DateRangeType, RangeType


class Evento(Base):
    __tablename__ = "eventos"

    id: Mapped[int] = mapped_column(primary_key=True)
    duracion: Mapped[DateRange] = mapped_column(DateRangeType)  # rango de fechas
```

```python
e = Evento(duracion=(date(2026, 1, 1), date(2026, 1, 31)))
print(e.duracion.lower, e.duracion.upper)
print("2026-01-15" in e.duracion)  # True
```

---

## 24.8 `Ltree` — jerarquías en PostgreSQL

```python
from sqlalchemy_utils import LtreeType


class Categoria(Base):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(primary_key=True)
    ruta: Mapped[str] = mapped_column(LtreeType)


# Crea una jerarquía
electronica = Categoria(ruta="electronica")
celulares = Categoria(ruta="electronica.celulares")
```

PostgreSQL tiene operadores especiales para hacer queries eficientes sobre árboles.

---

## 24.9 `PhoneNumberType`

```python
from sqlalchemy_utils import PhoneNumberType


class Cliente(Base):
    __tablename__ = "clientes"

    id: Mapped[int] = mapped_column(primary_key=True)
    telefono: Mapped[str] = mapped_column(PhoneNumberType())
```

Requiere `phonenumbers`:

```bash
pip install "sqlalchemy-utils[phone]"
```

---

## 24.10 Resumen de tipos y cuándo usarlos

| Tipo | Para qué | Ejemplo |
|---|---|---|
| `EmailType` | Emails validados. | `email` de usuario. |
| `URLType` | URLs HTTP. | `sitio_web` de empresa. |
| `ColorType` | Colores CSS/HEX. | `color_favorito`. |
| `UUIDType` | IDs UUID. | `id` de sesiones. |
| `ArrowType` | Datetime con timezone. | `fecha_evento`. |
| `ChoiceType` | Enums. | `estado` de pedido. |
| `JSONType` | JSON nativo. | `datos` de config. |
| `ScalarListType` | Lista de strings. | `tags` de artículo. |
| `PasswordType` | Hash de contraseñas. | `password` de usuario. |
| `EncryptedType` | Cifrado reversible. | `telefono`, datos sensibles. |
| `PhoneNumberType` | Teléfonos. | `telefono` de cliente. |
| `DateRangeType` | Rango de fechas (Postgres). | `duracion` de evento. |

---

## 24.11 Cuándo NO usar SQLAlchemy-Utils

| Caso | Mejor opción |
|---|---|
| Email de usuario | `EmailStr` de Pydantic en la API, `String` en la DB. |
| Passwords en producción | `passlib` o `bcrypt` directamente. |
| Validaciones complejas | Pydantic en la capa de API. |
| Tipos no soportados por tu DB | `String` con validación Pydantic. |

> 🎓 **Regla del profesor**: SQLAlchemy-Utils es excelente para **tipos especializados** y **helpers**. Pero no abuses: para validaciones de input, **siempre Pydantic**. Para passwords en producción, **siempre bcrypt/passlib**.

---

## 24.12 El proyecto final: combinación SQLAlchemy + SQLAlchemy-Utils + Pydantic

```python
# app/models/usuario.py
from datetime import date
from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import EmailType, PasswordType, EncryptedType

from app.database import Base
from app.models.base import TimestampMixin


class Usuario(Base, TimestampMixin):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(EmailType, unique=True, index=True)
    nombre: Mapped[str] = mapped_column(String(100))
    password: Mapped[str] = mapped_column(PasswordType(schemes=["pbkdf2_sha512"]))
    telefono: Mapped[str] = mapped_column(EncryptedType(String, key="clave-secreta"))
    fecha_nacimiento: Mapped[date] = mapped_column()
    dni: Mapped[str] = mapped_column(EncryptedType(String, key="otra-clave"))


# app/schemas/usuario.py
from pydantic import BaseModel, EmailStr, Field
from datetime import date


class UsuarioBase(BaseModel):
    email: EmailStr
    nombre: str = Field(min_length=2, max_length=100)
    fecha_nacimiento: date


class UsuarioCreate(UsuarioBase):
    password: str = Field(min_length=8)


class UsuarioPublic(UsuarioBase):
    id: int
    creado_en: datetime
    model_config = ConfigDict(from_attributes=True)
```

```python
# app/routers/usuarios.py
@router.post("/", response_model=UsuarioPublic, status_code=201)
def crear(data: UsuarioCreate, session: SessionDep) -> UsuarioPublic:
    nuevo = Usuario(
        email=data.email,
        nombre=data.nombre,
        password=data.password,    # hashea automáticamente
        fecha_nacimiento=data.fecha_nacimiento,
    )
    session.add(nuevo)
    session.commit()
    session.refresh(nuevo)
    return nuevo
```

---

## 🎓 Lo que aprendiste

- **SQLAlchemy-Utils** añade tipos especializados y helpers al ORM.
- Tipos como `EmailType`, `URLType`, `UUIDType` validan al asignar.
- `ChoiceType` es ideal para enums dinámicos.
- `EncryptedType` y `PasswordType` para seguridad.

---

## 🛠️ Ejercicios prácticos

### 🟢 Ejercicio 24.1: EmailType en uso

Creá un modelo `Suscripcion(email, fecha_alta)` usando `EmailType`. Probá asignar un email inválido: ¿qué pasa?

**Solución**: [soluciones/24-sqlalchemy-utils.md](../soluciones/24-sqlalchemy-utils.md#ejercicio-241)

---

### 🟡 Ejercicio 24.2: ChoiceType para estados

Modelá `Pedido` con `ChoiceType` para `estado`. Estados: `"pendiente"`, `"pagado"`, `"enviado"`, `"cancelado"`.

**Solución**: [soluciones/24-sqlalchemy-utils.md](../soluciones/24-sqlalchemy-utils.md#ejercicio-242)

---

### 🟡 Ejercicio 24.3: UUIDType

Modelá `Token` con `UUIDType` (binary=False, o sea, como string). Cada token tiene un UUID autogenerado.

**Solución**: [soluciones/24-sqlalchemy-utils.md](../soluciones/24-sqlalchemy-utils.md#ejercicio-243)

---

### 🟡 Ejercicio 24.4: PasswordType

Modelá `Usuario` con `PasswordType`. Demostrá que:

1. `Usuario(password="123")` valida (>= 8 chars).
2. `usuario.check_password("secret")` retorna `True` después de commit.
3. `usuario.check_password("otro")` retorna `False`.

**Solución**: [soluciones/24-sqlalchemy-utils.md](../soluciones/24-sqlalchemy-utils.md#ejercicio-244)

---

### 🔴 Ejercicio 24.5: EncryptedType en producción

Modelá `Usuario(telefono, dni)` con `EncryptedType`. Investigá:

1. ¿Dónde está la clave de cifrado? ¿Es segura?
2. ¿Cómo rotarías la clave sin perder los datos?
3. ¿Cómo harías backup/recuperación?

**Solución**: [soluciones/24-sqlalchemy-utils.md](../soluciones/24-sqlalchemy-utils.md#ejercicio-245)

---

## 🎓 Lo que aprendiste

- **SQLAlchemy-Utils** añade tipos especializados y helpers al ORM.
- Tipos como `EmailType`, `URLType`, `UUIDType` validan al asignar.
- `ChoiceType` es ideal para enums dinámicos.
- `EncryptedType` y `PasswordType` para seguridad.
- **Cuándo usarlo** vs **cuándo no** (Pydantic en API, bcrypt directo para passwords).
- `Timestamp` y `SoftDeleteMixin` te ahorran escribir.

## 📖 Cierre del manual

¡Felicidades! Llegaste al final del manual. Recorriste desde lo más básico (instalar y crear un modelo) hasta temas avanzados (eventos, async, migraciones, utilidades).

### Lo que aprendiste en este manual

- **21 capítulos anteriores** + **3 nuevos** = 24.
- ✅ Modelos modernos con `Mapped[T]`.
- ✅ Mixins y herencia de modelos.
- ✅ Relaciones 1—N, 1—1, N—M y recursivas.
- ✅ Eventos del ORM y validaciones con `@validates`.
- ✅ `AsyncSession` para apps no bloqueantes.
- ✅ FastAPI con `get_db()` con `yield` y `SessionDep`.
- ✅ Pydantic v2 en profundidad.
- ✅ Alembic para migraciones.
- ✅ SQLAlchemy-Utils para tipos especializados.

### Tu próximo paso

Armá tu propio proyecto. Copiá la estructura de `proyecto/fastapi_sqlalchemy/` y construí algo que te interese. La mejor forma de fijar el conocimiento es **romper cosas y arreglarlas**.

¡Mucho éxito! 🚀🐍