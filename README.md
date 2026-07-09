# Docker explicado desde cero, construyendo una app FastAPI + PostgreSQL

> El objetivo de este documento es que entiendas **qué es Docker**, **para qué se usa** y cómo aplicarlo construyendo, paso a paso, una aplicación real: una API **FastAPI** que se conecta a una base de datos **PostgreSQL**. Al final tendrás todo lo necesario para ejecutar la app en **cualquier máquina** con un solo comando.

---

## 1. ¿Qué es Docker?

Docker es una herramienta que permite **empaquetar** una aplicación junto con **todas sus dependencias** (librerías, versión de Python, configuración del sistema operativo, variables de entorno, etc.) dentro de una unidad autocontenida llamada **contenedor**.

Un contenedor es, a grandes rasgos, un proceso aislado que se ejecuta sobre el motor de Docker compartiendo el kernel de la máquina anfitriona, pero con su propio sistema de archivos, red y recursos.

**La analogía clásica:**
- Imagina que una aplicación es un plato de comida cocinado.
- Sin Docker: te llevas los ingredientes sueltos a otra cocina y rezas para que el plato salga igual (a veces la harina es otra, el horno calienta distinto...).
- Con Docker: te llevas el **plato ya cocinado y sellado**. Lo calientas y se come igual en cualquier sitio.

---

## 2. ¿Para qué se usa Docker?

Docker resuelve problemas muy concretos del desarrollo de software:

1. **"En mi máquina sí funciona"**
   Evita el clásico problema donde el código funciona en tu equipo pero falla en el de tu compañero o en producción porque las versiones de las librerías o del runtime son distintas.

2. **Aislamiento de entornos**
   Cada contenedor tiene sus propias dependencias. Puedes tener tres proyectos: uno con Python 3.9, otro con Python 3.12 y otro con Node 20, ejecutándose a la vez sin que se pisen.

3. **Reproducibilidad**
   Un `Dockerfile` es una receta. Quien la ejecute obtendrá exactamente el mismo resultado, sin importar el sistema operativo.

4. **Despliegue simple**
   En lugar de instalar manualmente Python, PostgreSQL, dependencias del sistema, etc., despliegas contenedores con un comando.

5. **Microservicios / arquitecturas multi-contenedor**
   Puedes definir varios contenedores (app, base de datos, cache, etc.) que se comunican entre sí y levantarlos todos a la vez.

6. **CI/CD**
   Los pipelines de integración continua usan contenedores para ejecutar tests en entornos limpios y reproducibles.

---

## 3. Conceptos clave (vocabulario que necesitas)

Antes de construir nada, necesitas conocer 4 palabras:

| Concepto | Qué es | Analogía |
|----------|--------|----------|
| **Imagen** | Una "plantilla" de solo lectura que contiene el sistema de archivos y la configuración. Se crea a partir de un `Dockerfile`. | Una receta de cocina escrita. |
| **Contenedor** | Una instancia en ejecución de una imagen. Es lo que corre la app. | El plato ya cocinado y servido. |
| **Dockerfile** | Un archivo de texto con instrucciones para construir una imagen. | Las instrucciones paso a paso de la receta. |
| **Docker Compose** | Una herramienta para definir y ejecutar **varios** contenedores que forman una aplicación. | El menú completo: plato + bebida + postre, servidos juntos. |

Otros términos útiles:
- **Volumen**: una carpeta persistente que Docker monta dentro del contenedor. Sirve para que los datos (como los de una base de datos) no se pierdan al apagar el contenedor.
- **Red (network)**: una red virtual donde los contenedores se comunican entre sí por nombre (no por IP).
- **Puerto mapeado**: expones un puerto del contenedor hacia la máquina anfitriona (por ejemplo `-p 8000:8000`).

---

## 4. Requisitos previos

Antes de empezar necesitas:

1. **Tener instalado Docker** (incluye Docker Engine y, opcionalmente, Docker Compose).
   - Linux: `curl -fsSL https://get.docker.com | sh`
   - Windows / macOS: instala **Docker Desktop**.
2. Verificar la instalación:
   ```bash
   docker --version
   docker compose version
   ```
