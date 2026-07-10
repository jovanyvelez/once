# Capítulo 22: Pydantic v2 en profundidad

> Pydantic es el **90% de FastAPI**. Si lo dominás, podés validar cualquier cosa con elegancia.

Este capítulo cubre los detalles avanzados de Pydantic v2: settings, validators, field constraints, modelos anidados, y patrones específicos para SQLAlchemy.

---

## 22.1 Recordatorio: ¿qué es Pydantic?

Pydantic es una librería de **validación y serialización de datos** basada en anotaciones de tipo. Es la columna vertebral de FastAPI.

```python
from pydantic import BaseModel


class Usuario(BaseModel):
    nombre: str
    edad: int
```

> 🎓 **Analogía del profesor**: Pydantic es como un **guardia de seguridad de discoteca** 🛡️. Antes de que un dato entre a tu sistema, lo revisa: ¿es string? ¿es número? ¿está en el rango? Si no pasa, lo rebota con un error claro.

### Diferencia entre v1 y v2

| Aspecto | Pydantic v1 🟠 | Pydantic v2 ✅ |
|---|---|---|
| `BaseSettings` | módulo aparte | `pydantic-settings` (separado) |
| `.dict()` | sí | `.model_dump()` |
| `Config` | clase `Config` | `model_config = ConfigDict(...)` |
| Validators | `@validator` | `@field_validator` / `@model_validator` |
| Performance | regular | 5x-50x más rápido (Rust) |

> ⚠️ **Pydantic v2 es obligatorio** para FastAPI 0.100+. Si ves tutoriales viejos con `.dict()` o `Config`, es v1.

---

## 22.2 `Field()`: restricciones por campo

```python
from pydantic import BaseModel, Field


class Producto(BaseModel):
    nombre: str = Field(
        ...,
        min_length=1,
        max_length=100,
        description="Nombre comercial del producto",
        examples=["Cafetera inteligente"],
    )
    sku: str = Field(
        ...,
        min_length=1,
        max_length=20,
        pattern=r"^[A-Z]{3}-\d{3}$",  # ej: CF-001
    )
    precio: float = Field(
        ...,
        gt=0,
        le=1_000_000,
        description="Precio en pesos",
    )
    stock: int = Field(default=0, ge=0)
    descripcion: str | None = Field(default=None, max_length=500)
```

| Argumento | Qué hace |
|---|---|
| `default` | Valor por defecto (puede ser un callable). |
| `default_factory` | Función que crea el default (útil para listas/dicts). |
| `gt`, `ge`, `lt`, `le` | Mayor/menor estricto y no estricto. |
| `min_length`, `max_length` | Para strings y listas. |
| `pattern` | Regex que debe cumplir. |
| `description` | Aparece en la docstring de OpenAPI. |
| `examples` | Ejemplos en la docstring. |
| `alias` | Nombre distinto en JSON (`"nombre_oficial"` → `nombre`). |
| `deprecated` | Marca como deprecated en OpenAPI. |

> 💡 **Para Pydantic v2 con FastAPI, `Field()` también acepta todos los metadatos que normalmente usarías en Query/Body/Path.**

---

## 22.3 Validadores personalizados

### `@field_validator` — valida un campo

```python
from pydantic import BaseModel, field_validator


class Usuario(BaseModel):
    nombre: str
    email: str

    @field_validator("email")
    @classmethod
    def validar_email(cls, v: str) -> str:
        if "@" not in v:
            raise ValueError("email debe contener @")
        return v.lower().strip()
```

### Validador con varios campos

```python
class RangoFechas(BaseModel):
    inicio: date
    fin: date

    @field_validator("fin")
    @classmethod
    def fin_mayor_que_inicio(cls, v: date, info) -> date:
        # `info.data` tiene los otros campos ya validados
        if "inicio" in info.data and v <= info.data["inicio"]:
            raise ValueError("`fin` debe ser mayor que `inicio`")
        return v
```

### `@model_validator` — valida el modelo entero

```python
from pydantic import BaseModel, model_validator


class CuentaBancaria(BaseModel):
    titular: str
    balance: float
    descubierto_max: float = 0.0

    @model_validator(mode="after")
    def verificar_balance(self):
        # el modelo ya está construido, accedemos a self.balance
        if self.balance < -self.descubierto_max:
            raise ValueError("Excede el descubierto permitido")
        return self
```

### `mode="before"` vs `mode="after"`

