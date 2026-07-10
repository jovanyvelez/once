# 🛒 Proyecto: API de Tienda con FastAPI + SQLAlchemy 2.0

> Este es el proyecto ejecutable que demuestra todo lo visto en los **[capítulos 17](../../capitulos/17-fastapi.md) y [25](../../capitulos/25-docker.md)**.
> Una API REST completa de gestión de productos y categorías con las mejores prácticas modernas, lista para correr con Docker.

---

## 📂 Estructura

```
fastapi_sqlalchemy/
├── app/
│   ├── main.py              # Punto de entrada FastAPI
│   ├── config.py            # Settings (Pydantic v2 + .env)
│   ├── database.py          # Engine, Base, get_db
│   ├── models/              # Modelos ORM
│   │   ├── base.py          # TimestampMixin
│   │   ├── categoria.py
│   │   └── producto.py
│   ├── schemas/             # Schemas Pydantic
│   │   ├── categoria.py
│   │   └── producto.py
│   └── routers/             # Endpoints
│       ├── categorias.py
│       └── productos.py
├── tests/                   # Tests con pytest
│   ├── conftest.py
│   └── test_productos.py
├── scripts/
│   └── entrypoint.sh        # Script de arranque (Alembic + app)
├── Dockerfile               # Multi-stage build
├── docker-compose.yml       # Stack dev (API + PostgreSQL)
├── docker-compose.prod.yml  # Stack producción
├── Makefile                 # Atajos de comandos
├── requirements.txt
├── .env.example
├── .dockerignore
└── README.md
```

---

## 🚀 Opción A: con Docker (recomendado)

Es la forma más rápida de correr todo. Solo necesitás Docker instalado.

### 1. Levantar el stack

```bash
cd fastapi_sqlalchemy
docker compose up --build
```

Esto:

1. Construye la imagen de la API (multi-stage).
2. Levanta PostgreSQL.
3. Espera a que la DB esté healthy.
4. Aplica las migraciones con Alembic.
5. Inicia Uvicorn con hot reload.

### 2. Visitar

- 📚 Docs interactiva: http://localhost:8000/docs
- 🔍 ReDoc: http://localhost:8000/redoc
- 🏠 Home: http://localhost:8000/
- 💚 Healthcheck: http://localhost:8000/health

### 3. Comandos útiles con `make`

Si tenés `make` instalado:

```bash
make help           # ver todos los comandos
make up             # levantar
make up-d           # levantar en background
make logs-api       # ver logs de la API
make shell          # shell dentro del contenedor de la API
make test           # correr tests
make migrate msg="agregar stock"   # crear migración
make fresh          # ⚠️ borrar DB y empezar de cero
```

O sin `make`, con `docker compose`:

```bash
docker compose up -d
docker compose logs -f api
docker compose exec api bash
docker compose exec api pytest tests/ -v
docker compose exec api alembic revision --autogenerate -m "msg"
docker compose down -v
```

---

## 🚀 Opción B: instalación local (sin Docker)

Si preferís correrlo en tu máquina directamente:

### 1. Crear el entorno virtual

```bash
python -m venv venv
source venv/bin/activate       # Linux/macOS
.\venv\Scripts\activate        # Windows
```

### 2. Instalar dependencias

```bash
pip install -r requirements.txt
```

### 3. Configurar variables de entorno

```bash
cp .env.example .env
```

Por default usa SQLite. Si querés PostgreSQL local, editá `.env`:

```
DATABASE_URL=postgresql+psycopg2://postgres:postgres@localhost:5432/tienda
```

### 4. Inicializar la base de datos

```bash
# Si usás Alembic (recomendado):
alembic init alembic
# Configurar alembic/env.py (ver capítulo 23)
alembic revision --autogenerate -m "inicial"
alembic upgrade head

# O crear las tablas directamente:
python -c "from app.database import engine, Base; import app.models; Base.metadata.create_all(engine)"
```

### 5. Levantar el servidor

```bash
uvicorn app.main:app --reload
```

---

## 🧪 Ejecutar los tests

### Con Docker

```bash
make test
# o
docker compose exec api pytest tests/ -v
```

### Sin Docker

