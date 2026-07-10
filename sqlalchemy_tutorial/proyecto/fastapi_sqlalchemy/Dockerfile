# =============================================================================
# Dockerfile para FastAPI + SQLAlchemy 2.0
# Multi-stage build para imagen final pequeña y segura
# =============================================================================

# -----------------------------------------------------------------------------
# Stage 1: builder
# Instala dependencias en un entorno con compiladores
# -----------------------------------------------------------------------------
FROM python:3.12-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

WORKDIR /app

# Instalar dependencias de compilación (luego se descartan)
RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar solo requirements primero (mejor cache de capas)
COPY requirements.txt .

# Instalar en un prefix que podamos copiar
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt


# -----------------------------------------------------------------------------
# Stage 2: runtime
# Imagen final pequeña, sin compiladores, usuario no-root
# -----------------------------------------------------------------------------
FROM python:3.12-slim AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/install/bin:$PATH" \
    PYTHONPATH="/install/lib/python3.12/site-packages"

# Solo lo necesario para correr psycopg2
RUN apt-get update && apt-get install -y --no-install-recommends \
        libpq5 \
        curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar las dependencias instaladas desde el builder
COPY --from=builder /install /install

# Crear usuario no-root (seguridad)
RUN groupadd -r appuser && useradd -r -g appuser --uid 1000 appuser

# Copiar código de la app
COPY app/ ./app/
COPY alembic.ini* ./
COPY scripts/ ./scripts/

# Copiar requirements.txt por si Alembic lo necesita
COPY requirements.txt .

# Hacer ejecutables los scripts
RUN chmod +x scripts/*.sh 2>/dev/null || true

# Cambiar ownership al usuario no-root
RUN chown -R appuser:appuser /app
USER appuser

EXPOSE 8000

# Healthcheck: verifica que la app responde
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -fsS http://localhost:8000/health || exit 1

# Comando por defecto
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]