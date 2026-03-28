# Curso Completo: CRUD E-Commerce con FastAPI, SQLModel y AsyncPG

## 20 Sesiones (40 Horas)

---

# PARTE 1: FUNDAMENTOS Y CRUD BÁSICO

---

# CONTEXTO DEL PROYECTO: Tienda Online "MarketHub"

## Descripción del Negocio

**MarketHub** es una plataforma de e-commerce que permite a múltiples vendedores ofrecer productos categorizedos a clientes. El sistema maneja el catálogo de productos, órdenes de compra, seguimiento de inventario y un sistema de etiquetas para búsqueda avanzada.

## Modelo de Datos Completo

```mermaid
erDiagram
    USUARIOS {
        int id PK
        string email
        string nombre
        string password_hash
        string rol
        bool is_active
        datetime created_at
    }

    VENDEDORES {
        int id PK
        int usuario_id FK
        string nombre_tienda
        string descripcion
        string telefono
        decimal rating
        bool is_verified
        datetime created_at
    }

    PRODUCTOS {
        int id PK
        int vendedor_id FK
        int categoria_id FK
        string nombre
        string descripcion
        decimal precio
        int stock
        bool is_active
        datetime created_at
    }

    CATEGORIAS {
        int id PK
        string nombre
        string slug
        string descripcion
        int parent_id FK
    }

    ETIQUETAS {
        int id PK
        string nombre
        string slug
        string color
    }

    PRODUCTO_ETIQUETA {
        int producto_id FK
        int etiqueta_id FK
    }

    ORDENES {
        int id PK
        int usuario_id FK
        string status
        decimal total
        datetime fecha_creacion
        datetime fecha_updated
    }

    ORDEN_ITEMS {
        int id PK
        int orden_id FK
        int producto_id FK
        int cantidad
        decimal precio_unitario
    }

    USUARIOS ||--o{ ORDENES : "1:N"
    VENDEDORES ||--o{ PRODUCTOS : "1:N"
    CATEGORIAS ||--o{ PRODUCTOS : "1:N"
    CATEGORIAS ||--o{ CATEGORIAS : "1:N (subcategorías)"
    ORDENES ||--o{ ORDEN_ITEMS : "1:N"
    ORDEN_ITEMS }o--|| PRODUCTOS : "N:1"
    PRODUCTOS }o--o{ ETIQUETAS : "N:M"
```

## Resumen de Relaciones

| Relación | Tipo | Descripción |
|----------|------|-------------|
| Usuario → Órdenes | 1:N | Un usuario puede tener muchas órdenes |
| Vendedor → Productos | 1:N | Un vendedor puede tener muchos productos |
| Categoría → Productos | 1:N | Una categoría agrupa muchos productos |
| Categoría → Subcategorías | 1:N | Autoreferencia para jerarquía |
| Orden → OrdenItems | 1:N | Una orden tiene muchos items |
| Producto ↔ Etiqueta | N:M | Muchos productos pueden tener muchas etiquetas |

## Stack Tecnológico

- **PostgreSQL 14+**: Base de datos relacional
- **AsyncPG**: Driver asíncrono para PostgreSQL
- **SQLModel**: ORM que combina Pydantic + SQLAlchemy
- **FastAPI**: Framework web de alto rendimiento
- **Uvicorn**: Servidor ASGI

## Estructura del Proyecto

```
marketHub/
├── app/
│   ├── __init__.py
│   ├── main.py              # App principal FastAPI
│   ├── config.py            # Configuración con pydantic-settings
│   ├── database/
│   │   ├── __init__.py
│   │   └── connection.py    # Async engine + session
│   ├── models/
│   │   ├── __init__.py
│   │   ├── usuario.py       # Modelo Usuario
│   │   ├── vendedor.py      # Modelo Vendedor
│   │   ├── producto.py      # Modelo Producto
│   │   ├── categoria.py     # Modelo Categoría
│   │   ├── etiqueta.py       # Modelo Etiqueta
│   │   ├── orden.py          # Modelo Orden
│   │   └── orden_item.py     # Modelo OrdenItem
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── vendedor.py
│   │   ├── producto.py
│   │   ├── categoria.py
│   │   ├── etiqueta.py
│   │   └── orden.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── usuario.py
│   │   ├── producto.py
│   │   └── orden.py
│   ├── routes/
│   │   ├── __init__.py
│   │   ├── usuarios.py
│   │   ├── productos.py
│   │   ├── categorias.py
│   │   ├── etiquetas.py
│   │   └── ordenes.py
│   └── exceptions/
│       └── handlers.py
├── tests/
│   ├── conftest.py
│   ├── test_usuarios.py
│   ├── test_productos.py
│   └── test_ordenes.py
├── alembic/
│   ├── ini
│   └── versions/
├── requirements.txt
├── .env
└── README.md
```

---

# SESIÓN 1: Fundamentos de Bases de Datos y SQL

## Duración: 2 horas

## Objetivos de Aprendizaje

Al finalizar esta sesión, el estudiante será capaz de:
- Comprender qué es una base de datos relacional y por qué PostgreSQL
- Explicar los conceptos de tablas, filas, columnas, claves primarias y foráneas
- Escribir consultas SQL básicas: SELECT, INSERT, UPDATE, DELETE
- Entender los tipos de relaciones entre tablas

## 1.1 ¿Qué es una Base de Datos Relacional?

Una **base de datos relacional** organiza los datos en **tablas** (relaciones) compuestas de:
- **Filas** (registros/tuplas): cada entrada individual
- **Columnas** (campos/atributos): un dato específico de cada entrada

PostgreSQL es un sistema de base de datos relacional open-source conocido por:
- Soporte completo de SQL estándar
- Tipos de datos avanzados (JSON, arrays, rangos)
- Índices powerful
- Control de concurrencia multiv rsión (MVCC)
- Búsqueda de texto completo

## 1.2 Creación de Tablas con SQL

```sql
-- Crear tabla de usuarios
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,           -- Autoincremento
    email VARCHAR(255) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    rol VARCHAR(20) DEFAULT 'cliente',  -- 'cliente' | 'admin'
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla de categorías (con autoreferencia)
CREATE TABLE categorias (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    slug VARCHAR(100) NOT NULL UNIQUE,
    descripcion TEXT,
    parent_id INTEGER REFERENCES categorias(id),  -- Autoreferencia
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla de vendedores
CREATE TABLE vendedores (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
    nombre_tienda VARCHAR(200) NOT NULL,
    descripcion TEXT,
    telefono VARCHAR(20),
    rating DECIMAL(3,2) DEFAULT 0.00,
    is_verified BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla de productos
CREATE TABLE productos (
    id SERIAL PRIMARY KEY,
    vendedor_id INTEGER NOT NULL REFERENCES vendedores(id),
    categoria_id INTEGER REFERENCES categorias(id),
    nombre VARCHAR(200) NOT NULL,
    descripcion TEXT,
    precio DECIMAL(10,2) NOT NULL CHECK (precio >= 0),
    stock INTEGER NOT NULL DEFAULT 0 CHECK (stock >= 0),
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Crear tabla de etiquetas
CREATE TABLE etiquetas (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    slug VARCHAR(50) NOT NULL UNIQUE,
    color VARCHAR(7) DEFAULT '#6366f1'  -- Hex color
);

-- Tabla intermedia para relación N:M (Producto ↔ Etiqueta)
CREATE TABLE producto_etiqueta (
    producto_id INTEGER REFERENCES productos(id) ON DELETE CASCADE,
    etiqueta_id INTEGER REFERENCES etiquetas(id) ON DELETE CASCADE,
    PRIMARY KEY (producto_id, etiqueta_id)
);

-- Crear tabla de órdenes
CREATE TABLE ordenes (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id),
    status VARCHAR(20) DEFAULT 'pendiente'
        CHECK (status IN ('pendiente', 'pagado', 'enviado', 'entregado', 'cancelado')),
    total DECIMAL(10,2) NOT NULL DEFAULT 0,
    fecha_creacion TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    fecha_updated TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Tabla intermedia para relación N:M (Orden ↔ Producto)
CREATE TABLE orden_items (
    id SERIAL PRIMARY KEY,
    orden_id INTEGER NOT NULL REFERENCES ordenes(id) ON DELETE CASCADE,
    producto_id INTEGER NOT NULL REFERENCES productos(id),
    cantidad INTEGER NOT NULL CHECK (cantidad > 0),
    precio_unitario DECIMAL(10,2) NOT NULL
);
```

## 1.3 Operaciones CRUD en SQL

### CREATE - Insertar Datos

```sql
-- Insertar un usuario
INSERT INTO usuarios (email, nombre, password_hash, rol)
VALUES ('maria@example.com', 'María García', 'hashed_password123', 'cliente');

-- Insertar múltiples usuarios
INSERT INTO usuarios (email, nombre, password_hash)
VALUES
    ('juan@example.com', 'Juan Pérez', 'hash456'),
    ('ana@example.com', 'Ana López', 'hash789');

-- Insertar con valores por defecto
INSERT INTO categorias (nombre, slug, descripcion)
VALUES ('Electrónica', 'electronica', 'Productos electrónicos y tecnológicos');

-- Insertar subcategoría
INSERT INTO categorias (nombre, slug, parent_id)
VALUES ('Smartphones', 'smartphones', 1);  -- parent_id = id de Electrónica
```

### READ - Leer Datos

```sql
-- Seleccionar todos los usuarios
SELECT * FROM usuarios;

-- Seleccionar columnas específicas
SELECT email, nombre, rol FROM usuarios;

-- Filtrar con WHERE
SELECT * FROM usuarios WHERE rol = 'cliente' AND is_active = TRUE;

-- Ordenar resultados
SELECT * FROM productos ORDER BY precio DESC;

-- Limitar resultados
SELECT * FROM productos ORDER BY created_at DESC LIMIT 10;

-- Contar registros
SELECT COUNT(*) as total_productos FROM productos;

-- Agregación
SELECT
    COUNT(*) as total,
    AVG(precio) as precio_promedio,
    SUM(stock) as stock_total
FROM productos;

-- Buscar con LIKE
SELECT * FROM productos WHERE nombre LIKE '%iphone%';

-- Buscar con ILIKE (case insensitive)
SELECT * FROM productos WHERE nombre ILIKE '%samsung%';
```

### UPDATE - Actualizar Datos

```sql
-- Actualizar un registro
UPDATE usuarios
SET nombre = 'María García López'
WHERE email = 'maria@example.com';

-- Actualizar múltiples campos
UPDATE productos
SET precio = 999.99, stock = 50
WHERE id = 1;

-- Actualizar con cálculo
UPDATE productos
SET stock = stock - 1
WHERE id = 1 AND stock > 0;
```

### DELETE - Eliminar Datos

```sql
-- Eliminar un registro
DELETE FROM usuarios WHERE id = 5;

-- Eliminar con condición
DELETE FROM ordenes WHERE status = 'cancelado' AND fecha_creacion < '2024-01-01';

-- No eliminarás filas que tengan foreign keys referenciándolas
-- sin antes manejar esas referencias (ON DELETE)
```

## 1.4 Claves Primarias y Foráneas

```sql
-- PRIMARY KEY: Identificador único de cada fila
-- Se crea automáticamente un índice único

-- FOREIGN KEY: Referencia a la primary key de otra tabla
-- Garantiza integridad referencial

-- Ejemplo de integridad referencial:
-- Intentemos insertar un vendedor con usuario_id que no existe:
INSERT INTO vendedores (usuario_id, nombre_tienda)
VALUES (999, 'Mi Tienda');  -- ERROR: foreign key violation

-- Primero creamos el usuario:
INSERT INTO usuarios (email, nombre, password_hash)
VALUES ('vendedor@example.com', 'Vendedor Uno', 'hash');
-- Retorna: id = 1

-- Ahora podemos crear el vendedor:
INSERT INTO vendedores (usuario_id, nombre_tienda)
VALUES (1, 'Mi Tienda Tech');
```

## 1.5 Consultas con JOIN

```sql
-- INNER JOIN: Solo filas con coincidencia en ambas tablas
SELECT
    p.nombre AS producto,
    p.precio,
    v.nombre_tienda AS vendedor
FROM productos p
INNER JOIN vendedores v ON p.vendedor_id = v.id;

-- LEFT JOIN: Todas las filas de la izquierda + coincidencia de la derecha
SELECT
    p.nombre AS producto,
    c.nombre AS categoria
FROM productos p
LEFT JOIN categorias c ON p.categoria_id = c.id;

-- Contar productos por categoría (incluyendo categorías sin productos)
SELECT
    c.nombre,
    COUNT(p.id) AS total_productos
FROM categorias c
LEFT JOIN productos p ON c.id = p.categoria_id
GROUP BY c.id, c.nombre
ORDER BY total_productos DESC;

-- JOIN múltiples tablas
SELECT
    o.id AS orden_id,
    u.nombre AS cliente,
    p.nombre AS producto,
    oi.cantidad,
    oi.precio_unitario
FROM ordenes o
INNER JOIN usuarios u ON o.usuario_id = u.id
INNER JOIN orden_items oi ON o.id = oi.orden_id
INNER JOIN productos p ON oi.producto_id = p.id
WHERE o.status = 'pagado';
```

## 1.6 Subconsultas

```sql
-- Productos con precio mayor al promedio
SELECT * FROM productos
WHERE precio > (SELECT AVG(precio) FROM productos);

-- Usuarios que han realizado órdenes
SELECT * FROM usuarios
WHERE id IN (SELECT DISTINCT usuario_id FROM ordenes);

-- Producto más caro de cada vendedor
SELECT * FROM productos p1
WHERE precio = (
    SELECT MAX(precio) FROM productos p2 WHERE p2.vendedor_id = p1.vendedor_id
);
```

## Ejercicios Prácticos

**Ejercicio 1**: Crear las tablas para un sistema de reseñas de productos.

```sql
-- Tabla: reseñas
-- - id (PK)
-- - producto_id (FK)
-- - usuario_id (FK)
-- - rating (1-5)
-- - comentario (TEXT)
-- - fecha_creacion
```

**Ejercicio 2**: Escribir consultas para:
1. Contar cuántos productos tiene cada vendedor
2. Encontrar el producto más caro por categoría
3. Listar todas las órdenes con el nombre del cliente

---

# SESIÓN 2: Python Asíncrono y AsyncIO

