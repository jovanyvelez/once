# Soluciones — Capítulo 23: Alembic

[Volver al capítulo 23](../capitulos/23-alembic.md)

---

## Ejercicio 23.1

**Init Alembic**

```bash
$ alembic init alembic
```

Archivos creados:

```
alembic/
├── versions/                  # directorio vacío para migraciones
├── env.py                     # configuración del entorno
├── script.py.mako             # template
└── README
alembic.ini                   # archivo principal de configuración
```

[Volver al ejercicio ↑](../capitulos/23-alembic.md#%C2%B0-ejercicio-231)

---

## Ejercicio 23.2

**Primera migración**

```bash
$ alembic revision --autogenerate -m "inicial con usuario"
```

Resultado:

```python
"""inicial con usuario

Revision ID: abc123
Revises: 
Create Date: 2026-XX-XX HH:MM:SS
"""
from alembic import op
import sqlalchemy as sa


def upgrade() -> None:
    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("nombre", sa.String(length=80), nullable=False),
        sa.Column("email", sa.String(length=120), nullable=False),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("email"),
    )


def downgrade() -> None:
    op.drop_table("usuarios")
```

**Qué hace**: lee `Base.metadata`, compara con la DB actual (vacía), y genera el SQL necesario.

[Volver al ejercicio ↑](../capitulos/23-alembic.md#%C2%B1-ejercicio-232)

---

## Ejercicio 23.3

**Modificar una columna**

```bash
$ alembic revision --autogenerate -m "agregar telefono a usuario"
$ alembic upgrade head
```

Migración generada:

```python
def upgrade() -> None:
    op.add_column("usuarios", sa.Column("telefono", sa.String(length=20), nullable=True))


def downgrade() -> None:
    op.drop_column("usuarios", "telefono")
```

Verificar con SQLite:

```bash
$ sqlite3 mi_base.db ".schema usuarios"
```

[Volver al ejercicio ↑](../capitulos/23-alembic.md#%C2%B1-ejercicio-233)

---

## Ejercicio 23.4

**Data migration**

```python
"""actualizar precio legacy

Revision ID: def456
Revises: abc123
"""
from alembic import op
import sqlalchemy as sa


def upgrade() -> None:
    # 1. Crear columna nueva
    op.add_column("productos", sa.Column("precio_nuevo", sa.Numeric(10, 2)))
    
    # 2. Copiar con aumento
    op.execute("UPDATE productos SET precio_nuevo = precio_legacy * 1.10")
    
    # 3. Borrar la vieja
    op.drop_column("productos", "precio_legacy")
    
    # 4. Renombrar
    op.alter_column("productos", "precio_nuevo", new_column_name="precio")


def downgrade() -> None:
    # Operación inversa
    op.add_column("productos", sa.Column("precio_legacy", sa.Numeric(10, 2)))
    op.execute("UPDATE productos SET precio_legacy = precio / 1.10")
    op.drop_column("productos", "precio")
    op.alter_column("productos", "precio_legacy", new_column_name="precio_legacy")
```

[Volver al ejercicio ↑](../capitulos/23-alembic.md#%C2%B1-ejercicio-234)

---

## Ejercicio 23.5

**Pipeline CI/CD**

```yaml
# .github/workflows/ci.yml
name: CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    
    services:
      postgres:
        image: postgres:16-alpine
        env:
          POSTGRES_USER: postgres
          POSTGRES_PASSWORD: postgres
          POSTGRES_DB: test_db
        ports:
          - 5432:5432
        options: >-
          --health-cmd pg_isready
          --health-interval 10s
          --health-timeout 5s
          --health-retries 5

    steps:
      - uses: actions/checkout@v4
      
      - name: Setup Python
        uses: actions/setup-python@v5
        with:
          python-version: "3.12"
      
      - name: Install deps
        run: pip install -r requirements.txt
      
      - name: Run migrations
        run: alembic upgrade head
        env:
          DATABASE_URL: postgresql+psycopg2://postgres:postgres@localhost:5432/test_db
      
      - name: Run tests
        run: pytest tests/ -v
        env:
          DATABASE_URL: postgresql+psycopg2://postgres:postgres@localhost:5432/test_db

  docker:
    needs: test
    runs-on: ubuntu-latest
    if: github.ref == 'refs/heads/main'
    
    steps:
      - uses: actions/checkout@v4
      
      - name: Build & Push
        run: |
          docker build -t ghcr.io/${{ github.repository }}:${{ github.sha }} .
          docker push ghcr.io/${{ github.repository }}:${{ github.sha }}
```

[Volver al ejercicio ↑](../capitulos/23-alembic.md#%F0%9F%94%B4-ejercicio-235)