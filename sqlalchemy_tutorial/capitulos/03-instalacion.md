# Capítulo 3: Instalación y entorno

> Cinco minutos para tener todo funcionando. Después de esto, vamos a escribir código real.

---

## 3.1 Lo mínimo necesario

```bash
# 1. Creamos un entorno virtual (buenas prácticas)
python -m venv venv
source venv/bin/activate          # Linux/macOS
# .\venv\Scripts\activate        # Windows (PowerShell)

# 2. Instalamos SQLAlchemy 2.0+
pip install "sqlalchemy>=2.0"

# 3. Para FastAPI (lo veremos en el capítulo 17)
pip install "fastapi[standard]"

# Si solo querés FastAPI + Pydantic minimalista:
# pip install fastapi pydantic

# 4. Driver de base de datos (opcional, depende de cuál usemos)
# Para SQLite: ya viene incluido
# Para PostgreSQL:
pip install psycopg2-binary
# Para MySQL:
pip install pymysql
```

> 💡 `fastapi[standard]` incluye el servidor `uvicorn`, validación, generación de schemas OpenAPI y más.

---

## 3.2 Verificá que todo está bien

```python
import sqlalchemy
print(sqlalchemy.__version__)
# Debe imprimir algo como '2.0.x' o superior
```

Si te muestra `2.0.0` o más, estás listo para escribir código moderno.

---

## 3.3 Estructura de carpetas recomendada

```
mi_proyecto/
├── venv/                    # entorno virtual
├── src/
│   ├── __init__.py
│   ├── database.py          # engine, Base, get_db
│   ├── models.py            # modelos ORM
│   ├── schemas.py           # schemas Pydantic
│   ├── routers/             # endpoints separados por recurso
│   │   ├── __init__.py
│   │   └── productos.py
│   └── main.py              # punto de entrada FastAPI
├── tests/
├── requirements.txt
└── README.md
```

> 🎓 **Consejo**: usar `src/` en vez de tirar todo en la raíz es una convención muy útil cuando tu proyecto crece.

---

## 3.4 ¿Qué base de datos uso?

Empezamos con **SQLite** porque **no requiere instalar nada extra** (vive dentro de Python). Cuando tu proyecto crezca, podés cambiar a PostgreSQL cambiando **una sola línea**: la URL de conexión.

| Base de datos | URL de conexión ejemplo |
|---|---|
| SQLite (en memoria) | `"sqlite:///:memory:"` |
| SQLite (archivo) | `"sqlite:///./mi_base.db"` |
| PostgreSQL | `"postgresql://user:pass@localhost:5432/db"` |
| MySQL | `"mysql+pymysql://user:pass@localhost:3306/db"` |
| SQL Server | `"mssql+pyodbc://user:pass@server/db"` |

### Ejemplo: crear un engine

```python
from sqlalchemy import create_engine

# SQLite en memoria (se pierde al cerrar el programa)
engine = create_engine("sqlite:///:memory:", echo=True)

# SQLite en archivo (persistente)
engine = create_engine("sqlite:///./tienda.db", echo=True)

# PostgreSQL
engine = create_engine("postgresql://mi_user:mi_pass@localhost:5432/mi_db", echo=False)
```

> 🎓 **Consejo del profesor**: empezá siempre con SQLite para aprender. Después migrá a PostgreSQL cuando tengas datos reales. La **misma** clase funciona en ambas bases. Esa es la magia de SQLAlchemy.

---

## 3.5 Configuración recomendada para desarrollo

Vamos a crear un archivo `src/database.py` que reutilizaremos en los próximos capítulos:

```python
# src/database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

DATABASE_URL = "sqlite:///./tienda.db"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    echo=True,       # True en dev, False en producción
)

# Esta clase Base heredará cualquier modelo
class Base(DeclarativeBase):
    pass

# Lo usaremos para inyectar sesiones en FastAPI
def get_db():
    with Session(engine) as session:
        yield session
```

- `check_same_thread=False` es **obligatorio** si vas a usar SQLite + FastAPI (porque las peticiones pueden ejecutarse en hilos distintos).
- `echo=True` imprime el SQL en consola. Perfecto para aprender, **apagalo en producción**.

