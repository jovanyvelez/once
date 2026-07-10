"""
Fixtures compartidas para los tests.

Cada test tiene una base de datos limpia (en memoria).
"""
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app as fastapi_app
import app.models  # noqa: F401  (registra modelos)


@pytest.fixture
def engine():
    """Engine de SQLite en memoria con StaticPool (para tests)."""
    eng = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(eng)
    yield eng
    eng.dispose()


@pytest.fixture
def session(engine):
    """Sesión de SQLAlchemy fresca por test."""
    SessionLocal = sessionmaker(bind=engine)
    with SessionLocal() as s:
        yield s


@pytest.fixture
def client(engine):
    """Cliente HTTP con la base en memoria."""
    TestingSessionLocal = sessionmaker(bind=engine)

    def override_get_db():
        with TestingSessionLocal() as session:
            yield session

    fastapi_app.dependency_overrides[get_db] = override_get_db
    with TestClient(fastapi_app) as c:
        yield c
    fastapi_app.dependency_overrides.clear()


@pytest.fixture
def categoria_sample(session: Session):
    """Categoría precargada para tests."""
    from app.models import Categoria

    cat = Categoria(nombre="Electrónica", descripcion="Productos electrónicos")
    session.add(cat)
    session.commit()
    session.refresh(cat)
    return cat
