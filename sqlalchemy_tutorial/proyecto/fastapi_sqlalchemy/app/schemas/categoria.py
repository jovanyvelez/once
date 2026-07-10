"""
Schemas Pydantic v2 para Categoria.
Patrón Base / Create / Public explicado en capítulo 17.
"""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CategoriaBase(BaseModel):
    nombre: str = Field(min_length=1, max_length=50)
    descripcion: Optional[str] = None


class CategoriaCreate(CategoriaBase):
    """Lo que el cliente envía al crear."""
    pass


class CategoriaPublic(CategoriaBase):
    """Lo que devolvemos al cliente."""
    id: int
    creado_en: datetime
    actualizado_en: datetime

    # Permite leer atributos de objetos ORM
    model_config = ConfigDict(from_attributes=True)
