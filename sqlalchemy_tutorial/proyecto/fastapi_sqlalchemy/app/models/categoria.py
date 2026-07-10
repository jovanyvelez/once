"""
Modelo ORM `Categoria`. Ver capítulo 13 (Relaciones) para entender
cómo se conecta con Producto.
"""
from typing import TYPE_CHECKING, List

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.producto import Producto


class Categoria(Base, TimestampMixin):
    __tablename__ = "categorias"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), unique=True, index=True)
    descripcion: Mapped[str | None] = mapped_column(default=None)

    # 🔗 relación 1—N con productos
    productos: Mapped[List["Producto"]] = relationship(
        back_populates="categoria",
        cascade="all, delete-orphan",
    )
