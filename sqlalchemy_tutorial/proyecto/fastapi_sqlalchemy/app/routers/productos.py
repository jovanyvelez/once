"""
Endpoints REST para productos.
Demuestra:
  - CRUD completo
  - PATCH parcial con `exclude_unset=True`
  - response_model para evitar filtrar datos sensibles
  - Validación de Pydantic v2
"""
from decimal import Decimal
from typing import List, Optional

from fastapi import APIRouter, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

from app.database import SessionDep
from app.models import Producto
from app.schemas import ProductoCreate, ProductoPublic, ProductoUpdate

router = APIRouter(prefix="/productos", tags=["productos"])


@router.post(
    "/",
    response_model=ProductoPublic,
    status_code=status.HTTP_201_CREATED,
)
def crear(data: ProductoCreate, session: SessionDep) -> ProductoPublic:
    nuevo = Producto(**data.model_dump())
    try:
        session.add(nuevo)
        session.commit()
        session.refresh(nuevo)
    except IntegrityError:
        session.rollback()
        raise HTTPException(400, detail="SKU duplicado")
    return nuevo


@router.get("/", response_model=List[ProductoPublic])
def listar(
    session: SessionDep,
    offset: int = Query(0, ge=0, description="Salto inicial (paginación)"),
    limit: int = Query(50, ge=1, le=500, description="Máximo resultados"),
    categoria_id: Optional[int] = Query(None, description="Filtrar por categoría"),
    min_precio: Optional[Decimal] = Query(None, ge=0),
    max_precio: Optional[Decimal] = Query(None, ge=0),
    search: Optional[str] = Query(None, description="Buscar en nombre o SKU"),
) -> List[ProductoPublic]:
    stmt = select(Producto)

    # filtros dinámicos
    if categoria_id is not None:
        stmt = stmt.where(Producto.categoria_id == categoria_id)
    if min_precio is not None:
        stmt = stmt.where(Producto.precio >= min_precio)
    if max_precio is not None:
        stmt = stmt.where(Producto.precio <= max_precio)
    if search:
        patron = f"%{search}%"
        stmt = stmt.where(
            (Producto.nombre.ilike(patron)) | (Producto.sku.ilike(patron))
        )

    stmt = stmt.offset(offset).limit(limit).order_by(Producto.nombre)

    return list(session.scalars(stmt))


@router.get("/{producto_id}", response_model=ProductoPublic)
def obtener(producto_id: int, session: SessionDep) -> ProductoPublic:
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(404, detail="Producto no encontrado")
    return producto


@router.patch("/{producto_id}", response_model=ProductoPublic)
def actualizar(
    producto_id: int,
    data: ProductoUpdate,
    session: SessionDep,
) -> ProductoPublic:
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(404, detail="Producto no encontrado")

    # Solo actualizar los campos que vinieron en el body
    cambios = data.model_dump(exclude_unset=True)
    if not cambios:
        return producto  # no-op

    for campo, valor in cambios.items():
        setattr(producto, campo, valor)

    try:
        session.commit()
        session.refresh(producto)
    except IntegrityError:
        session.rollback()
        raise HTTPException(400, detail="SKU duplicado")

    return producto


@router.delete("/{producto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar(producto_id: int, session: SessionDep) -> None:
    producto = session.get(Producto, producto_id)
    if not producto:
        raise HTTPException(404, detail="Producto no encontrado")
    session.delete(producto)
    session.commit()