3. Crear una carpeta para el proyecto:
   ```bash
   mkdir docker-fastapi-postgres
   cd docker-fastapi-postgres
   ```

> **Importante sobre los archivos de código**: en este documento se muestra el contenido de cada archivo. Puedes crearlos manualmente o dejar que te los genere, pero la estructura debe ser la que se indica en cada paso.

---

## 5. Estructura del proyecto

Cuando terminemos, la carpeta tendrá esta estructura:

```
docker-fastapi-postgres/
├── app/
│   ├── __init__.py          (vacío)
│   ├── main.py              (código de la API)
│   └── database.py          (conexión a PostgreSQL)
├── requirements.txt         (dependencias Python)
├── Dockerfile              (receta de la imagen de la API)
├── docker-compose.yml      (orquesta API + PostgreSQL)
└── DOCKER.md               (este documento)
```

Vamos a construirla pieza por pieza y a explicar cada parte.

---

## 6. Paso 1: La aplicación FastAPI (sin Docker todavía)

Primero escribimos una API **sencilla** en FastAPI, como si no usáramos Docker. Esto nos sirve para entender qué es lo que luego vamos a empaquetar.

### 6.1 Archivo: `requirements.txt`

Lista las dependencias Python que la app necesita.

```txt
fastapi
uvicorn[standard]
psycopg2-binary
```

- `fastapi`: el framework web.
- `uvicorn`: el servidor ASGI que ejecuta FastAPI.
- `psycopg2-binary`: el driver para conectarse a PostgreSQL.

### 6.2 Archivo: `app/__init__.py`

Archivo vacío. Solo sirve para que Python trate `app` como un paquete.

```python
```

### 6.3 Archivo: `app/database.py`

Aquí definimos **cómo** nos conectamos a PostgreSQL. Para mantenerlo simple, usamos la librería estándar `psycopg2` directamente (sin ORM, sin SQLAlchemy). Esto evita capas extra y hace evidente qué pasa.

```python
import os
import psycopg2
from psycopg2 import pool

# Obtenemos las variables de entorno que Docker Compose nos inyectará.
# Si no están definidas, usamos valores por defecto útiles para desarrollo local.
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "apppass")

# Creamos un pool de conexiones reutilizable.
_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=5,
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
)


def get_connection():
    """Devuelve una conexión del pool. Debe liberarse con putconn."""
    return _pool.getconn()


def put_connection(conn):
    """Devuelve la conexión al pool."""
    _pool.putconn(conn)


def init_db():
    """Crea la tabla de ejemplo si no existe."""
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS items (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    price NUMERIC(10, 2) NOT NULL
                );
                """
            )
        conn.commit()
    finally:
        put_connection(conn)
```

**Detalles importantes para entender la integración con Docker:**

- Los valores de conexión **no están escritos a fuego** en el código. Se leen de **variables de entorno** (`os.getenv`). Esto es clave: cuando la app corra dentro de un contenedor, le inyectaremos esos valores desde `docker-compose.yml`.
- El valor por defecto de `DB_HOST` es `localhost`, útil para correr la app sin Docker en tu máquina. Pero **dentro de Docker**, `DB_HOST` será el nombre del contenedor de PostgreSQL (por ejemplo `db`), porque en la red virtual de Docker los contenedores se encuentran por nombre.

### 6.4 Archivo: `app/main.py`

La API en sí: cuatro endpoints muy básicos sobre una tabla `items`.

```python
from fastapi import FastAPI, HTTPException
from app import database

app = FastAPI(title="Docker Demo API")


@app.on_event("startup")
def startup():
    """Crea la tabla al arrancar la app."""
    database.init_db()


@app.get("/")
def root():
    return {"status": "ok", "message": "API corriendo dentro de Docker"}


@app.get("/items")
def list_items():
    conn = database.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, price FROM items ORDER BY id;")
            rows = cur.fetchall()
        return {"items": [{"id": r[0], "name": r[1], "price": float(r[2])} for r in rows]}
    finally:
        database.put_connection(conn)


@app.post("/items")
def create_item(name: str, price: float):
    conn = database.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO items (name, price) VALUES (%s, %s) RETURNING id;",
                (name, price),
            )
            new_id = cur.fetchone()[0]
        conn.commit()
        return {"id": new_id, "name": name, "price": price}
    finally:
        database.put_connection(conn)


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    conn = database.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM items WHERE id = %s;", (item_id,))
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Item no encontrado")
        conn.commit()
        return {"deleted": item_id}
    finally:
        database.put_connection(conn)
```

