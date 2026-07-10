"""
Punto de entrada de la aplicación FastAPI.
"""
from fastapi import FastAPI

from app.config import get_settings
from app.database import Base, engine
from app.routers import categorias_router, productos_router
import app.models  # noqa: F401  registra modelos en Base.metadata

settings = get_settings()


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="1.0.0",
        description="API REST moderna con FastAPI + SQLAlchemy 2.0",
    )

    # Solo para dev. En producción: usar Alembic.
    Base.metadata.create_all(bind=engine)

    # Routers
    app.include_router(productos_router)
    app.include_router(categorias_router)

    @app.get("/", tags=["meta"])
    def root():
        return {
            "app": settings.app_name,
            "docs": "/docs",
            "redoc": "/redoc",
        }

    @app.get("/health", tags=["meta"])
    def health():
        return {"status": "ok"}

    return app


app = create_app()
