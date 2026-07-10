"""
Modelo ORM `Producto`. Ver capítulo 13 (Relaciones) para entender
la relación N—1 con Categoria.
"""
from decimal import Decimal
from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base
from app.models.base import TimestampMixin

if TYPE_CHECKING:
    from app.models.categoria import Categoria


class Producto(Base, TimestampMixin):
    __tablename__ = "productos"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100), index=True)
    sku: Mapped[str] = mapped_column(String(20), unique=True, index=True)
    precio: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    descripcion: Mapped[Optional[str]] = mapped_column(default=None)

    # 🔗 relación N—1 con Categoria
    categoria_id: Mapped[int | None] = mapped_column(
        ForeignKey("categorias.id"), default=None
    )
    categoria: Mapped["Categoria | None"] = relationship(
        back_populates="productos",
        lazy="selectin",  # evita N+1 al listar
    )