**Lo importante aquí:**
- En `startup` llamamos a `init_db()`, de modo que la tabla se crea sola la primera vez.
- Los endpoints son intencionalmente simples (sin schemas Pydantic complejos) para que el foco esté en **Docker**, no en la lógica de la API.

> Si tuvieras Python y PostgreSQL instalados en tu máquina, ahora podrías correr esto localmente con:
> ```bash
> pip install -r requirements.txt
> uvicorn app.main:app --reload
> ```
> Pero **no lo haremos así**. La gracia es que todo corra dentro de Docker, sin instalar nada en la máquina anfitriona (salvo el propio Docker).

---

## 7. Paso 2: El Dockerfile (empaquetar la API)

El `Dockerfile` es la receta para construir la **imagen** de nuestra API. Vamos a verlo línea por línea.

### 7.1 Archivo: `Dockerfile`

```dockerfile
# Partimos de una imagen oficial de Python ligera.
# 'slim' contiene lo mínimo necesario para correr Python, sin herramientas innecesarias.
FROM python:3.12-slim

# Establecemos el directorio de trabajo dentro del contenedor.
# Todo lo que ocurra a partir de aquí será relativo a /app.
WORKDIR /app

# Copiamos SOLO el archivo de dependencias y lo instalamos ANTES de copiar el resto del código.
# ¿Por qué este orden? Porque Docker caches cada paso (capa).
# Si solo cambias app/main.py, esta capa no se reconstruye y la instalación
# de dependencias es instantánea (usa caché). Si copiaras todo junto,
# cualquier cambio en tu código invalidaría la caché y reinstalaría todo.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Ahora sí copiamos el código de la aplicación.
COPY app/ ./app/

# Exponemos el puerto por el que escucha uvicorn.
# Esto es solo documentación: no publica el puerto por sí solo.
# La publicación real se hace en docker-compose.yml con 'ports'.
EXPOSE 8000

# Comando por defecto para arrancar la API.
# --host 0.0.0.0 es obligatorio: si pones 127.0.0.1 el servidor solo escuchará
# DENTRO del contenedor y no podrías acceder desde tu navegador.
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Puntos clave que hay que entender bien:**

1. **`FROM`**: toda imagen parte de otra imagen. Aquí usamos `python:3.12-slim`, una imagen oficial que ya trae Python 3.12.
2. **`WORKDIR`**: crea el directorio (si no existe) y se "mueve" ahí. Equivale a `cd /app`.
3. **`COPY` y `RUN`**: copian archivos del anfitrión al contenedor (`COPY`) o ejecutan comandos durante la construcción (`RUN`).
4. **El orden de las capas importa para el caché**: copiar primero `requirements.txt` e instalar, luego copiar el código. Esto es una de las buenas prácticas más importantes de Docker.
5. **`EXPOSE`** es declarativo. No abre puertos automáticamente.
6. **`CMD`** es lo que se ejecuta cuando alguien hace `docker run` de esta imagen. Solo puede haber un `CMD`.

### 7.2 Construir la imagen manualmente (opcional, para entender)

Podrías construir y correr solo la API con:
```bash
docker build -t mi-api .
docker run -p 8000:8000 mi-api
```
Pero la API fallaría porque no encuentra PostgreSQL. Aquí es donde entra **Docker Compose**: necesitamos levantar **dos** contenedores (API + base de datos) que se vean entre sí.

---

## 8. Paso 3: Docker Compose (orquestar varios contenedores)

Docker Compose te permite describir **todos** los contenedores de tu aplicación en un único archivo YAML y levantarlos con un comando. Es ideal para entornos de desarrollo y para apps compuestas.

### 8.1 Archivo: `docker-compose.yml`

```yaml
# 'services' es la lista de contenedores que forman la aplicación.
services:
  # ---- Base de datos PostgreSQL ----
  db:
    # Usamos la imagen oficial de PostgreSQL 16 (versión estable).
    image: postgres:16

    # Reinicia automáticamente si el contenedor se cae.
    restart: unless-stopped

    # Variables de entorno que configuran la base de datos al crearse.
    # Estas las define la imagen oficial de postgres.
    environment:
      POSTGRES_DB: ${DB_NAME:-appdb}
      POSTGRES_USER: ${DB_USER:-appuser}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-apppass}

    # Mapeamos el puerto 5432 del contenedor al 5432 de la máquina anfitriona.
    # Así puedes conectarte con un cliente como DBeaver o pgAdmin si quieres.
    ports:
      - "5432:5432"

    # Un volumen con nombre: los datos de PostgreSQL se guardan aquí.
    # Si el contenedor se borra o se reinicia, los datos persisten.
    # Sin esto, cada vez que recrearas el contenedor la BD empezaría de cero.
    volumes:
      - pgdata:/var/lib/postgresql/data

    # Un chequeo de salud: Compose esperará a que 'pg_isready' responda OK
    # antes de considerar que la BD está lista. Lo usaremos con 'depends_on'
    # en el servicio 'api' para que la API no arranque antes de que la BD esté lista.
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-appuser} -d ${DB_NAME:-appdb}"]
      interval: 5s
      timeout: 5s
      retries: 5

  # ---- API FastAPI ----
  api:
    # Construye la imagen a partir del Dockerfile del directorio actual.
    build: .

    restart: unless-stopped

    # Mapeamos el puerto de la API.
    ports:
      - "8000:8000"

    # Variables de entorno que nuestra app/database.py lee con os.getenv.
    # Fíjate en DB_HOST: apunta a 'db', que es el nombre del servicio de base de datos.
    # Dentro de la red que Compose crea automáticamente, los contenedores se
    # resuelven por nombre de servicio. Por eso no usamos 'localhost'.
    environment:
      DB_HOST: db
      DB_PORT: 5432
      DB_NAME: ${DB_NAME:-appdb}
      DB_USER: ${DB_USER:-appuser}
      DB_PASSWORD: ${DB_PASSWORD:-apppass}

    # La API depende de la BD. Además, esperamos a que el healthcheck
    # marque la BD como 'healthy' antes de arrancar la API.
    depends_on:
      db:
        condition: service_healthy

