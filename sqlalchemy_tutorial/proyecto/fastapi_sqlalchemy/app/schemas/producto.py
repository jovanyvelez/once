"""
Schemas Pydantic v2 para Producto.
"""
from datetime import datetime
from decimal import Decimal
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.schemas.categoria import CategoriaPublic


class ProductoBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=100)
    sku: str = Field(min_length=1, max_length=20)
    precio: Decimal = Field(gt=0, max_digits=10, decimal_places=2)
    descripcion: Optional[str] = None
    categoria_id: Optional[int] = None


class ProductoCreate(ProductoBase):
    """Lo que el cliente envía al crear."""
    pass


class ProductoPublic(ProductoBase):
    """Lo que devolvemos al cliente."""
    id: int
    creado_en: datetime
    actualizado_en: datetime
    categoria: Optional[CategoriaPublic] = None

    model_config = ConfigDict(from_attributes=True)


class ProductoUpdate(BaseModel):
    """PATCH: todos los campos opcionales."""
    nombre: Optional[str] = Field(default=None, min_length=1, max_length=100)
    sku: Optional[str] = Field(default=None, min_length=1, max_length=20)
    precio: Optional[Decimal] = Field(default=None, gt=0)
    descripcion: Optional[str] = None
    categoria_id: Optional[int] = None
