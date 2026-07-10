# Capítulo 10: Crear las tablas (DDL)

> Cómo llevar tus clases Python a tablas reales en la base de datos.

---

## 10.1 ¿Qué es DDL?

**DDL** = *Data Definition Language*. Son las instrucciones SQL que **definen la estructura** de la base: `CREATE TABLE`, `DROP TABLE`, `ALTER TABLE`, etc.

En SQLAlchemy 2.0, una sola línea de Python se encarga de generar y ejecutar todo eso:

```python
Base.metadata.create_all(engine)
```

---

## 10.2 Uso básico

```python
from src.database import engine, Base
import src.models  # importante: importar los modelos para que se registren en Base

Base.metadata.create_all(engine)
```

> ⚠️ **Trampa frecuente**: si no importás los modelos antes, SQLAlchemy no sabe que existen y no genera ninguna tabla. La forma más limpia es importarlos en un `src/models/__init__.py`.

### Cómo organizar las imports

```python
# src/models/__init__.py
from src.models.categoria import Categoria
from src.models.producto import Producto
from src.models.inventario import Inventario

# al importarlos, SQLAlchemy los registra en Base.metadata
```

Luego en tu script principal:

```python
import src.models   # 👈 esto activa todos los registros
Base.metadata.create_all(engine)
```

---

## 10.3 ¿Qué hace `create_all` exactamente?

- Lee **todos los modelos** registrados en `Base.metadata`.
- Emite las sentencias `CREATE TABLE` necesarias.
- Emite los `CREATE INDEX` para cada columna con `index=True`.
- **No borra** ni **sobrescribe** tablas existentes.
- **No agrega columnas** nuevas a una tabla existente.

```python
Base.metadata.create_all(engine)
# Equivalente a:
# CREATE TABLE IF NOT EXISTS productos (...);
# CREATE TABLE IF NOT EXISTS categorias (...);
```

> 💡 En SQLite, `IF NOT EXISTS` es lo que se usa. Si la tabla ya está, no hace nada.

---

## 10.4 Opciones: el parámetro `checkfirst`

```python
Base.metadata.create_all(engine, checkfirst=True)  # default
```

`checkfirst=True` (default): antes de crear, verifica si ya existe. Si ya existe, no hace nada.

```python
Base.metadata.create_all(engine, checkfirst=False)
```

`checkfirst=False`: si la tabla existe, intenta crearla igual y la base tira error.

> 🎓 **Consejo**: dejá siempre `checkfirst=True` (default) en producción. En testing podés usar `drop_all` + `create_all`.

---

## 10.5 Borrar todo (útil en tests)

```python
# ¡CUIDADO! Borra todas las tablas definidas en Base.metadata.
Base.metadata.drop_all(engine)
```

Esto genera `DROP TABLE IF EXISTS productos` para cada tabla registrada.

### Patrón clásico para tests

```python
@pytest.fixture(scope="function")
def session(engine):
    Base.metadata.drop_all(engine)        # clean start
    Base.metadata.create_all(engine)
    with Session(engine) as session:
        yield session
        session.rollback()                # rollback por si las moscas
```

---

## 10.6 Ver las tablas que se crearán

Antes de ejecutar `create_all`, podés inspeccionar las tablas que se van a generar:

```python
for tabla in Base.metadata.sorted_tables:
    print(tabla)
    print(f"  Columnas: {[c.name for c in tabla.columns]}")
```

---

## 10.7 ⚠️ Cuándo NO usar `create_all`

En producción, **NO** uses `create_all`:

| Escenario | `create_all` | Migraciones (Alembic) |
|---|---|---|
| **Desarrollo local** | ✅ Perfecto | Sobra |
| **Testing** | ✅ Perfecto | Sobra |
| **Producción** | ❌ Peligroso | ✅ Obligatorio |

### ¿Por qué no en producción?

Imaginá que tu app tiene 3 tablas en producción y agregás una columna nueva a `Producto`. `create_all` no la va a crear (no modifica tablas existentes). Tu app va a explotar.

**Alembic** (lo vemos en el [capítulo 21](./21-recursos.md)) resuelve esto: detecta cambios en los modelos y genera migraciones incrementales sin perder datos.

---

## 10.8 Uso típico en una app real