## Duración: 2 horas

## Objetivos de Aprendizaje

- Comprender la diferencia entre programación síncrona y asíncrona
- Dominar async/await en Python
- Entender el event loop y las coroutines
- Aplicar patrones async en operaciones de base de datos

## 2.1 Programación Síncrona vs Asíncrona

### Síncrono (Bloqueante)

```python
# código_sincrono.py
import time

def descargar_datos(id):
    """Simula una operación de red/bd que toma tiempo."""
    print(f"Iniciando descarga {id}")
    time.sleep(2)  # Bloquea todo el hilo por 2 segundos
    print(f"Descarga {id} completada")
    return f"Datos {id}"

def main():
    start = time.time()
    # Ejecuta secuencialmente: 6 segundos total
    resultado1 = descargar_datos(1)
    resultado2 = descargar_datos(2)
    resultado3 = descargar_datos(3)
    elapsed = time.time() - start
    print(f"Tiempo total: {elapsed:.2f}s")

main()
# Salida:
# Iniciando descarga 1
# Descarga 1 completada
# Iniciando descarga 2
# Descarga 2 completada
# Iniciando descarga 3
# Descarga 3 completada
# Tiempo total: 6.00s
```

### Asíncrono (No Bloqueante)

```python
# codigo_asincrono.py
import asyncio
import time

async def descargar_datos(id: int) -> str:
    """Simula operación async (I/O-bound)."""
    print(f"Iniciando descarga {id}")
    await asyncio.sleep(2)  # No bloquea, cede control al event loop
    print(f"Descarga {id} completada")
    return f"Datos {id}"

async def main():
    start = time.time()
    # Ejecuta concurrentemente: ~2 segundos total
    # create_task programa la ejecución pero no espera
    task1 = asyncio.create_task(descargar_datos(1))
    task2 = asyncio.create_task(descargar_datos(2))
    task3 = asyncio.create_task(descargar_datos(3))

    # Ahora esperamos todas en paralelo
    resultado1 = await task1
    resultado2 = await task2
    resultado3 = await task3

    elapsed = time.time() - start
    print(f"Tiempo total: {elapsed:.2f}s")
    print(f"Resultados: {resultado1}, {resultado2}, {resultado3}")

# Ejecutar con event loop
asyncio.run(main())
# Salida:
# Iniciando descarga 1
# Iniciando descarga 2
# Iniciando descarga 3
# (2 segundos de espera)
# Descarga 1 completada
# Descarga 2 completada
# Descarga 3 completada
# Tiempo total: 2.00s
```

## 2.2 Conceptos Fundamentales de AsyncIO

### Coroutines (Coroutines)

```python
# Las funciones async son "coroutines" - funciones que pueden pausar su ejecución
async def greet(name: str) -> str:
    return f"Hola, {name}!"

# Llamar una coroutine NO la ejecuta, devuelve un objeto coroutine
coro = greet("María")
print(type(coro))  # <class 'coroutine'>

# Para ejecutarla, necesitamos await o asyncio.run()
result = asyncio.run(coro)
print(result)  # Hola, María!
```

### Await y el Event Loop

```python
async def operacion_lenta():
    print("Antes del await")
    await asyncio.sleep(1)  # Pausa aquí, permite otras tareas
    print("Después del await")
    return "resultado"

async def main():
    # Sequential await: secuencial, ~2 segundos
    r1 = await operacion_lenta()
    r2 = await operacion_lenta()

    # Parallel con create_task: ~1 segundo
    t1 = asyncio.create_task(operacion_lenta())
    t2 = asyncio.create_task(operacion_lenta())
    r3 = await t1
    r4 = await t2

asyncio.run(main())
```

### Gather - Ejecutar Múltiples Coroutines

```python
async def obtener_usuario(user_id: int) -> dict:
    await asyncio.sleep(0.5)
    return {"id": user_id, "nombre": f"Usuario {user_id}"}

async def obtener_productos(categoria: str) -> list:
    await asyncio.sleep(0.3)
    return [f"Producto {categoria} 1", f"Producto {categoria} 2"]

async def main():
    # Ejecuta múltiples coroutines concurrentemente
    resultados = await asyncio.gather(
        obtener_usuario(1),
        obtener_usuario(2),
        obtener_productos("electronics")
    )

    # resultados es una lista con los resultados en orden
    usuario1, usuario2, productos = resultados
    print(f"{usuario1}, {usuario2}, productos: {productos}")

asyncio.run(main())
```

### Wait - Similar a Gather pero con Control

```python
async def tarea_larga():
    await asyncio.sleep(3)
    return "completada"

async def tarea_corta():
    await asyncio.sleep(1)
    return "rápida"

async def main():
    # Ejecutar ambas, pero podemos hacer otras cosas mientras esperamos
    long_task = asyncio.create_task(tarea_larga())
    short_task = asyncio.create_task(tarea_corta())

    # done, pending = await asyncio.wait([long_task, short_task])
    # wait retorna cuando TODAS completan (o según timeout)

    # También podemos esperar solo la primera
    done, pending = await asyncio.wait(
        [long_task, short_task],
        return_when=asyncio.FIRST_COMPLETED
    )

    for task in done:
        print(f"Tarea completada: {task.result()}")

asyncio.run(main())
```

## 2.3 Async para Operaciones de Base de Datos

### Sin Async vs Con Async

```python
# ❌ Operaciones síncronas (bloqueantes)
import psycopg2

def obtener_usuarios():
    conn = psycopg2.connect("postgresql://...")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conn.close()
    return usuarios

# Durante el execute() y fetchall() el hilo está BLOQUEADO
# No puede procesar otras requests mientras espera la BD

# ✅ Operaciones asíncronas (no bloqueantes)
import asyncpg

async def obtener_usuarios():
    conn = await asyncpg.connect("postgresql://...")
    usuarios = await conn.fetch("SELECT * FROM usuarios")
    await conn.close()
    return usuarios

# Durante el await la aplicación puede procesar otras requests
# Ideal para servidores web con alta concurrencia
```

### Pool de Conexiones Async

```python
import asyncpg
from contextlib import asynccontextmanager

# Crear pool de conexiones
pool = None

async def setup_pool():
    global pool
    pool = await asyncpg.create_pool(
        host="localhost",
        port=5432,
        user="postgres",
        password="password",
        database="marketdb",
        min_size=5,      # Conexiones mínimas
        max_size=20      # Conexiones máximas
    )

async def close_pool():
    await pool.close()

# Usar el pool
async def obtener_usuario_por_id(user_id: int) -> dict:
    async with pool.acquire() as conn:
        # acquire obtiene una conexión del pool
        # al salir del context manager se devuelve al pool
        usuario = await conn.fetchrow(
            "SELECT id, email, nombre FROM usuarios WHERE id = $1",
            user_id
        )
        return dict(usuario) if usuario else None

# Ejecutar múltiples queries concurrentemente
async def obtener_multiples_usuarios(user_ids: list[int]) -> list[dict]:
    async with pool.acquire() as conn:
        # fetchmany, fetchall, fetchrow
        usuarios = await conn.fetch(
            "SELECT id, email FROM usuarios WHERE id = ANY($1)",
            user_ids
        )
        return [dict(u) for u in usuarios]

# Ejecutar queries concurrentemente usando el pool
async def main():
    await setup_pool()

    # Queries concurrentes - todas usan conexiones del pool
    results = await asyncio.gather(
        obtener_usuario_por_id(1),
        obtener_usuario_por_id(2),
        obtener_usuario_por_id(3),
    )

    print(results)

    await close_pool()

asyncio.run(main())
```

### Transacciones con Async

```python
async def crear_ordenYPago(usuario_id: int, productos: list[dict]):
    """
    Crea una orden y procesa el pago atómicamente.
    Si algo falla, todo se revierte.
    """
    async with pool.acquire() as conn:
        # Iniciar transacción
        async with conn.transaction():
            # 1. Crear la orden
            orden = await conn.fetchrow(
                """
                INSERT INTO ordenes (usuario_id, status, total)
                VALUES ($1, 'pendiente', 0)
                RETURNING id
                """,
                usuario_id
            )
            orden_id = orden['id']

            total = 0

            # 2. Crear items y calcular total
            for producto in productos:
                item = await conn.fetchrow(
                    """
                    INSERT INTO orden_items (orden_id, producto_id, cantidad, precio_unitario)
                    VALUES ($1, $2, $3, $4)
                    RETURNING id
                    """,
                    orden_id,
                    producto['producto_id'],
                    producto['cantidad'],
                    producto['precio']
                )
                total += producto['cantidad'] * producto['precio']

            # 3. Actualizar total y status
            await conn.execute(
                """
                UPDATE ordenes SET total = $1, status = 'pagado'
                WHERE id = $2
                """,
                total,
                orden_id
            )

            return orden_id

    # Si algo falla, el transaction() hace ROLLBACK automáticamente
```

## 2.4 Errores Comunes en Async

```python
# ❌ ERROR: Llamar función async sin await
async def obtener():
    return "datos"

result = obtener()  # Esto es un objeto coroutine, no el resultado!
print(result)  # <coroutine object obtener at ...>

# ✅ CORRECTO
result = await obtener()

# ❌ ERROR: Usar time.sleep() en código async
async def mala_practica():
    time.sleep(5)  # BLOQUEA el event loop!

# ✅ CORRECTO
async def buena_practica():
    await asyncio.sleep(5)  # Cede el control al event loop

# ❌ ERROR: Mixing sync y async sin bridge
def operacion_sync():
    return "sync"

async def main():
    # Esto funciona pero bloquea el event loop
    result = await operacion_sync()  # No es awaitable!
    # Usar asyncio.to_thread() para ejecutar sync en thread pool
    result = await asyncio.to_thread(operacion_sync)
```

## Ejercicios Prácticos

**Ejercicio 1**: Sin ejecutar, determina el tiempo total:

```python
import asyncio

async def tarea(n):
    print(f"Iniciando {n}")
    await asyncio.sleep(n)
    print(f"Completada {n}")

async def main():
    # ¿Cuánto tarda?
    await tarea(2)
    await tarea(1)

asyncio.run(main())
```

**Ejercicio 2**: Modifica para ejecutar concurrentemente:

```python
import asyncio

async def fetch_data(url: str, delay: int) -> dict:
    await asyncio.sleep(delay)
    return {"url": url, "data": "contenido"}

async def main():
    urls = [
        ("https://api.com/users", 2),
        ("https://api.com/products", 1),
        ("https://api.com/orders", 3),
    ]
    # Ejecutar concurrentemente y medir tiempo
    # ¿Cuánto tarda vs secuencial?

asyncio.run(main())
```

---

# SESIÓN 3: SQLModel - ORM Moderno para Python

## Duración: 2 horas

## Objetivos de Aprendizaje

- Comprender qué es un ORM y por qué SQLModel
- Definir modelos con SQLModel usando tipos de Python
- Configurar relaciones (1:N y N:M)
- Usar SQLModel con asyncpg

## 3.1 ¿Qué es SQLModel?

SQLModel es un ORM creado por el mismo autor de FastAPI. Combina:
- **Pydantic**: Validación de datos, serialización
- **SQLAlchemy**: Potencia y flexibilidad ORM
- **Type hints**: IDE support completo, mypy compatible

```python
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

# Modelo = Pydantic + SQLAlchemy
class Usuario(SQLModel, table=True):
    """Modelo de usuario - tabla en BD y schema de validación."""
    __tablename__ = "usuarios"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    nombre: str = Field(max_length=100)
    password_hash: str
    rol: str = Field(default="cliente", max_length=20)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

## 3.2 Modelos Básicos

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class Categoria(SQLModel, table=True):
    __tablename__ = "categorias"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100, index=True)
    slug: str = Field(max_length=100, unique=True)
    descripcion: Optional[str] = None
    parent_id: Optional[int] = Field(default=None, foreign_key="categorias.id")

    # Relación: una categoría puede tener muchos productos
    productos: List["Producto"] = Relationship(back_populates="categoria")

    # Autoreferencia: subcategorías
    subcategorias: List["Categoria"] = Relationship(
        back_populates="parent",
        sa_relationship_kwargs={"remote_side": [id]}
    )
    parent: Optional["Categoria"] = Relationship(back_populates="subcategorias")


class Producto(SQLModel, table=True):
    __tablename__ = "productos"

    id: Optional[int] = Field(default=None, primary_key=True)
    vendedor_id: int = Field(foreign_key="vendedores.id", index=True)
    categoria_id: Optional[int] = Field(default=None, foreign_key="categorias.id")

    nombre: str = Field(max_length=200, index=True)
    descripcion: Optional[str] = None
    precio: Decimal = Field(default=Decimal("0.00"), decimal_places=2, index=True)
    stock: int = Field(default=0, ge=0)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relaciones
    categoria: Optional[Categoria] = Relationship(back_populates="productos")
    vendedor: "Vendedor" = Relationship(back_populates="productos")
    etiquetas: List["Etiqueta"] = Relationship(
        back_populates="productos",
        link_model="ProductoEtiqueta"
    )


class Etiqueta(SQLModel, table=True):
    __tablename__ = "etiquetas"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=50, index=True)
    slug: str = Field(max_length=50, unique=True)
    color: str = Field(default="#6366f1", max_length=7)

    productos: List[Producto] = Relationship(
        back_populates="etiquetas",
        link_model="ProductoEtiqueta"
    )


# Tabla intermedia para N:M (generada automáticamente)
class ProductoEtiqueta(SQLModel, table=True):
    __tablename__ = "producto_etiqueta"

    producto_id: int = Field(foreign_key="productos.id", primary_key=True)
    etiqueta_id: int = Field(foreign_key="etiquetas.id", primary_key=True)
```

## 3.3 Relaciones Uno a Muchos (1:N)

```python
class Vendedor(SQLModel, table=True):
    __tablename__ = "vendedores"

    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuarios.id", unique=True)
    nombre_tienda: str = Field(max_length=200)
    descripcion: Optional[str] = None
    telefono: Optional[str] = Field(default=None, max_length=20)
    rating: Decimal = Field(default=Decimal("0.00"), decimal_places=2)
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Un vendedor tiene muchos productos (1:N)
    productos: List[Producto] = Relationship(back_populates="vendedor")


class Producto(SQLModel, table=True):
    # ... otros campos ...

    # Muchos productos pertenecen a UN vendedor (N:1)
    vendedor_id: int = Field(foreign_key="vendedores.id")
    vendedor: Vendedor = Relationship(back_populates="productos")
```

