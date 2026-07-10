# Soluciones — Capítulo 24: SQLAlchemy-Utils

[Volver al capítulo 24](../capitulos/24-sqlalchemy-utils.md)

---

## Ejercicio 24.1

**EmailType**

```python
from sqlalchemy_utils import EmailType
from datetime import datetime
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Suscripcion(Base):
    __tablename__ = "suscripciones"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(EmailType)
    fecha_alta: Mapped[datetime]


# ✅ Válido
s = Suscripcion(email="ana@ejemplo.com", fecha_alta=datetime.now())

# ❌ Inválido
try:
    s = Suscripcion(email="esto-no-es-email", fecha_alta=datetime.now())
except Exception as e:
    print(f"Error: {e}")
    # -> AssertionError: esto-no-es-email
```

[Volver al ejercicio ↑](../capitulos/24-sqlalchemy-utils.md#%C2%B0-ejercicio-241)

---

## Ejercicio 24.2

**ChoiceType para estados**

```python
from sqlalchemy_utils import ChoiceType


class Pedido(Base):
    __tablename__ = "pedidos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    ESTADOS = [
        ("pendiente", "Pendiente"),
        ("pagado", "Pagado"),
        ("enviado", "Enviado"),
        ("cancelado", "Cancelado"),
    ]
    estado: Mapped[str] = mapped_column(
        ChoiceType(choices=ESTADOS),
        default="pendiente",
    )


# Uso
p = Pedido(nombre="Test", estado="pagado")
print(p.estado.code)  # "pagado"
print(p.estado.value)  # "Pagado"
```

[Volver al ejercicio ↑](../capitulos/24-sqlalchemy-utils.md#%C2%B1-ejercicio-242)

---

## Ejercicio 24.3

**UUIDType**

```python
from sqlalchemy_utils import UUIDType
import uuid


class Token(Base):
    __tablename__ = "tokens"

    id: Mapped[str] = mapped_column(
        UUIDType(binary=False),
        primary_key=True,
        default=uuid.uuid4,
    )
    valor: Mapped[str]

    def __repr__(self):
        return f"Token(id={self.id!r}, valor={self.valor!r})"


t = Token(valor="abc123")
print(t.id)
# -> UUID('3f2504e0-4f89-11d3-9a0c-0305e82c3301')
```

[Volver al ejercicio ↑](../capitulos/24-sqlalchemy-utils.md#%C2%B1-ejercicio-243)

---

## Ejercicio 24.4

**PasswordType**

```python
from sqlalchemy_utils import PasswordType


class Usuario(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    password: Mapped[str] = mapped_column(
        PasswordType(schemes=["pbkdf2_sha512"], max_length=255)
    )


# 1. Crear
with Session(engine) as session:
    u = Usuario(nombre="Ana", password="secreto123")
    session.add(u)
    session.commit()

# 2. Verificar
u = session.get(Usuario, 1)
print(f"Hash guardado: {u.password[:30]}...")
# -> pbkdf2_sha512$200000$...

# 3. Check
print(u.check_password("secreto123"))  # True
print(u.check_password("otro"))        # False
```

[Volver al ejercicio ↑](../capitulos/24-sqlalchemy-utils.md#%C2%B1-ejercicio-244)

---

## Ejercicio 24.5

**EncryptedType en producción**

```python
import os
from sqlalchemy_utils import EncryptedType


class Usuario(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    telefono: Mapped[str] = mapped_column(
        EncryptedType(String, key=os.environ["DB_ENCRYPTION_KEY"])
    )
    dni: Mapped[str] = mapped_column(
        EncryptedType(String, key=os.environ["DB_ENCRYPTION_KEY"])
    )
```

**1. ¿Dónde está la clave?** En variable de entorno `DB_ENCRYPTION_KEY`. Es la forma segura, pero **crítica**: perderla = perder todos los datos cifrados.

**2. ¿Cómo rotar la clave sin perder datos?**

Estrategia de **doble escritura**:

```python
# 1. Leer todos los registros con la clave vieja
old_key = "clave_vieja"
old_encrypted = connection.execute(text("SELECT id, telefono FROM usuarios")).fetchall()

# 2. Descifrar manualmente con la clave vieja
# 3. Cifrar con la nueva clave y actualizar
new_key = "clave_nueva"
for row in old_encrypted:
    decrypted = decrypt_with_key(row.telefono, old_key)
    re_encrypted = encrypt_with_key(decrypted, new_key)
    connection.execute(
        update(Usuario)
        .where(Usuario.id == row.id)
        .values(telefono=re_encrypted)
    )
```

**3. ¿Backups?** Sí, pero los datos cifrados **no se pueden descifrar** sin la clave. Guardá backups separados de las claves (en un vault: AWS KMS, HashiCorp Vault, etc.).

[Volver al ejercicio ↑](../capitulos/24-sqlalchemy-utils.md#%F0%9F%94%B4-ejercicio-245)