```python
@field_validator("nombre", mode="before")
def normalizar_nombre(cls, v):
    """Se ejecuta ANTES del tipado. Sirve para limpiar datos crudos."""
    if isinstance(v, str):
        return v.strip().title()
    return v


@field_validator("nombre", mode="after")
def validar_nombre(cls, v):
    """Se ejecuta DESPUÉS del tipado. `v` ya es del tipo declarado."""
    if len(v) < 2:
        raise ValueError("Nombre muy corto")
    return v
```

| Modo | Cuándo corre | Uso típico |
|---|---|---|
| `before` | Antes de la coerción de tipo | Limpiar strings, normalizar. |
| `after` (default) | Después de la coerción | Validar reglas de negocio. |
| `wrap` | Antes y después | Modificar el valor tras validar. |

---

## 22.4 `model_config` — ConfigDict

En v2, la clase `Config` desapareció. Ahora se usa `model_config = ConfigDict(...)`.

```python
from pydantic import BaseModel, ConfigDict


class ProductoPublic(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,         # leer atributos de objetos ORM
        str_strip_whitespace=True,    # trim automático en str
        str_to_lower=False,           # NO lower (default)
        validate_assignment=True,     # valida cuando hacés producto.campo = ...
        frozen=False,                 # no se puede mutar el modelo
        extra="forbid",               # no permite campos extra
        populate_by_name=True,        # permite tanto `nombre` como alias
        arbitrary_types_allowed=True, # permite Decimal, etc.
    )
```

| Opción | Para qué sirve |
|---|---|
| `from_attributes=True` | Que Pydantic pueda leer atributos de objetos ORM (antes `orm_mode`). |
| `str_strip_whitespace` | Auto-trim en strings. |
| `validate_assignment` | Valida cuando hacés `obj.campo = ...`. |
| `frozen` | Inmutabilidad (estilo `dataclass(frozen=True)`). |
| `extra="forbid"` | Lanza error si vienen campos no declarados. |
| `extra="ignore"` | Los campos extra se descartan silenciosamente. |
| `populate_by_name` | Permite que se llame con el alias O con el nombre del campo. |
| `arbitrary_types_allowed` | Para tipos como `Decimal`, `datetime` con tz. |

> 🎓 **Típico en schemas FastAPI**: `from_attributes=True` para `Public` (lee de ORM), `extra="forbid"` en `Create` (que el cliente no mande basura).

---

## 22.5 Modelos anidados

### Lista de objetos anidados

```python
class Item(BaseModel):
    nombre: str
    cantidad: int


class Pedido(BaseModel):
    cliente: str
    items: list[Item]   # lista de objetos anidados

    @field_validator("items")
    @classmethod
    def minimo_un_item(cls, v: list[Item]) -> list[Item]:
        if len(v) == 0:
            raise ValueError("El pedido debe tener al menos un item")
        return v
```

### Estructuras recursivas

```python
from typing import Optional
from pydantic import BaseModel


class Comentario(BaseModel):
    texto: str
    respuestas: list["Comentario"] = []  # self-reference


# Pydantic resuelve las referencias circulares automáticamente
Comentario.model_rebuild()

uso = Comentario(
    texto="¿Pregunta?",
    respuestas=[
        Comentario(texto="Una respuesta"),
        Comentario(
            texto="Otra respuesta",
            respuestas=[Comentario(texto="Respuesta anidada")],
        ),
    ],
)
```

---

## 22.6 Discriminated unions (polimorfismo con Pydantic)

Imaginá que un endpoint recibe distintos tipos de pagos:

```python
from typing import Annotated, Literal
from pydantic import BaseModel, Field


class PagoTarjeta(BaseModel):
    tipo: Literal["tarjeta"]
    ultimos_4: str = Field(min_length=4, max_length=4)
    marca: Literal["visa", "mastercard", "amex"]


class PagoEfectivo(BaseModel):
    tipo: Literal["efectivo"]
    monto: float = Field(gt=0)


class PagoTransferencia(BaseModel):
    tipo: Literal["transferencia"]
    banco: str
    cbu: str = Field(min_length=22, max_length=22)


Pago = Annotated[
    PagoTarjeta | PagoEfectivo | PagoTransferencia,
    Field(discriminator="tipo"),
]


class Pedido(BaseModel):
    items: list[str]
    pago: Pago   # Pydantic elige la subclase según `tipo`


# Uso
p1 = Pedido(items=["A"], pago={"tipo": "tarjeta", "ultimos_4": "1234", "marca": "visa"})
# Funciona con cualquier subclase:
p2 = Pedido(items=["B"], pago={"tipo": "efectivo", "monto": 1000})
```

