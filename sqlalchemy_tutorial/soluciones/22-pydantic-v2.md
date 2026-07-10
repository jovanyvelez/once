# Soluciones — Capítulo 22: Pydantic v2 en profundidad

[Volver al capítulo 22](../capitulos/22-pydantic-v2.md)

---

## Ejercicio 22.1

**Field con constraints**

```python
from pydantic import BaseModel, EmailStr, Field
from typing import Optional


class UsuarioCreate(BaseModel):
    username: str = Field(
        ..., min_length=3, max_length=20, pattern=r"^[a-zA-Z0-9_]+$"
    )
    password: str = Field(..., min_length=8)
    email: EmailStr
    edad: Optional[int] = Field(default=None, ge=0, le=120)

    @field_validator("password")
    @classmethod
    def password_tiene_digito(cls, v: str) -> str:
        if not any(c.isdigit() for c in v):
            raise ValueError("password debe tener al menos un dígito")
        return v
```

[Volver al ejercicio ↑](../capitulos/22-pydantic-v2.md#%C2%B0-ejercicio-221)

---

## Ejercicio 22.2

**Settings para tu app**

```python
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    database_url: str = "sqlite:///./tienda.db"
    debug: bool = False
    secret_key: str   # sin default, requerido
    allowed_hosts: List[str] = Field(default_factory=lambda: ["localhost"])

    model_config = SettingsConfigDict(env_file=".env", case_sensitive=False)
```

`.env`:

```bash
SECRET_KEY=mi-clave-muy-secreta-32-chars
DATABASE_URL=postgresql://user:pass@db/tienda
ALLOWED_HOSTS=["example.com", "localhost"]
DEBUG=true
```

[Volver al ejercicio ↑](../capitulos/22-pydantic-v2.md#%C2%B1-ejercicio-222)

---

## Ejercicio 22.3

**Validador custom de teléfono**

```python
import re
from pydantic import BaseModel, field_validator


class Contacto(BaseModel):
    nombre: str
    telefono: str

    @field_validator("telefono", mode="before")
    @classmethod
    def normalizar_telefono(cls, v: str) -> str:
        # Limpiar todo lo que no sea dígito
        digits = re.sub(r"\D", "", v)
        if not digits:
            raise ValueError("Teléfono vacío")
        
        # Asumimos Argentina: 54 + 11 + 8 dígitos
        if not digits.startswith("54"):
            digits = "54" + digits
        
        if len(digits) < 12:
            raise ValueError("Teléfono demasiado corto")
        
        # Formato +54 11 1234-5678
        return f"+{digits[:2]} {digits[2:4]} {digits[4:8]}-{digits[8:]}"


# Test
c = Contacto(nombre="Ana", telefono="(011) 1234-5678")
print(c.telefono)  # "+54 11 1234-5678"
```

[Volver al ejercicio ↑](../capitulos/22-pydantic-v2.md#%C2%B1-ejercicio-223)

---

## Ejercicio 22.4

**Model validator complejo**

```python
from pydantic import BaseModel, Field, model_validator, field_validator
from typing import Literal


class Transferencia(BaseModel):
    origen: str = Field(...)
    destino: str = Field(...)
    monto: float
    origen_tipo: Literal["USD", "ARS"] = "ARS"

    @field_validator("monto")
    @classmethod
    def monto_positivo(cls, v):
        if v <= 0:
            raise ValueError("monto debe ser positivo")
        return v

    @model_validator(mode="after")
    def validar_transferencia(self):
        if self.origen == self.destino:
            raise ValueError("origen y destino deben ser distintos")
        
        if self.origen_tipo == "USD":
            # En USD, múltiplos de 0.01
            if round(self.monto, 2) != self.monto:
                raise ValueError("monto en USD debe tener 2 decimales")
        
        return self
```

[Volver al ejercicio ↑](../capitulos/22-pydantic-v2.md#%C2%B1-ejercicio-224)

---

## Ejercicio 22.5

**Discriminated union**

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
    cbu: str = Field(min_length=22, max_length=22)


Pago = Annotated[
    PagoTarjeta | PagoEfectivo | PagoTransferencia,
    Field(discriminator="tipo"),
]


class Pedido(BaseModel):
    items: list[str]
    pago: Pago


# Tests
p1 = Pedido(items=["A"], pago={"tipo": "tarjeta", "ultimos_4": "1234", "marca": "visa"})
print(p1.pago.marca)  # "visa"

p2 = Pedido(items=["B"], pago={"tipo": "efectivo", "monto": 1000})
print(p2.pago.monto)  # 1000.0
```

[Volver al ejercicio ↑](../capitulos/22-pydantic-v2.md#%F0%9F%94%B4-ejercicio-225)