# Soluciones — Capítulo 18: Buenas prácticas

[Volver al capítulo 18](../capitulos/18-buenas-practicas.md)

---

## Ejercicio 18.1

**Aplicá las 10 reglas**

Para cada regla, maracá con ✅ (cumple) o ❌ (no cumple) y escribí qué harías para mejorar:

1. ✅/❌ Schemas separados (Base, Create, Public, Update)
2. ✅/❌ `try/except + rollback` en operaciones riesgosas
3. ✅/❌ `selectinload` / `joinedload` para evitar N+1
4. ✅/❌ `with Session(engine) as session:` siempre
5. ✅/❌ Alembic en producción (no `create_all`)
6. ✅/❌ Tests automatizados
7. ✅/❌ `response_model=` en endpoints
8. ✅/❌ `exclude_unset=True` en PATCH
9. ✅/❌ Repositorios / Services separados
10. ✅/❌ `.env` con `pydantic-settings`

[Volver al ejercicio ↑](../capitulos/18-buenas-practicas.md#%C2%B0-ejercicio-181)

---

## Ejercicio 18.2

**Patrón Repository**

```python
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session


class ProductoRepository:
    def __init__(self, session: Session):
        self.session = session

    def listar(
        self, skip: int = 0, limit: int = 100
    ) -> List[Producto]:
        stmt = select(Producto).offset(skip).limit(limit)
        return list(self.session.scalars(stmt))

    def obtener(self, id: int) -> Optional[Producto]:
        return self.session.get(Producto, id)

    def crear(self, **kwargs) -> Producto:
        producto = Producto(**kwargs)
        self.session.add(producto)
        self.session.commit()
        self.session.refresh(producto)
        return producto

    def eliminar(self, id: int) -> bool:
        producto = self.obtener(id)
        if not producto:
            return False
        self.session.delete(producto)
        self.session.commit()
        return True


# En el router
@router.get("/", response_model=List[ProductoPublic])
def listar(session: SessionDep, skip: int = 0, limit: int = 100):
    repo = ProductoRepository(session)
    return repo.listar(skip=skip, limit=limit)
```

[Volver al ejercicio ↑](../capitulos/18-buenas-practicas.md#%C2%B1-ejercicio-182)

---

## Ejercicio 18.3

**Patrón Service**

```python
from typing import Optional


class ProductoService:
    def __init__(self, repo: ProductoRepository):
        self.repo = repo

    def crear_producto(self, data: ProductoCreate) -> Producto:
        """Lógica de negocio: validar antes de persistir."""
        if data.precio <= 0:
            raise ValueError("El precio debe ser positivo")
        
        # Validar que la categoría existe
        if data.categoria_id is not None:
            categoria = self.repo.session.get(Categoria, data.categoria_id)
            if not categoria:
                raise ValueError("La categoría no existe")
        
        return self.repo.crear(**data.model_dump())

    def actualizar_producto(
        self, id: int, data: ProductoUpdate
    ) -> Optional[Producto]:
        cambios = data.model_dump(exclude_unset=True)
        if not cambios:
            return self.repo.obtener(id)
        
        producto = self.repo.obtener(id)
        if not producto:
            return None
        
        for campo, valor in cambios.items():
            setattr(producto, campo, valor)
        
        self.repo.session.commit()
        return producto


# En el router
@router.post("/", response_model=ProductoPublic)
def crear(data: ProductoCreate, session: SessionDep):
    repo = ProductoRepository(session)
    service = ProductoService(repo)
    
    try:
        return service.crear_producto(data)
    except ValueError as e:
        raise HTTPException(400, str(e))
```

[Volver al ejercicio ↑](../capitulos/18-buenas-practicas.md#%C2%B1-ejercicio-183)

---

## Ejercicio 18.4

**URL de DB con variables de entorno**

```python
# src/config.py
from functools import lru_cache
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    database_url: str = "sqlite:///./tienda.db"
    debug: bool = False
    secret_key: str = "change-me"
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )


@lru_cache
def get_settings() -> Settings:
    return Settings()


# src/database.py
from app.config import get_settings

settings = get_settings()
engine = create_engine(settings.database_url, echo=settings.debug)
```

`.env`:

```bash
DATABASE_URL=postgresql://user:pass@localhost/tienda
DEBUG=true
SECRET_KEY=mi-clave-secreta-de-32-chars
```

[Volver al ejercicio ↑](../capitulos/18-buenas-practicas.md#%C2%B1-ejercicio-184)

---

## Ejercicio 18.5

**Anti-patrones**

```python
# ❌ ANTI-PATRÓN 1: N+1
"categoria": p.categoria.nombre if p.categoria else None,
# Solución: usar .options(selectinload(Producto.categoria))

# ❌ ANTI-PATRÓN 2: expone datos sensibles
"password_hash_admin": "secret123",
# Solución: nunca incluir campos sensibles en response. Usar `response_model=`.

# ❌ ANTI-PATRÓN 3: dict manual en vez de response_model
# No se valida, no se documenta, no se filtra.
resultado.append({...})
# Solución: usar `response_model=List[ProductoPublic]`
```

**Versión corregida**:

```python
@router.get("/", response_model=List[ProductoPublic])
def listar(session: SessionDep):
    stmt = select(Producto).options(selectinload(Producto.categoria))
    return list(session.scalars(stmt))
```

[Volver al ejercicio ↑](../capitulos/18-buenas-practicas.md#%F0%9F%94%B4-ejercicio-185)