> 🎓 **Por qué `discriminator`**: Pydantic valida en función de un campo común (`tipo`), lo que es 2-3x más rápido que un Union tradicional.

---

## 22.7 `EmailStr`, `HttpUrl`, `IPvAnyAddress`: tipos pre-construidos

```bash
pip install pydantic[email]
```

```python
from pydantic import BaseModel, EmailStr, HttpUrl, IPvAnyAddress


class Cliente(BaseModel):
    email: EmailStr                # valida formato de email
    sitio_web: HttpUrl | None      # valida URL
    ip_registro: IPvAnyAddress     # IPv4 o IPv6
```

Tipos disponibles sin instalar nada extra:

| Tipo | Validación |
|---|---|
| `EmailStr` | Email válido (con `pydantic[email]`). |
| `HttpUrl` | URL HTTP/HTTPS válida. |
| `AnyUrl` | Cualquier URL (FTP, file, etc.). |
| `IPvAnyAddress` | IPv4 o IPv6. |
| `PositiveInt` | `int > 0`. |
| `NegativeFloat` | `float < 0`. |
| `conint(ge=10, le=100)` | `int` con rango. |
| `constr(min_length=1)` | `str` con mínimo. |
| `Decimal` | (sin librerías extra). |
| `UUID4` | UUID versión 4. |
| `Json` | String que es JSON parseable. |
| `PaymentCardNumber` | (con `pydantic[email]`) número de tarjeta. |
| `Color` | Color CSS o hexadecimal. |

---

## 22.8 Validación y serialización personalizada

### `field_serializer`

```python
from pydantic import BaseModel, field_serializer
from datetime import datetime


class Evento(BaseModel):
    nombre: str
    fecha: datetime

    @field_serializer("fecha")
    def serializar_fecha(self, dt: datetime) -> str:
        return dt.isoformat()
```

### `field_validator` + `field_serializer` (antes y después)

```python
class Persona(BaseModel):
    nombre: str

    @field_validator("nombre", mode="before")
    def normalizar_nombre(cls, v):
        return v.strip().title() if isinstance(v, str) else v

    @field_serializer("nombre")
    def serializar_nombre(self, v):
        return v.upper()
```

### `model_serializer`

```python
from pydantic import BaseModel, model_serializer


class RespuestaApi(BaseModel):
    status: str
    data: dict
    timestamp: datetime

    @model_serializer
    def serializar(self):
        return {
            "status": self.status,
            "data": self.data,
            "ts": self.timestamp.isoformat(),
        }
```

---

## 22.9 `model_dump` vs `model_dump_json` vs `dict`

En v1 era `.dict()`. En v2 son:

| Método | Devuelve | Uso |
|---|---|---|
| `model.model_dump()` | `dict` Python | Pasa a otro sistema, ORM, JSON antes de serializar. |
| `model.model_dump_json()` | `str` JSON | Directamente al cliente. |
| `model.model_dump(exclude_unset=True)` | Solo lo que el cliente mandó | PATCH parcial. |
| `model.model_dump(exclude={"password"})` | Sin campos sensibles | Para serializar. |
| `model.model_dump(include={"id", "nombre"})` | Solo estos campos | Filtros de salida. |
| `model.model_dump(by_alias=True)` | Usa los alias | Para el JSON externo. |

```python
data_dict = producto.model_dump()
data_json = producto.model_dump_json()
data_parcial = producto.model_dump(exclude_unset=True, exclude={"password"})
```

---

## 22.10 Pydantic Settings — variables de entorno

`BaseSettings` se movió al paquete `pydantic-settings` (v2). Es la forma estándar de leer configuración.

```bash
pip install pydantic-settings
```

```python
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración global cargada de variables de entorno."""
    
    # Variables
    database_url: str = Field(default="sqlite:///./tienda.db", alias="DATABASE_URL")
    debug: bool = False
    secret_key: str
    allowed_hosts: list[str] = Field(default_factory=lambda: ["localhost"])

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        env_nested_delimiter="_",
    )
```

### `.env` file

```bash
DATABASE_URL=postgresql://user:pass@localhost/db
DEBUG=true
SECRET_KEY=super-secreto
ALLOWED_HOSTS=["api.example.com","localhost"]
```

### Uso

```python
settings = Settings()  # lee de .env y variables de entorno
print(settings.database_url)
print(settings.allowed_hosts)
```