# Volúmenes con nombre. Docker los gestiona automáticamente.
# 'pgdata' es donde PostgreSQL guardará los ficheros de la base de datos.
volumes:
  pgdata:
```

**Conceptos nuevos que aparecen aquí y que debes entender:**

1. **Servicios**: cada clave bajo `services` (`db`, `api`) define un contenedor. Compose les da como nombre de host en la red interna exactamente esa clave. Por eso `DB_HOST=db` funciona: la app resuelve `db` al contenedor de PostgreSQL.

2. **`build: .`**: le dice a Compose que construya la imagen usando el `Dockerfile` del directorio actual (el `.`). En vez de `build:` podríamos haber puesto `image: mi-api`, pero entonces tendrías que construirla a mano primero. Con `build:` Compose la construye solo si no existe o si cambió.

3. **Variables de entorno `${VAR:-default}`**:
   - Compose sustituye `${DB_NAME:-appdb}` por el valor de la variable de entorno `DB_NAME` del anfitrión, o por `appdb` si no está definida.
   - Así puedes sobreescribir valores sin tocar el archivo, ideal para producción. Ejemplo:
     ```bash
     DB_PASSWORD=supersecreto docker compose up
     ```

4. **`ports`**: formato `"puerto_anfitrion:puerto_contenedor"`. `"8000:8000"` expone el 8000 del contenedor en el 8000 de tu máquina. Si quisieras acceder a la API en otro puerto de tu equipo, usarías `"8080:8000"`.

5. **`volumes` (persistencia)**:
   - Los contenedores son **efímeros**: cuando se borran, su sistema de archivos desaparece.
   - PostgreSQL guarda sus datos en `/var/lib/postgresql/data`. Si no mapeamos esa ruta a un volumen, al destruir el contenedor perderíamos la base de datos.
   - `pgdata:/var/lib/postgresql/data` monta un volumen gestionado por Docker llamado `pgdata` en esa ruta. El volumen vive fuera del contenedor y sobrevive a sus recreaciones.

6. **`healthcheck`**: define cómo comprobar si un contenedor está sano. Para PostgreSQL usamos `pg_isready`, que devuelve OK cuando la BD acepta conexiones. Esto es importante porque si la API arrancase antes que la BD, fallaría al intentar conectarse.

7. **`depends_on` con `condition: service_healthy`**: la API no arranca hasta que la BD esté no solo levantada, sino **lista para aceptar conexiones** (gracias al healthcheck).

---

## 9. Paso 4: Levantar todo

Desde la carpeta del proyecto (donde está el `docker-compose.yml`):

```bash
# Construye las imágenes (si hace falta) y levanta los contenedores en segundo plano.
docker compose up -d --build
```

- `up`: crea y arranca los contenedores definidos en el archivo.
- `-d` (detached): los corre en segundo plano, liberando la terminal.
- `--build`: fuerza la reconstrucción de la imagen de la API (útil cuando cambias el código).

### 9.1 Ver los logs

```bash
# Logs de todos los servicios.
docker compose logs -f

