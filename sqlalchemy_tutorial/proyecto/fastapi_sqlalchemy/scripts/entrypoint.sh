#!/bin/sh
# =============================================================================
# entrypoint.sh
# Se ejecuta al iniciar el contenedor.
# Aplica migraciones y luego arranca la app.
# =============================================================================

set -e

echo "🐳 Iniciando contenedor FastAPI + SQLAlchemy"
echo "📅 $(date)"
echo "🐍 Python: $(python --version)"

# Esperar a que la DB esté lista (en compose, el otro servicio debe estar healthy)
echo "⏳ Esperando a la base de datos..."

# Loop simple: intenta conectar hasta 30 veces (1s cada una)
for i in $(seq 1 30); do
    if python -c "from app.database import engine; engine.connect().close()" 2>/dev/null; then
        echo "✅ Base de datos lista"
        break
    fi
    echo "  intento $i/30..."
    sleep 1
done

# Aplicar migraciones
echo "📦 Aplicando migraciones con Alembic..."
alembic upgrade head

# Ejecutar el comando pasado como argumento (CMD del Dockerfile)
echo "🚀 Iniciando aplicación: $@"
exec "$@"