> 💡 **Por qué se movió a `pydantic-settings`**: para que Pydantic core quede más liviano. Pydantic-settings se enfoca en leer de .env, secrets, AWS, etc.

---

## 22.11 Patrones con SQLAlchemy

### Schema que representa un modelo ORM

```python
from pydantic import BaseModel, ConfigDict


class ProductoPublic(BaseModel):
    id: int
    nombre: str
    precio: float
    categoria_id: int | None
    creado_en: datetime

    # Lee atributos de objetos ORM
    model_config = ConfigDict(from_attributes=True)


# En el endpoint:
@app.get("/productos/{id}", response_model=ProductoPublic)
def obtener(id: int, session: SessionDep):
    p = session.get(Producto, id)
    if not p:
        raise HTTPException(404)
    return p   # se convierte automáticamente a ProductoPublic
```

### Schema que hereda de otro schema

```python
class ProductoBase(BaseModel):
    nombre: str
    sku: str
    precio: float


class ProductoCreate(ProductoBase):
    categoria_id: int | None = None


class ProductoPublic(ProductoBase):
    id: int
    creado_en: datetime
    model_config = ConfigDict(from_attributes=True)


class ProductoUpdate(BaseModel):
    """PATCH: todos opcionales."""
    nombre: str | None = None
    sku: str | None = None
    precio: float | None = None
```

> 💡 **Por qué `Update` no hereda de `Base`**: en PATCH querés campos opcionales, no validar los mínimos de `Base`.

### Schema con `Decimal` (¡plata!)

```python
from decimal import Decimal
from pydantic import BaseModel, Field


class ProductoBase(BaseModel):
    precio: Decimal = Field(
        ...,
        gt=0,
        max_digits=10,   # total de dígitos
        decimal_places=2,  # después de la coma
    )
```

> ⚠️ **Nunca uses `float` para plata**: por errores de redondeo. `Decimal` es exacto.

### Schema que filtra un campo sensible

```python
class UsuarioDB(BaseModel):
    id: int
    email: str
    password_hash: str   # nunca se muestra


class UsuarioPublic(BaseModel):
    id: int
    email: str
    # password_hash NO se expone

    @classmethod
    def from_db(cls, u: UsuarioDB) -> "UsuarioPublic":
        return cls(id=u.id, email=u.email)
```

> 🎓 **El patrón definitivo**: tené `*DB` (todo) y `*Public` (lo que se muestra). El router solo expone `*Public`.

---

## 22.12 Validadores con SQLAlchemy — ejemplo completo

```python
from pydantic import BaseModel, EmailStr, Field, field_validator
from sqlalchemy import select
from sqlalchemy.orm import Session


class UsuarioCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=8)
    nombre: str = Field(min_length=2, max_length=50)

    @field_validator("password")
    @classmethod
    def password_fuerte(cls, v: str) -> str:
        if not any(c.isupper() for c in v):
            raise ValueError("Debe tener al menos una mayúscula")
        if not any(c.isdigit() for c in v):
            raise ValueError("Debe tener al menos un número")
        return v

    @field_validator("nombre")
    @classmethod
    def nombre_limpio(cls, v: str) -> str:
        return v.strip().title()


# En el endpoint, podemos chequear duplicados antes de insertar:
@app.post("/usuarios/")
def crear(data: UsuarioCreate, session: SessionDep):
    existe = session.scalar(select(Usuario).where(Usuario.email == data.email))
    if existe:
        raise HTTPException(400, "Email ya registrado")

    nuevo = Usuario(
        email=data.email,
        password_hash=hash_password(data.password),  # bcrypt, etc.
        nombre=data.nombre,
    )
    session.add(nuevo)
    session.commit()
    return {"id": nuevo.id, "email": nuevo.email}
```

> 💡 **Validación cruzada** (ej: chequear contra la DB) conviene hacerla en el endpoint o en una capa de servicio, no en el schema. El schema valida **forma**; el servicio valida **estado**.

---

## 22.13 Errores personalizados

```python
from pydantic import BaseModel, Field, ValidationError


def custom_handler(err: ValidationError):
    return {
        "errors": [
            {
                "field": ".".join(str(x) for x in e["loc"]),
                "message": e["msg"],
                "type": e["type"],
            }
            for e in err.errors()
        ]
    }


# En FastAPI:
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse


@app.exception_handler(RequestValidationError)
async def custom_validation_handler(request, exc):
    return JSONResponse(
        status_code=422,
        content=custom_handler(exc),
    )
```

---

## 22.14 Performance: cuando Pydantic se vuelve lento

