"""
Configuración de la app usando Pydantic v2 + pydantic-settings.

Lee automáticamente las variables de entorno (o de un .env).
Ver capítulo 22 para más detalle sobre Pydantic Settings.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Configuración global de la aplicación."""

    database_url: str = "sqlite:///./tienda.db"
    debug: bool = False
    app_name: str = "Mi API de Tienda"

    # Configuración de Pydantic Settings: leer de .env, case-insensitive
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    """
    Singleton de configuración.

    `lru_cache` evita leer .env cada vez (solo se lee la primera vez).
    Útil para FastAPI si querés inyectar settings en una dependencia.
    """
    return Settings()