```bash
pytest tests/ -v
```

---

## 📡 Endpoints disponibles

### Productos (`/productos`)

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/productos/` | Crear producto. |
| GET | `/productos/` | Listar productos (paginado, con filtros). |
| GET | `/productos/{id}` | Obtener un producto por ID. |
| PATCH | `/productos/{id}` | Actualizar campos parciales. |
| DELETE | `/productos/{id}` | Borrar producto. |

**Filtros disponibles** en `GET /productos/`:

- `?offset=0&limit=50` — paginación.
- `?categoria_id=1` — filtrar por categoría.
- `?min_precio=100&max_precio=500` — rango de precio.
- `?search=laptop` — buscar por nombre o SKU.

### Categorías (`/categorias`)

| Método | Ruta | Descripción |
|---|---|---|
| POST | `/categorias/` | Crear categoría. |
| GET | `/categorias/` | Listar categorías. |
| DELETE | `/categorias/{id}` | Borrar categoría (cascade). |

---

## 🧠 Qué patrones aplicados hay acá

1. **`get_db()` con `yield`** — `app/database.py`.
2. **`SessionDep = Annotated[...]`** — `app/database.py`.
3. **Schemas separados (`Base`, `Create`, `Public`, `Update`)** — `app/schemas/`.
4. **`response_model=` correcto** — routers.
5. **PATCH con `model_dump(exclude_unset=True)`** — `app/routers/productos.py`.
6. **Mixins (`TimestampMixin`)** — `app/models/base.py`.
7. **`ConfigDict(from_attributes=True)`** — para que Pydantic lea objetos ORM.
8. **Settings con `pydantic-settings`** — `app/config.py`.
9. **Relaciones con `lazy="selectin"`** — evita N+1.
10. **Manejo de `IntegrityError`** con rollback — `app/routers/productos.py`.

---

## 🔧 Personalizar

- Cambiar de SQLite a PostgreSQL: editar `DATABASE_URL` en `.env`.
- Activar logs SQL: cambiar `DEBUG=true` en `.env`.
- Cambiar de SQLite a PostgreSQL: ya viene con docker-compose.
- Configurar Alembic para migraciones en producción: ver **[capítulo 23](../../capitulos/23-alembic.md)**.

---

## 🚀 Deploy a producción

Para deploy, usá el archivo `docker-compose.prod.yml`:

```bash
# 1. Construir imagen
docker build -t mi-usuario/tienda-api:1.0.0 .

# 2. Subir a un registry
docker push mi-usuario/tienda-api:1.0.0

# 3. En el servidor, configurar .env
cat > .env.prod <<EOF
POSTGRES_PASSWORD=contraseña-muy-segura-de-32-chars
API_IMAGE=mi-usuario/tienda-api:1.0.0
EOF

# 4. Levantar
docker compose -f docker-compose.prod.yml --env-file .env.prod up -d
```

Ver **[capítulo 25](../../capitulos/25-docker.md)** para más detalle sobre Dockerfile, multi-stage builds, healthchecks, secrets, y troubleshooting.

---

## 📖 Cómo está mapeado al manual

| Concepto | Capítulo | Archivo |
|---|---|---|
| Declarative Base | [05](../../capitulos/05-declarative-base.md) | `app/database.py` |
| Mapped[T] | [06](../../capitulos/06-anotaciones-mapped.md) | `app/models/*` |
| Mixins | [07](../../capitulos/07-mixins.md) | `app/models/base.py` |
| Relaciones | [13](../../capitulos/13-relaciones.md) | `app/models/producto.py` |
| get_db con yield | [17](../../capitulos/17-fastapi.md) | `app/database.py` |
| SessionDep | [17](../../capitulos/17-fastapi.md) | `app/database.py` |
| Pydantic schemas | [17](../../capitulos/17-fastapi.md) | `app/schemas/*` |
| Pydantic v2 avanzado | [22](../../capitulos/22-pydantic-v2.md) | `app/config.py` |
| Alembic | [23](../../capitulos/23-alembic.md) | `scripts/entrypoint.sh` |
| Deploy con Docker | [25](../../capitulos/25-docker.md) | `Dockerfile`, `docker-compose*.yml` |