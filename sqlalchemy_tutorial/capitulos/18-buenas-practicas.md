# Capítulo 18: Buenas prácticas — lo que aprendes con la experiencia

> Cosas que separan a un junior de un senior.

---

## 18.1 Estructura de proyecto

```
mi_proyecto/
├── alembic/                        # migraciones (prod)
├── src/
│   ├── database.py                 # engine, Base, get_db
│   ├── models/                     # modelos ORM (uno por dominio)
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   └── producto.py
│   ├── schemas/                    # schemas Pydantic
│   ├── routers/                    # endpoints por recurso
│   ├── services/                   # lógica de negocio
│   ├── repositories/               # capa de acceso a datos
│   ├── tests/
│   ├── main.py
│   └── config.py
├── requirements.txt
└── README.md
```

### El patrón "capas"

```mermaid
flowchart LR
    Client[Cliente HTTP] --> Router
    Router[router/<br/>validar input/output] --> Service
    Service[service/<br/>reglas de negocio] --> Repository
    Repository[repository/<br/>queries ORM] --> Models
    Models[models/<br/>ORM puro] --> DB[(Base de datos)]

    style Router fill:#4A90E2,color:#fff
    style Service fill:#F5A623,color:#fff
    style Repository fill:#7ED321,color:#fff
    style Models fill:#BD10E0,color:#fff
```

| Capa | Su responsabilidad |
|---|---|
| **router** | Validar input, formatear output, errores HTTP. |
| **service** | Reglas de negocio (no sabe de HTTP). |
| **repository** | Queries y CRUD (no sabe de negocio). |
| **models** | ORM puro. |

> 🎓 **Consejo del profesor**: aunque parezca "mucho para algo chico", este patrón escala **muy bien** y testea con menos dolor.

---

## 18.2 Las reglas de oro del Senior Dev

### 1. 🧠 **Schemas separados**: nunca mezcles ORM y Pydantic

```python
# ❌ Mal: devolver ORM directamente
@app.get("/productos/{id}")
def obtener(producto_id: int, session: SessionDep):
    return session.get(Producto, producto_id)  # 💥 expone TODA la tabla

# ✅ Bien: response_model explícito
@app.get("/productos/{id}", response_model=ProductoPublic)
def obtener(producto_id: int, session: SessionDep):
    p = session.get(Producto, producto_id)
    if not p:
        raise HTTPException(404)
    return p   # Pydantic filtra solo los campos públicos
```

### 2. 🔁 **Siempre `commit()` o `rollback()`**

```python
# Mal:
with Session(engine) as session:
    session.add(objeto)  # si algo falla, queda en limbo

# Bien:
with Session(engine) as session:
    try:
        session.add(objeto)
        session.commit()
    except Exception:
        session.rollback()
        raise
```

### 3. 🚫 **Nunca** hagas `session.delete()` sin commit

```python
# Esto solo marca para borrar, NO lo borra
session.delete(objeto)
# Si salís sin commit, el objeto sigue en la DB
```

### 4. ⚡ **Evitá el problema N+1**

```python
# 🚫 problema N+1
for producto in session.scalars(select(Producto)):
    print(producto.categoria.nombre)   # un SELECT por cada producto

# ✅ una sola query
from sqlalchemy.orm import selectinload

stmt = select(Producto).options(selectinload(Producto.categoria))
for producto in session.scalars(stmt):
    print(producto.categoria.nombre)
```

### 5. 📚 **En producción: Alembic, no `create_all`**

`create_all` está perfecto para dev y tests. En producción necesitás:

- ✅ Migraciones incrementales.
- ✅ No perder datos.
- ✅ Control de versiones del schema.

```bash
pip install alembic
alembic init alembic
alembic revision --autogenerate -m "nueva columna"
alembic upgrade head
```

### 6. 🧪 **Tests con base en memoria**

```python
import pytest
from src.database import engine, Base

@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)
```

### 7. 📊 **Logs y observabilidad**

```python
import logging
logging.basicConfig()
logging.getLogger("sqlalchemy.engine").setLevel(logging.INFO)
```

