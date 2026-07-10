# Capítulo 23: Alembic — migraciones de base de datos

> "No sé si notaron que `create_all` no actualiza tablas existentes. ¿Cómo hago entonces?" — El junior.

`Base.metadata.create_all(engine)` está bien para empezar. Pero cuando tu esquema evoluciona (agregás columnas, renombrás, etc.), necesitás **migraciones incrementales** que no rompan los datos existentes. Para eso existe **Alembic**.

---

## 23.1 ¿Qué es Alembic?

**Alembic** es la herramienta de migración oficial de SQLAlchemy. Es como un "control de versiones" para tu esquema de base de datos.

> 🎓 **Analogía del profesor**: Alembic es como **Git, pero para tu base de datos**. Cada migración es un commit. Podés ir hacia adelante (`upgrade`) o hacia atrás (`downgrade`).

### ¿Por qué no usar `create_all` en producción?

| Acción | `create_all` | Alembic |
|---|---|---|
| Crear tabla nueva | ✅ | ✅ |
| Agregar columna a tabla existente | ❌ | ✅ |
| Renombrar columna | ❌ | ✅ |
| Cambiar tipo de columna | ❌ | ✅ |
| Crear índice | ✅ | ✅ |
| Eliminar columna | ❌ | ✅ |
| Conservar datos | ❌ | ✅ |
| Reproducible | ❌ | ✅ |
| Rollback | ❌ | ✅ |

> ⚠️ **Regla clara**: `create_all` es solo para dev y testing. En producción, **siempre Alembic**.

---

## 23.2 Instalación e inicialización

### Instalación

```bash
pip install alembic
```

### Inicializar Alembic en tu proyecto

```bash
cd mi_proyecto/
alembic init alembic
```

Esto crea:
```
mi_proyecto/
├── alembic/
│   ├── versions/        # acá van las migraciones
│   ├── env.py           # configuración del entorno
│   ├── script.py.mako   # template para nuevas migraciones
│   └── README
├── alembic.ini          # configuración global
└── ...
```

---

## 23.3 Configurar `alembic.ini`

```ini
# alembic.ini

# URL de la base de datos (puede leerla de env var)
sqlalchemy.url = sqlite:///./tienda.db
```

O mejor, leela de tu variable de entorno:

```ini
sqlalchemy.url = 
```

Y en `env.py`, leés la variable:

```python
# alembic/env.py
import os
from logging.config import fileConfig
from sqlalchemy import engine_from_config, pool
from alembic import context
from app.database import Base
import app.models  # registra los modelos

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Permite leer la URL del entorno
config.set_main_option("sqlalchemy.url", os.getenv("DATABASE_URL", "sqlite:///./tienda.db"))

target_metadata = Base.metadata


def run_migrations_offline() -> None:
    context.configure(
        url=config.get_main_option("sqlalchemy.url"),
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online() -> None:
    connectable = engine_from_config(
        config.get_section(config.config_ini_section, {}),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
            compare_type=True,    # 👈 detecta cambios de tipo
            compare_server_default=True,
        )
        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
```

> 🎓 **Detalle clave**: `compare_type=True` le dice a Alembic que detecte cambios de tipo (ej: `String(50) → String(100)`). Si lo dejás en `False`, no los ve.

---

## 23.4 La primera migración: inicial

### Crear la migración

```bash
alembic revision --autogenerate -m "inicial"
```

Alembic compara `Base.metadata` con la DB actual y genera un archivo de migración.

### Estructura de la migración