## 3.4 Relaciones Muchos a Muchos (N:M)

```python
# Opción 1: Tabla intermedia explícita (recomendada)
class ProductoEtiqueta(SQLModel, table=True):
    """Tabla intermedia para relación N:M."""
    __tablename__ = "producto_etiqueta"

    producto_id: int = Field(foreign_key="productos.id", primary_key=True)
    etiqueta_id: int = Field(foreign_key="etiquetas.id", primary_key=True)


class Producto(SQLModel, table=True):
    # En el modelo Producto:
    etiquetas: List["Etiqueta"] = Relationship(
        back_populates="productos",
        link_model=ProductoEtiqueta  # Referencia a tabla intermedia
    )


class Etiqueta(SQLModel, table=True):
    productos: List["Producto"] = Relationship(
        back_populates="etiquetas",
        link_model=ProductoEtiqueta
    )
```

## 3.5 Validaciones con Field

```python
from sqlmodel import SQLModel, Field, validate
from typing import Optional
from decimal import Decimal
import re

class Producto(SQLModel, table=True):
    __tablename__ = "productos"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(
        max_length=200,
        min_length=3,           # Mínimo 3 caracteres
        index=True
    )
    slug: str = Field(max_length=200)
    precio: Decimal = Field(
        default=Decimal("0.00"),
        decimal_places=2,
        ge=Decimal("0.00")      # Greater than or equal (no negativo)
    )
    stock: int = Field(
        default=0,
        ge=0                    # No puede ser negativo
    )
    email: Optional[str] = Field(default=None, unique=True, index=True)

    class Config:
        # Validaciones adicionales
        json_schema_extra = {
            "example": {
                "nombre": "Laptop Gaming",
                "precio": "1299.99",
                "stock": 10
            }
        }
```

## 3.6 Índices y Constraints

```python
from sqlmodel import SQLModel, Field, Index
from sqlalchemy import UniqueConstraint, CheckConstraint

class Producto(SQLModel, table=True):
    __tablename__ = "productos"
    __table_args__ = (
        Index("idx_productos_precio_stock", "precio", "stock"),  # Índice compuesto
        Index("idx_productos_nombre_lower", None, postgresql_using="hash",
              postgresql_ops={"nombre": "varchar_pattern_ops"}),  # Índice para LIKE
        CheckConstraint("precio >= 0", name="check_precio_positivo"),
        CheckConstraint("stock >= 0", name="check_stock_positivo"),
        {"schema": "market"}  # Schema de la BD
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=200)
    precio: Decimal = Field(ge=0)
    stock: int = Field(ge=0)
```

## 3.7 Herencia de Modelos

```python
from sqlmodel import SQLModel, Field
from datetime import datetime
from typing import Optional

# Modelo base con campos comunes
class BaseModel(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default=None)


class ProductoBase(BaseModel):
    """Schema base para productos."""
    nombre: str = Field(max_length=200)
    precio: float = Field(ge=0)


class ProductoCreate(ProductoBase):
    """Schema para crear producto (no incluye campos de lectura)."""
    categoria_id: Optional[int] = None
    vendedor_id: int
    etiquetas: list[int] = []  # IDs de etiquetas


class ProductoDB(ProductoBase, table=True):
    """Modelo completo de producto en BD."""
    __tablename__ = "productos"

    vendedor_id: int = Field(foreign_key="vendedores.id")
    categoria_id: Optional[int] = Field(default=None, foreign_key="categorias.id")
    stock: int = Field(default=0, ge=0)
    is_active: bool = Field(default=True)


class ProductoRead(ProductoBase):
    """Schema para leer producto (respuesta API)."""
    id: int
    stock: int
    is_active: bool
```

## 3.8 Crear Tablas con SQLModel

```python
from sqlmodel import SQLModel, create_engine
from app.models.usuario import Usuario
from app.models.producto import Producto, Categoria, Etiqueta
from app.models.vendedor import Vendedor
from app.models.orden import Orden, OrdenItem

# Connection string para sync (para crear tablas)
DATABASE_URL = "postgresql://postgres:password@localhost:5432/marketdb"

engine = create_engine(DATABASE_URL, echo=True)

# Crear todas las tablas
SQLModel.metadata.create_all(engine)

# Con async + asyncpg se usa create_async_engine
# pero la creación de tablas se hace diferente (ver sesión de Alembic)
```

## Ejercicios Prácticos

**Ejercicio 1**: Define el modelo `Orden` con:
- Relación 1:N con OrdenItem
- Relación N:1 con Usuario
- Campos: id, usuario_id, status, total, timestamps

**Ejercicio 2**: Crea una tabla intermedia `Favorito` para que usuarios puedan marcar productos favoritos (N:M).

**Ejercicio 3**: Implementa una jerarquía de categorías con autoreferencia (categoría → subcategorías).

---

# SESIÓN 4: FastAPI - Fundamentos y Routing

## Duración: 2 horas

## Objetivos de Aprendizaje

- Crear una aplicación FastAPI básica
- Definir rutas GET, POST, PUT, PATCH, DELETE
- Usar Path, Query, Body parameters
- Documentación automática con OpenAPI/Swagger

## 4.1 Tu Primera Aplicación FastAPI

```python
# app/main.py
from fastapi import FastAPI
from fastapi.responses import JSONResponse

# Crear aplicación FastAPI
app = FastAPI(
    title="MarketHub API",
    description="API para plataforma de e-commerce",
    version="1.0.0",
    docs_url="/docs",      # Swagger UI
    redoc_url="/redoc"      # ReDoc
)

# Endpoint básico
@app.get("/")
async def root():
    return {"message": "¡Bienvenido a MarketHub API!"}

# Health check
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

# Ejecutar:
# uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
# Documentación: http://localhost:8000/docs
```

## 4.2 Tipos de Parámetros

```python
from fastapi import FastAPI, Path, Query, Body, Header, Cookie
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

app = FastAPI()

# --- PATH PARAMETERS ---
# Parámetros en la URL: /usuarios/5

@app.get("/usuarios/{usuario_id}")
async def get_usuario(usuario_id: int):
    """usuario_id se convierte automáticamente a int."""
    return {"usuario_id": usuario_id, "tipo": type(usuario_id).__name__}


@app.get("/productos/{categoria}/{producto_id}")
async def get_producto(categoria: str, producto_id: int):
    return {"categoria": categoria, "producto_id": producto_id}

# Con validación
@app.get("/ordenes/{orden_id}")
async def get_orden(
    orden_id: int = Path(gt=0, description="ID de la orden")
):
    """orden_id debe ser mayor a 0."""
    return {"orden_id": orden_id}


# --- QUERY PARAMETERS ---
# Parámetros después de ?: /productos?categoria=electronica&min_precio=100

@app.get("/productos")
async def listar_productos(
    categoria: Optional[str] = None,
    min_precio: Optional[float] = Query(None, ge=0),
    max_precio: Optional[float] = Query(None, ge=0),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """Lista productos con filtros opcionales."""
    return {
        "filtros": {"categoria": categoria, "min_precio": min_precio, "max_precio": max_precio},
        "paginacion": {"skip": skip, "limit": limit}
    }


# --- BODY PARAMETERS ---
# Datos en el cuerpo de la petición (POST, PUT)

class UsuarioCreate(BaseModel):
    email: str
    nombre: str
    password: str
    rol: str = "cliente"

class ProductoCreate(BaseModel):
    nombre: str
    precio: Decimal
    categoria_id: Optional[int] = None

@app.post("/usuarios")
async def crear_usuario(usuario: UsuarioCreate):
    """Body como Pydantic model."""
    return {"datos_recibidos": usuario.model_dump()}


@app.post("/productos")
async def crear_producto(
    producto: ProductoCreate,
    vendedor_id: int = Body(..., embed=True)  # Wrapped en objeto
):
    return {
        "vendedor_id": vendedor_id,
        "producto": producto
    }


# --- HEADER, COOKIE PARAMETERS ---

@app.get("/stats")
async def get_stats(
    x_request_id: str = Header(None),
    auth_token: Optional[str] = Cookie(None)
):
    return {
        "request_id": x_request_id,
        "has_auth_token": auth_token is not None
    }
```

## 4.3 Schemas Pydantic para Request/Response

```python
from fastapi import FastAPI
from pydantic import BaseModel, EmailStr, Field, validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

app = FastAPI()

# --- SCHEMAS DE ENTRADA (Request) ---

class UsuarioCreate(BaseModel):
    """Schema para crear un usuario."""
    email: EmailStr  # Validación automática de email
    nombre: str = Field(min_length=2, max_length=100)
    password: str = Field(min_length=8)
    rol: str = Field(default="cliente", pattern="^(cliente|vendedor|admin)$")

    @validator("password")
    def password_debe_ser_seguro(cls, v):
        if not any(c.isupper() for c in v):
            raise ValueError("La contraseña debe tener al menos una mayúscula")
        if not any(c.isdigit() for c in v):
            raise ValueError("La contraseña debe tener al menos un número")
        return v


class ProductoCreate(BaseModel):
    """Schema para crear un producto."""
    nombre: str = Field(min_length=3, max_length=200)
    descripcion: Optional[str] = None
    precio: Decimal = Field(ge=0, decimal_places=2)
    stock: int = Field(ge=0, default=0)
    categoria_id: Optional[int] = None
    etiquetas: List[int] = []

    @validator("nombre")
    def nombre_no_puede_vacio(cls, v):
        if not v.strip():
            raise ValueError("El nombre no puede estar vacío")
        return v.strip()


class ProductoUpdate(BaseModel):
    """Schema para actualizar (todos opcionales)."""
    nombre: Optional[str] = Field(None, min_length=3)
    descripcion: Optional[str] = None
    precio: Optional[Decimal] = Field(None, ge=0)
    stock: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


# --- SCHEMAS DE SALIDA (Response) ---

class UsuarioResponse(BaseModel):
    """Schema para devolver usuario."""
    id: int
    email: str
    nombre: str
    rol: str
    is_active: bool
    created_at: datetime

    class Config:
        from_attributes = True  # Permite crear desde modelos SQLModel


class ProductoResponse(BaseModel):
    """Schema completo de producto."""
    id: int
    nombre: str
    descripcion: Optional[str]
    precio: Decimal
    stock: int
    is_active: bool
    categoria_id: Optional[int]
    vendedor_id: int
    created_at: datetime

    class Config:
        from_attributes = True


class ProductoWithCategoriaResponse(ProductoResponse):
    """Producto incluyendo datos de categoría."""
    categoria_nombre: Optional[str] = None


class OrdenCreate(BaseModel):
    usuario_id: int
    items: List[dict]  # [{producto_id: int, cantidad: int}]

    @validator("items")
    def debe_tener_items(cls, v):
        if not v:
            raise ValueError("La orden debe tener al menos un item")
        return v


# --- ENDPOINTS ---

@app.post("/usuarios", response_model=UsuarioResponse, status_code=201)
async def crear_usuario(usuario: UsuarioCreate):
    """Crea un usuario y retorna la respuesta formateada."""
    # En producción: guardar en BD
    return {
        "id": 1,
        **usuario.model_dump(),
        "is_active": True,
        "created_at": datetime.utcnow()
    }
```

## 4.4 Rutas con Múltiples Métodos HTTP

```python
from fastapi import APIRouter, HTTPException, status

# Crear router modular
router = APIRouter(prefix="/usuarios", tags=["Usuarios"])

@router.get("/", response_model=List[UsuarioResponse])
async def listar_usuarios(skip: int = 0, limit: int = 10):
    """GET /usuarios"""
    return []

@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def get_usuario(usuario_id: int):
    """GET /usuarios/{id}"""
    if usuario_id <= 0:
        raise HTTPException(status_code=400, detail="ID inválido")
    return {"id": usuario_id}

@router.post("/", response_model=UsuarioResponse, status_code=201)
async def crear_usuario(usuario: UsuarioCreate):
    """POST /usuarios"""
    return {"id": 1, **usuario.model_dump(), "is_active": True, "created_at": datetime.utcnow()}

@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def actualizar_usuario(usuario_id: int, usuario: UsuarioCreate):
    """PUT /usuarios/{id}"""
    return {"id": usuario_id, **usuario.model_dump(), "is_active": True, "created_at": datetime.utcnow()}

@router.delete("/{usuario_id}", status_code=204)
async def eliminar_usuario(usuario_id: int):
    """DELETE /usuarios/{id}"""
    return None

@router.patch("/{usuario_id}/desactivar")
async def desactivar_usuario(usuario_id: int):
    """PATCH /usuarios/{id}/desactivar"""
    return {"id": usuario_id, "is_active": False}
```

## 4.5 Incluir Routers en Main

```python
from fastapi import FastAPI
from app.routes import usuarios, productos, categorias, ordenes

app = FastAPI(title="MarketHub API")

# Incluir routers
app.include_router(usuarios.router)
app.include_router(productos.router, prefix="/api/v1")  # Con prefijo de versión
app.include_router(categorias.router)
app.include_router(ordenes.router)
```

## 4.6 Response Models y Códigos de Estado

```python
from fastapi import FastAPI, status
from fastapi.responses import JSONResponse
from typing import Optional, List

app = FastAPI()

# Códigos de estado comunes
"""
200 OK - GET exitoso, PUT/PATCH exitoso
201 Created - Recurso creado exitosamente (POST)
204 No Content - DELETE exitoso
400 Bad Request - Datos inválidos
401 Unauthorized - No autenticado
403 Forbidden - No autorizado
404 Not Found - Recurso no encontrado
422 Unprocessable Entity - Validación fallida
500 Internal Server Error - Error del servidor
"""

@router.get(
    "/{producto_id}",
    response_model=ProductoResponse,
    responses={
        404: {"description": "Producto no encontrado"},
        403: {"description": "No tienes acceso a este producto"}
    }
)
async def get_producto(producto_id: int):
    producto = await obtener_producto_db(producto_id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto {producto_id} no encontrado"
        )
    return producto


# Response con headers personalizados
@router.get("/exportar/{formato}")
async def exportar_datos(formato: str):
    return JSONResponse(
        content={"data": "..."},
        headers={"Content-Disposition": f"attachment; filename=datos.{formato}"}
    )
```

