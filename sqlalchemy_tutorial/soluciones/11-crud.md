# Soluciones — Capítulo 11: CRUD

[Volver al capítulo 11](../capitulos/11-crud.md)

---

## Ejercicio 11.1

**Crear y leer**

```python
from sqlalchemy import create_engine
from sqlalchemy.orm import Session


engine = create_engine("sqlite:///:memory:")
Base.metadata.create_all(engine)

with Session(engine) as session:
    # 1. Crear 3 productos
    productos = [
        Producto(nombre=f"Producto {i}", sku=f"SKU-{i}", precio=100 + i*10)
        for i in range(1, 4)
    ]
    session.add_all(productos)
    session.commit()

    # 2. Leer el primero
    p = session.get(Producto, 1)
    print(p)  # Producto(id=1, nombre='Producto 1', precio=110)
```

[Volver al ejercicio ↑](../capitulos/11-crud.md#%C2%B0-ejercicio-111)

---

## Ejercicio 11.2

**UPDATE masivo**

```python
from sqlalchemy import update


with Session(engine) as session:
    stmt = (
        update(Producto)
        .where(Producto.precio < 1000)
        .values(precio=Producto.precio * 1.15)
    )
    session.execute(stmt)
    session.commit()
```

Esto dispara **UNA sola query**: `UPDATE productos SET precio = precio * 1.15 WHERE precio < 1000`. Mucho más eficiente que traer todos los productos y modificarlos uno a uno.

[Volver al ejercicio ↑](../capitulos/11-crud.md#%C2%B1-ejercicio-112)

---

## Ejercicio 11.3

**DELETE con verificación**

```python
from sqlalchemy.exc import SQLAlchemyError


def eliminar_si_existe(session: Session, id: int) -> bool:
    """Elimina un producto. Retorna True si lo eliminó, False si no existía."""
    try:
        producto = session.get(Producto, id)
        if not producto:
            return False
        
        session.delete(producto)
        session.commit()
        return True
    except SQLAlchemyError:
        session.rollback()
        raise
```

[Volver al ejercicio ↑](../capitulos/11-crud.md#%C2%B1-ejercicio-113)

---

## Ejercicio 11.4

**Patrón Repository**

```python
from typing import List, Optional
from sqlalchemy import select
from sqlalchemy.orm import Session


class ClienteRepository:
    def __init__(self, session: Session):
        self.session = session

    def crear(self, nombre: str, email: str, saldo: float = 0.0) -> "Cliente":
        cliente = Cliente(nombre=nombre, email=email, saldo=saldo)
        self.session.add(cliente)
        self.session.commit()
        self.session.refresh(cliente)
        return cliente

    def obtener(self, id: int) -> Optional["Cliente"]:
        return self.session.get(Cliente, id)

    def listar(self, skip: int = 0, limit: int = 100) -> List["Cliente"]:
        stmt = select(Cliente).offset(skip).limit(limit)
        return list(self.session.scalars(stmt))

    def actualizar_saldo(self, id: int, nuevo_saldo: float) -> Optional["Cliente"]:
        if nuevo_saldo < 0:
            raise ValueError("El saldo no puede ser negativo")
        
        cliente = self.obtener(id)
        if not cliente:
            return None
        
        cliente.saldo = nuevo_saldo
        self.session.commit()
        self.session.refresh(cliente)
        return cliente


# Uso
with Session(engine) as session:
    repo = ClienteRepository(session)
    cliente = repo.crear("Ana", "ana@ejemplo.com", saldo=1000)
    repo.actualizar_saldo(cliente.id, 2000)
    clientes = repo.listar(limit=10)
```

[Volver al ejercicio ↑](../capitulos/11-crud.md#%C2%B1-ejercicio-114)

---

## Ejercicio 11.5

**Transacción atómica**

```python
def transferir_stock(
    session: Session,
    origen_id: int,
    destino_id: int,
    cantidad: int,
) -> bool:
    """Transfiere stock entre productos. Retorna True si fue exitosa."""
    try:
        origen = session.get(Producto, origen_id)
        destino = session.get(Producto, destino_id)

        if not origen or not destino:
            return False
        if cantidad <= 0:
            raise ValueError("cantidad debe ser positiva")
        if origen.stock < cantidad:
            return False

        # Operación atómica
        origen.stock -= cantidad
        destino.stock += cantidad

        session.commit()
        return True
    except Exception:
        session.rollback()
        return False
```

**Clave**: ambas modificaciones se hacen ANTES del commit. Si falla alguna, el `rollback` revierte las dos.

[Volver al ejercicio ↑](../capitulos/11-crud.md#%F0%9F%94%B4-ejercicio-115)