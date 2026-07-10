# 🐍 SQLAlchemy 2.0 — El Manual Definitivo en Español

> **Una guía completa, moderna y didáctica para dominar SQLAlchemy 2.0 con FastAPI.**
> Escrita para estudiantes hispanohablantes, con un enfoque paso a paso, ejemplos reales y las mejores prácticas de la industria.
>
> _Última revisión: 2026._

---

## 🎁 Bonus incluidos

- 🚀 **[Proyecto FastAPI ejecutable](./proyecto/fastapi_sqlalchemy/)** — código completo del capítulo 17 listo para correr, con tests y Docker.
- 📚 **25 capítulos** que cubren desde cero hasta Docker.
- ✍️ **[Ejercicios prácticos con soluciones](./soluciones/)** — cada capítulo técnico (3-25) tiene 5 ejercicios por nivel (🟢🟡🔴) con su resolución detallada.
- 📊 **Diagramas Mermaid** — reemplazamos los ASCII art por diagramas profesionales de flujo, ER, secuencias y arquitectura.

---

## 📑 Índice de capítulos

### 🟢 Fundamentos

| # | Capítulo | Resumen |
|---|---|---|
| 01 | [Bienvenida](./capitulos/01-bienvenida.md) | Qué vas a aprender y por qué este manual existe. |
| 02 | [Conceptos previos](./capitulos/02-conceptos-previos.md) | ORM, transacciones, Core vs ORM, qué cambia en 2.0. |
| 03 | [Instalación y entorno](./capitulos/03-instalacion.md) | Cómo preparar tu proyecto desde cero. |
| 04 | [Engine y Session](./capitulos/04-engine-session.md) | Las dos piezas que mueven todo. |
| 05 | [Declarative Base](./capitulos/05-declarative-base.md) | El ADN de tus modelos. |

### 🔵 Trabajando con modelos

| # | Capítulo | Resumen |
|---|---|---|
| 06 | [Anotaciones `Mapped[T]`](./capitulos/06-anotaciones-mapped.md) | El truco mágico de SQLAlchemy 2.0. |
| 07 | [🆕 Mixins](./capitulos/07-mixins.md) | Reutilizá columnas entre muchos modelos. |
| 08 | [🆕 Herencia de modelos](./capitulos/08-herencia-modelos.md) | Concrete, Joined y Single Table. |
| 09 | [El primer modelo completo](./capitulos/09-primer-modelo.md) | Uniendo las piezas. |
| 10 | [Crear tablas (DDL)](./capitulos/10-crear-tablas.md) | Llevar tus clases a la base real. |
| 11 | [CRUD](./capitulos/11-crud.md) | Crear, Leer, Actualizar y Borrar. |
| 12 | [Consultas (`SELECT`, `WHERE`, `JOIN`)](./capitulos/12-consultas.md) | Cómo pedirle datos a la base. |

### 🔴 Temas avanzados

| # | Capítulo | Resumen |
|---|---|---|
| 13 | [🔥 Relaciones entre tablas](./capitulos/13-relaciones.md) | 1—N, 1—1, N—M, autorreferencias, cascades. |
| 14 | [Subconsultas y operadores avanzados](./capitulos/14-subconsultas.md) | `EXISTS`, agregaciones, `GROUP BY`. |
| 15 | [🆕 Eventos SQLAlchemy](./capitulos/15-eventos.md) | Hooks para auditoría, validación, timestamps. |
| 16 | [🆕 AsyncSession](./capitulos/16-async-session.md) | SQLAlchemy con `async/await` y FastAPI async. |

### ⚡ Integración con FastAPI

| # | Capítulo | Resumen |
|---|---|---|
| 17 | [FastAPI + SQLAlchemy (patrón moderno)](./capitulos/17-fastapi.md) | `get_db()` con `yield`, `SessionDep`, Pydantic, CRUD completo. |
| 18 | [Buenas prácticas](./capitulos/18-buenas-practicas.md) | Lo que aprendes con la experiencia. |
| 19 | [Errores comunes](./capitulos/19-errores-comunes.md) | Los problemas más frecuentes y cómo arreglarlos. |
| 20 | [Glosario rápido](./capitulos/20-glosario.md) | Las definiciones que siempre olvidás. |
| 21 | [Recursos y siguiente paso](./capitulos/21-recursos.md) | Documentación oficial, siguientes temas. |

### 🆕 Temas extendidos (bonus)

