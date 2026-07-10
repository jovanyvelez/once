# Capítulo 19: Errores comunes y cómo solucionarlos

> Los problemas que **todos** enfrentamos al empezar. Acá están las soluciones.

---

## 19.1 `MissingGreenlet` — accediste a una relación fuera de la sesión

```python
with Session(engine) as session:
    u = session.get(Usuario, 1)
    direcciones = u.direcciones   # ❌ dentro del with: OK
print(direcciones)               # ❌ fuera del with: EXPLOTA
```

**Error**:
```
sqlalchemy.exc.MissingGreenlet: greenlet not found
```

**Causa**: la relación se carga perezosamente, pero el `with` ya cerró la sesión.

**Solución**: accedé a las relaciones **dentro** del bloque `with`:

```python
with Session(engine) as session:
    u = session.get(Usuario, 1)
    direcciones = u.direcciones   # ✅ dentro del with
    print(direcciones)
```

**Alternativa**: cargá la relación explícitamente con `selectinload`:

```python
from sqlalchemy.orm import selectinload

stmt = select(Usuario).options(selectinload(Usuario.direcciones))
usuario = session.scalars(stmt).one()
# ya tenés las direcciones cargadas, incluso fuera del with
```

---

## 19.2 `DetachedInstanceError` — usar un objeto tras cerrar la sesión

```python
session = Session(engine)
usuario = session.get(Usuario, 1)
session.close()
print(usuario.direcciones)   # 💥 EXCEPCIÓN
```

**Error**:
```
sqlalchemy.orm.exc.DetachedInstanceError: Instance <Usuario ...> is not bound to a Session
```

**Causa**: cerraste la sesión, pero querés acceder a un atributo que dispara lazy load.

**Solución**: usá el objeto dentro del contexto:

```python
with Session(engine) as session:
    usuario = session.get(Usuario, 1)
    print(usuario.direcciones)   # ✅
```

---

## 19.3 `IntegrityError` al insertar duplicado

```python
session.add(Producto(sku="DUPLICADO", ...))
session.commit()
# sqlalchemy.exc.IntegrityError: UNIQUE constraint failed: productos.sku
```

**Causa**: el campo `sku` es único y ya existe.

**Solución**: capturá y rechazá:

```python
from sqlalchemy.exc import IntegrityError

try:
    session.add(Producto(sku="DUPLICADO", ...))
    session.commit()
except IntegrityError:
    session.rollback()
    raise HTTPException(400, "Ya existe un producto con ese SKU")
```

---

## 19.4 `PendingRollbackError` — olvidaste un rollback

```python
try:
    session.add(...)
    session.commit()
except Exception:
    raise HTTPException(...)  # sin rollback ❌
```

**Error**:
```
sqlalchemy.exc.PendingRollbackError: This Session's transaction has been rolled back due to a previous exception during flush.
```

**Causa**: cuando falla un flush, SQLAlchemy queda en estado pendiente. La próxima operación revienta.

**Solución**:

```python
try:
    session.add(...)
    session.commit()
except Exception:
    session.rollback()         # 👈 muy importante
    raise
```

---

## 19.5 Foreign Key mal escrita

```python
# ❌ Mal: tabla no existe / mal escrita
usuario_id: Mapped[int] = mapped_column(ForeignKey("Usuario.id"))

# ❌ Mal: columna no existe
producto_id: Mapped[int] = mapped_column(ForeignKey("productos.precio"))

# ✅ Bien
usuario_id: Mapped[int] = mapped_column(ForeignKey("usuarios.id"))
```

**Reglas para ForeignKey**:
- ✅ Nombre exacto de la tabla.
- ✅ Nombre exacto de la columna.
- ✅ Sin esquemas a menos que sean parte de `__table_args__`.

---

## 19.6 `argument of type 'NoneType' is not iterable`

```python
session.scalars(select(Usuario).where(Usuario.email == email))
```

**Causa**: `email` es `None` cuando el usuario no lo mandó.

**Solución**: validá antes:

```python
if not email:
    return []
stmt = select(Usuario).where(Usuario.email == email)
```

---

## 19.7 `NoResultFound` / `MultipleResultsFound`

```python
stmt = select(Usuario).where(Usuario.email == email)
session.scalars(stmt).one()  # 💥 si hay 0 o más de 1
```

**Solución**: usá `.first()` o `.one_or_none()`:

```python
stmt = select(Usuario).where(Usuario.email == email)
usuario = session.scalars(stmt).one_or_none()   # None si no hay, error si > 1
if not usuario:
    raise HTTPException(404)
```

---

## 19.8 `InvalidRequestError: Mapper 'mapped class ...' has no property 'X'`

```python
stmt = select(Producto).where(Producto.categoria_id == 1)
# Traceback: InvalidRequestError: ...
```

**Causa**: `Producto` no tiene `categoria_id` (quizás lo llamaste de otra forma).

**Solución**: revisá el nombre del atributo en el modelo. Recordá que `Mapped[T]` mapea el nombre del atributo al nombre de la columna.

---

## 19.9 Cambios no se persisten (no hiciste commit)

```python
session.add(...)
session.close()  # sin commit: se pierde todo
```

**Solución**: `commit()` antes del `close()`:

```python
session.add(...)
session.commit()   # 👈 indispensable
session.close()
```

O usá `with`, que **no** hace commit automáticamente. Debés hacerlo explícito.

---

## 19.10 Recursión infinita con relaciones circulares