En producción, conviene usar:
- `Sentry` o `Rollbar` para errores.
- `Prometheus + Grafana` para métricas.
- `OpenTelemetry` para tracing distribuido.

### 8. 🎯 **Nombres descriptivos**

```python
# 🟠 Confuso
u = session.get(U, 1)

# ✅ Claro
usuario_existente = session.get(Usuario, 1)
```

### 9. 🧹 **`with Session(engine) as session:` siempre que puedas**

```python
# 🟠 Mal
session = Session(engine)
session.add(...)
session.commit()
session.close()    # si falla antes, no se cierra

# ✅ Bien
with Session(engine) as session:
    session.add(...)
    session.commit()
# Cierre automático
```

### 10. 📖 **Documentá tu modelo**

```python
class Producto(Base):
    """Representa un producto en el catálogo."""
    __tablename__ = "productos"
    
    id: Mapped[int] = mapped_column(primary_key=True, doc="Identificador")
    nombre: Mapped[str] = mapped_column(String(100), doc="Nombre comercial")
    ...
```

---

## 18.3 Patrones avanzados

### Pattern: Repository

Encapsulá queries en una clase:

```python
from typing import Optional, List
from sqlalchemy import select
from sqlalchemy.orm import Session


class ProductoRepository:
    def __init__(self, session: Session):
        self.session = session
    
    def listar(self, skip: int = 0, limit: int = 100) -> List[Producto]:
        stmt = select(Producto).offset(skip).limit(limit)
        return list(self.session.scalars(stmt))
    
    def obtener(self, id: int) -> Optional[Producto]:
        return self.session.get(Producto, id)
    
    def buscar_por_sku(self, sku: str) -> Optional[Producto]:
        stmt = select(Producto).where(Producto.sku == sku)
        return self.session.scalars(stmt).first()
```

Uso:

```python
@app.get("/productos/")
def listar(session: SessionDep):
    repo = ProductoRepository(session)
    return repo.listar()
```

### Pattern: Service Layer

Lógica de negocio aislada de HTTP:

```python
class ProductoService:
    def __init__(self, repo: ProductoRepository):
        self.repo = repo
    
    def crear_o_validar(self, data: ProductoCreate) -> Producto:
        """Crea un producto validando unicidad del SKU."""
        if self.repo.buscar_por_sku(data.sku):
            raise ValueError("SKU ya existe")
        return self.repo.crear(**data.model_dump())
```

### Pattern: Dependency de autenticación

```python
from fastapi.security import OAuth2PasswordBearer

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_current_user(
    session: SessionDep,
    token: str = Depends(oauth2_scheme),
) -> Usuario:
    usuario = session.scalar(
        select(Usuario).where(Usuario.token == token)
    )
    if not usuario:
        raise HTTPException(401, "Token inválido")
    return usuario


UsuarioDep = Annotated[Usuario, Depends(get_current_user)]


@app.get("/perfil/")
def perfil(usuario: UsuarioDep):
    return {"nombre": usuario.nombre}
```

---

## 18.4 Performance

| Tip | Cuándo |
|---|---|
| Índices en columnas de `WHERE` y `ORDER BY` | Cuando filtras u ordenás por esa columna seguido. |
| `selectinload()` para relaciones 1—N | Cuando accedés a la lista de hijos. |
| `joinedload()` para 1—1 | Cuando siempre usás el padre. |
| `bulk_insert_mappings()` para inserciones masivas | Inserts de miles de filas. |
| `returning()` para hacer UPDATE/INSERT y devolver valores | Evitar `SELECT` adicional. |
| Particionado de tablas | Tablas con millones de filas. |

> ⚠️ **Importante**: medí antes de optimizar. Si una query funciona en 50ms, no la toques.

---

## 18.5 Seguridad

| Consejo | Detalle |
|---|---|
| **Nunca uses `f"..."` para SQL crudo**. | SQL Injection |
| **Validá inputs con Pydantic**. | Doble defensa. |
| **No expongas passwords en endpoints**. | Schemas `Public` separados. |
| **Usá variables de entorno para la URL de DB**. | `.env` con `pydantic-settings`. |
| **Limitá tamaño de requests**. | Pydantic ya lo hace. |
| **Rate limit** | Middleware o API gateway. |