```python
# alembic/versions/abc123_inicial.py

"""inicial

Revision ID: abc123def456
Revises: 
Create Date: 2026-XX-XX HH:MM:SS
"""
from typing import Sequence, Union
from alembic import op
import sqlalchemy as sa

revision: str = "abc123def456"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "categorias",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=50), nullable=False),
        sa.Column("descripcion", sa.String(), nullable=True),
        sa.Column("creado_en", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("actualizado_en", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("nombre"),
    )
    op.create_index(op.f("ix_categorias_nombre"), "categorias", ["nombre"], unique=True)

    op.create_table(
        "productos",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=100), nullable=False),
        sa.Column("sku", sa.String(length=20), nullable=False),
        sa.Column("precio", sa.Numeric(precision=10, scale=2), nullable=False),
        sa.Column("descripcion", sa.String(), nullable=True),
        sa.Column("categoria_id", sa.Integer(), nullable=True),
        sa.Column("creado_en", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.Column("actualizado_en", sa.DateTime(), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(["categoria_id"], ["categorias.id"]),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("sku"),
    )
    op.create_index(op.f("ix_productos_nombre"), "productos", ["nombre"], unique=False)
    op.create_index(op.f("ix_productos_sku"), "productos", ["sku"], unique=True)


def downgrade() -> None:
    op.drop_index(op.f("ix_productos_sku"), table_name="productos")
    op.drop_index(op.f("ix_productos_nombre"), table_name="productos")
    op.drop_table("productos")
    op.drop_index(op.f("ix_categorias_nombre"), table_name="categorias")
    op.drop_table("categorias")
```

### Aplicar la migración

```bash
alembic upgrade head
```

Output esperado:

```
INFO  [alembic.runtime.migration] Context impl SQLiteImpl.
INFO  [alembic.runtime.migration] Will assume non-transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> abc123def456, inicial
```

### Ver el estado actual

```bash
alembic current
# abc123def456 (head)
```

### Ver el historial completo

```bash
alembic history --verbose
```

---

## 23.5 Flujo típico: agregar una columna

### Paso 1: modificás el modelo

```python
# app/models/producto.py
class Producto(Base, TimestampMixin):
    # ...
    stock: Mapped[int] = mapped_column(default=0, nullable=False)   # 👈 nueva
```

### Paso 2: generás la migración

```bash
alembic revision --autogenerate -m "agregar stock a producto"
```

Alembic genera:

```python
def upgrade() -> None:
    op.add_column("productos", sa.Column("stock", sa.Integer(), nullable=False, server_default="0"))


def downgrade() -> None:
    op.drop_column("productos", "stock")
```

### Paso 3: revisás y aplicás

```bash
# ⚠️ SIEMPRE revisá el archivo generado antes de aplicar
alembic upgrade head
```

---

## 23.6 Operaciones comunes con `op`

Alembic ofrece `op` con métodos para casi todo. Los más usados:

### Tablas

```python
op.create_table("usuarios", sa.Column("id", sa.Integer(), primary_key=True))
op.drop_table("usuarios")
op.rename_table("usuarios", "users")
```

### Columnas

```python
op.add_column("usuarios", sa.Column("email", sa.String(100)))
op.drop_column("usuarios", "email")
op.alter_column("usuarios", "email", new_column_name="correo")
op.alter_column("usuarios", "email", type_=sa.String(200))   # cambiar tipo
op.alter_column("usuarios", "email", nullable=True)          # cambiar nulabilidad
op.alter_column("usuarios", "email", server_default="n/a")   # default
```

### Índices

```python
op.create_index("ix_usuarios_email", "usuarios", ["email"], unique=True)
op.drop_index("ix_usuarios_email", table_name="usuarios")
```

### Constraints

```python
op.create_unique_constraint("uq_usuarios_email", "usuarios", ["email"])
op.drop_constraint("uq_usuarios_email", "usuarios", type_="unique")

op.create_foreign_key(
    "fk_productos_categoria",
    "productos",
    "categorias",
    ["categoria_id"],
    ["id"],
    ondelete="CASCADE",
)
op.drop_constraint("fk_productos_categoria", "productos", type_="foreignkey")
```

### Datos

```python
# Insertar filas iniciales
op.execute("INSERT INTO categorias (nombre) VALUES ('Electrónica')")
op.execute("INSERT INTO categorias (nombre) VALUES ('Ropa')")
```

---

## 23.7 Data migrations (migraciones con lógica)

A veces necesitás transformar datos durante la migración:

```python
"""actualizar precios con 10% de descuento

Revision ID: xyz789
Revises: abc123
Create Date: 2026-XX-XX
"""
from alembic import op
import sqlalchemy as sa


def upgrade() -> None:
    # 1. Agregar columna temporal
    op.add_column("productos", sa.Column("precio_nuevo", sa.Numeric(10, 2)))
    
    # 2. Copiar con transformación
    op.execute("UPDATE productos SET precio_nuevo = precio * 0.9")
    
    # 3. Borrar la vieja
    op.drop_column("productos", "precio")
    
    # 4. Renombrar la nueva
    op.alter_column("productos", "precio_nuevo", new_column_name="precio")


def downgrade() -> None:
    op.add_column("productos", sa.Column("precio_viejo", sa.Numeric(10, 2)))
    op.execute("UPDATE productos SET precio_viejo = precio / 0.9")
    op.drop_column("productos", "precio")
    op.alter_column("productos", "precio_viejo", new_column_name="precio")
```

