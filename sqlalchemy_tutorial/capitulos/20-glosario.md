# Capítulo 20: Glosario rápido

> Las definiciones que siempre olvidás. Pegalo en un sticky note. 😄

| Término | Definición corta |
|---|---|
| **ORM** | Object-Relational Mapping: convierte objetos Python a SQL y viceversa. |
| **SQLAlchemy** | Librería Python para acceder a bases de datos relacionales de forma ORM o Core. |
| **Declarative Base** | Clase base (`DeclarativeBase`) de la que heredan los modelos en SQLAlchemy 2.0. |
| **`Mapped[T]`** | Anotación que le dice a SQLAlchemy: "este atributo es columna SQL de tipo T". |
| **`mapped_column(...)`** | Configuración explícita de una columna (PK, FK, default, etc.). |
| **`relationship()`** | Función que crea una conexión lógica entre dos modelos. |
| **Foreign Key (FK)** | Columna que referencia la primary key de otra tabla. |
| **Primary Key (PK)** | Columna que identifica de forma única una fila. |
| **`back_populates`** | Conecta ambos lados de una relación. Cada lado es explícito. |
| **`backref`** | Atajo automático para conectar el otro lado de una relación. |
| **`cascade`** | Qué operaciones se propagan del padre a los hijos (delete-orphan, all, etc.). |
| **Lazy loading** | Los hijos se cargan solo cuando los pedís (`lazy="select"`, default). |
| **Eager loading** | Los hijos se cargan junto con el padre (`lazy="joined"` o `joinedload`). |
| **N+1 query** | Patrón lento: 1 consulta + N consultas por cada hijo. ¡Evitalo! |
| **`selectinload`** | Carga relaciones 1—N de forma eficiente con `IN (...)`. |
| **`joinedload`** | Carga relaciones con un JOIN (ideal para 1—1 y muchos-a-uno). |
| **`Session`** | Conversación con la base. Tiene una transacción implícita. |
| **`yield`** | Palabra clave de Python para crear generadores. Ideal para dependencias. |
| **`with Session(engine) as session:`** | Patrón moderno y seguro para usar sesiones. |
| **`session.get(Modelo, id)`** | Búsqueda rápida por Primary Key. |
| **`session.scalars(stmt)`** | Ejecuta un `SELECT` y devuelve iterable de objetos ORM. |
| **`session.execute(stmt)`** | Ejecuta cualquier statement, devuelve filas. |
| **`session.commit()`** | Flush + commit. Hace los cambios oficiales. |
| **`session.flush()`** | Emite SQL pendiente sin commitear. |
| **`session.rollback()`** | Revierte cambios no confirmados. |
| **`session.refresh(obj)`** | Recarga el objeto desde la base de datos. |
| **Backend** | El motor de la base de datos (PostgreSQL, MySQL, SQLite, etc.). |
| **Driver** | Librería que conecta Python a la base (`psycopg2`, `pymysql`, etc.). |
| **`Engine`** | Fábrica de conexiones a la base de datos. |
| **Pydantic** | Librería que valida y serializa datos. Usa modelos (`BaseModel`). |
| **`response_model`** | Indicás a FastAPI el schema a usar para la respuesta. |
| **`exclude_unset=True`** | En PATCH, excluye campos no enviados por el cliente. |
| **`SessionDep`** | Alias de `Annotated[Session, Depends(get_db)]` (FastAPI). |
| **Migration (Alembic)** | Sistema para evolucionar el esquema de la DB sin perder datos. |
| **`from_attributes=True`** | Permite a Pydantic leer atributos de objetos ORM. |
| **`model_dump()`** | Convierte un modelo Pydantic a dict (reemplazo de `dict()` en Pydantic v2). |
| **sessionmaker** | Fábrica de sesiones. |
| **echo=True** | Modo del engine que imprime SQL por consola (útil para aprender). |
| **`__tablename__`** | Atributo de la clase que define el nombre de la tabla en SQL. |
| **`uselist=False`** | Define una relación 1—1 (en vez de lista). |
| **`secondary=`** | En N—M, indica la tabla de asociación. |
| **`remote_side`** | En autorreferencias, indica el lado "padre". |
| **`server_default`** | Default que pone la base al insertar. |
| **`onupdate=`** | Lanza una función cada vez que la fila se actualiza. |

---

## 🎓 Lo que aprendiste

- Los términos que vas a escuchar en cualquier conversación sobre SQLAlchemy.
- Bocadillo: pegalo en un `Cheat-Sheet` al lado de tu monitor. 😉

## 📖 Siguiente

[Capítulo 21: Recursos y siguiente paso →](./21-recursos.md)