```python
class A(Base):
    b: Mapped["B"] = relationship(back_populates="a")

class B(Base):
    a: Mapped["A"] = relationship(back_populates="b")
```

**Problema**: cuando serializás, A muestra a B que muestra a A que muestra a B... infinito.

**Solución**: en los schemas de Pydantic, **no anides infinitamente**:

```python
class BPublic(BaseModel):
    nombre: str
    model_config = ConfigDict(from_attributes=True)

class APublic(BaseModel):
    nombre: str
    b: Optional[BPublic] = None   # 👈 solo un nivel
    model_config = ConfigDict(from_attributes=True)
```

---

## 19.11 Driver no encontrado

```
ImportError: No module named 'psycopg2'
```

**Solución**: instalá el driver.

```bash
pip install psycopg2-binary
```

| DB | Driver | Comando |
|---|---|---|
| PostgreSQL | `psycopg2-binary` | `pip install psycopg2-binary` |
| MySQL | `pymysql` | `pip install pymysql` |
| SQLite | built-in | (ya viene) |

---

## 19.12 SQLite sin `check_same_thread=False`

**Error**: en FastAPI con SQLite, a veces hay errores raros de threading.

**Solución**:

```python
engine = create_engine(
    "sqlite:///./db.sqlite",
    connect_args={"check_same_thread": False},   # 👈 crucial para SQLite + FastAPI
)
```

---

## 19.13 Tabla no se crea

```python
Base.metadata.create_all(engine)
# no se crea la tabla de mi modelo nuevo
```

**Causa más común**: no importaste el modelo en el módulo donde llamás `create_all`.

**Solución**:

```python
# src/models/__init__.py
from src.models.producto import Producto
from src.models.categoria import Categoria

# src/main.py
import src.models   # 👈 esto registra los modelos
Base.metadata.create_all(engine)
```

---

## 19.14 `OperationalError: no such table` al usar `:memory:`

Causa: cada `engine = create_engine("sqlite:///:memory:")` crea una DB **separada**.

**Solución 1**: compartir el mismo engine:

```python
# Guardá el engine como singleton (módulo global)
engine = create_engine("sqlite:///:memory:")
```

**Solución 2**: usar archivo:

```python
engine = create_engine("sqlite:///./db.sqlite")
```

---

## 19.15 Mezclar sesiones en distintos request

```python
# En una dependencia
session1 = Session(engine)

# En el endpoint
session2 = Session(engine)
session1.add(...)
session2.commit()  # los cambios no se guardan
```

**Causa**: cada request debe tener **una sola sesión**.

**Solución**: usá `SessionDep` SIEMPRE:

```python
# En el endpoint
def endpoint(session: SessionDep):
    session.add(...)
    session.commit()
```

---

## 19.16 Resumen: checklist de debugging

Cuando algo falla, esta es la lista que tu cerebro debe seguir:

- [ ] ¿Importé los modelos?
- [ ] ¿Usé `with Session(engine) as session:`?
- [ ] ¿Hice `session.commit()` al final?
- [ ] ¿El ForeignKey apunta a una tabla que existe?
- [ ] ¿Los nombres de columnas coinciden?
- [ ] ¿El `select()` tiene el typo correcto?
- [ ] ¿La validación de Pydantic pasa?
- [ ] ¿Los roles están bien definidos en el schema?
- [ ] ¿Hice `session.refresh()` si necesito datos autogenerados?
- [ ] ¿Tengo el driver de la DB instalado?

---

## 🛠️ Ejercicios prácticos

### 🟢 Ejercicio 19.1: Detectá el bug

Este código tira `DetachedInstanceError`. Encontrá el problema y arreglalo:

```python
def procesar():
    with Session(engine) as session:
        u = session.get(Usuario, 1)
    print(u.direcciones)   # 💥 ERROR
```

**Solución**: [soluciones/19-errores-comunes.md](../soluciones/19-errores-comunes.md#ejercicio-191)

---

### 🟡 Ejercicio 19.2: `IntegrityError` en endpoint

Modificá un endpoint POST para que maneje `IntegrityError` con un rollback explícito y devuelva `HTTPException(400, "SKU duplicado")`.

**Solución**: [soluciones/19-errores-comunes.md](../soluciones/19-errores-comunes.md#ejercicio-192)

---

### 🟡 Ejercicio 19.3: Foreign Key mal escrita

El siguiente modelo NO crea la FK correctamente. ¿Por qué?

```python
class Comentario(Base):
    __tablename__ = "comentarios"
    id: Mapped[int] = mapped_column(primary_key=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("Post.id"))  # ❌
    texto: Mapped[str]
```

**Solución**: [soluciones/19-errores-comunes.md](../soluciones/19-errores-comunes.md#ejercicio-193)

---

### 🔴 Ejercicio 19.4: Depurá N+1 en producción

Te llega un reporte: "el endpoint `/api/reports/` tarda 30 segundos". Investigá con `echo=True` y corregí.

**Pista**: el problema es muy probablemente N+1.

**Solución**: [soluciones/19-errores-comunes.md](../soluciones/19-errores-comunes.md#ejercicio-194)

---

## 🎓 Lo que aprendiste

- Los errores más comunes son por **sesiones mal cerradas** y **commits olvidados**.
- `try/except + rollback()` es esencial al manejar errores.
- Las relaciones requieren importar correctamente los modelos.
- SQLite + FastAPI necesita `check_same_thread=False`.
- Hay un **checklist mental** que siempre podés revisar cuando algo falla.

## 📖 Siguiente

[Capítulo 20: Glosario rápido →](./20-glosario.md)