## Ejercicios Prácticos

**Ejercicio 1**: Crea un CRUD completo de categorías con:
- GET / - Listar todas
- GET /{id} - Obtener una
- POST / - Crear
- PUT /{id} - Actualizar
- DELETE /{id} - Eliminar

**Ejercicio 2**: Implementa paginación con `skip` y `limit` en el endpoint de listar productos.

**Ejercicio 3**: Añade validación para que no se pueda crear un producto con precio negativo.

---

# SESIÓN 5: Conexión a PostgreSQL con AsyncPG y SQLModel

## Duración: 2 horas

## Objetivos de Aprendizaje

- Configurar conexión async a PostgreSQL con SQLModel
- Implementar un pool de conexiones
- Crear una dependencia de sesión para FastAPI
- Ejecutar queries CRUD básicas de forma async

## 5.1 Configuración del Proyecto

```bash
# requirements.txt
fastapi==0.109.0
uvicorn[standard]==0.27.0
sqlmodel==0.0.14
asyncpg==0.29.0
pydantic==2.5.0
pydantic-settings==2.1.0
python-dotenv==1.0.0
```

```bash
pip install -r requirements.txt
```

## 5.2 Configuración con Pydantic Settings

```python
# app/config.py
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    """Configuración de la aplicación desde variables de entorno."""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False  # No distingue mayúsculas/minúsculas
    )

    # Database
    database_url: str = "postgresql+asyncpg://postgres:password@localhost:5432/marketdb"
    database_pool_size: int = 10
    database_max_overflow: int = 20

    # App
    app_name: str = "MarketHub API"
    debug: bool = False
    api_version: str = "v1"

    # Security
    secret_key: str = "change-me-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60 * 24  # 24 horas


# Instancia global de configuración
settings = Settings()
```

```env
# .env
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/marketdb
DATABASE_POOL_SIZE=10
DEBUG=true
SECRET_KEY=my-super-secret-key-change-in-production
```

## 5.3 Conexión Async con SQLModel

```python
# app/database/connection.py
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from app.config import settings

# Crear engine asíncrono
engine = create_async_engine(
    settings.database_url,
    echo=settings.debug,                    # Mostrar SQL en desarrollo
    pool_size=settings.database_pool_size,   # Conexiones en pool
    max_overflow=settings.database_max_overflow,
    pool_pre_ping=True,                     # Verificar conexiones antes de usar
)

# Session factory
async_session = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,   # No expirar objetos después del commit
    autocommit=False,
    autoflush=False,
)


async def init_db():
    """Crea todas las tablas. Usar Alembic en producción."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)


async def close_db():
    """Cierra el engine."""
    await engine.dispose()


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Dependencia de FastAPI para obtener una sesión de BD.
    Se encarga de commit/rollback y cierre automático.
    """
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


@asynccontextmanager
async def get_session_context() -> AsyncGenerator[AsyncSession, None]:
    """Context manager para uso fuera de FastAPI."""
    async with async_session() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
```

## 5.4 Modelos Completos del Proyecto

```python
# app/models/usuario.py
from sqlmodel import SQLModel, Field
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from decimal import Decimal

if TYPE_CHECKING:
    from app.models.vendedor import Vendedor
    from app.models.orden import Orden


class Usuario(SQLModel, table=True):
    __tablename__ = "usuarios"

    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    nombre: str = Field(max_length=100)
    password_hash: str = Field(max_length=255)
    rol: str = Field(default="cliente", max_length=20)  # cliente, vendedor, admin
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relaciones
    vendedor: Optional["Vendedor"] = Relationship(back_populates="usuario")
    ordenes: List["Orden"]"] = Relationship(back_populates="usuario")
```

```python
# app/models/vendedor.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime
from decimal import Decimal

class Vendedor(SQLModel, table=True):
    __tablename__ = "vendedores"

    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(unique=True, foreign_key="usuarios.id")
    nombre_tienda: str = Field(max_length=200)
    descripcion: Optional[str] = None
    telefono: Optional[str] = Field(default=None, max_length=20)
    rating: Decimal = Field(default=Decimal("0.00"), decimal_places=2)
    is_verified: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relaciones
    usuario: "Usuario" = Relationship(back_populates="vendedor")
    productos: List["Producto"] = Relationship(back_populates="vendedor")
```

```python
# app/models/producto.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from decimal import Decimal

if TYPE_CHECKING:
    from app.models.vendedor import Vendedor
    from app.models.categoria import Categoria
    from app.models.etiqueta import Etiqueta

class Producto(SQLModel, table=True):
    __tablename__ = "productos"

    id: Optional[int] = Field(default=None, primary_key=True)
    vendedor_id: int = Field(foreign_key="vendedores.id", index=True)
    categoria_id: Optional[int] = Field(default=None, foreign_key="categorias.id")

    nombre: str = Field(max_length=200, index=True)
    descripcion: Optional[str] = None
    precio: Decimal = Field(default=Decimal("0.00"), decimal_places=2, index=True)
    stock: int = Field(default=0, ge=0)
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # Relaciones
    vendedor: "Vendedor" = Relationship(back_populates="productos")
    categoria: Optional["Categoria"] = = Relationship(back_populates="productos")
    etiquetas: List["Etiqueta"] = Relationship(
        back_populates="productos",
        link_model="ProductoEtiqueta"
    )
```

```python
# app/models/categoria.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.producto import Producto

class Categoria(SQLModel, table=True):
    __tablename__ = "categorias"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=100, index=True)
    slug: str = Field(max_length=100, unique=True, index=True)
    descripcion: Optional[str] = None
    parent_id: Optional[int] = Field(default=None, foreign_key="categorias.id")

    # Relaciones
    productos: List["Producto"] = Relationship(back_populates="categoria")
    subcategorias: List["Categoria"] = Relationship(
        back_populates="parent",
        sa_relationship_kwargs={"remote_side": [id]}
    )
    parent: Optional["Categoria"] = Relationship(back_populates="subcategorias")
```

```python
# app/models/etiqueta.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.producto import Producto

class Etiqueta(SQLModel, table=True):
    __tablename__ = "etiquetas"

    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(max_length=50, index=True)
    slug: str = Field(max_length=50, unique=True, index=True)
    color: str = Field(default="#6366f1", max_length=7)

    productos: List["Producto"] = Relationship(
        back_populates="etiquetas",
        link_model="ProductoEtiqueta"
    )


class ProductoEtiqueta(SQLModel, table=True):
    """Tabla intermedia para N:M."""
    __tablename__ = "producto_etiqueta"

    producto_id: int = Field(foreign_key="productos.id", primary_key=True)
    etiqueta_id: int = Field(foreign_key="etiquetas.id", primary_key=True)
```

```python
# app/models/orden.py
from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from datetime import datetime
from decimal import Decimal

if TYPE_CHECKING:
    from app.models.usuario import Usuario
    from app.models.producto import Producto

class Orden(SQLModel, table=True):
    __tablename__ = "ordenes"

    id: Optional[int] = Field(default=None, primary_key=True)
    usuario_id: int = Field(foreign_key="usuarios.id", index=True)
    status: str = Field(default="pendiente", max_length=20, index=True)
    total: Decimal = Field(default=Decimal("0.00"), decimal_places=2)
    fecha_creacion: datetime = Field(default_factory=datetime.utcnow)
    fecha_updated: Optional[datetime] = Field(default=None)

    # Relaciones
    usuario: "Usuario" = Relationship(back_populates="ordenes")
    items: List["OrdenItem"] = Relationship(back_populates="orden")


class OrdenItem(SQLModel, table=True):
    __tablename__ = "orden_items"

    id: Optional[int] = Field(default=None, primary_key=True)
    orden_id: int = Field(foreign_key="ordenes.id")
    producto_id: int = Field(foreign_key="productos.id")
    cantidad: int = Field(ge=1)
    precio_unitario: Decimal = Field(decimal_places=2)

    # Relaciones
    orden: Orden = Relationship(back_populates="items")
    producto: "Producto" = Relationship()
```

```python
# app/models/__init__.py
from app.models.usuario import Usuario
from app.models.vendedor import Vendedor
from app.models.producto import Producto, ProductoEtiqueta
from app.models.categoria import Categoria
from app.models.etiqueta import Etiqueta
from app.models.orden import Orden, OrdenItem

__all__ = [
    "Usuario", "Vendedor", "Producto", "Categoria",
    "Etiqueta", "ProductoEtiqueta", "Orden", "OrdenItem"
]
```

## 5.5 App Principal con Lifecycle

```python
# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config import settings
from app.database.connection import init_db, close_db
from app.routes import usuarios, productos, categorias, etiquetas, ordenes

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Maneja el ciclo de vida de la aplicación."""
    # Startup
    print("Iniciando aplicación...")
    await init_db()
    print("Base de datos inicializada")
    yield
    # Shutdown
    print("Cerrando aplicación...")
    await close_db()
    print("Conexiones cerradas")

app = FastAPI(
    title=settings.app_name,
    version=settings.api_version,
    lifespan=lifespan
)

# Incluir routers
app.include_router(usuarios.router)
app.include_router(productos.router)
app.include_router(categorias.router)
app.include_router(etiquetas.router)
app.include_router(ordenes.router)

@app.get("/health")
async def health():
    return {"status": "ok"}
```

## 5.6 Patrón Repository (Capa de Acceso a Datos)

```python
# app/repositories/base.py
from typing import TypeVar, Generic, Type, Optional, List, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlmodel import SQLModel

ModelType = TypeVar("ModelType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType")
UpdateSchemaType = TypeVar("UpdateSchemaType")


class BaseRepository(Generic[ModelType]):
    """Repository genérico con operaciones CRUD básicas."""

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, session: AsyncSession, id: int) -> Optional[ModelType]:
        """Obtiene un registro por ID."""
        result = await session.execute(
            select(self.model).where(self.model.id == id)
        )
        return result.scalar_one_or_none()

    async def get_all(
        self,
        session: AsyncSession,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        """Obtiene todos los registros con paginación."""
        result = await session.execute(
            select(self.model).offset(skip).limit(limit)
        )
        return list(result.scalars().all())

    async def create(
        self,
        session: AsyncSession,
        obj: ModelType
    ) -> ModelType:
        """Crea un nuevo registro."""
        session.add(obj)
        await session.flush()  # Obtiene el ID sin hacer commit
        await session.refresh(obj)
        return obj

    async def update(
        self,
        session: AsyncSession,
        obj: ModelType,
        updates: dict
    ) -> ModelType:
        """Actualiza campos de un registro."""
        for key, value in updates.items():
            if value is not None:
                setattr(obj, key, value)
        await session.flush()
        await session.refresh(obj)
        return obj

    async def delete(self, session: AsyncSession, id: int) -> bool:
        """Elimina un registro."""
        obj = await self.get(session, id)
        if obj:
            await session.delete(obj)
            await session.flush()
            return True
        return False

    async def count(self, session: AsyncSession) -> int:
        """Cuenta todos los registros."""
        result = await session.execute(select(self.model))
        return len(list(result.scalars().all()))
```

```python
# app/repositories/usuario.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_
from app.models.usuario import Usuario
from app.repositories.base import BaseRepository
from typing import Optional

class UsuarioRepository(BaseRepository[Usuario]):
    def __init__(self):
        super().__init__(Usuario)

    async def get_by_email(self, session: AsyncSession, email: str) -> Optional[Usuario]:
        """Busca usuario por email."""
        result = await session.execute(
            select(Usuario).where(Usuario.email == email)
        )
        return result.scalar_one_or_none()

    async def get_by_email_with_vendedor(
        self, session: AsyncSession, email: str
    ) -> Optional[Usuario]:
        """Busca usuario con su vendedor cargado."""
        result = await session.execute(
            select(Usuario)
            .where(Usuario.email == email)
        )
        return result.scalar_one_or_none()

    async def get_activos(
        self, session: AsyncSession, skip: int = 0, limit: int = 10
    ) -> list[Usuario]:
        """Obtiene solo usuarios activos."""
        result = await session.execute(
            select(Usuario)
            .where(Usuario.is_active == True)
            .offset(skip)
            .limit(limit)
        )
        return list(result.scalars().all())


# Instancia singleton
usuario_repo = UsuarioRepository()
```

## Ejercicios Prácticos

**Ejercicio 1**: Implementa `ProductoRepository` con métodos:
- `get_by_categoria(categoria_id)`
- `get_activos()`
- `get_by_precio_range(min, max)`

**Ejercicio 2**: Crea el archivo `app/repositories/orden.py` con métodos:
- `get_by_usuario(usuario_id)`
- `get_by_status(status)`
- `get_con_items(orden_id)` - retorna la orden con sus items

**Ejercicio 3**: Implementa el método `get_or_create_etiqueta` que busca una etiqueta por slug y la crea si no existe.

---

# SESIÓN 6: CRUD Completo - Create y Read

## Duración: 2 horas

## Objetivos de Aprendizaje

- Implementar endpoints POST para crear recursos
- Implementar endpoints GET para leer recursos
- Validar datos de entrada con Pydantic
- Manejar errores 404 y 400 apropiadamente

## 6.1 Schemas (Pydantic Models)

```python
# app/schemas/usuario.py
from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional
from datetime import datetime
from decimal import Decimal


class UsuarioBase(BaseModel):
    email: EmailStr
    nombre: str = Field(min_length=2, max_length=100)


class UsuarioCreate(UsuarioBase):
    password: str = Field(min_length=8)
    rol: str = Field(default="cliente", pattern="^(cliente|vendedor|admin)$")


class UsuarioUpdate(BaseModel):
    email: Optional[EmailStr] = None
    nombre: Optional[str] = Field(None, min_length=2, max_length=100)
    is_active: Optional[bool] = None


class UsuarioResponse(UsuarioBase):
    id: int
    rol: str
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UsuarioWithVendedor(UsuarioResponse):
    vendedor_id: Optional[int] = None
    nombre_tienda: Optional[str] = None
```