### Ejemplo: URL de DB con variables de entorno

```python
# src/config.py
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = "sqlite:///./tienda.db"
    debug: bool = False


settings = Settings()  # lee de variables de entorno automáticamente
```

```python
engine = create_engine(settings.database_url, echo=settings.debug)
```

```bash
export DATABASE_URL="postgresql://user:pass@localhost/db"
```

---

## 18.6 Testing

```python
import pytest
from src.main import app
from fastapi.testclient import TestClient
from src.database import engine, Base


@pytest.fixture(autouse=True)
def reset_db():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


@pytest.fixture
def client():
    return TestClient(app)


def test_crear_producto(client):
    response = client.post("/productos/", json={
        "nombre": "Test",
        "sku": "TST-001",
        "precio": 100.0,
    })
    assert response.status_code == 201
    assert response.json()["nombre"] == "Test"


def test_listar_productos(client):
    client.post("/productos/", json={"nombre": "A", "sku": "A-1", "precio": 10})
    client.post("/productos/", json={"nombre": "B", "sku": "B-1", "precio": 20})
    
    response = client.get("/productos/")
    assert response.status_code == 200
    assert len(response.json()) == 2
```

---

## 🛠️ Ejercicios prácticos

### 🟢 Ejercicio 18.1: Aplicá las 10 reglas

Releé las [10 reglas de oro del Senior Dev](#182-las-reglas-de-oro-del-senior-dev). Para tu proyecto actual, maracá cuáles cumplís y cuáles no.

**Solución**: [soluciones/18-buenas-practicas.md](../soluciones/18-buenas-practicas.md#ejercicio-181)

---

### 🟡 Ejercicio 18.2: Implementá el patrón Repository

Convertí los endpoints CRUD de productos en un repositorio:

```python
class ProductoRepository:
    def __init__(self, session: Session): ...
    def listar(...): ...
    def obtener(...): ...
    # etc.
```

**Solución**: [soluciones/18-buenas-practicas.md](../soluciones/18-buenas-practicas.md#ejercicio-182)

---

### 🟡 Ejercicio 18.3: Implementá el patrón Service

Agregá una capa `ProductoService` que tenga la lógica de negocio (validación de precio, existencia de categoría, etc.). El router solo debe llamar al service.

**Solución**: [soluciones/18-buenas-practicas.md](../soluciones/18-buenas-practicas.md#ejercicio-183)

---

### 🟡 Ejercicio 18.4: URL de DB con variables de entorno

Convertí la URL hardcodeada a usar `pydantic-settings` y `.env`.

**Solución**: [soluciones/18-buenas-practicas.md](../soluciones/18-buenas-practicas.md#ejercicio-184)

---

### 🔴 Ejercicio 18.5: Detectá el anti-patrón

Este código tiene **3 anti-patrones** del capítulo. Encontrálos:

```python
@app.get("/productos/")
def listar(session: SessionDep):
    productos = session.scalars(select(Producto)).all()
    
    resultado = []
    for p in productos:
        resultado.append({
            "id": p.id,
            "nombre": p.nombre,
            "sku": p.sku,
            "precio": p.precio,
            "creado_en": str(p.creado_en),
            "categoria": p.categoria.nombre if p.categoria else None,  # 💥 N+1
            "password_hash_admin": "secret123",  # 💥 expone dato sensible
        })
    return resultado
```

**Solución**: [soluciones/18-buenas-practicas.md](../soluciones/18-buenas-practicas.md#ejercicio-185)

---

## 🎓 Lo que aprendiste

- Estructura de proyecto con capas (router/service/repository).
- 10 reglas de oro que te separan del junior.
- Patrones avanzados: Repository, Service, Auth con Depends.
- Tips de performance y seguridad.
- Testing básico con `TestClient` y fixtures.

## 📖 Siguiente

[Capítulo 19: Errores comunes y cómo solucionarlos →](./19-errores-comunes.md)