# Logs solo de la API.
docker compose logs -f api
```

### 9.2 Comprobar que la BD está lista

```bash
docker compose ps
```
Deberías ver algo así:
```
NAME                STATUS
docker-db-1         Up (healthy)
docker-api-1        Up
```

### 9.3 Probar la API

Abre en el navegador o con `curl`:

```bash
# Estado de la API.
curl http://localhost:8000/

# Crear un item.
curl -X POST "http://localhost:8000/items?name=Teclado&price=25.50"

# Listar los items.
curl http://localhost:8000/items

# Borrar un item.
curl -X DELETE http://localhost:8000/items/1
```

También puedes abrir la **documentación interactiva** automática de FastAPI en:
```
http://localhost:8000/docs
```

---

## 10. Paso 5: Parar y limpiar

```bash
# Parar y eliminar contenedores (mantiene el volumen pgdata, los datos sobreviven).
docker compose down

# Parar y eliminar contenedores Y el volumen (los datos se pierden).
docker compose down -v
```

---

## 11. Cómo ejecutar la app en otra máquina

Aquí es donde se ve el valor real de Docker.

**En otra máquina que tenga Docker instalado**, solo necesitas copiar la carpeta del proyecto y ejecutar:

```bash
docker compose up -d --build
```

Eso es todo. No hay que instalar Python, ni PostgreSQL, ni configurar nada. Docker se encarga de:
1. Descargar la imagen oficial de PostgreSQL 16.
2. Construir la imagen de tu API desde el `Dockerfile` (que descargará `python:3.12-slim` e instalará las dependencias de `requirements.txt`).
3. Crear la red virtual para que los contenedores se comuniquen.
4. Levantar ambos contenedores con la configuración del `docker-compose.yml`.

> Puedes empaquetar la carpeta en un ZIP, subirla a un repo de Git, enviarla por email... y quien la reciba la ejecuta con el mismo comando obteniendo el mismo resultado. Esa es la magia de Docker.

---

## 12. Comandos de Docker que conviene memorizar

| Comando | Para qué sirve |
|---------|----------------|
| `docker compose up -d --build` | Levanta todo el proyecto en segundo plano. |
| `docker compose down` | Para y elimina los contenedores. |
| `docker compose down -v` | Igual que el anterior, pero borra los volúmenes. |
| `docker compose logs -f` | Sigue los logs en vivo. |
| `docker compose ps` | Lista los contenedores del proyecto y su estado. |
| `docker compose restart api` | Reinicia solo el servicio `api`. |
| `docker compose exec db psql -U appuser -d appdb` | Entra en la BD con el cliente `psql`. |
| `docker compose exec api bash` | Abre una shell dentro del contenedor de la API. |
| `docker image ls` | Lista las imágenes construidas/descargadas. |
| `docker volume ls` | Lista los volúmenes. |
| `docker system prune -f` | Limpia imágenes, contenedores y redes no usadas. |

---

## 13. Resumen de lo que has aprendido

- **Docker** empaqueta aplicaciones con todas sus dependencias en **contenedores** reproducibles.
- Un **Dockerfile** describe cómo construir una **imagen** (la receta).
- Un **contenedor** es una imagen en ejecución (el plato servido).
- **Docker Compose** coordina varios contenedores y define cómo se comunican.
- Las **variables de entorno** permiten configurar la app sin tocar el código.
- Los **volúmenes** persisten datos que deben sobrevivir al borrado del contenedor.
- Las **redes internas** permiten que los contenedores se encuentren por nombre de servicio.
- Con un solo comando (`docker compose up -d --build`) la app corre en **cualquier máquina** con Docker, de forma idéntica.

Con esta base ya puedes:
- Empaquetar cualquier aplicación Python en un contenedor.
- Añadir más servicios (Redis, Nginx, RabbitMQ...) al `docker-compose.yml`.
- Configurar entornos distintos (dev, test, prod) cambiando variables de entorno o usando archivos `.env`.

---

## 14. Archivos finales (resumen para copiar)

### `requirements.txt`
```txt
fastapi
uvicorn[standard]
psycopg2-binary
```

### `app/__init__.py`
```python
```

### `app/database.py`
```python
import os
import psycopg2
from psycopg2 import pool

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "appdb")
DB_USER = os.getenv("DB_USER", "appuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "apppass")

_pool = pool.SimpleConnectionPool(
    minconn=1,
    maxconn=5,
    host=DB_HOST,
    port=DB_PORT,
    dbname=DB_NAME,
    user=DB_USER,
    password=DB_PASSWORD,
)


def get_connection():
    return _pool.getconn()


def put_connection(conn):
    _pool.putconn(conn)


def init_db():
    conn = get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS items (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    price NUMERIC(10, 2) NOT NULL
                );
                """
            )
        conn.commit()
    finally:
        put_connection(conn)
```

### `app/main.py`
```python
from fastapi import FastAPI, HTTPException
from app import database

app = FastAPI(title="Docker Demo API")


@app.on_event("startup")
def startup():
    database.init_db()


@app.get("/")
def root():
    return {"status": "ok", "message": "API corriendo dentro de Docker"}


@app.get("/items")
def list_items():
    conn = database.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT id, name, price FROM items ORDER BY id;")
            rows = cur.fetchall()
        return {"items": [{"id": r[0], "name": r[1], "price": float(r[2])} for r in rows]}
    finally:
        database.put_connection(conn)


@app.post("/items")
def create_item(name: str, price: float):
    conn = database.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO items (name, price) VALUES (%s, %s) RETURNING id;",
                (name, price),
            )
            new_id = cur.fetchone()[0]
        conn.commit()
        return {"id": new_id, "name": name, "price": price}
    finally:
        database.put_connection(conn)


@app.delete("/items/{item_id}")
def delete_item(item_id: int):
    conn = database.get_connection()
    try:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM items WHERE id = %s;", (item_id,))
            if cur.rowcount == 0:
                raise HTTPException(status_code=404, detail="Item no encontrado")
        conn.commit()
        return {"deleted": item_id}
    finally:
        database.put_connection(conn)
```

### `Dockerfile`
```dockerfile
FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### `docker-compose.yml`
```yaml
services:
  db:
    image: postgres:16
    restart: unless-stopped
    environment:
      POSTGRES_DB: ${DB_NAME:-appdb}
      POSTGRES_USER: ${DB_USER:-appuser}
      POSTGRES_PASSWORD: ${DB_PASSWORD:-apppass}
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${DB_USER:-appuser} -d ${DB_NAME:-appdb}"]
      interval: 5s
      timeout: 5s
      retries: 5

  api:
    build: .
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      DB_HOST: db
      DB_PORT: 5432
      DB_NAME: ${DB_NAME:-appdb}
      DB_USER: ${DB_USER:-appuser}
      DB_PASSWORD: ${DB_PASSWORD:-apppass}
    depends_on:
      db:
        condition: service_healthy

volumes:
  pgdata:
```

---

### Ejecución final (en cualquier máquina con Docker)

```bash
docker compose up -d --build
```

La API estará disponible en `http://localhost:8000` y la documentación en `http://localhost:8000/docs`.