```python
# app/schemas/producto.py
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class ProductoBase(BaseModel):
    nombre: str = Field(min_length=3, max_length=200)
    descripcion: Optional[str] = None
    precio: Decimal = Field(ge=0, decimal_places=2)


class ProductoCreate(ProductoBase):
    vendedor_id: int
    categoria_id: Optional[int] = None
    stock: int = Field(default=0, ge=0)
    etiquetas: List[int] = []  # IDs de etiquetas


class ProductoUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=3)
    descripcion: Optional[str] = None
    precio: Optional[Decimal] = Field(None, ge=0)
    stock: Optional[int] = Field(None, ge=0)
    is_active: Optional[bool] = None


class ProductoResponse(ProductoBase):
    id: int
    stock: int
    is_active: bool
    vendedor_id: int
    categoria_id: Optional[int]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ProductoWithDetails(ProductoResponse):
    categoria_nombre: Optional[str] = None
    vendedor_nombre_tienda: Optional[str] = None
    etiquetas: List[str] = []  # Nombres de etiquetas
```

```python
# app/schemas/categoria.py
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class CategoriaBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=100)
    slug: str = Field(min_length=2, max_length=100, pattern=r"^[a-z0-9-]+$")
    descripcion: Optional[str] = None


class CategoriaCreate(CategoriaBase):
    parent_id: Optional[int] = None


class CategoriaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2)
    slug: Optional[str] = Field(None, min_length=2, pattern=r"^[a-z0-9-]+$")
    descripcion: Optional[str] = None
    parent_id: Optional[int] = None


class CategoriaResponse(CategoriaBase):
    id: int
    parent_id: Optional[int]
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CategoriaWithCount(CategoriaResponse):
    productos_count: int = 0
```

```python
# app/schemas/orden.py
from pydantic import BaseModel, Field, ConfigDict, field_validator
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class OrdenItemCreate(BaseModel):
    producto_id: int = Field(gt=0)
    cantidad: int = Field(gt=0)


class OrdenCreate(BaseModel):
    usuario_id: int = Field(gt=0)
    items: List[OrdenItemCreate] = Field(min_length=1)

    @field_validator("items")
    @classmethod
    def items_no_vacios(cls, v):
        if not v:
            raise ValueError("La orden debe tener al menos un item")
        return v


class OrdenItemResponse(BaseModel):
    id: int
    producto_id: int
    cantidad: int
    precio_unitario: Decimal

    model_config = ConfigDict(from_attributes=True)


class OrdenResponse(BaseModel):
    id: int
    usuario_id: int
    status: str
    total: Decimal
    fecha_creacion: datetime
    fecha_updated: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class OrdenWithItems(OrdenResponse):
    items: List[OrdenItemResponse] = []
```

## 6.2 Rutas de Usuarios

```python
# app/routes/usuarios.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database.connection import get_session
from app.models.usuario import Usuario
from app.models.vendedor import Vendedor
from app.schemas.usuario import (
    UsuarioCreate,
    UsuarioUpdate,
    UsuarioResponse,
    UsuarioWithVendedor
)
from app.repositories.usuario import usuario_repo

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.post("/", response_model=UsuarioResponse, status_code=201)
async def crear_usuario(
    usuario_data: UsuarioCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Crea un nuevo usuario.

    - **email**: Correo electrónico único
    - **nombre**: Nombre completo
    - **password**: Contraseña (mínimo 8 caracteres)
    - **rol**: Rol del usuario (cliente, vendedor, admin)
    """
    # Verificar email único
    existing = await usuario_repo.get_by_email(session, usuario_data.email)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El email {usuario_data.email} ya está registrado"
        )

    # Crear usuario
    db_usuario = Usuario(
        email=usuario_data.email,
        nombre=usuario_data.nombre,
        password_hash=usuario_data.password,  # En producción: hashear!
        rol=usuario_data.rol,
        is_active=True
    )

    usuario_creado = await usuario_repo.create(session, db_usuario)
    return usuario_creado


@router.get("/", response_model=List[UsuarioResponse])
async def listar_usuarios(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    is_active: bool = Query(None),
    session: AsyncSession = Depends(get_session)
):
    """
    Lista usuarios con paginación.

    - **skip**: Número de registros a omitir
    - **limit**: Número máximo de registros a devolver
    - **is_active**: Filtrar por estado activo
    """
    if is_active is not None:
        result = await session.execute(
            select(Usuario)
            .where(Usuario.is_active == is_active)
            .offset(skip)
            .limit(limit)
        )
    else:
        result = await session.execute(
            select(Usuario).offset(skip).limit(limit)
        )

    usuarios = result.scalars().all()
    return list(usuarios)


@router.get("/{usuario_id}", response_model=UsuarioResponse)
async def obtener_usuario(
    usuario_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Obtiene un usuario por su ID."""
    usuario = await usuario_repo.get(session, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario {usuario_id} no encontrado"
        )
    return usuario


@router.get("/email/{email}", response_model=UsuarioResponse)
async def obtener_usuario_por_email(
    email: str,
    session: AsyncSession = Depends(get_session)
):
    """Obtiene un usuario por su email."""
    usuario = await usuario_repo.get_by_email(session, email)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario con email {email} no encontrado"
        )
    return usuario


@router.get("/vendedor/{vendedor_id}", response_model=UsuarioWithVendedor)
async def obtener_usuario_por_vendedor(
    vendedor_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Obtiene el usuario asociado a un vendedor."""
    result = await session.execute(
        select(Usuario)
        .join(Vendedor)
        .where(Vendedor.id == vendedor_id)
    )
    usuario = result.scalar_one_or_none()

    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No se encontró usuario para vendedor {vendedor_id}"
        )

    # Obtener datos del vendedor
    result_vendedor = await session.execute(
        select(Vendedor).where(Vendedor.id == vendedor_id)
    )
    vendedor = result_vendedor.scalar_one_or_none()

    return UsuarioWithVendedor(
        id=usuario.id,
        email=usuario.email,
        nombre=usuario.nombre,
        rol=usuario.rol,
        is_active=usuario.is_active,
        created_at=usuario.created_at,
        vendedor_id=vendedor.id if vendedor else None,
        nombre_tienda=vendedor.nombre_tienda if vendedor else None
    )
```

## 6.3 Rutas de Productos

```python
# app/routes/productos.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload
from typing import List, Optional

from app.database.connection import get_session
from app.models.producto import Producto, ProductoEtiqueta
from app.models.categoria import Categoria
from app.models.etiqueta import Etiqueta
from app.models.vendedor import Vendedor
from app.schemas.producto import (
    ProductoCreate,
    ProductoUpdate,
    ProductoResponse,
    ProductoWithDetails
)
from app.repositories.producto import producto_repo

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.post("/", response_model=ProductoResponse, status_code=201)
async def crear_producto(
    producto_data: ProductoCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Crea un nuevo producto.

    - **nombre**: Nombre del producto
    - **precio**: Precio (no negativo)
    - **vendedor_id**: ID del vendedor (requerido)
    - **categoria_id**: ID de la categoría (opcional)
    - **stock**: Cantidad disponible
    - **etiquetas**: Lista de IDs de etiquetas
    """
    # Verificar que el vendedor existe
    result = await session.execute(
        select(Vendedor).where(Vendedor.id == producto_data.vendedor_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Vendedor {producto_data.vendedor_id} no encontrado"
        )

    # Verificar categoría si se proporciona
    if producto_data.categoria_id:
        result = await session.execute(
            select(Categoria).where(Categoria.id == producto_data.categoria_id)
        )
        if not result.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Categoría {producto_data.categoria_id} no encontrada"
            )

    # Crear producto
    db_producto = Producto(
        nombre=producto_data.nombre,
        descripcion=producto_data.descripcion,
        precio=producto_data.precio,
        stock=producto_data.stock,
        vendedor_id=producto_data.vendedor_id,
        categoria_id=producto_data.categoria_id,
        is_active=True
    )

    producto_creado = await producto_repo.create(session, db_producto)

    # Asignar etiquetas
    if producto_data.etiquetas:
        for etiqueta_id in producto_data.etiquetas:
            result = await session.execute(
                select(Etiqueta).where(Etiqueta.id == etiqueta_id)
            )
            etiqueta = result.scalar_one_or_none()
            if etiqueta:
                producto_creado.etiquetas.append(etiqueta)
        await session.flush()
        await session.refresh(producto_creado)

    return producto_creado


@router.get("/", response_model=List[ProductoResponse])
async def listar_productos(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    categoria_id: Optional[int] = Query(None),
    vendedor_id: Optional[int] = Query(None),
    min_precio: Optional[float] = Query(None, ge=0),
    max_precio: Optional[float] = Query(None, ge=0),
    is_active: Optional[bool] = Query(True),
    session: AsyncSession = Depends(get_session)
):
    """
    Lista productos con filtros opcionales.

    - **categoria_id**: Filtrar por categoría
    - **vendedor_id**: Filtrar por vendedor
    - **min_precio**: Precio mínimo
    - **max_precio**: Precio máximo
    - **is_active**: Solo productos activos (default True)
    """
    query = select(Producto)
    conditions = []

    if categoria_id:
        conditions.append(Producto.categoria_id == categoria_id)
    if vendedor_id:
        conditions.append(Producto.vendedor_id == vendedor_id)
    if min_precio is not None:
        conditions.append(Producto.precio >= min_precio)
    if max_precio is not None:
        conditions.append(Producto.precio <= max_precio)
    if is_active is not None:
        conditions.append(Producto.is_active == is_active)

    if conditions:
        query = query.where(and_(*conditions))

    query = query.offset(skip).limit(limit).order_by(Producto.created_at.desc())

    result = await session.execute(query)
    productos = result.scalars().all()
    return list(productos)


@router.get("/{producto_id}", response_model=ProductoWithDetails)
async def obtener_producto(
    producto_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Obtiene un producto con detalles expandidos."""
    result = await session.execute(
        select(Producto)
        .options(selectinload(Producto.etiquetas))
        .where(Producto.id == producto_id)
    )
    producto = result.scalar_one_or_none()

    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto {producto_id} no encontrado"
        )

    # Obtener nombre de categoría
    categoria_nombre = None
    if producto.categoria_id:
        result_cat = await session.execute(
            select(Categoria.nombre).where(Categoria.id == producto.categoria_id)
        )
        categoria_nombre = result_cat.scalar_one_or_none()

    # Obtener nombre de tienda del vendedor
    result_vend = await session.execute(
        select(Vendedor.nombre_tienda).where(Vendedor.id == producto.vendedor_id)
    )
    vendedor_nombre = result_vend.scalar_one_or_none()

    return ProductoWithDetails(
        id=producto.id,
        nombre=producto.nombre,
        descripcion=producto.descripcion,
        precio=producto.precio,
        stock=producto.stock,
        is_active=producto.is_active,
        vendedor_id=producto.vendedor_id,
        categoria_id=producto.categoria_id,
        created_at=producto.created_at,
        categoria_nombre=categoria_nombre,
        vendedor_nombre_tienda=vendedor_nombre,
        etiquetas=[e.nombre for e in producto.etiquetas]
    )


@router.get("/buscar/", response_model=List[ProductoResponse])
async def buscar_productos(
    q: str = Query(..., min_length=2),
    limit: int = Query(10, ge=1, le=50),
    session: AsyncSession = Depends(get_session)
):
    """Busca productos por nombre (búsqueda parcial)."""
    result = await session.execute(
        select(Producto)
        .where(
            and_(
                Producto.nombre.ilike(f"%{q}%"),
                Producto.is_active == True
            )
        )
        .limit(limit)
    )
    return list(result.scalars().all())
```

## 6.4 Rutas de Órdenes

```python
# app/routes/ordenes.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload
from typing import List
from decimal import Decimal

from app.database.connection import get_session
from app.models.orden import Orden, OrdenItem
from app.models.producto import Producto
from app.schemas.orden import (
    OrdenCreate,
    OrdenItemCreate,
    OrdenResponse,
    OrdenWithItems,
    OrdenItemResponse
)

router = APIRouter(prefix="/ordenes", tags=["Órdenes"])


@router.post("/", response_model=OrdenWithItems, status_code=201)
async def crear_orden(
    orden_data: OrdenCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Crea una nueva orden con sus items.

    Valida que los productos existan y tengan stock suficiente.
    Calcula el total automáticamente.
    """
    # Verificar que los productos existen y tienen stock
    total = Decimal("0.00")
    items_data = []

    for item_data in orden_data.items:
        result = await session.execute(
            select(Producto).where(Producto.id == item_data.producto_id)
        )
        producto = result.scalar_one_or_none()

        if not producto:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Producto {item_data.producto_id} no encontrado"
            )

        if not producto.is_active:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Producto {producto.nombre} no está activo"
            )

        if producto.stock < item_data.cantidad:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Stock insuficiente para {producto.nombre}. Disponible: {producto.stock}"
            )

        items_data.append({
            "producto": producto,
            "cantidad": item_data.cantidad,
            "precio_unitario": producto.precio
        })
        total += producto.precio * item_data.cantidad

    # Crear la orden
    db_orden = Orden(
        usuario_id=orden_data.usuario_id,
        status="pendiente",
        total=total
    )
    session.add(db_orden)
    await session.flush()  # Obtener el ID

    # Crear items y actualizar stock
    orden_items = []
    for item in items_data:
        orden_item = OrdenItem(
            orden_id=db_orden.id,
            producto_id=item["producto"].id,
            cantidad=item["cantidad"],
            precio_unitario=item["precio_unitario"]
        )
        session.add(orden_item)

        # Reducir stock
        item["producto"].stock -= item["cantidad"]

        orden_items.append(orden_item)

    await session.flush()
    await session.refresh(db_orden)

    return OrdenWithItems(
        id=db_orden.id,
        usuario_id=db_orden.usuario_id,
        status=db_orden.status,
        total=db_orden.total,
        fecha_creacion=db_orden.fecha_creacion,
        fecha_updated=db_orden.fecha_updated,
        items=[OrdenItemResponse.model_validate(i) for i in orden_items]
    )


@router.get("/", response_model=List[OrdenResponse])
async def listar_ordenes(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    usuario_id: int = Query(None),
    status_filter: str = Query(None, alias="status"),
    session: AsyncSession = Depends(get_session)
):
    """Lista órdenes con filtros opcionales."""
    query = select(Orden)
    conditions = []

    if usuario_id:
        conditions.append(Orden.usuario_id == usuario_id)
    if status_filter:
        conditions.append(Orden.status == status_filter)

    if conditions:
        query = query.where(and_(*conditions))

    query = query.offset(skip).limit(limit).order_by(Orden.fecha_creacion.desc())

    result = await session.execute(query)
    return list(result.scalars().all())


@router.get("/{orden_id}", response_model=OrdenWithItems)
async def obtener_orden(
    orden_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Obtiene una orden con todos sus items."""
    result = await session.execute(
        select(Orden)
        .options(selectinload(Orden.items))
        .where(Orden.id == orden_id)
    )
    orden = result.scalar_one_or_none()

    if not orden:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Orden {orden_id} no encontrada"
        )

    return OrdenWithItems.model_validate(orden)
```

