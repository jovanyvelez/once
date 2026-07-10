"""
Importar todos los modelos para que SQLAlchemy los registre en `Base.metadata`.
Sin este import, `create_all` no genera ninguna tabla.
"""
from app.models.categoria import Categoria  # noqa: F401
from app.models.producto import Producto  # noqa: F401