> 💡 En el [capítulo 4](./04-engine-session.md) vamos a entender por qué `get_db()` con `yield` es el patrón correcto.

---

## 3.6 Probando todo en un solo archivo

Para verificar de un tirón que todo funciona, copiá esto en `test.py` y ejecutalo:

```python
from sqlalchemy import create_engine, text
from sqlalchemy.orm import DeclarativeBase, Session

engine = create_engine("sqlite:///:memory:", echo=True)

# Probamos conexión
with engine.connect() as conn:
    resultado = conn.execute(text("SELECT 'Hola SQLAlchemy' as msg"))
    print(resultado.one())
    # -> ('Hola SQLAlchemy',)
```

**Output esperado** (con `echo=True`):

```
2026-01-XX HH:MM:SS info sqlalchemy.engine.Engine SELECT 'Hola SQLAlchemy' as msg
2026-01-XX HH:MM:SS info sqlalchemy.engine.Engine ()
Hola SQLAlchemy
```

Si ves la respuesta, todo está funcionando. 🎉

---

## 3.7 Errores frecuentes en la instalación

| Error | Causa | Solución |
|---|---|---|
| `ModuleNotFoundError: No module named 'sqlalchemy'` | No está instalado | `pip install "sqlalchemy>=2.0"` |
| `sqlite3.OperationalError: unable to open database file` | Ruta mal escrita | Usá ruta absoluta o `./mi_base.db` |
| `ImportError: No module named 'psycopg2'` | Falta el driver | `pip install psycopg2-binary` |
| `AttributeError: 'NoneType' object has no attribute ...` | Algún campo `Optional` se quedó sin manejar | Revisa las anotaciones |

---

## 🛠️ Ejercicios prácticos

### 🟢 Ejercicio 3.1: Setup completo

Configurá tu entorno desde cero:

1. Creá un entorno virtual llamado `mi_entorno`.
2. Activá el entorno.
3. Instalá SQLAlchemy 2.0.
4. Verificá que la versión instalada sea >= 2.0.
5. Copiá el script de prueba del [capítulo 3.6](#36-probando-todo-en-un-solo-archivo) y ejecutalo.

**Solución**: [soluciones/03-instalacion.md](../soluciones/03-instalacion.md#ejercicio-31)

---

### 🟢 Ejercicio 3.2: URL de base de datos

Escribí en tu libreta o en un comentario de código la URL de conexión correcta para cada caso:

1. SQLite en memoria.
2. SQLite en el archivo `biblioteca.db`.
3. PostgreSQL en el host `db.local`, usuario `app`, contraseña `secreta123`, base `biblioteca`.
4. MySQL en el host `mysql.servidor.com`, usuario `app`, contraseña `xyz`, base `biblioteca`.

**Solución**: [soluciones/03-instalacion.md](../soluciones/03-instalacion.md#ejercicio-32)

---

### 🟡 Ejercicio 3.3: Estructura de carpetas

Creá la estructura del manual en tu máquina:

```bash
mi_proyecto/
├── venv/
├── src/
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   ├── routers/
│   │   └── __init__.py
│   └── main.py
```

1. Asegurate de que cada `__init__.py` esté vacío (o casi).
2. Verificá que Python reconoce el paquete `src`.

**Solución**: [soluciones/03-instalacion.md](../soluciones/03-instalacion.md#ejercicio-33)

---

### 🟡 Ejercicio 3.4: Probá drivers

1. Instalá `psycopg2-binary`.
2. **Sin** conectar a una DB real, escribí un script que intente crear el engine. ¿Qué pasa?
3. ¿Cómo verificarías que el driver está bien instalado **sin** una DB real?

**Solución**: [soluciones/03-instalacion.md](../soluciones/03-instalacion.md#ejercicio-34)

---

## 🎓 Lo que aprendiste

- Instalamos SQLAlchemy 2.0 y verificamos la versión.
- Aprendimos la estructura de carpetas recomendada.
- Conocemos las URLs comunes para distintas bases de datos.
- Creamos nuestro primer `engine` y verificamos que conecta.

## 📖 Siguiente

[Capítulo 4: Engine y Session →](./04-engine-session.md)
