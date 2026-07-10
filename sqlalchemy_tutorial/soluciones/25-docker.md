# Soluciones — Capítulo 25: Deploy con Docker

[Volver al capítulo 25](../capitulos/25-docker.md)

---

## Ejercicio 25.1

**Tu primer Dockerfile**

```python
# app.py
print("¡Hola desde Docker!")
```

```dockerfile
# Dockerfile
FROM python:3.12-slim

WORKDIR /app
COPY app.py .

CMD ["python", "app.py"]
```

```bash
docker build -t mi-app:1.0 .
docker run --rm mi-app:1.0
# -> ¡Hola desde Docker!
```

[Volver al ejercicio ↑](../capitulos/25-docker.md#%C2%B0-ejercicio-251)

---

## Ejercicio 25.2

**Compose simple**

```yaml
# docker-compose.yml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
      POSTGRES_DB: tienda
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U postgres -d tienda"]
      interval: 5s
      timeout: 5s
      retries: 10

  app:
    build: .
    depends_on:
      db:
        condition: service_healthy
    environment:
      DATABASE_URL: postgresql+psycopg2://postgres:postgres@db:5432/tienda
    ports:
      - "8000:8000"

volumes:
  pgdata:
```

[Volver al ejercicio ↑](../capitulos/25-docker.md#%C2%B1-ejercicio-252)

---

## Ejercicio 25.3

**Multi-stage build**

```dockerfile
# syntax=docker/dockerfile:1.6
FROM python:3.12-slim AS builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

FROM python:3.12-slim
COPY --from=builder /install /install

WORKDIR /app
COPY app.py .

CMD ["python", "app.py"]
```

Comparación de tamaño:

```bash
docker build -t single -f Dockerfile.single .
docker build -t multi -f Dockerfile.multi .

docker images | grep -E 'single|multi'
```

Típicamente el multi-stage es **50-70% más pequeño**.

[Volver al ejercicio ↑](../capitulos/25-docker.md#%C2%B1-ejercicio-253)

---

## Ejercicio 25.4

**Healthcheck**

```python
# main.py
from fastapi import FastAPI

app = FastAPI()


@app.get("/health")
def health():
    return {"status": "ok"}
```

```dockerfile
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -fsS http://localhost:8000/health || exit 1
```

Verificar:

```bash
docker run -d -p 8000:8000 --name test mi-app
docker inspect --format='{{.State.Health.Status}}' test
# -> "healthy" después de 10s

docker stop test
```

[Volver al ejercicio ↑](../capitulos/25-docker.md#%C2%B1-ejercicio-254)

---

## Ejercicio 25.5

**Entrypoint con migración**

```bash
#!/bin/sh
# entrypoint.sh
set -e

echo "Esperando a la DB..."
for i in $(seq 1 30); do
    if python -c "from app.database import engine; engine.connect().close()" 2>/dev/null; then
        break
    fi
    sleep 1
done

echo "Aplicando migraciones..."
alembic upgrade head

echo "Iniciando Uvicorn..."
exec "$@"
```

```dockerfile
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh
ENTRYPOINT ["/entrypoint.sh"]
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

[Volver al ejercicio ↑](../capitulos/25-docker.md#%C2%B1-ejercicio-255)

---

## Ejercicio 25.6

**CI/CD con GitHub Actions**

```yaml
# .github/workflows/deploy.yml
name: Build & Push

on:
  push:
    branches: [main]

jobs:
  build:
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write

    steps:
      - uses: actions/checkout@v4

      - name: Login to GHCR
        uses: docker/login-action@v3
        with:
          registry: ghcr.io
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ghcr.io/${{ github.repository }}:latest
            ghcr.io/${{ github.repository }}:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max
```

[Volver al ejercicio ↑](../capitulos/25-docker.md#%F0%9F%94%B4-ejercicio-256)