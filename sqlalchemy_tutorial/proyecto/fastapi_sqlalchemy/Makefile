# =============================================================================
# Makefile: atajos para comandos comunes
# Usá `make <comando>` para ejecutar.
# =============================================================================

.PHONY: help build up down logs ps shell test migrate fresh

help:  ## Mostrar esta ayuda
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-15s\033[0m %s\n", $$1, $$2}'

build:  ## Construir la imagen Docker
	docker compose build

up:  ## Levantar todos los servicios (dev)
	docker compose up

up-d:  ## Levantar en background (detached)
	docker compose up -d

down:  ## Detener todos los servicios
	docker compose down

down-v:  ## Detener Y borrar volúmenes (⚠️ borra la DB)
	docker compose down -v

logs:  ## Ver logs de todos los servicios
	docker compose logs -f

logs-api:  ## Ver logs solo de la API
	docker compose logs -f api

ps:  ## Listar servicios corriendo
	docker compose ps

shell:  ## Abrir shell en el contenedor de la API
	docker compose exec api /bin/bash

shell-db:  ## Abrir psql en el contenedor de la DB
	docker compose exec db psql -U postgres -d tienda

test:  ## Correr tests
	docker compose exec api pytest tests/ -v

migrate:  ## Crear nueva migración (autogenerate)
	docker compose exec api alembic revision --autogenerate -m "$(msg)"

migrate-up:  ## Aplicar migraciones pendientes
	docker compose exec api alembic upgrade head

migrate-down:  ## Rollback una migración
	docker compose exec api alembic downgrade -1

fresh:  ## Borrar DB y empezar de cero (⚠️ PELIGRO: borra datos)
	docker compose down -v
	docker compose up -d