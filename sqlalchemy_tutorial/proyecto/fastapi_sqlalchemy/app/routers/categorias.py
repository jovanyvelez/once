"""Endpoints REST para categorías."""
from typing import List

from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.database import SessionDep
from app.models import Categoria
from app.schemas import CategoriaCreate, CategoriaPublic

router = APIRouter(prefix="/categorias", tags=["categorias"])


@router.post(
    "/",
    response_model=CategoriaPublic,
    status_code=status.HTTP_201_CREATED,
)
def crear(data: CategoriaCreate, session: SessionDep) -> CategoriaPublic:
    nueva = Categoria(**data.model_dump())
    session.add(nueva)
    session.commit()
    session.refresh(nueva)
    return nueva


@router.get("/", response_model=List[CategoriaPublic])
def listar(session: SessionDep) -> List[CategoriaPublic]:
    return list(session.scalars(select(Categoria).order_by(Categoria.nombre)))


@router.delete("/{categoria_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(categoria_id: int, session: SessionDep) -> None:
    categoria = session.get(Categoria, categoria_id)
    if not categoria:
        raise HTTPException(404, "Categoría no encontrada")
    session.delete(categoria)
    session.commit()