Si tenés schemas con muchos validadores y los instanciás millones de veces:

1. 🟢 **Usá `model_construct()`** (no valida nada, solo crea el objeto):

```python
# Pydantic v2
datos = {"id": 1, "nombre": "A"}
obj = ProductoPublic.model_construct(**datos)   # sin validar
```

2. 🟢 **Usá `TypeAdapter`** para validar un dict contra un modelo:

```python
from pydantic import TypeAdapter

adapter = TypeAdapter(ProductoPublic)
obj = adapter.validate_python(datos)   # valida una vez
```

3. 🟢 **Reusá el adapter** (no recrees el schema cada vez).

4. 🟢 **Para queries masivas**, traé dicts y validá solo al final.

> 💡 **Regla**: solo optimices Pydantic cuando sea el cuello de botella. Para el 95% de las apps, la performance nativa es suficiente.

---

## 22.15 Resumen: mejores prácticas

| Caso | Patrón |
|---|---|
| Validar request body | `BaseModel` con `Field(...)` y validadores. |
| Output a cliente | `BaseModel` con `response_model=` y `from_attributes`. |
| Variables de entorno | `BaseSettings` con `pydantic-settings`. |
| Schemas que comparten campos | Herencia: `Base → Create`, `Base → Public`. |
| PATCH parcial | `BaseModel` con todos opcionales + `exclude_unset=True`. |
| Tipos de dominio | `EmailStr`, `HttpUrl`, `Decimal`, `UUID4`. |
| Datos sensibles | Schema `DB` separado del `Public`. |
| Discriminated unions | `Annotated[T1 \| T2, Field(discriminator="tipo")]`. |

---

## 🛠️ Ejercicios prácticos

### 🟢 Ejercicio 22.1: Field con constraints

Creá un modelo `UsuarioCreate` con:

- `username`: str, 3-20 chars, alfanumérico.
- `password`: str, mínimo 8 chars, debe tener al menos un dígito.
- `email`: EmailStr.
- `edad`: Optional[int], entre 0 y 120.

**Solución**: [soluciones/22-pydantic-v2.md](../soluciones/22-pydantic-v2.md#ejercicio-221)

---

### 🟡 Ejercicio 22.2: Settings para tu app

Implementá un `Settings` que lea de `.env`:

- `database_url` (default SQLite).
- `debug` (bool, default False).
- `secret_key` (sin default, requerido).
- `allowed_hosts` (lista, default `["localhost"]`).

**Solución**: [soluciones/22-pydantic-v2.md](../soluciones/22-pydantic-v2.md#ejercicio-222)

---

### 🟡 Ejercicio 22.3: Validador custom

Creá un `@field_validator("telefono")` que normalice teléfonos al formato `+54 11 1234-5678`.

**Solución**: [soluciones/22-pydantic-v2.md](../soluciones/22-pydantic-v2.md#ejercicio-223)

---

### 🟡 Ejercicio 22.4: Model validator

Creá un modelo `Transferencia(origen, destino, monto)`. Validá con `@model_validator`:

- `monto` positivo.
- `origen != destino`.
- Si `origen.tipo == "USD"`, el monto debe ser múltiplo de 0.01.

**Solución**: [soluciones/22-pydantic-v2.md](../soluciones/22-pydantic-v2.md#ejercicio-224)

---

### 🔴 Ejercicio 22.5: Discriminated union

Modelá un sistema de pagos con discriminated union:

- `PagoTarjeta(ultimos_4, marca)`.
- `PagoEfectivo(monto)`.
- `PagoTransferencia(cbu)`.

Que un `Pedido` acepte cualquiera de los tres tipos según `tipo`.

**Solución**: [soluciones/22-pydantic-v2.md](../soluciones/22-pydantic-v2.md#ejercicio-225)

---

## 🎓 Lo que aprendiste

- Pydantic v2 es **5x-50x más rápido** que v1 gracias al core en Rust.
- `Field()` permite restricciones detalladas (`gt`, `min_length`, `pattern`).
- `@field_validator` valida un campo; `@model_validator` valida el modelo entero.
- `ConfigDict` reemplaza la vieja clase `Config`.
- `model_dump(exclude_unset=True)` es el patrón canónico de PATCH.
- `pydantic-settings` lee configuración de `.env` y variables de entorno.
- `from_attributes=True` permite leer desde objetos ORM.

## 📖 Siguiente

[Capítulo 23: Alembic — migraciones de base de datos →](./23-alembic.md)