"""
Configuración del Engine y Session.
Aquí vive el patrón `get_db()` con `yield` y el alias `SessionDep`.

Ver capítulo 17 del manual para entender por qué este patrón.
"""
from typing import Annotated, Generator

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session

from app.config import get_settings

settings = get_settings()

# SQLite necesita check_same_thread=False para usarse con FastAPI
connect_args = {}
if settings.database_url.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(
    settings.database_url,
    connect_args=connect_args,
    echo=settings.debug,  # True imprime SQL por consola
)


class Base(DeclarativeBase):
    """Base de la cual heredan todos los modelos ORM."""


def get_db() -> Generator[Session, None, None]:
    """
    Generador que abre una sesión de DB por request.

    Garantiza:
      1. La sesión se abre al iniciar el endpoint.
      2. Se cierra al finalizar (incluso si hubo error).
    """
    with Session(engine) as session:
        yield session


# ✨ Alias moderno para usar en endpoints
SessionDep = Annotated[Session, Depends(get_db)]
