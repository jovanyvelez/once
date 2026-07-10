# Soluciones — Capítulo 15: Eventos SQLAlchemy

[Volver al capítulo 15](../capitulos/15-eventos.md)

---

## Ejercicio 15.1

**`@validates` simple**

```python
from sqlalchemy.orm import validates


class Usuario(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str]

    @validates("email")
    @classmethod
    def validar_email(cls, v: str) -> str:
        if not v or "@" not in v:
            raise ValueError(f"Email inválido: {v}")
        return v.strip().lower()


# Test
u = Usuario(email="  Ana@Ejemplo.COM  ")
print(u.email)  # "ana@ejemplo.com"
```

[Volver al ejercicio ↑](../capitulos/15-eventos.md#%C2%B0-ejercicio-151)

---

## Ejercicio 15.2

**`@model_validator`**

```python
from pydantic import BaseModel  # no, usa SQLAlchemy
from sqlalchemy.orm import validates, model_validator


class Transferencia(Base):
    __tablename__ = "transferencias"
    id: Mapped[int] = mapped_column(primary_key=True)
    origen_id: Mapped[int]
    destino_id: Mapped[int]
    monto: Mapped[float]

    @validates("monto")
    @classmethod
    def validar_monto(cls, v):
        if v <= 0:
            raise ValueError("monto debe ser positivo")
        return v

    @model_validator(mode="after")
    def validar_cuentas(self):
        if self.origen_id == self.destino_id:
            raise ValueError("origen y destino deben ser distintos")
        return self


# Test
t = Transferencia(origen_id=1, destino_id=1, monto=100)
# -> ValueError: origen y destino deben ser distintos
```

[Volver al ejercicio ↑](../capitulos/15-eventos.md#%C2%B0-ejercicio-152)

---

## Ejercicio 15.3

**Log de creación**

```python
from sqlalchemy import event


@event.listens_for(Producto, "before_insert")
def log_crear(mapper, connection, target):
    print(f"Producto a crear: {target.nombre}, precio={target.precio}")


# Test
with Session(engine) as session:
    p = Producto(nombre="Test", sku="TST-1", precio=100)
    session.add(p)
    session.commit()
    # -> Producto a crear: Test, precio=100
```

[Volver al ejercicio ↑](../capitulos/15-eventos.md#%C2%B1-ejercicio-153)

---

## Ejercicio 15.4

**Auditoría completa**

```python
from datetime import datetime
from sqlalchemy import JSON, DateTime


class AuditLog(Base):
    __tablename__ = "audit_logs"
    id: Mapped[int] = mapped_column(primary_key=True)
    tabla: Mapped[str]
    operacion: Mapped[str]
    pk_cambiada: Mapped[str]
    datos: Mapped[dict] = mapped_column(JSON)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


def registrar(target, op):
    session = object_session(target)
    if session:
        session.add(AuditLog(
            tabla=target.__tablename__,
            operacion=op,
            pk_cambiada=str(target.id),
            datos={c.name: getattr(target, c.name) for c in target.__table__.columns},
        ))


@event.listens_for(Producto, "after_insert")
def auditar_insert(mapper, connection, target):
    registrar(target, "INSERT")


@event.listens_for(Producto, "after_update")
def auditar_update(mapper, connection, target):
    registrar(target, "UPDATE")


@event.listens_for(Producto, "after_delete")
def auditar_delete(mapper, connection, target):
    registrar(target, "DELETE")
```

[Volver al ejercicio ↑](../capitulos/15-eventos.md#%C2%B1-ejercicio-154)

---

## Ejercicio 15.5

**Engine event**

```python
@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()
```

[Volver al ejercicio ↑](../capitulos/15-eventos.md#%C2%B1-ejercicio-155)

---

## Ejercicio 15.6

**Soft delete con evento**

```python
from datetime import datetime
from sqlalchemy import event


@event.listens_for(Producto, "before_delete")
def soft_delete_producto(mapper, connection, target):
    """Convierte el DELETE físico en un UPDATE."""
    connection.execute(
        Producto.__table__.update()
        .where(Producto.id == target.id)
        .values(eliminado_en=datetime.utcnow())
    )
```

> ⚠️ **Limitación**: esto emite el UPDATE antes que el DELETE. Si el objeto tiene relaciones con `cascade="all, delete-orphan"`, pueden quedar inconsistencias. Para producción, mejor usar Session custom o un evento `before_flush`.

[Volver al ejercicio ↑](../capitulos/15-eventos.md#%F0%9F%94%B4-ejercicio-156)