## Ejercicios Prácticos

**Ejercicio 1**: Implementa el endpoint DELETE para productos que marque como inactivo en lugar de eliminar (soft delete).

**Ejercicio 2**: Crea un endpoint `POST /productos/bulk` que permita crear múltiples productos en una sola transacción.

**Ejercicio 3**: Implementa un endpoint `GET /productos/stats` que retorne estadísticas: total de productos, precio promedio, stock total.

---

# SESIÓN 7: CRUD Completo - Update y Delete

## Duración: 2 horas

## Objetivos de Aprendizaje

- Implementar endpoints PUT y PATCH para actualizar recursos
- Implementar DELETE para eliminar recursos
- Manejar actualizaciones parciales vs completas
- Implementar soft delete

## 7.1 Actualización Completa vs Parcial

```python
# PUT vs PATCH

# PUT - Reemplaza completamente el recurso
# Todos los campos son requeridos
@router.put("/{usuario_id}")
async def actualizar_usuario_completo(
    usuario_id: int,
    usuario_data: UsuarioCreate  # Todos los campos requeridos
):
    """
    PUT reemplaza todos los campos.
    Si no mando "is_active", se pierde el valor actual.
    """
    pass

# PATCH - Actualización parcial
# Solo los campos proporcionados se actualizan
@router.patch("/{usuario_id}")
async def actualizar_usuario_parcial(
    usuario_id: int,
    usuario_data: UsuarioUpdate  # Todos opcionales
):
    """
    PATCH solo actualiza los campos no nulos.
    Los campos omitidos mantienen su valor actual.
    """
    pass
```

## 7.2 Rutas de Actualización

```python
# app/routes/usuarios.py (continuación)

@router.put("/{usuario_id}", response_model=UsuarioResponse)
async def actualizar_usuario(
    usuario_id: int,
    usuario_data: UsuarioCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Actualización completa de usuario (PUT).
    Requiere todos los campos.
    """
    # Obtener usuario existente
    usuario = await usuario_repo.get(session, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario {usuario_id} no encontrado"
        )

    # Verificar si el nuevo email ya está en uso por otro usuario
    if usuario_data.email != usuario.email:
        existing = await usuario_repo.get_by_email(session, usuario_data.email)
        if existing and existing.id != usuario_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El email {usuario_data.email} ya está en uso"
            )

    # Actualizar todos los campos
    usuario.email = usuario_data.email
    usuario.nombre = usuario_data.nombre
    usuario.password_hash = usuario_data.password  # En producción: hashear
    usuario.rol = usuario_data.rol

    await session.flush()
    await session.refresh(usuario)
    return usuario


@router.patch("/{usuario_id}", response_model=UsuarioResponse)
async def actualizar_usuario_parcial(
    usuario_id: int,
    usuario_data: UsuarioUpdate,
    session: AsyncSession = Depends(get_session)
):
    """
    Actualización parcial de usuario (PATCH).
    Solo actualiza los campos proporcionados.
    """
    usuario = await usuario_repo.get(session, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario {usuario_id} no encontrado"
        )

    # Solo actualizar campos no nulos
    updates = usuario_data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(usuario, field, value)

    await session.flush()
    await session.refresh(usuario)
    return usuario


@router.delete("/{usuario_id}", status_code=204)
async def eliminar_usuario(
    usuario_id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Elimina un usuario (hard delete).
    ADVERTENCIA: Esto elimina permanentemente el registro.
    """
    usuario = await usuario_repo.get(session, usuario_id)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario {usuario_id} no encontrado"
        )

    await session.delete(usuario)
    await session.flush()
    return None
```

## 7.3 Soft Delete vs Hard Delete

```python
# app/routes/productos.py (continuación)

@router.put("/{producto_id}", response_model=ProductoResponse)
async def actualizar_producto(
    producto_id: int,
    producto_data: ProductoCreate,
    session: AsyncSession = Depends(get_session)
):
    """Actualización completa de producto."""
    producto = await producto_repo.get(session, producto_id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto {producto_id} no encontrado"
        )

    # Verificar vendedor
    result = await session.execute(
        select(Vendedor).where(Vendedor.id == producto_data.vendedor_id)
    )
    if not result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Vendedor no válido"
        )

    # Actualizar campos
    producto.nombre = producto_data.nombre
    producto.descripcion = producto_data.descripcion
    producto.precio = producto_data.precio
    producto.stock = producto_data.stock
    producto.vendedor_id = producto_data.vendedor_id
    producto.categoria_id = producto_data.categoria_id

    await session.flush()
    await session.refresh(producto)
    return producto


@router.patch("/{producto_id}", response_model=ProductoResponse)
async def actualizar_producto_parcial(
    producto_id: int,
    producto_data: ProductoUpdate,
    session: AsyncSession = Depends(get_session)
):
    """Actualización parcial de producto."""
    producto = await producto_repo.get(session, producto_id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto {producto_id} no encontrado"
        )

    updates = producto_data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(producto, field, value)

    await session.flush()
    await session.refresh(producto)
    return producto


@router.delete("/{producto_id}", status_code=204)
async def eliminar_producto(
    producto_id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Eliminación suave (soft delete) de producto.
    En lugar de eliminar, marca como inactivo.
    """
    producto = await producto_repo.get(session, producto_id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto {producto_id} no encontrado"
        )

    producto.is_active = False
    await session.flush()
    return None


@router.post("/{producto_id}/reactivar", response_model=ProductoResponse)
async def reactivar_producto(
    producto_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Reactiva un producto previamente desactivado."""
    producto = await producto_repo.get(session, producto_id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto {producto_id} no encontrado"
        )

    if producto.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El producto ya está activo"
        )

    producto.is_active = True
    await session.flush()
    await session.refresh(producto)
    return producto


@router.delete("/{producto_id}/hard", status_code=204)
async def eliminar_producto_permanente(
    producto_id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Eliminación permanente (hard delete).
    SOLO para uso administrativo. No reversible.
    """
    producto = await producto_repo.get(session, producto_id)
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto {producto_id} no encontrado"
        )

    await session.delete(producto)
    await session.flush()
    return None
```

## 7.4 Actualización de Órdenes

```python
# app/routes/ordenes.py (continuación)

# Posibles transiciones de status
STATUS_TRANSITIONS = {
    "pendiente": ["pagado", "cancelado"],
    "pagado": ["enviado", "cancelado"],
    "enviado": ["entregado"],
    "entregado": [],  # Estado final
    "cancelado": []   # Estado final
}


@router.patch("/{orden_id}/status", response_model=OrdenResponse)
async def actualizar_status_orden(
    orden_id: int,
    new_status: str = Query(..., alias="status"),
    session: AsyncSession = Depends(get_session)
):
    """
    Actualiza el status de una orden.

    Respects the status workflow:
    - pendiente → pagado, cancelado
    - pagado → enviado, cancelado
    - enviado → entregado
    - entregado → (final)
    - cancelado → (final)
    """
    orden = await producto_repo.get(session, orden_id)
    if not orden:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Orden {orden_id} no encontrada"
        )

    # Validar transición
    allowed = STATUS_TRANSITIONS.get(orden.status, [])
    if new_status not in allowed:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"No se puede cambiar de '{orden.status}' a '{new_status}'. "
                   f"Estados permitidos: {allowed}"
        )

    # Si se cancela, restaurar stock
    if new_status == "cancelado":
        result = await session.execute(
            select(OrdenItem).where(OrdenItem.orden_id == orden_id)
        )
        items = result.scalars().all()

        for item in items:
            result_prod = await session.execute(
                select(Producto).where(Producto.id == item.producto_id)
            )
            producto = result_prod.scalar_one()
            producto.stock += item.cantidad

    orden.status = new_status
    await session.flush()
    await session.refresh(orden)
    return orden


@router.delete("/{orden_id}", status_code=204)
async def cancelar_orden(
    orden_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Cancela una orden (soft delete)."""
    orden = await producto_repo.get(session, orden_id)
    if not orden:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Orden {orden_id} no encontrada"
        )

    if orden.status == "entregado":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="No se puede cancelar una orden entregada"
        )

    # Restaurar stock si ya estaba pagada
    if orden.status in ("pagado", "enviado"):
        result = await session.execute(
            select(OrdenItem).where(OrdenItem.orden_id == orden_id)
        )
        items = result.scalars().all()
        for item in items:
            result_prod = await session.execute(
                select(Producto).where(Producto.id == item.producto_id)
            )
            producto = result_prod.scalar_one()
            producto.stock += item.cantidad

    orden.status = "cancelado"
    await session.flush()
    return None
```

## 7.5 Validaciones en Cascada

```python
# Validaciones al eliminar categorías
@router.delete("/categorias/{categoria_id}", status_code=204)
async def eliminar_categoria(
    categoria_id: int,
    force: bool = Query(False, description="Forzar eliminación incluso con productos"),
    session: AsyncSession = Depends(get_session)
):
    """
    Elimina una categoría.

    Si force=False y tiene productos, retorna error.
    Si force=True, desvincula los productos primero.
    """
    result = await session.execute(
        select(Categoria).where(Categoria.id == categoria_id)
    )
    categoria = result.scalar_one_or_none()

    if not categoria:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Categoría {categoria_id} no encontrada"
        )

    # Verificar si tiene productos
    result_prod = await session.execute(
        select(Producto).where(Producto.categoria_id == categoria_id)
    )
    productos = result_prod.scalars().all()

    if productos and not force:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La categoría tiene {len(productos)} productos. "
                   f"Use ?force=true para forzar la eliminación."
        )

    # Desvincular productos
    if productos:
        for prod in productos:
            prod.categoria_id = None

    await session.delete(categoria)
    await session.flush()
    return None
```

## 7.6 Batch Updates

```python
# app/routes/productos.py

@router.patch("/batch/stock")
async def actualizar_stock_batch(
    updates: List[dict],  # [{"producto_id": 1, "stock_delta": -5}, ...]
    session: AsyncSession = Depends(get_session)
):
    """
    Actualiza stock de múltiples productos en una operación.

    Recibe cambios delta (positivos o negativos).
    Valida stock no quede negativo.
    """
    results = []
    errors = []

    for update in updates:
        producto_id = update.get("producto_id")
        delta = update.get("stock_delta", 0)

        result = await session.execute(
            select(Producto).where(Producto.id == producto_id)
        )
        producto = result.scalar_one_or_none()

        if not producto:
            errors.append({"producto_id": producto_id, "error": "No encontrado"})
            continue

        new_stock = producto.stock + delta
        if new_stock < 0:
            errors.append({
                "producto_id": producto_id,
                "error": f"Stock insuficiente. Actual: {producto.stock}, Delta: {delta}"
            })
            continue

        producto.stock = new_stock
        results.append({"producto_id": producto_id, "new_stock": new_stock})

    await session.flush()

    return {
        "updated": results,
        "errors": errors,
        "total_updated": len(results),
        "total_errors": len(errors)
    }
```

## Ejercicios Prácticos

**Ejercicio 1**: Implementa el endpoint `PATCH /vendedores/{id}` para actualizar solo el `rating` y `is_verified`.

**Ejercicio 2**: Crea un endpoint `POST /ordenes/{orden_id}/cancel` que cancele la orden y restaure el stock de todos sus items.

**Ejercicio 3**: Implementa `DELETE /usuarios/{id}` que verifique primero si el usuario tiene órdenes activas antes de eliminarlo.

---

# SESIÓN 8: Relaciones Uno a Muchos (1:N)

## Duración: 2 horas

## Objetivos de Aprendizaje

- Implementar relaciones 1:N con SQLModel
- Cargar relaciones con selectinload y joinedload
- Diseñar endpoints que aprovechen las relaciones
- Manejar datos relacionados en schemas

## 8.1 Concepto de Relaciones 1:N

```mermaid
erDiagram
    VENDEDOR ||--o{ PRODUCTO : "1:N"
    VENDEDOR {
        int id PK
        string nombre_tienda
    }
    PRODUCTO {
        int id PK
        int vendedor_id FK
        string nombre
        decimal precio
    }

    note right of VENDEDOR : "Un vendedor tiene MUCHOS productos"
    note left of PRODUCTO : "Cada producto pertenece a UN vendedor"
```

## 8.2 Schemas con Relaciones

```python
# app/schemas/vendedor.py
from pydantic import BaseModel, ConfigDict
from typing import Optional, List
from datetime import datetime
from decimal import Decimal


class VendedorBase(BaseModel):
    usuario_id: int
    nombre_tienda: str
    descripcion: Optional[str] = None
    telefono: Optional[str] = None


class VendedorCreate(VendedorBase):
    pass


class VendedorUpdate(BaseModel):
    nombre_tienda: Optional[str] = None
    descripcion: Optional[str] = None
    telefono: Optional[str] = None
    is_verified: Optional[bool] = None


class VendedorResponse(VendedorBase):
    id: int
    rating: Decimal
    is_verified: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class VendedorWithStats(VendedorResponse):
    total_productos: int = 0
    productos_activos: int = 0


class ProductoMini(BaseModel):
    """Producto resumido para incluir en respuestas de vendedor."""
    id: int
    nombre: str
    precio: Decimal
    is_active: bool

    model_config = ConfigDict(from_attributes=True)


class VendedorWithProductos(VendedorResponse):
    productos: List[ProductoMini] = []
```

## 8.3 Repository con Carga de Relaciones

