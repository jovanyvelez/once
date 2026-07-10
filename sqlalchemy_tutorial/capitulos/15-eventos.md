# Capítulo 15: Eventos SQLAlchemy — hooks para auditoría, validación, timestamps

> Automatizá tareas repetitivas: timestamps, validaciones, soft-delete, notificaciones.

---

## 15.1 ¿Qué son los eventos?

SQLAlchemy tiene un sistema de **eventos** que te permite ejecutar código cuando pasan cosas internas. Es como escuchar Webhooks pero dentro del ORM.

> 🎓 **Analogía**: pensá en una alarma de casa. Definís qué pasa cuando abren la puerta (evento) y qué acción tomar (handler). SQLAlchemy hace lo mismo: cuando un objeto se inserta, vos disparás una función.

### Tipos de eventos

| Evento | Cuándo dispara |
|---|---|
| `before_insert` | Antes de un `INSERT`. |
| `after_insert` | Después de un `INSERT`. |
| `before_update` | Antes de un `UPDATE`. |
| `after_update` | Después de un `UPDATE`. |
| `before_delete` | Antes de un `DELETE`. |
| `after_delete` | Después de un `DELETE`. |
| `before_flush` | Antes del flush general (cualquier cambio). |
| `after_commit` | Después de un commit exitoso. |
| `after_rollback` | Después de un rollback. |

---

## 15.2 Evento simple: timestamps automáticos

Si no querés usar `server_default` (que solo lo llena la base), podés usar un evento Python que se ejecute antes del INSERT/UPDATE.

```python
from datetime import datetime
from sqlalchemy import event
from sqlalchemy.orm import Session

@event.listens_for(Session, "before_flush")
def actualizar_timestamps(session, flush_context, instances):
    """Set creado_en en INSERT y actualizado_en en UPDATE."""
    for obj in session.new:           # objetos por insertar
        if hasattr(obj, "creado_en") and not obj.creado_en:
            obj.creado_en = datetime.utcnow()
        if hasattr(obj, "actualizado_en"):
            obj.actualizado_en = datetime.utcnow()

    for obj in session.dirty:         # objetos por actualizar
        if hasattr(obj, "actualizado_en"):
            obj.actualizado_en = datetime.utcnow()
```

> ⚠️ Cuidado: usar `datetime.utcnow()` es **deprecado en Python 3.12+**. En su lugar:
>
> ```python
> from datetime import datetime, timezone
> obj.creado_en = datetime.now(timezone.utc)
> ```

> 🎓 **Alternativa**: en lugar de eventos, usá `server_default=func.now()` y `onupdate=func.now()` (lo vimos en el cap. 6). Es más performante y se hace a nivel de base.

---

## 15.3 Evento de validación: normalizar emails antes de guardar

```python
import re
from sqlalchemy import event

@event.listens_for(Usuario, "before_insert")
@event.listens_for(Usuario, "before_update")
def normalizar_email(mapper, connection, target):
    """Normaliza el email antes de guardar: trim y lowercase."""
    if target.email:
        target.email = target.email.strip().lower()


@event.listens_for(Usuario, "before_insert")
def validar_email(mapper, connection, target):
    """Verifica formato básico de email."""
    if target.email:
        patron = r"^[\w\.-]+@[\w\.-]+\.\w+$"
        if not re.match(patron, target.email):
            raise ValueError(f"Email inválido: {target.email}")
```

> 💡 **Consejo**: si la validación es crítica, hacela también a nivel de DB (CHECK constraint o trigger).

---

## 15.4 Evento para auditoría completa (quién, cuándo, qué)

Imaginá que necesitás registrar **cada cambio** a una tabla:

```python
from datetime import datetime
from sqlalchemy import event, Column, Integer, String, DateTime, JSON

class AuditLog(Base):
    """Registro de auditoría."""
    __tablename__ = "audit_logs"

    id: Mapped[int] = mapped_column(primary_key=True)
    tabla: Mapped[str] = mapped_column(String(50))
    operacion: Mapped[str] = mapped_column(String(10))  # INSERT, UPDATE, DELETE
    pk_cambiada: Mapped[str] = mapped_column(String(50))
    datos_anteriores: Mapped[Optional[dict]] = mapped_column(JSON)
    datos_nuevos: Mapped[Optional[dict]] = mapped_column(JSON)
    usuario: Mapped[Optional[str]] = mapped_column(String(100), default=None)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


def registrar_cambio(
    target, operation, valores_anteriores=None, usuario=None
):
    """Inserta un registro de auditoría."""
    from sqlalchemy.orm import object_session

    session = object_session(target)
    if not session:
        return

    pk = getattr(target, "id", None)
    pk_str = str(pk) if pk else "sin-id"

    audit = AuditLog(
        tabla=target.__tablename__,
        operacion=operation,
        pk_cambiada=pk_str,
        datos_anteriores=valores_anteriores,
        datos_nuevos={
            c.name: getattr(target, c.name)
            for c in target.__table__.columns
        },
        usuario=usuario,
    )
    session.add(audit)


@event.listens_for(Producto, "before_update")
def auditar_update(mapper, connection, target):
    """Captura los valores anteriores ANTES de aplicar cambios."""
    from sqlalchemy.orm.attributes import get_committed_state

    estado_anterior = get_committed_state(target)
    target._audit_anterior = {
        c.name: getattr(estado_anterior, c.name, None)
        for c in target.__table__.columns
    }


@event.listens_for(Producto, "after_update")
def registrar_update(mapper, connection, target):
    """Genera el log de auditoría para UPDATE."""
    registrar_cambio(target, "UPDATE", valores_anteriores=target._audit_anterior)


@event.listens_for(Producto, "after_insert")
def registrar_insert(mapper, connection, target):
    """Genera el log de auditoría para INSERT."""
    registrar_cambio(target, "INSERT")


@event.listens_for(Producto, "after_delete")
def registrar_delete(mapper, connection, target):
    """Genera el log de auditoría para DELETE."""
    registrar_cambio(target, "DELETE")
```

### Consultando el log

```python
with Session(engine) as session:
    cambios = session.scalars(
        select(AuditLog)
        .where(AuditLog.tabla == "productos")
        .order_by(AuditLog.timestamp.desc())
    )
    for c in cambios:
        print(f"{c.timestamp}: {c.operacion} en {c.tabla} ({c.pk_cambiada})")
```

---

## 15.5 Validaciones con `validates` (decorador moderno)

Para validaciones simples, SQLAlchemy 2.0 ofrece `@validates`:

```python
from sqlalchemy.orm import validates

class Producto(Base):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    precio: Mapped[float]
    sku: Mapped[str]

    @validates("precio")
    def validar_precio(self, key, value):
        if value < 0:
            raise ValueError("El precio no puede ser negativo")
        return value

    @validates("sku")
    def validar_sku(self, key, value):
        if not value or not value.strip():
            raise ValueError("El SKU no puede estar vacío")
        return value.strip().upper()

    @validates("nombre")
    def validar_nombre(self, key, value):
        if not value or len(value) < 3:
            raise ValueError("El nombre debe tener al menos 3 caracteres")
        return value.strip().title()
```

```python
with Session(engine) as session:
    # Pasa validación
    p1 = Producto(nombre="Cafetera", sku="cf-001", precio=100)
    session.add(p1)
    # SKU se guardó como "CF-001" (mayúsculas)

    # Falla validación
    try:
        p2 = Producto(nombre="X", sku="x", precio=100)
        session.add(p2)
        session.commit()  # 💥 ValueError
    except ValueError as e:
        session.rollback()
        print(f"Error: {e}")
```

> 🎓 **Cuándo usar `@validates` vs evento**: `@validates` es para validaciones **de campo**. Eventos son para **acciones complejas** (logs, envíos de email, etc.).

---

## 15.6 Eventos sobre la `Engine`

También podés reaccionar a eventos del motor de base:

```python
from sqlalchemy import event

@event.listens_for(engine, "connect")
def set_sqlite_pragma(dbapi_connection, connection_record):
    """Activa foreign keys en SQLite."""
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()


@event.listens_for(engine, "checkout")
def verificar_conexion(dbapi_connection, connection_record, connection_proxy):
    """Hook al sacar una conexión del pool."""
    print("Conexión sacada del pool")


@event.listens_for(engine, "checkin")
def devolver_conexion(dbapi_connection, connection_record):
    """Hook al devolver una conexión al pool."""
    print("Conexión devuelta al pool")
```

---

## 15.7 Eventos personalizados para soft delete

En lugar de borrar, marcá como eliminado:

```python
@event.listens_for(Producto, "before_delete")
def soft_delete(mapper, connection, target):
    """Convierte el DELETE en un UPDATE."""
    connection.execute(
        update(Producto)
        .where(Producto.id == target.id)
        .values(eliminado=True, eliminado_en=datetime.utcnow())
    )
    # Evita el DELETE real
    return mapper.dispatch.before_delete.__class__(target)  # workaround


# Más limpio: redefinir el comportamiento vía Session
from sqlalchemy.orm import Session

class SesionConSoftDelete(Session):
    """Session que nunca hace DELETE físico."""

    def delete(self, obj):
        if hasattr(obj, "eliminado"):
            self.query(type(obj)).filter_by(id=obj.id).update(
                {type(obj).eliminado: True}
            )
        else:
            super().delete(obj)
```

---

## 15.8 Orden de ejecución de eventos

Importante saber el orden cuando hay varios eventos:

1. `before_flush` (uno por Session)
2. `before_insert` / `before_update` / `before_delete` (uno por mapper)
3. SQL emitido a la base.
4. `after_insert` / `after_update` / `after_delete` (uno por mapper)
5. `after_flush` (uno por Session)
6. `after_commit` (uno por Session, solo si commit exitoso)

> 🎓 **Regla**: si necesitás detener una operación, usá `before_*`. Si querés reaccionar **después** de que la base ya hizo su parte, usá `after_*`.

---

## 15.9 ¿Eventos o lógica manual?

| Caso | Mejor opción |
|---|---|
| Llenar `creado_en` | `server_default=func.now()` (en DB) |
| Validar un campo | `@validates` |
| Auditar cambios | Evento `after_*` |
| Soft delete | Evento `before_delete` + override |
| Sincronizar datos externos | Evento `after_commit` |
| Enviar email de bienvenida | Evento `after_commit` |

> 💡 **Regla del profesor**: preferí siempre **declarativo** (`server_default`, `@validates`) antes que eventos. Los eventos son la última capa de extensibilidad, no la primera opción.

---

## 🛠️ Ejercicios prácticos

### 🟢 Ejercicio 15.1: `@validates` simple

Creá un modelo `Usuario` con un `@validates("email")` que normalice el email (trim + lowercase).

**Solución**: [soluciones/15-eventos.md](../soluciones/15-eventos.md#ejercicio-151)

---

### 🟢 Ejercicio 15.2: `@model_validator`

Creá un modelo `Transferencia(origen_id, destino_id, monto)`. Validá que `monto > 0` y que `origen_id != destino_id`.

**Solución**: [soluciones/15-eventos.md](../soluciones/15-eventos.md#ejercicio-152)

---

### 🟡 Ejercicio 15.3: Log de creación

Implementá un evento `before_insert` para `Producto` que imprima en consola: `"Producto a crear: {nombre}, precio={precio}"`.

**Solución**: [soluciones/15-eventos.md](../soluciones/15-eventos.md#ejercicio-153)

---

### 🟡 Ejercicio 15.4: Auditoría completa

Replicá el patrón del capítulo 15.4 (AuditLog). Cada INSERT/UPDATE/DELETE en `Producto` debe quedar registrado en una tabla `AuditLog`. Probá creando, actualizando y borrando un producto, y verificá que la tabla tenga 3 entradas.

**Solución**: [soluciones/15-eventos.md](../soluciones/15-eventos.md#ejercicio-154)

---

### 🟡 Ejercicio 15.5: Engine event

Implementá un evento `engine.connect` que configure `PRAGMA foreign_keys=ON` cuando se conecte a SQLite.

**Solución**: [soluciones/15-eventos.md](../soluciones/15-eventos.md#ejercicio-155)

---

### 🔴 Ejercicio 15.6: Soft delete con evento

Implementá un sistema de soft-delete completo:

- Cada modelo tiene un campo `eliminado_en: datetime | None`.
- Al llamar `session.delete(obj)`, en vez de borrar físicamente, setea `eliminado_en = now()`.
- Probalo creando y "borrando" un objeto, y verificá que sigue en la DB.

**Solución**: [soluciones/15-eventos.md](../soluciones/15-eventos.md#ejercicio-156)

---

## 🎓 Lo que aprendiste

- Eventos te permiten **engancharte** al ciclo de vida de un objeto ORM.
- `@validates` valida campos en `before_insert/update`.
- Eventos `before_*` permiten **modificar valores antes** de emitir SQL.
- Eventos `after_*` son para **reacciones** post-cambio.
- Preferí lo declarativo (`server_default`) cuando es posible.

## 📖 Siguiente

[Capítulo 16: AsyncSession →](./16-async-session.md)