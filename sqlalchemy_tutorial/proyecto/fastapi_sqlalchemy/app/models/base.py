"""
Mixin con columnas de auditoría compartidas.

Ver capítulo 7 (Mixins) del manual para entender esta sección.
"""
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column


class TimestampMixin:
    """Columnas `creado_en` y `actualizado_en` para todos los modelos."""

    creado_en: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        nullable=False,
    )
    actualizado_en: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