```python
# app/repositories/vendedor.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlalchemy.orm import selectinload
from app.models.vendedor import Vendedor
from app.models.producto import Producto
from app.repositories.base import BaseRepository
from typing import Optional, List

class VendedorRepository(BaseRepository[Vendedor]):
    def __init__(self):
        super().__init__(Vendedor)

    async def get_with_productos(
        self, session: AsyncSession, id: int
    ) -> Optional[Vendedor]:
        """Obtiene vendedor con sus productos cargados."""
        result = await session.execute(
            select(Vendedor)
            .options(selectinload(Vendedor.productos))
            .where(Vendedor.id == id)
        )
        return result.scalar_one_or_none()

    async def get_with_stats(
        self, session: AsyncSession, id: int
    ) -> Optional[dict]:
        """Obtiene vendedor con estadísticas."""
        result = await session.execute(
            select(Vendedor).where(Vendedor.id == id)
        )
        vendedor = result.scalar_one_or_none()

        if not vendedor:
            return None

        # Contar productos
        result_prod = await session.execute(
            select(func.count(Producto.id))
            .where(Producto.vendedor_id == id)
        )
        total = result_prod.scalar() or 0

        result_prod_act = await session.execute(
            select(func.count(Producto.id))
            .where(Producto.vendedor_id == id, Producto.is_active == True)
        )
        activos = result_prod_act.scalar() or 0

        return {
            "vendedor": vendedor,
            "total_productos": total,
            "productos_activos": activos
        }

    async def get_all_with_pagination(
        self, session: AsyncSession, skip: int, limit: int,
        is_verified: Optional[bool] = None
    ) -> tuple[List[Vendedor], int]:
        """Obtiene lista de vendedores con paginación."""
        query = select(Vendedor)
        count_query = select(func.count(Vendedor.id))

        if is_verified is not None:
            query = query.where(Vendedor.is_verified == is_verified)
            count_query = count_query.where(Vendedor.is_verified == is_verified)

        # Total
        total_result = await session.execute(count_query)
        total = total_result.scalar()

        # Resultados paginados
        result = await session.execute(
            query.offset(skip).limit(limit).order_by(Vendedor.created_at.desc())
        )
        vendedores = list(result.scalars().all())

        return vendedores, total


vendedor_repo = VendedorRepository()
```

## 8.4 Rutas de Vendedores

```python
# app/routes/vendedores.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional

from app.database.connection import get_session
from app.models.vendedor import Vendedor
from app.models.usuario import Usuario
from app.models.producto import Producto
from app.schemas.vendedor import (
    VendedorCreate,
    VendedorUpdate,
    VendedorResponse,
    VendedorWithProductos,
    VendedorWithStats
)
from app.repositories.vendedor import vendedor_repo

router = APIRouter(prefix="/vendedores", tags=["Vendedores"])


@router.post("/", response_model=VendedorResponse, status_code=201)
async def crear_vendedor(
    vendedor_data: VendedorCreate,
    session: AsyncSession = Depends(get_session)
):
    """
    Crea un nuevo vendedor.

    Requiere que el usuario exista y no tenga ya un vendedor asociado.
    """
    # Verificar que el usuario existe
    result = await session.execute(
        select(Usuario).where(Usuario.id == vendedor_data.usuario_id)
    )
    usuario = result.scalar_one_or_none()
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Usuario {vendedor_data.usuario_id} no encontrado"
        )

    # Verificar que no tenga ya vendedor
    result = await session.execute(
        select(Vendedor).where(Vendedor.usuario_id == vendedor_data.usuario_id)
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"El usuario {vendedor_data.usuario_id} ya tiene un vendedor asociado"
        )

    db_vendedor = Vendedor(
        usuario_id=vendedor_data.usuario_id,
        nombre_tienda=vendedor_data.nombre_tienda,
        descripcion=vendedor_data.descripcion,
        telefono=vendedor_data.telefono
    )

    vendedor_creado = await vendedor_repo.create(session, db_vendedor)
    return vendedor_creado


@router.get("/", response_model=List[VendedorResponse])
async def listar_vendedores(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    is_verified: Optional[bool] = Query(None),
    session: AsyncSession = Depends(get_session)
):
    """Lista vendedores con paginación."""
    vendedores, _ = await vendedor_repo.get_all_with_pagination(
        session, skip, limit, is_verified
    )
    return vendedores


@router.get("/{vendedor_id}", response_model=VendedorWithStats)
async def obtener_vendedor(
    vendedor_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Obtiene vendedor con estadísticas de productos."""
    result = await vendedor_repo.get_with_stats(session, vendedor_id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vendedor {vendedor_id} no encontrado"
        )

    vendedor = result["vendedor"]
    return VendedorWithStats(
        id=vendedor.id,
        usuario_id=vendedor.usuario_id,
        nombre_tienda=vendedor.nombre_tienda,
        descripcion=vendedor.descripcion,
        telefono=vendedor.telefono,
        rating=vendedor.rating,
        is_verified=vendedor.is_verified,
        created_at=vendedor.created_at,
        total_productos=result["total_productos"],
        productos_activos=result["productos_activos"]
    )


@router.get("/{vendedor_id}/productos", response_model=List[dict])
async def obtener_productos_vendedor(
    vendedor_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    is_active: bool = Query(True),
    session: AsyncSession = Depends(get_session)
):
    """Obtiene todos los productos de un vendedor."""
    # Verificar vendedor existe
    vendedor = await vendedor_repo.get(session, vendedor_id)
    if not vendedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vendedor {vendedor_id} no encontrado"
        )

    query = select(Producto).where(Producto.vendedor_id == vendedor_id)

    if is_active is not None:
        query = query.where(Producto.is_active == is_active)

    result = await session.execute(
        query.offset(skip).limit(limit).order_by(Producto.created_at.desc())
    )
    productos = result.scalars().all()

    return [
        {
            "id": p.id,
            "nombre": p.nombre,
            "precio": p.precio,
            "stock": p.stock,
            "is_active": p.is_active,
            "categoria_id": p.categoria_id
        }
        for p in productos
    ]


@router.get("/{vendedor_id}/full", response_model=VendedorWithProductos)
async def obtener_vendedor_completo(
    vendedor_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Obtiene vendedor con todos sus productos."""
    result = await vendedor_repo.get_with_productos(session, vendedor_id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vendedor {vendedor_id} no encontrado"
        )

    return VendedorWithProductos.model_validate(result)


@router.patch("/{vendedor_id}", response_model=VendedorResponse)
async def actualizar_vendedor(
    vendedor_id: int,
    vendedor_data: VendedorUpdate,
    session: AsyncSession = Depends(get_session)
):
    """Actualización parcial de vendedor."""
    vendedor = await vendedor_repo.get(session, vendedor_id)
    if not vendedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vendedor {vendedor_id} no encontrado"
        )

    updates = vendedor_data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(vendedor, field, value)

    await session.flush()
    await session.refresh(vendedor)
    return vendedor


@router.delete("/{vendedor_id}", status_code=204)
async def eliminar_vendedor(
    vendedor_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Elimina un vendedor (soft delete de sus productos primero)."""
    vendedor = await vendedor_repo.get(session, vendedor_id)
    if not vendedor:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Vendedor {vendedor_id} no encontrado"
        )

    # Desactivar productos asociados
    result = await session.execute(
        select(Producto).where(Producto.vendedor_id == vendedor_id)
    )
    productos = result.scalars().all()
    for prod in productos:
        prod.is_active = False

    await session.delete(vendedor)
    await session.flush()
    return None
```

## 8.5 Carga Eager vs Lazy

```python
# Diferencia entre joinedload y selectinload

# joinedload: Hace un JOIN en la misma query
# Bueno para relaciones 1:1 o cuando siempre necesitas los datos relacionados
async def get_con_join(session, vendedor_id):
    result = await session.execute(
        select(Vendedor)
        .options(joinedload(Vendedor.productos))  # JOIN
        .where(Vendedor.id == vendedor_id)
    )
    return result.unique().scalar_one()

# selectinload: Hace una segunda query con WHERE IN
# Bueno para relaciones 1:N cuando quieres evitar multiplicación de filas
async def get_con_selectin(session, vendedor_id):
    result = await session.execute(
        select(Vendedor)
        .options(selectinload(Vendedor.productos))  # 2 queries
        .where(Vendedor.id == vendedor_id)
    )
    return result.unique().scalar_one()

# PROBLEMA de joinedload con 1:N: multiplicación de filas
# Si un vendedor tiene 100 productos, el JOIN retorna 100 filas duplicadas
# SQLModel/SQLAlchemy las "deduplica" con .unique(), pero es ineficiente

# selectinload es generalmente mejor para relaciones 1:N
```

## 8.6 Filtros Basados en Relaciones

```python
# Encontrar productos con categoría específica
@router.get("/productos/categoria/{categoria_nombre}")
async def productos_por_categoria(
    categoria_nombre: str,
    session: AsyncSession = Depends(get_session)
):
    """Busca productos por nombre de categoría."""
    # Opción 1: Con subquery
    result = await session.execute(
        select(Producto)
        .join(Categoria)
        .where(Categoria.nombre.ilike(f"%{categoria_nombre}%"))
    )
    productos = result.scalars().all()

    # Opción 2: Con exists
    # from sqlalchemy import exists
    # subq = select(Categoria.id).where(
    #     Categoria.id == Producto.categoria_id,
    #     Categoria.nombre.ilike(f"%{categoria_nombre}%")
    # ).exists()
    # result = await session.execute(
    #     select(Producto).where(subq)
    # )

    return productos


# Vendedores con productos de cierto rango de precio
@router.get("/vendedores/productos/rango-precio")
async def vendedores_con_productos_en_rango(
    min_precio: float,
    max_precio: float,
    session: AsyncSession = Depends(get_session)
):
    """Encuentra vendedores que tienen productos en un rango de precio."""
    # Subquery: productos que cumplen el rango
    from sqlalchemy import and_

    result = await session.execute(
        select(Vendedor)
        .join(Producto)
        .where(
            and_(
                Producto.precio >= min_precio,
                Producto.precio <= max_precio,
                Producto.is_active == True
            )
        )
        .group_by(Vendedor.id)
        .having(func.count(Producto.id) >= 1)  # Al menos 1 producto
    )
    return list(result.scalars().all())
```

## Ejercicios Prácticos

**Ejercicio 1**: Implementa `GET /categorias/{id}/productos` que liste todos los productos de una categoría.

**Ejercicio 2**: Crea `GET /usuarios/{id}/ordenes` que retorne todas las órdenes de un usuario con sus items.

**Ejercicio 3**: Implementa `GET /vendedores/{id}/stats` que retorne: total productos, productos activos, valor total del inventario (suma de precio * stock).

---

# SESIÓN 9: Relaciones Muchos a Muchos (N:M)

## Duración: 2 horas

## Objetivos de Aprendizaje

- Implementar relaciones N:M con tabla intermedia
- CRUD sobre relaciones muchos a muchos
- Queries en tablas intermedias
- Sincronización de datos en relaciones N:M

## 9.1 Concepto de Relaciones N:M

```mermaid
erDiagram
    PRODUCTO ||--o{ PRODUCTO_ETIQUETA : "N:M"
    ETIQUETA ||--o{ PRODUCTO_ETIQUETA : "N:M"

    PRODUCTO {
        int id PK
        string nombre
    }

    PRODUCTO_ETIQUETA {
        int producto_id FK
        int etiqueta_id FK
    }

    ETIQUETA {
        int id PK
        string nombre
    }

    note for PRODUCTO "Producto 1 tiene etiquetas: Oferta, Nuevo"
    note for ETIQUETA "Etiqueta 'Oferta' tienen productos: Laptop, Mouse"
```

## 9.2 Schemas para Etiquetas

```python
# app/schemas/etiqueta.py
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime


class EtiquetaBase(BaseModel):
    nombre: str = Field(min_length=2, max_length=50)
    slug: str = Field(min_length=2, max_length=50, pattern=r"^[a-z0-9-]+$")
    color: Optional[str] = Field(default="#6366f1", pattern=r"^#[0-9a-fA-F]{6}$")


class EtiquetaCreate(EtiquetaBase):
    pass


class EtiquetaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=2)
    slug: Optional[str] = Field(None, min_length=2, pattern=r"^[a-z0-9-]+$")
    color: Optional[str] = Field(None, pattern=r"^#[0-9a-fA-F]{6}$")


class EtiquetaResponse(EtiquetaBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class EtiquetaWithCount(EtiquetaResponse):
    productos_count: int = 0
```

## 9.3 Repository de Etiquetas

```python
# app/repositories/etiqueta.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, and_
from app.models.etiqueta import Etiqueta
from app.models.producto import Producto, ProductoEtiqueta
from app.repositories.base import BaseRepository
from typing import Optional, List

class EtiquetaRepository(BaseRepository[Etiqueta]):
    def __init__(self):
        super().__init__(Etiqueta)

    async def get_by_slug(
        self, session: AsyncSession, slug: str
    ) -> Optional[Etiqueta]:
        result = await session.execute(
            select(Etiqueta).where(Etiqueta.slug == slug)
        )
        return result.scalar_one_or_none()

    async def get_or_create(
        self, session: AsyncSession, etiqueta_data: EtiquetaCreate
    ) -> Etiqueta:
        """Busca por slug, crea si no existe."""
        etiqueta = await self.get_by_slug(session, etiqueta_data.slug)
        if etiqueta:
            return etiqueta

        db_etiqueta = Etiqueta(**etiqueta_data.model_dump())
        return await self.create(session, db_etiqueta)

    async def get_with_count(
        self, session: AsyncSession, id: int
    ) -> Optional[dict]:
        etiqueta = await self.get(session, id)
        if not etiqueta:
            return None

        result = await session.execute(
            select(func.count(ProductoEtiqueta.producto_id))
            .where(ProductoEtiqueta.etiqueta_id == id)
        )
        count = result.scalar()

        return {"etiqueta": etiqueta, "productos_count": count}

    async def get_productos(
        self, session: AsyncSession, etiqueta_id: int
    ) -> List[Producto]:
        result = await session.execute(
            select(Producto)
            .join(ProductoEtiqueta)
            .where(ProductoEtiqueta.etiqueta_id == etiqueta_id)
            .where(Producto.is_active == True)
        )
        return list(result.scalars().all())


etiqueta_repo = EtiquetaRepository()
```

## 9.4 Rutas de Etiquetas