```python
# src/main.py
from src.database import engine, Base
import src.models  # registra los modelos

def inicializar_base():
    """Crea las tablas si no existen. Llamar al arrancar la app."""
    Base.metadata.create_all(engine)

if __name__ == "__main__":
    inicializar_base()
    print("✅ Base de datos inicializada")
```

### Versión FastAPI con evento de inicio

```python
from fastapi import FastAPI

app = FastAPI()


@app.on_event("startup")
def startup_event():
    Base.metadata.create_all(engine)
```

> 🎓 **Consejo del profesor**: en apps de desarrollo se puede usar el evento `startup`. En producción, ejecutá migraciones con Alembic en el pipeline de deploy.

---

## 10.9 Inspección de SQL emitido

Si `echo=True` en el engine, vas a ver todo el SQL:

```python
engine = create_engine("sqlite:///./tienda.db", echo=True)

Base.metadata.create_all(engine)
```

**Output (resumido)**:

```
2026-01-XX 12:00:00 sqlalchemy.engine.Engine CREATE TABLE categorias (
    id INTEGER NOT NULL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL UNIQUE,
    descripcion VARCHAR,
    creado_en DATETIME DEFAULT CURRENT_TIMESTAMP
)
2026-01-XX 12:00:00 sqlalchemy.engine.Engine []
2026-01-XX 12:00:00 sqlalchemy.engine.Engine COMMIT
2026-01-XX 12:00:00 sqlalchemy.engine.Engine CREATE TABLE productos (...)
2026-01-XX 12:00:00 sqlalchemy.engine.Engine COMMIT
...
```

Perfecto para entender qué pasa "bajo el capó". En producción, desactivá `echo`.

---

## 🛠️ Ejercicios prácticos

### 🟢 Ejercicio 10.1: `echo=True` vs `echo=False`

Creá un script que compare las salidas de `create_all(engine)` con `echo=True` y `echo=False`. ¿Qué cambia?

**Solución**: [soluciones/10-crear-tablas.md](../soluciones/10-crear-tablas.md#ejercicio-101)

---

### 🟡 Ejercicio 10.2: Inspección de tablas

Antes de ejecutar `create_all`, listá todas las tablas que **se van a crear**. Ayudita: `Base.metadata.sorted_tables`.

**Solución**: [soluciones/10-crear-tablas.md](../soluciones/10-crear-tablas.md#ejercicio-102)

---

### 🟡 Ejercicio 10.3: Patrón de tests

Creá un `pytest fixture` llamado `db_session` que:

1. Cree un engine en memoria (`sqlite:///:memory:`).
2. Llame a `Base.metadata.drop_all(engine)`.
3. Llame a `Base.metadata.create_all(engine)`.
4. Devuelva una `Session`.
5. Después del test, cierre la sesión.

**Solución**: [soluciones/10-crear-tablas.md](../soluciones/10-crear-tablas.md#ejercicio-103)

---

### 🟡 Ejercicio 10.4: `checkfirst`

Demostrá con un script qué pasa cuando llamás a `create_all(engine)` dos veces seguidas. ¿Crea las tablas otra vez? ¿Qué pasa con `checkfirst=False`?

**Solución**: [soluciones/10-crear-tablas.md](../soluciones/10-crear-tablas.md#ejercicio-104)

---

### 🔴 Ejercicio 10.5: Schema versionado

Sin usar Alembic, implementá un sistema súper simple de "schema versionado":

1. Una tabla `schema_version(id, version)` en la DB.
2. Al iniciar la app, chequeá la versión actual.
3. Si el modelo tiene una nueva columna, agregala manualmente (con SQL crudo).

Esto es **NO** la forma profesional (usá Alembic en producción), pero el ejercicio es entender qué pasa "bajo el capó".

**Solución**: [soluciones/10-crear-tablas.md](../soluciones/10-crear-tablas.md#ejercicio-105)

---

## 🎓 Lo que aprendiste

- `Base.metadata.create_all(engine)` genera el SQL `CREATE TABLE`.
- Es importante **importar los modelos** antes (para que se registren).
- No modifica tablas existentes. Solo crea las que faltan.
- En producción, usá **Alembic** en su lugar.
- `drop_all` es ideal para testing (reset de DB).

## 📖 Siguiente

[Capítulo 11: CRUD — Crear, Leer, Actualizar, Borrar →](./11-crud.md)