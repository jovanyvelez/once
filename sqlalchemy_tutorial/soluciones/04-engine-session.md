# Soluciones — Capítulo 4: Engine y Session

> Volvé al [capítulo 4](../capitulos/04-engine-session.md) si necesitás repasar la teoría.

---

## Ejercicio 4.1

**Tu primer engine**

```python
from sqlalchemy import create_engine, text

engine = create_engine("sqlite:///:memory:", echo=True)

with engine.connect() as conn:
    resultado = conn.execute(text("SELECT 1 + 1 AS suma"))
    print("El resultado es:", resultado.scalar())
    # -> El resultado es: 2
```

Con `echo=True`, vas a ver en consola algo como:
```
INFO sqlalchemy.engine.Engine SELECT 1 + 1 AS suma
INFO sqlalchemy.engine.Engine ()
INFO sqlalchemy.engine.Engine (2,)
El resultado es: 2
```

> 💡 `.scalar()` devuelve la primera columna de la primera fila, perfecto para `SELECT` que devuelven un único valor.

[Volver al ejercicio ↑](../capitulos/04-engine-session.md#%C2%B0-ejercicio-41)

---

## Ejercicio 4.2

**Pool de conexiones**

1. **Tres engines con la misma URL**: cada `create_engine()` crea un objeto Engine distinto. **No** comparten el pool. Esto es ineficiente: si abrís 3 engines con la misma URL, tenés 3 pools diferentes.

2. **¿Tiene sentido tener varios engines en FastAPI?** **No.** Un solo Engine por aplicación es la regla. Es thread-safe, mantiene el pool, y se reutiliza. Si necesitás conectar a **distintas DBs** (ej: principal + analytics), ahí sí podés tener 2 engines, uno por URL.

```python
# ✅ CORRECTO: un solo engine global
engine = create_engine("sqlite:///./app.db")

# ❌ INCORRECTO: un engine por request/función
def alguna_funcion():
    engine = create_engine("sqlite:///./app.db")  # 💥 desperdicia recursos
    ...
```

[Volver al ejercicio ↑](../capitulos/04-engine-session.md#%C2%B0-ejercicio-42)

---

## Ejercicio 4.3

**Detectá un bug**

```python
# ❌ Original: dos problemas
def agregar_usuario(nombre, email):
    session = Session(engine)
    usuario = Usuario(nombre=nombre, email=email)
    session.add(usuario)
    session.commit()
    session.close()
    return usuario.id
```

**Problemas**:

1. **No usa `with`**: si `commit()` lanza una excepción, `session.close()` no se llama → **conexión filtrada**.
2. **No maneja excepciones**: si falla, la sesión queda en estado raro.

**Versión corregida**:

```python
from sqlalchemy.orm import Session


def agregar_usuario(nombre, email):
    with Session(engine) as session:
        try:
            usuario = Usuario(nombre=nombre, email=email)
            session.add(usuario)
            session.commit()
            return usuario.id
        except Exception:
            session.rollback()
            raise
```

> ✅ El `with` cierra la sesión SIEMPRE. El `try/except/rollback` asegura que cualquier fallo deshaga la transacción.

[Volver al ejercicio ↑](../capitulos/04-engine-session.md#%C2%B1-ejercicio-43)

---

## Ejercicio 4.4

**Comparar `flush` vs `commit`**

```python
from datetime import datetime
from sqlalchemy import create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, Session


class Base(DeclarativeBase):
    pass


class Usuario(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]


engine = create_engine("sqlite:///:memory:", echo=True)
Base.metadata.create_all(engine)


# --- Sesión 1: insertar ---
with Session(engine) as session:
    u = Usuario(nombre="Ana")
    session.add(u)
    session.flush()
    print(f"Después de flush(): id={u.id}, nombre={u.nombre}")
    # ✅ El id YA está disponible, aunque no hicimos commit

    u.nombre = "Anabel"
    session.commit()
    print(f"Después de commit(): id={u.id}, nombre={u.nombre}")


# --- Sesión 2: verificar persistencia ---
with Session(engine) as session:
    resultado = session.scalars(select(Usuario)).all()
    print(f"\nEn la nueva sesión:")
    for r in resultado:
        print(f"  id={r.id}, nombre={r.nombre}")
    # -> id=1, nombre='Anabel'
```

**Lo que demuestra este script**:

| Acción | ¿SQL emitido? | ¿Datos persistidos? |
|---|---|---|
| `session.add()` | ❌ No todavía | ❌ No |
| `session.flush()` | ✅ Sí (`INSERT`) | 🟠 Parcialmente (sin commit) |
| `session.commit()` | ✅ Sí (`INSERT` + cierre tx) | ✅ Sí, permanente |

**Experimento extra**: comentá el `session.commit()` y ejecutá. Vas a ver que en la segunda sesión no hay datos (rollback automático).

[Volver al ejercicio ↑](../capitulos/04-engine-session.md#%C2%B1-ejercicio-44)

---

## Ejercicio 4.5

**Manejo de errores transaccionales**

```python
from sqlalchemy import select
from sqlalchemy.orm import Session


class Usuario(Base):
    __tablename__ = "usuarios"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    saldo: Mapped[float] = mapped_column(default=0.0)


def transferir_dinero(
    session: Session, origen_id: int, destino_id: int, monto: float
) -> bool:
    """
    Transfiere `monto` del usuario origen al destino.
    Retorna True si la transferencia fue exitosa, False si falló.
    """
    try:
        # Cargamos ambos usuarios
        origen = session.get(Usuario, origen_id)
        destino = session.get(Usuario, destino_id)

        if not origen or not destino:
            raise ValueError("Usuario origen o destino no existe")

        # Validamos saldo
        if origen.saldo < monto:
            return False

        # Hacemos las dos operaciones
        origen.saldo -= monto
        destino.saldo += monto

        # Confirmamos todo junto (atomicidad)
        session.commit()
        return True

    except Exception:
        # Si algo falla, revertimos todo
        session.rollback()
        return False


# --- Uso ---
engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)

with Session(engine) as session:
    ana = Usuario(nombre="Ana", saldo=1000)
    juan = Usuario(nombre="Juan", saldo=500)
    session.add_all([ana, juan])
    session.commit()

# Transferencia exitosa
with Session(engine) as session:
    exito = transferir_dinero(session, origen_id=ana.id, destino_id=juan.id, monto=200)
    print(f"Transferencia 200: {'✅' if exito else '❌'}")

# Transferencia fallida (saldo insuficiente)
with Session(engine) as session:
    exito = transferir_dinero(session, origen_id=juan.id, destino_id=ana.id, monto=99999)
    print(f"Transferencia 99999: {'✅' if exito else '❌'}")
```

**Aspectos clave**:

- ✅ `try/except` envuelve **ambas** operaciones.
- ✅ Si algo falla, `rollback()` revierte **todo** (incluyendo el saldo restado al origen).
- ✅ El saldo del origen NO se modifica parcialmente: o se restan los 200 y se suman los 200, o no se hace nada.

**Mejora opcional**: usar `SELECT ... FOR UPDATE` para evitar race conditions:

```python
stmt = select(Usuario).where(Usuario.id == origen_id).with_for_update()
origen = session.scalars(stmt).one()
```

Esto bloquea la fila hasta que termine la transacción, evitando que dos transferencias simultáneas causen saldo negativo.

[Volver al ejercicio ↑](../capitulos/04-engine-session.md#%F0%9F%94%B4-ejercicio-45)