```python
# app/routes/etiquetas.py
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List

from app.database.connection import get_session
from app.models.etiqueta import Etiqueta
from app.schemas.etiqueta import (
    EtiquetaCreate,
    EtiquetaUpdate,
    EtiquetaResponse,
    EtiquetaWithCount
)
from app.repositories.etiqueta import etiqueta_repo

router = APIRouter(prefix="/etiquetas", tags=["Etiquetas"])


@router.post("/", response_model=EtiquetaResponse, status_code=201)
async def crear_etiqueta(
    etiqueta_data: EtiquetaCreate,
    session: AsyncSession = Depends(get_session)
):
    """Crea una nueva etiqueta."""
    # Verificar slug único
    existing = await etiqueta_repo.get_by_slug(session, etiqueta_data.slug)
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"La etiqueta con slug '{etiqueta_data.slug}' ya existe"
        )

    db_etiqueta = Etiqueta(**etiqueta_data.model_dump())
    return await etiqueta_repo.create(session, db_etiqueta)


@router.get("/", response_model=List[EtiquetaResponse])
async def listar_etiquetas(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    session: AsyncSession = Depends(get_session)
):
    """Lista todas las etiquetas."""
    return await etiqueta_repo.get_all(session, skip, limit)


@router.get("/{etiqueta_id}", response_model=EtiquetaWithCount)
async def obtener_etiqueta(
    etiqueta_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Obtiene etiqueta con conteo de productos."""
    result = await etiqueta_repo.get_with_count(session, etiqueta_id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Etiqueta {etiqueta_id} no encontrada"
        )

    etiqueta = result["etiqueta"]
    return EtiquetaWithCount(
        id=etiqueta.id,
        nombre=etiqueta.nombre,
        slug=etiqueta.slug,
        color=etiqueta.color,
        productos_count=result["productos_count"]
    )


@router.patch("/{etiqueta_id}", response_model=EtiquetaResponse)
async def actualizar_etiqueta(
    etiqueta_id: int,
    etiqueta_data: EtiquetaUpdate,
    session: AsyncSession = Depends(get_session)
):
    """Actualiza parcialmente una etiqueta."""
    etiqueta = await etiqueta_repo.get(session, etiqueta_id)
    if not etiqueta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Etiqueta {etiqueta_id} no encontrada"
        )

    # Si cambia slug, verificar que no exista
    if etiqueta_data.slug and etiqueta_data.slug != etiqueta.slug:
        existing = await etiqueta_repo.get_by_slug(session, etiqueta_data.slug)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"El slug '{etiqueta_data.slug}' ya está en uso"
            )

    updates = etiqueta_data.model_dump(exclude_unset=True)
    for field, value in updates.items():
        setattr(etiqueta, field, value)

    await session.flush()
    await session.refresh(etiqueta)
    return etiqueta


@router.delete("/{etiqueta_id}", status_code=204)
async def eliminar_etiqueta(
    etiqueta_id: int,
    session: AsyncSession = Depends(get_session)
):
    """
    Elimina una etiqueta.
    Las relaciones en producto_etiqueta se eliminan en cascada (ON DELETE CASCADE).
    """
    etiqueta = await etiqueta_repo.get(session, etiqueta_id)
    if not etiqueta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Etiqueta {etiqueta_id} no encontrada"
        )

    await session.delete(etiqueta)
    await session.flush()
    return None
```

## 9.5 Gestión de Etiquetas en Productos

```python
# Añadir endpoint para añadir etiquetas a un producto
@router.post("/{producto_id}/etiquetas/{etiqueta_id}", status_code=201)
async def agregar_etiqueta_producto(
    producto_id: int,
    etiqueta_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Asocia una etiqueta a un producto."""
    # Verificar producto
    result = await session.execute(
        select(Producto).where(Producto.id == producto_id)
    )
    producto = result.scalar_one_or_none()
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto {producto_id} no encontrado"
        )

    # Verificar etiqueta
    etiqueta = await etiqueta_repo.get(session, etiqueta_id)
    if not etiqueta:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Etiqueta {etiqueta_id} no encontrada"
        )

    # Verificar que no existe ya la relación
    result = await session.execute(
        select(ProductoEtiqueta)
        .where(
            ProductoEtiqueta.producto_id == producto_id,
            ProductoEtiqueta.etiqueta_id == etiqueta_id
        )
    )
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La etiqueta ya está asociada al producto"
        )

    # Crear relación
    rel = ProductoEtiqueta(producto_id=producto_id, etiqueta_id=etiqueta_id)
    session.add(rel)
    await session.flush()

    return {"message": "Etiqueta agregada", "etiqueta_id": etiqueta_id}


@router.delete("/{producto_id}/etiquetas/{etiqueta_id}", status_code=204)
async def quitar_etiqueta_producto(
    producto_id: int,
    etiqueta_id: int,
    session: AsyncSession = Depends(get_session)
):
    """Desasocia una etiqueta de un producto."""
    result = await session.execute(
        select(ProductoEtiqueta)
        .where(
            ProductoEtiqueta.producto_id == producto_id,
            ProductoEtiqueta.etiqueta_id == etiqueta_id
        )
    )
    rel = result.scalar_one_or_none()
    if not rel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La relación no existe"
        )

    await session.delete(rel)
    await session.flush()
    return None


@router.put("/{producto_id}/etiquetas", response_model=List[EtiquetaResponse])
async def actualizar_etiquetas_producto(
    producto_id: int,
    etiquetas_ids: List[int],
    session: AsyncSession = Depends(get_session)
):
    """
    Reemplaza todas las etiquetas de un producto.

    Útil para actualizaciones completas del conjunto de etiquetas.
    """
    # Verificar producto
    result = await session.execute(
        select(Producto).where(Producto.id == producto_id)
    )
    producto = result.scalar_one_or_none()
    if not producto:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Producto {producto_id} no encontrado"
        )

    # Verificar todas las etiquetas existen
    for etiqueta_id in etiquetas_ids:
        etiqueta = await etiqueta_repo.get(session, etiqueta_id)
        if not etiqueta:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Etiqueta {etiqueta_id} no encontrada"
            )

    # Eliminar relaciones actuales
    result = await session.execute(
        select(ProductoEtiqueta).where(ProductoEtiqueta.producto_id == producto_id)
    )
    for rel in result.scalars().all():
        await session.delete(rel)

    # Crear nuevas relaciones
    etiquetas = []
    for etiqueta_id in etiquetas_ids:
        rel = ProductoEtiqueta(producto_id=producto_id, etiqueta_id=etiqueta_id)
        session.add(rel)
        etiqueta = await etiqueta_repo.get(session, etiqueta_id)
        etiquetas.append(etiqueta)

    await session.flush()
    return etiquetas
```

## 9.6 Queries con Múltiples Tags

```python
# Buscar productos que tengan TODAS las etiquetas especificadas
@router.get("/productos/con-etiquetas/")
async def productos_con_todas_etiquetas(
    etiquetas: List[int] = Query(...),  # /productos/con-etiquetas/?etiquetas=1&etiquetas=2
    session: AsyncSession = Depends(get_session)
):
    """
    Retorna productos que tienen TODAS las etiquetas especificadas.

    Ejemplo: /productos/con-etiquetas/?etiquetas=1&etiquetas=2
    Retorna productos que tienen etiqueta 1 Y etiqueta 2.
    """
    if not etiquetas:
        return []

    # Productos que tienen cada etiqueta
    result = await session.execute(
        select(Producto.id)
        .join(ProductoEtiqueta)
        .where(ProductoEtiqueta.etiqueta_id.in_(etiquetas))
        .group_by(Producto.id)
        .having(func.count(ProductoEtiqueta.etiqueta_id) == len(etiquetas))
    )
    producto_ids = [row[0] for row in result.all()]

    if not producto_ids:
        return []

    # Obtener productos completos
    result = await session.execute(
        select(Producto).where(Producto.id.in_(producto_ids))
    )
    return list(result.scalars().all())


# Buscar productos que tengan AL MENOS UNA de las etiquetas
@router.get("/productos/etiquetas/")
async def productos_con_alguna_etiqueta(
    etiquetas: List[int] = Query(...),
    session: AsyncSession = Depends(get_session)
):
    """
    Retorna productos que tienen AL MENOS UNA de las etiquetas.

    Ejemplo: /productos/etiquetas/?etiquetas=1&etiquetas=2
    Retorna productos que tienen etiqueta 1 Ó etiqueta 2.
    """
    if not etiquetas:
        return []

    result = await session.execute(
        select(Producto)
        .join(ProductoEtiqueta)
        .where(ProductoEtiqueta.etiqueta_id.in_(etiquetas))
        .distinct()
    )
    return list(result.scalars().all())
```

## 9.7 Tags Más Populares

```python
# Endpoint para obtener tags más usados
@router.get("/etiquetas/populares", response_model=List[dict])
async def etiquetas_populares(
    limit: int = Query(10, ge=1, le=50),
    session: AsyncSession = Depends(get_session)
):
    """Retorna las etiquetas más usadas, ordenadas por cantidad de productos."""
    result = await session.execute(
        select(
            Etiqueta.id,
            Etiqueta.nombre,
            Etiqueta.slug,
            func.count(ProductoEtiqueta.producto_id).label("productos_count")
        )
        .join(ProductoEtiqueta, Etiqueta.id == ProductoEtiqueta.etiqueta_id)
        .join(Producto, Producto.id == ProductoEtiqueta.producto_id)
        .where(Producto.is_active == True)
        .group_by(Etiqueta.id, Etiqueta.nombre, Etiqueta.slug)
        .order_by(func.count(ProductoEtiqueta.producto_id).desc())
        .limit(limit)
    )

    return [
        {"id": row[0], "nombre": row[1], "slug": row[2], "productos_count": row[3]}
        for row in result.all()
    ]
```

## Ejercicios Prácticos

**Ejercicio 1**: Implementa `GET /etiquetas/{id}/productos` que liste todos los productos asociados a una etiqueta.

**Ejercicio 2**: Crea un endpoint `POST /productos/{id}/etiquetas/batch` que añada múltiples etiquetas a un producto.

**Ejercicio 3**: Implementa `DELETE /productos/{id}/etiquetas` que quite todas las etiquetas de un producto.

---

# SESIÓN 10: Proyecto Integrador de la Parte 1

## Duración: 2 horas

## Objetivos

- Integrar todos los conceptos aprendidos
- Construir una API funcional con todas las operaciones
- Practicar el flujo completo de desarrollo

## 10.1 Estructura Final del Proyecto

```
marketHub/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── config.py
│   ├── database/
│   │   ├── __init__.py
│   │   └── connection.py
│   ├── models/
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── vendedor.py
│   │   ├── producto.py
│   │   ├── categoria.py
│   │   ├── etiqueta.py
│   │   └── orden.py
│   ├── schemas/
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── vendedor.py
│   │   ├── producto.py
│   │   ├── categoria.py
│   │   ├── etiqueta.py
│   │   └── orden.py
│   ├── repositories/
│   │   ├── __init__.py
│   │   ├── base.py
│   │   ├── usuario.py
│   │   ├── producto.py
│   │   └── orden.py
│   └── routes/
│       ├── __init__.py
│       ├── usuarios.py
│       ├── vendedores.py
│       ├── productos.py
│       ├── categorias.py
│       ├── etiquetas.py
│       └── ordenes.py
├── tests/
│   └── ...
├── requirements.txt
├── .env
└── alembic/
```

## 10.2 Aplicación Completa

```python
# app/main.py
from fastapi import FastAPI
from contextlib import asynccontextmanager

from app.config import settings
from app.database.connection import init_db, close_db
from app.routes import (
    usuarios, vendedores, productos,
    categorias, etiquetas, ordenes
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    await close_db()

app = FastAPI(
    title="MarketHub API",
    description="API completa de e-commerce",
    version="1.0.0",
    lifespan=lifespan
)

app.include_router(usuarios.router)
app.include_router(vendedores.router)
app.include_router(productos.router)
app.include_router(categorias.router)
app.include_router(etiquetas.router)
app.include_router(ordenes.router)

@app.get("/")
async def root():
    return {"message": "MarketHub API", "version": "1.0.0"}

@app.get("/health")
async def health():
    return {"status": "healthy"}
```

## 10.3 Endpoints Resumen

### Usuarios
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | /usuarios | Crear usuario |
| GET | /usuarios | Listar usuarios |
| GET | /usuarios/{id} | Obtener usuario |
| GET | /usuarios/email/{email} | Obtener por email |
| PUT | /usuarios/{id} | Actualización completa |
| PATCH | /usuarios/{id} | Actualización parcial |
| DELETE | /usuarios/{id} | Eliminar usuario |

### Productos
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | /productos | Crear producto |
| GET | /productos | Listar con filtros |
| GET | /productos/{id} | Obtener producto |
| GET | /productos/buscar | Buscar por nombre |
| PUT | /productos/{id} | Actualización completa |
| PATCH | /productos/{id} | Actualización parcial |
| DELETE | /productos/{id} | Soft delete |
| POST | /productos/{id}/reactivar | Reactivar |
| POST | /productos/{id}/etiquetas/{et_id} | Añadir etiqueta |
| DELETE | /productos/{id}/etiquetas/{et_id} | Quitar etiqueta |
| PUT | /productos/{id}/etiquetas | Reemplazar etiquetas |

### Órdenes
| Método | Endpoint | Descripción |
|--------|----------|-------------|
| POST | /ordenes | Crear orden |
| GET | /ordenes | Listar órdenes |
| GET | /ordenes/{id} | Obtener orden con items |
| PATCH | /ordenes/{id}/status | Cambiar status |
| DELETE | /ordenes/{id} | Cancelar orden |

## 10.4 Ejercicio Final: Prueba Integral

Implementa los siguientes escenarios usando la API:

1. **Registro de vendedor**: Crear usuario → Crear vendedor → Crear productos
2. **Compra completa**: Crear orden → Verificar stock → Actualizar status
3. **Búsqueda por tags**: Crear etiquetas → Asignar a productos → Buscar
4. **Reportes**: Productos por vendedor → Órdenes por usuario → Stats

---

# PARTE 1 COMPLETADA

## Resumen de Conceptos

Sesiones 1-10 cubrieron:
- Fundamentos de SQL y PostgreSQL
- Programación asíncrona con async/await
- SQLModel como ORM
- FastAPI para APIs REST
- CRUD completo (Create, Read, Update, Delete)
- Relaciones 1:N y N:M
- Carga de relaciones (selectinload, joinedload)
- Patrón Repository

## Próxima Parte: Sesiones 11-20

- Consultas avanzadas y agregaciones
- Validación y serialización
- Manejo de errores
- Paginación y ordenamiento
- Transacciones y concurrencia
- Migraciones con Alembic
- Autenticación JWT
- Testing
- Optimización
- Proyecto final
