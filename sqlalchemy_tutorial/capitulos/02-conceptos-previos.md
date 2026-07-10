# Capítulo 2: Conceptos previos

> Antes de escribir la primera línea de SQLAlchemy, asegurate de entender *qué* estás haciendo y *por qué*. Este capítulo es la pieza que falta antes de empezar.

---

## 2.1 ¿Qué es un ORM?

**ORM** significa *Object-Relational Mapping* (Mapeo Objeto-Relacional). Es una técnica que **relaciona** una clase de Python con una tabla de SQL.

| Mundo Python 🐍 | Mundo SQL 🗄️ |
|---|---|
| Clase | Tabla |
| Atributo de clase | Columna |
| Instancia (`usuario = User(...)`) | Fila / registro |
| Atributo de instancia (`usuario.nombre`) | Valor de una celda |

Cuando tu código dice `usuario.nombre`, SQLAlchemy traduce eso por ti a `SELECT nombre FROM usuarios WHERE ...`. Magia, ¿no?

> 🎓 **Analogía del profesor**: ORM es como un **intérprete de la ONU** 🌍. Vos hablás en Python, él habla en SQL y ambos se entienden perfectamente.

---

## 2.2 ¿Qué es una transacción?

Es una **unidad de trabajo indivisible**. O se hace todo o no se hace nada.

**Ejemplo real**: si transferís dinero entre dos cuentas, **debitás** una y **acreditás** la otra. Si falla la segunda, la primera debe deshacerse también. A eso le llamamos **atomicidad**.

SQLAlchemy maneja una transacción automáticamente cada vez que abrís una sesión. Vos solo te preocupás por llamar a `session.commit()` al final.

### Las 4 propiedades ACID

| Letra | Significado | Qué garantiza |
|---|---|---|
| **A** | Atomicity | Todo o nada. |
| **C** | Consistency | La base nunca queda en estado roto. |
| **I** | Isolation | Dos transacciones paralelas no se pisan. |
| **D** | Durability | Una vez que hacés `commit()`, no se pierde. |

> 🎓 **Mental model**: la transacción es un **borrador con Ctrl-Z**. O imprimís el documento final (`commit`) o descartás todo (`rollback`).

---

## 2.3 Diferencia entre Core y ORM

SQLAlchemy tiene dos "pisos":

- 🧱 **Core**: manipula SQL puro, pero con esteroides (tipo `select(tabla)`).
- 🚀 **ORM**: encima de Core, te permite trabajar con objetos en vez de tablas.

```python
# 🟢 Core: SELECT pero SQL puro con esteroides
from sqlalchemy import select
usuarios = conn.execute(select(usuarios_tabla)).fetchall()

# 🚀 ORM: objetos en vez de tuplas
usuarios = session.scalars(select(Usuario)).all()
```

**La diferencia**: el ORM te entrega **instancias de clases** con sus métodos. Core entrega tuplas o diccionarios. El ORM es más cómodo, Core es más rápido (ligeramente) y flexible.

Este manual se enfoca en el ORM, que es lo que vas a usar el 90% del tiempo con FastAPI.

---

## 2.4 ¿Qué cambia de SQLAlchemy 1.x a 2.0?

La versión 2.0 (lanzada en enero de 2023) fue una **revolución**. El cambio más visible: pasó del estilo **imperativo** al **declarativo**.

| Aspecto | 1.x 🟠 | 2.0 ✅ |
|---|---|---|
| Base | `declarative_base()` | `class Base(DeclarativeBase)` |
| Tipos | `Column(String)` | `Mapped[str]` |
| Consultas | `session.query(User)` | `session.scalars(select(User))` |
| Anotaciones | Opcionales | PEP 484 obligatorio |
| Lazy loading | Implícito, oculto | Explícito, configurable |
| Tipado | Dinámico | Compatible con mypy, IDE |

### El cambio más visible: `query()` → `select()`

```python
# ❌ SQLAlchemy 1.x
usuarios = session.query(Usuario).filter_by(activo=True).all()

# ✅ SQLAlchemy 2.0
from sqlalchemy import select
stmt = select(Usuario).where(Usuario.activo == True)
usuarios = session.scalars(stmt).all()
```

> 🎓 **Regla de oro**: si ves `session.query(...)` o `declarative_base()` en un tutorial de 2024 en adelante, **es viejo**. Date vuelta.

---

## 2.5 ¿Qué es FastAPI y por qué lo mencionamos?

FastAPI es un framework para crear APIs (puntos de acceso HTTP) en Python. Usa **Pydantic** para validar datos y **inyección de dependencias** para mantener el código limpio. Lo interesante es que tiene una forma muy elegante de compartir la sesión de SQLAlchemy en cada petición: el patrón `get_db()` con `yield`.

### ¿Por qué FastAPI se lleva bien con SQLAlchemy?

1. 🚀 **Pydantic** valida los datos de entrada y salida de la API.
2. 🔁 **Inyección de dependencias** comparte la sesión de DB por request.
3. 🧠 **Tipado estático**: lo que SQLAlchemy 2.0 trae, FastAPI ya lo pide.
4. 📚 **Docs automáticas**: `GET /docs` te muestra todos los endpoints con sus schemas.

En el [capítulo 17](./17-fastapi.md) vamos a ver todo el patrón en detalle.

---

## 2.6 Vocabulario que necesitás antes de empezar

| Término | Significado en una frase |
|---|---|
| **Tabla** | Estructura en SQL con filas y columnas. |
| **Fila / Registro** | Una entrada concreta de la tabla. |
| **Columna** | Atributo de la tabla (`nombre`, `edad`, etc.). |
| **Primary Key (PK)** | Columna que identifica de forma única una fila. |
| **Foreign Key (FK)** | Columna que apunta a la PK de otra tabla. |
| **Índice** | Estructura auxiliar que acelera búsquedas. |
| **JOIN** | Operación que une filas de varias tablas. |
| **Transacción** | Conjunto de operaciones que se hacen todas o ninguna. |
| **Cursor** | Objeto que recorre filas en Core (no se usa mucho en ORM). |

> 💡 Si alguno de estos términos no te resulta claro, no te preocupés: lo vamos a ver en acción a medida que avancemos.

---

## 🎓 Lo que aprendiste

- **ORM** = mapeo entre clases Python y tablas SQL.
- **Transacción** = unidad atómica (todo o nada).
- **Core vs ORM**: ORM es más cómodo, Core es más fino.
- La **versión 2.0** es moderna, tipada y muy distinta a la 1.x.
- **FastAPI** es la pareja perfecta para SQLAlchemy.

## 📖 Siguiente

[Capítulo 3: Instalación y entorno →](./03-instalacion.md)