> ⚠️ **Importante**: si la transformación es compleja, hacela en Python con SQLAlchemy Core, no en SQL puro:

```python
from sqlalchemy import table, column

productos_t = table(
    "productos",
    column("id", sa.Integer),
    column("precio", sa.Numeric),
    column("precio_nuevo", sa.Numeric),
)

def upgrade() -> None:
    op.add_column("productos", sa.Column("precio_nuevo", sa.Numeric(10, 2)))
    
    bind = op.get_bind()
    for row in bind.execute(productos_t.select()):
        nuevo = row.precio * 0.9
        bind.execute(
            productos_t.update()
            .where(productos_t.c.id == row.id)
            .values(precio_nuevo=nuevo)
        )
    
    op.drop_column("productos", "precio")
    op.alter_column("productos", "precio_nuevo", new_column_name="precio")
```

---

## 23.8 Migraciones manuales (sin autogenerate)

A veces `autogenerate` no capta un cambio (por ejemplo, un CHECK constraint). En ese caso, hacé la migración a mano:

```bash
alembic revision -m "agregar check de precio positivo"
```

Editás el archivo:

```python
def upgrade() -> None:
    op.create_check_constraint(
        "ck_productos_precio_positivo",
        "productos",
        "precio > 0",
    )


def downgrade() -> None:
    op.drop_constraint(
        "ck_productos_precio_positivo",
        "productos",
        type_="check",
    )
```

---

## 23.9 Reversión de migraciones

### Volver a una versión específica

```bash
alembic downgrade abc123def456
```

### Volver una versión atrás

```bash
alembic downgrade -1
```

### Volver a cero (¡borrar todo!)

```bash
alembic downgrade base
```

> ⚠️ **Peligro**: `alembic downgrade base` borra todas las tablas. En producción, hacé backup primero.

---

## 23.10 Branching y merge de migraciones

Si dos developers crean migraciones en paralelo, Alembic crea un **branch**. Hay que **mergear**:

```bash
# Crear merge
alembic merge -m "merge heads" head1 head2

# Aplicar
alembic upgrade head
```

> 🎓 **Tip del profesor**: para evitar esto, intentá que las migraciones sean **secuenciales** y cortas.

---

## 23.11 Integración con FastAPI

### Opción A: ejecutar migraciones en el startup

```python
# app/main.py
from alembic import command
from alembic.config import Config
from fastapi import FastAPI


def run_migrations():
    """Aplica migraciones pendientes al iniciar."""
    cfg = Config("alembic.ini")
    command.upgrade(cfg, "head")


app = FastAPI()


@app.on_event("startup")
def startup():
    run_migrations()
```

### Opción B: ejecutar migraciones antes de levantar la app

```bash
# En tu pipeline de deploy
alembic upgrade head
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

> 🎓 **Opción B es la preferida en producción**: separar el deploy de la app de la migración evita problemas de concurrencia.

---

## 23.12 Workflow profesional

### En desarrollo

```bash
# 1. Modificás un modelo
# 2. Generás la migración
alembic revision --autogenerate -m "agregar columna X"

# 3. REVISÁS el archivo generado
# 4. Aplicás
alembic upgrade head

# 5. Si algo salió mal
alembic downgrade -1
# Corregís el modelo
alembic revision --autogenerate -m "..."
alembic upgrade head
```

### En producción

```bash
# 1. Backup de la DB (importante!)
pg_dump mydb > backup.sql

# 2. Aplicar migraciones
alembic upgrade head

# 3. Si falló, rollback
alembic downgrade -1

# 4. Restaurar backup si es grave
psql mydb < backup.sql
```

### En CI/CD

```yaml
# .github/workflows/deploy.yml
- name: Aplicar migraciones
  run: alembic upgrade head

- name: Levantar app
  run: uvicorn app.main:app --host 0.0.0.0 --port 8000