| # | Capítulo | Resumen |
|---|---|---|
| 22 | [🆕 Pydantic v2 en profundidad](./capitulos/22-pydantic-v2.md) | `Field`, validadores, `ConfigDict`, Settings, discriminated unions. |
| 23 | [🆕 Alembic: migraciones de DB](./capitulos/23-alembic.md) | Setup, autogenerate, data migrations, deploy en producción. |
| 24 | [🆕 SQLAlchemy-Utils y extensiones](./capitulos/24-sqlalchemy-utils.md) | `EmailType`, `EncryptedType`, `ChoiceType`, mixins avanzados. |
| 25 | [🆕 Deploy con Docker](./capitulos/25-docker.md) | Dockerfile multi-stage, docker-compose dev/prod, healthchecks, CI/CD. |

---

## 🚀 Proyecto completo incluido

📁 **[`proyecto/fastapi_sqlalchemy/`](./proyecto/fastapi_sqlalchemy/)** — código real, listo para correr con Docker.

```
proyecto/fastapi_sqlalchemy/
├── app/
│   ├── main.py              # Punto de entrada FastAPI
│   ├── config.py            # Pydantic Settings + .env
│   ├── database.py          # Engine, Base, get_db, SessionDep
│   ├── models/              # Modelos ORM con relaciones
│   ├── schemas/             # Pydantic schemas (Base/Create/Public/Update)
│   └── routers/             # Endpoints REST
├── tests/                   # Tests con pytest + TestClient
├── scripts/entrypoint.sh    # Script de arranque (Alembic + app)
├── Dockerfile               # Multi-stage build
├── docker-compose.yml       # Stack dev (API + PostgreSQL)
├── docker-compose.prod.yml  # Stack producción
├── Makefile                 # Atajos de comandos
├── requirements.txt
├── .env.example
├── .dockerignore
└── README.md
```

**Para correrlo con Docker**:

```bash
cd proyecto/fastapi_sqlalchemy
docker compose up --build
# → http://localhost:8000/docs
```

**O sin Docker**:

```bash
cd proyecto/fastapi_sqlalchemy
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
uvicorn app.main:app --reload
# → http://127.0.0.1:8000/docs
```

---

## 🚀 Cómo leer este manual

- 📕 **Lectura lineal**: cada capítulo construye sobre el anterior. Si recién empezás, leélo de corrido.
- 📂 **Lectura por tema**: si ya conocés las bases, usá la tabla de arriba para saltar a lo que te interesa.
- 💻 **Práctica activa**: cada capítulo tiene ejemplos copiables. La mejor forma de aprender es **ejecutarlos, romperlos y arreglarlos**.
- ✍️ **Ejercicios + soluciones**: cada capítulo técnico termina con 5 ejercicios por nivel (🟢🟡🔴) y enlaces a las soluciones en [`soluciones/`](./soluciones/).

> 💡 **Tip**: cada capítulo termina con una sección **"Lo que aprendiste"** y un enlace al siguiente capítulo. Usala como checklist.

## ⚙️ Requisitos previos

- Python 3.10 o superior (recomendado 3.11+).
- Conocimientos básicos de SQL (`SELECT`, `WHERE`, `JOIN`).
- Algo de familiaridad con clases y anotaciones en Python.

Si te sentís oxidado en SQL, no te preocupes: el manual explica lo esencial cuando lo necesitás.

---

## 🗺️ Mapa de aprendizaje

```
🟢 FUNDAMENTOS (Caps. 1-6)
   Aprendés a definir modelos y conectarte a la base
   ↓
🟡 INTERMEDIO (Caps. 7-12)
   Reutilizás con mixins, heredás, hacés CRUD y consultas reales
   ↓
🔴 AVANZADO (Caps. 13-16)
   Dominás relaciones, eventos, async, todo el poder del ORM
   ↓
⚡ INTEGRACIÓN (Caps. 17-21)
   Conectás todo a FastAPI y aprendés el patrón de la industria
   ↓
🎁 BONUS (Caps. 22-25)
   Pydantic v2, Alembic, SQLAlchemy-Utils, Docker — todo lo que necesitás
   para el día a día
   ↓
🚀 PROYECTO
   El código del cap. 17 listo para correr con Docker, con tests incluidos
```

---

## 🔗 Agradecimientos y fuentes

Este manual se basa en la documentación oficial de:

- 📖 [SQLAlchemy 2.0 ORM Quickstart](https://docs.sqlalchemy.org/en/20/orm/quickstart.html).
- 📖 [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/).
- 📖 [Pydantic v2 Docs](https://docs.pydantic.dev/latest/).
- 📖 [SQLAlchemy-Utils](https://sqlalchemy-utils.readthedocs.io/).

El contenido fue sintetizado, ampliado y reorganizado con un enfoque pedagógico para hispanohablantes. Todos los ejemplos fueron actualizados para usar las mejores prácticas de la versión 2.0+ y los patrones modernos de FastAPI.

---

¡A programar! 🚀