```

---

## 23.13 Troubleshooting

| Problema | Solución |
|---|---|
| Alembic no detecta cambios | ¿Habilitaste `compare_type=True`? ¿Importaste el modelo? |
| `Target database is not up to date` | Hacé `alembic stamp head` o `alembic upgrade head`. |
| Conflicto de versiones (dos heads) | `alembic merge -m "merge" head1 head2`. |
| Migración generada con cambios raros | Revisar y editar manualmente. `autogenerate` no es perfecto. |
| Datos corruptos al cambiar tipo | Hacer data migration con cuidado, columna intermedia. |

---

## 23.14 El comando `stamp`

A veces tu DB ya tiene las tablas (ej: creada con `create_all`) y querés que Alembic las reconozca sin generar cambios:

```bash
alembic stamp head
```

Esto marca la DB como si tuviera aplicada la última migración, sin tocar las tablas.

> 💡 Útil al migrar un proyecto viejo a Alembic por primera vez.

---

## 23.15 Resumen

| Comando | Para qué sirve |
|---|---|
| `alembic init alembic` | Inicializar la estructura. |
| `alembic revision --autogenerate -m "msg"` | Generar migración automática. |
| `alembic revision -m "msg"` | Generar migración manual. |
| `alembic upgrade head` | Aplicar todas las migraciones pendientes. |
| `alembic upgrade +1` | Aplicar la siguiente migración. |
| `alembic downgrade -1` | Volver una versión atrás. |
| `alembic current` | Ver versión actual. |
| `alembic history` | Ver historial. |
| `alembic stamp head` | Marcar la DB como actualizada. |
| `alembic merge` | Resolver conflicto de branches. |

---

## 🛠️ Ejercicios prácticos

### 🟢 Ejercicio 23.1: Init Alembic

Inicializá Alembic en un proyecto nuevo. Después de ejecutar `alembic init alembic`, ¿qué archivos se crearon?

**Solución**: [soluciones/23-alembic.md](../soluciones/23-alembic.md#ejercicio-231)

---

### 🟡 Ejercicio 23.2: Primera migración

Dada un modelo `Usuario(nombre, email)`, generá la primera migración con `revision --autogenerate`. ¿Qué hace Alembic exactamente? Verificá con `cat alembic/versions/*.py`.

**Solución**: [soluciones/23-alembic.md](../soluciones/23-alembic.md#ejercicio-232)

---

### 🟡 Ejercicio 23.3: Modificar una columna

Agregá una columna `telefono: Optional[str]` a `Usuario`. Generá la migración. Aplicala con `upgrade`. Verificá que la columna existe con `pragma table_info(usuarios)` (SQLite) o `\d usuarios` (Postgres).

**Solución**: [soluciones/23-alembic.md](../soluciones/23-alembic.md#ejercicio-233)

---

### 🟡 Ejercicio 23.4: Data migration

Imaginá que tenés una columna `precio_legacy: Numeric`. Escribí una migración que:

1. Agregue `precio_nuevo: Numeric`.
2. Copie `precio_legacy` a `precio_nuevo` con un 10% de aumento.
3. Borre `precio_legacy`.
4. Renombre `precio_nuevo` a `precio`.

**Solución**: [soluciones/23-alembic.md](../soluciones/23-alembic.md#ejercicio-234)

---

### 🔴 Ejercicio 23.5: Pipeline CI/CD

Escribí un workflow de GitHub Actions que:

1. Levante PostgreSQL en un servicio.
2. Instale dependencias.
3. Corra `alembic upgrade head`.
4. Corra los tests.
5. Si todo pasa, construya la imagen Docker.

**Solución**: [soluciones/23-alembic.md](../soluciones/23-alembic.md#ejercicio-235)

---

## 🎓 Lo que aprendiste

- Alembic gestiona la **evolución del esquema** de la DB.
- `alembic revision --autogenerate` detecta cambios en los modelos.
- `upgrade` aplica, `downgrade` revierte.
- Las **data migrations** transforman datos durante la migración.
- En producción, **siempre** Alembic (jamás `create_all` en deploy).
- `compare_type=True` detecta cambios de tipo.

## 📖 Siguiente

[Capítulo 24: SQLAlchemy-Utils y extensiones útiles →](./24-sqlalchemy-utils.md)