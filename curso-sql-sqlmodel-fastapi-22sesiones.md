# 🗄️ De Cero a tu Primera API: SQL, SQLModel y FastAPI
### Curso para jóvenes programadores · 20 sesiones · 2 horas cada una

---

> **¿Para quién es este curso?**
> Para jóvenes de 15 y 16 años con conocimientos básicos de Python que quieren aprender a manejar bases de datos y crear APIs reales. No necesitas saber SQL ni nada de servidores web. Empezamos desde cero y terminamos con un proyecto propio funcionando en internet.

---

## 📋 Mapa completo del curso

| # | Sesión | Bloque |
|---|--------|--------|
| 01 | ¿Qué es una base de datos y para qué sirve? | 🧱 Fundamentos |
| 02 | ¿Cómo diseño las tablas de mi base de datos? | 🧱 Fundamentos |
| 03 | Instalación del entorno y primera base de datos | 🧱 Fundamentos |
| 04 | SQL Básico: SELECT y WHERE | 🔍 SQL Básico |
| 05 | SQL Básico: ORDER BY, LIMIT, LIKE, IN, BETWEEN y AS | 🔍 SQL Básico |
| 06 | SQL Básico: INSERT y UPDATE | 🔍 SQL Básico |
| 07 | SQL Básico: DELETE, transacciones y agregaciones | 🔍 SQL Básico |
| 08 | SQL Relaciones: INNER JOIN con dos tablas | 🔗 Relaciones |
| 09 | SQL Relaciones: LEFT JOIN y unir tres tablas | 🔗 Relaciones |
| 10 | SQL Relaciones: GROUP BY y HAVING | 🔗 Relaciones |
| 11 | SQL Relaciones: Subconsultas y repaso general | 🔗 Relaciones |
| 12 | Python + SQLite: Conectando Python con una BD | 🐍 Python + BD |
| 13 | Introducción a SQLModel: Modelos como tablas | 🐍 Python + BD |
| 14 | SQLModel: CRUD completo con Sessions | 🐍 Python + BD |
| 15 | SQLModel: Relaciones y separación de modelos | 🐍 Python + BD |
| 16 | ¡Hola FastAPI! Tu primer servidor web | ⚡ FastAPI |
| 17 | FastAPI + SQLModel: La combinación ganadora | ⚡ FastAPI |
| 18 | Endpoints GET y POST | ⚡ FastAPI |
| 19 | Endpoints PUT y DELETE + Debugging | ⚡ FastAPI |
| 20 | Proyecto Final: Diseño e inicio | 🏆 Proyecto |
| 21 | Proyecto Final: Construcción y revisión entre pares | 🏆 Proyecto |
| 22 | Proyecto Final: Presentaciones y cierre | 🏆 Proyecto |

---

## 🛠️ Herramientas que usaremos

- **Python 3.11+**
- **SQLite** — Base de datos en un archivo (sin instalación de servidor)
- **DB Browser for SQLite** — Interfaz visual para explorar bases de datos
- **SQLModel** — Manejo de BD con Python de forma elegante
- **FastAPI** — Framework para crear APIs web
- **Uvicorn** — Servidor para correr tu API
- **VS Code** — Editor de código recomendado

### Instalación en un solo comando

```bash
pip install sqlmodel fastapi uvicorn
```

---
---

# 🧱 BLOQUE 1 — FUNDAMENTOS

---

## Sesión 01 — ¿Qué es una base de datos y para qué sirve?

**Duración:** 2 horas
**Objetivo:** Entender qué es una base de datos relacional, por qué la necesitamos y cómo organiza la información.

---

### Parte 1 — El problema que resuelven las bases de datos (30 min)

Imagina que eres el creador de una app de música. Tienes miles de canciones, artistas y usuarios con listas de reproducción. ¿Cómo guardas todo eso?

**Opción A: Variables de Python**
```python
canciones = [
    {"id": 1, "titulo": "Bohemian Rhapsody", "artista": "Queen", "año": 1975},
    {"id": 2, "titulo": "Blinding Lights", "artista": "The Weeknd", "año": 2019},
]
```
❌ Cuando el programa se cierra, todo se pierde.

**Opción B: Archivo de texto**
```
1,Bohemian Rhapsody,Queen,1975
2,Blinding Lights,The Weeknd,2019
```
❌ Buscar es lento, actualizar es difícil, un error puede corromper todo.

**Opción C: Base de datos** ✅
- Datos permanentes
- Búsqueda ultrarrápida
- Múltiples programas la usan simultáneamente
- Mecanismos de recuperación ante errores
- Control de quién puede leer o escribir qué

---

### Parte 2 — Tablas, filas y columnas (30 min)

Una base de datos relacional organiza los datos en **tablas**, como hojas de cálculo inteligentes.

**Tabla: `canciones`**

| id | titulo | artista | año | duracion_seg |
|----|--------|---------|-----|--------------|
| 1 | Bohemian Rhapsody | Queen | 1975 | 354 |
| 2 | Blinding Lights | The Weeknd | 2019 | 200 |
| 3 | Shape of You | Ed Sheeran | 2017 | 234 |

Vocabulario fundamental:

- **Tabla** → Agrupa datos del mismo tipo
- **Columna (campo)** → Un tipo de dato: `titulo`, `artista`, `año`
- **Fila (registro)** → Un dato concreto: la canción "Blinding Lights"
- **Celda** → La intersección de una fila y una columna

> 💡 **Clave Primaria (Primary Key):** El campo `id` identifica cada fila de forma única. No pueden existir dos canciones con el mismo `id`. Es la "huella digital" de cada registro.

---

### Parte 3 — Tipos de datos (20 min)

Cada columna guarda un tipo específico de dato:

| Tipo SQL | Qué guarda | Ejemplo |
|----------|-----------|---------|
| `INTEGER` | Números enteros | 42, -7, 0 |
| `REAL` | Números con decimales | 3.14, 9.99 |
| `TEXT` | Texto | "Hola mundo" |
| `BOOLEAN` | Verdadero o falso | True, False |

---

### Parte 4 — Actividad: Explorando DB Browser for SQLite (40 min)

1. Descarga e instala **DB Browser for SQLite** desde https://sqlitebrowser.org/
2. Crea una nueva base llamada `sesion01.db`
3. Crea manualmente la tabla `canciones` con la interfaz gráfica
4. Inserta 5 canciones favoritas tuyas
5. Explora la pestaña "Browse Data"

**Columnas a crear:**
- `id` — INTEGER, PRIMARY KEY, AUTOINCREMENT
- `titulo` — TEXT, NOT NULL
- `artista` — TEXT, NOT NULL
- `año` — INTEGER
- `duracion_seg` — INTEGER

---

### Resumen de la Sesión 01

✅ Una BD guarda información permanente y organizada.
✅ Las BDs relacionales usan tablas (filas + columnas).
✅ La clave primaria identifica cada fila de forma única.
✅ Cada columna tiene un tipo de dato específico.

### 📝 Tarea
Piensa en una app que te gustaría crear. Dibuja en papel qué tablas necesitaría y qué columnas tendría cada una. La semana que viene la analizamos en clase.

---
---

## Sesión 02 — ¿Cómo diseño las tablas de mi base de datos?

**Duración:** 2 horas
**Objetivo:** Aprender a modelar una base de datos desde cero: entidades, atributos, relaciones y reglas de buen diseño.

---

### Parte 1 — El proceso de diseño en 4 pasos (15 min)

```
1. ENTIDADES   → ¿De qué cosas guardo información?
2. ATRIBUTOS   → ¿Qué sé de cada cosa?
3. RELACIONES  → ¿Cómo se conectan las cosas entre sí?
4. REGLAS      → ¿El diseño está limpio y sin repeticiones?
```

---

### Parte 2 — Identificando entidades y atributos (25 min)

**Caso de uso: App de una librería online**

*"Los usuarios buscan libros, ven los autores y dejan reseñas."*

**Entidades:** `Usuario`, `Libro`, `Autor`, `Reseña`

```
Usuario:  id, nombre, email, contraseña_hash, fecha_registro
Libro:    id, titulo, isbn, precio, año_publicacion, stock
Autor:    id, nombre, nacionalidad, fecha_nacimiento
Reseña:   id, puntuacion (1-5), comentario, fecha
```

---

### Parte 3 — Tipos de relaciones (40 min)

#### 🔁 Uno a Muchos (1:N) — La más común

Un autor escribe muchos libros. Cada libro tiene un autor principal.

```
Autor (1) ──────< Libro (N)
```

Se implementa poniendo el `id` del autor **dentro** de la tabla libro:

**Tabla `autores`**

| id | nombre | nacionalidad |
|----|--------|--------------|
| 1 | Gabriel García Márquez | Colombiano |
| 2 | Ursula K. Le Guin | Estadounidense |

**Tabla `libros`**

| id | titulo | precio | autor_id |
|----|--------|--------|----------|
| 1 | Cien Años de Soledad | 35000 | 1 |
| 2 | El amor en los tiempos del cólera | 28000 | 1 |
| 3 | The Left Hand of Darkness | 40000 | 2 |

> 💡 `autor_id` en `libros` se llama **Clave Foránea (Foreign Key)**: apunta a un registro de otra tabla.

#### 🔁 Muchos a Muchos (N:M)

Un usuario compra muchos libros. Un libro es comprado por muchos usuarios. Se necesita una **tabla intermedia**:

**Tabla `compras`**

| id | usuario_id | libro_id | fecha | precio_pagado |
|----|-----------|---------|-------|---------------|
| 1 | 5 | 3 | 2024-03-15 | 40000 |
| 2 | 5 | 1 | 2024-03-15 | 35000 |

#### 🔁 Uno a Uno (1:1)
Un usuario tiene exactamente un perfil extendido. Menos común.

---

### Parte 4 — Las 3 Reglas de Oro (20 min)

**Regla 1: No repitas datos**

❌ Mal:
| id | titulo | nombre_autor | email_autor |
|----|--------|-------------|------------|
| 1 | Libro A | Ana Torres | ana@mail.com |
| 2 | Libro B | Ana Torres | ana@mail.com |

Si Ana cambia su email hay que actualizar todas las filas. Propenso a inconsistencias.

✅ Bien: tabla `autores` separada + `autor_id` en libros.

**Regla 2: Cada tabla tiene una sola responsabilidad**

No mezcles libros y reseñas en la misma tabla.

**Regla 3: Toda tabla tiene clave primaria**

Siempre un campo `id` único y nunca NULL.

---

### Parte 5 — Actividad grupal (20 min)

Diseñen la BD para una app de seguimiento de series:
- Usuarios marcan series como "viendo", "terminada" o "pendiente"
- Cada serie tiene episodios con duración y número
- Los usuarios puntúan series del 1 al 10

Definan entidades, atributos, relaciones y el tipo de cada una.

---

### Diagrama del ejemplo librería

```
┌─────────────┐        ┌──────────────┐
│   autores   │        │    libros    │
├─────────────┤        ├──────────────┤
│ id (PK)     │◄───────│ id (PK)      │
│ nombre      │        │ titulo       │
│ nacionalidad│        │ precio       │
│ fecha_nac   │        │ autor_id (FK)│
└─────────────┘        └──────┬───────┘
                              │
                    ┌─────────▼──────────┐
     ┌──────────┐   │      reseñas       │
     │ usuarios │   ├────────────────────┤
     ├──────────┤   │ id (PK)            │
     │ id (PK)  │◄──│ usuario_id (FK)    │
     │ nombre   │   │ libro_id (FK)      │
     │ email    │   │ puntuacion         │
     └──────────┘   │ comentario         │
                    └────────────────────┘
```

---

### Resumen de la Sesión 02

✅ El diseño sigue 4 pasos: entidades → atributos → relaciones → reglas.
✅ Las relaciones son 1:1, 1:N o N:M.
✅ 1:N se implementa con clave foránea.
✅ N:M necesita tabla intermedia.
✅ No repetir datos, una responsabilidad por tabla, siempre tener PK.

### 📝 Tarea
Toma la app de la sesión anterior y dibuja el diagrama completo con todas las relaciones.

---
---

## Sesión 03 — Instalación del entorno y primera base de datos

**Duración:** 2 horas
**Objetivo:** Tener el entorno listo y crear la base de datos de práctica que usaremos durante todo el curso.

---

### Parte 1 — Instalación y verificación (40 min)

#### Checklist de instalación

```bash
# 1. Verificar Python
python --version   # Debe ser 3.11 o superior

# 2. Instalar las librerías del curso
pip install sqlmodel fastapi uvicorn

# 3. Verificar instalación
python -c "import sqlmodel; import fastapi; print('¡Todo listo!')"
```

#### VS Code — extensiones recomendadas
- Python (Microsoft)
- SQLite Viewer
- Thunder Client (para probar APIs)

---

### Parte 2 — Creando la base de datos de práctica (80 min)

Esta base de datos la usaremos en todas las sesiones de SQL. Abre DB Browser for SQLite, crea `practica.db` y ejecuta en la pestaña "Execute SQL":

```sql
-- =====================================================
-- BASE DE DATOS DE PRÁCTICA: Plataforma Musical
-- =====================================================

CREATE TABLE generos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL
);

CREATE TABLE artistas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    pais TEXT,
    año_inicio INTEGER
);

CREATE TABLE canciones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    titulo TEXT NOT NULL,
    artista_id INTEGER NOT NULL,
    genero_id INTEGER,
    año INTEGER,
    duracion_seg INTEGER,
    reproducciones INTEGER DEFAULT 0,
    FOREIGN KEY (artista_id) REFERENCES artistas(id),
    FOREIGN KEY (genero_id) REFERENCES generos(id)
);

CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    fecha_registro TEXT DEFAULT (date('now'))
);

CREATE TABLE playlists (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT NOT NULL,
    usuario_id INTEGER NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);

CREATE TABLE playlist_canciones (
    playlist_id INTEGER,
    cancion_id INTEGER,
    orden INTEGER,
    PRIMARY KEY (playlist_id, cancion_id),
    FOREIGN KEY (playlist_id) REFERENCES playlists(id),
    FOREIGN KEY (cancion_id) REFERENCES canciones(id)
);

-- =====================================================
-- DATOS DE PRÁCTICA
-- =====================================================

INSERT INTO generos (nombre) VALUES
    ('Pop'), ('Rock'), ('Reggaeton'),
    ('Hip-Hop'), ('Electrónica'), ('R&B'), ('Latin Pop');

INSERT INTO artistas (nombre, pais, año_inicio) VALUES
    ('Bad Bunny',       'Puerto Rico',    2016),
    ('Taylor Swift',    'Estados Unidos', 2006),
    ('Queen',           'Reino Unido',    1970),
    ('Karol G',         'Colombia',       2010),
    ('Kendrick Lamar',  'Estados Unidos', 2003),
    ('Rosalía',         'España',         2017),
    ('J Balvin',        'Colombia',       2009),
    ('Dua Lipa',        'Reino Unido',    2015);

INSERT INTO canciones (titulo, artista_id, genero_id, año, duracion_seg, reproducciones) VALUES
    ('Tití Me Preguntó',     1, 3, 2022, 238, 1500000000),
    ('Anti-Hero',            2, 1, 2022, 200,  900000000),
    ('Bohemian Rhapsody',    3, 2, 1975, 354, 1800000000),
    ('CAIRO',                4, 3, 2023, 195,  400000000),
    ('HUMBLE.',              5, 4, 2017, 177,  800000000),
    ('Me Porto Bonito',      1, 3, 2022, 178, 1200000000),
    ('Shake It Off',         2, 1, 2014, 219,  600000000),
    ('We Will Rock You',     3, 2, 1977, 122,  500000000),
    ('PROVENZA',             4, 7, 2022, 196,  700000000),
    ('DNA.',                 5, 4, 2017, 185,  600000000),
    ('BIZCOCHITO',           6, 1, 2022, 139,  250000000),
    ('Con Altura',           6, 3, 2019, 184,  900000000),
    ('Mi Gente',             7, 3, 2017, 194, 1100000000),
    ('Levitating',           8, 1, 2020, 203,  700000000),
    ('Dont Start Now',       8, 1, 2019, 183,  800000000);

INSERT INTO usuarios (nombre, email) VALUES
    ('Ana García',    'ana@ejemplo.com'),
    ('Carlos López',  'carlos@ejemplo.com'),
    ('María Torres',  'maria@ejemplo.com'),
    ('Juan Pérez',    'juan@ejemplo.com');

INSERT INTO playlists (nombre, usuario_id) VALUES
    ('Mis favoritas',   1),
    ('Para estudiar',   1),
    ('Fiesta',          2),
    ('Relax',           3);

INSERT INTO playlist_canciones (playlist_id, cancion_id, orden) VALUES
    (1, 1, 1), (1, 3, 2), (1, 6, 3),
    (2, 5, 1), (2, 10, 2), (2, 14, 3),
    (3, 1, 1), (3, 6, 2), (3, 13, 3), (3, 12, 4),
    (4, 3, 1), (4, 14, 2), (4, 15, 3);
```

---

### Resumen de la Sesión 03

✅ Entorno instalado y verificado.
✅ Base de datos `practica.db` lista con 6 tablas y datos reales.
✅ Comprendemos la estructura de la BD que usaremos en las próximas sesiones.

---
---

# 🔍 BLOQUE 2 — SQL BÁSICO

---

## Sesión 04 — SQL Básico: SELECT y WHERE

**Duración:** 2 horas
**Objetivo:** Dominar las consultas de lectura básicas: SELECT, FROM y WHERE con todos sus operadores.

---

### Parte 1 — El comando SELECT (30 min)

`SELECT` es cómo le preguntamos a la BD que nos muestre datos.

```sql
-- Sintaxis básica
SELECT columnas FROM tabla;

-- Mostrar todo de la tabla canciones
SELECT * FROM canciones;

-- Solo algunas columnas
SELECT titulo, año FROM canciones;

-- De la tabla artistas
SELECT nombre, pais FROM artistas;
```

> 💡 El `*` significa "todas las columnas". En producción, evítalo y sé explícito.

---

### Parte 2 — Filtrando con WHERE (50 min)

```sql
SELECT columnas FROM tabla WHERE condicion;

-- Canciones del año 2022
SELECT titulo, año FROM canciones WHERE año = 2022;

-- Canciones con más de 1000 millones de reproducciones
SELECT titulo, reproducciones FROM canciones
WHERE reproducciones > 1000000000;

-- Artistas de Colombia
SELECT nombre FROM artistas WHERE pais = 'Colombia';
```

#### Operadores de comparación

| Operador | Significado |
|----------|------------|
| `=` | Igual |
| `!=` o `<>` | Diferente |
| `>` | Mayor que |
| `<` | Menor que |
| `>=` | Mayor o igual |
| `<=` | Menor o igual |

#### Operadores lógicos: AND, OR, NOT

```sql
-- Canciones de 2022 con más de 500M de reproducciones
SELECT titulo FROM canciones
WHERE año = 2022 AND reproducciones > 500000000;

-- Artistas de Colombia o Puerto Rico
SELECT nombre, pais FROM artistas
WHERE pais = 'Colombia' OR pais = 'Puerto Rico';

-- Canciones que NO son de 2022
SELECT titulo, año FROM canciones WHERE NOT año = 2022;

-- Combinando: artistas latinoamericanos con inicio antes de 2015
SELECT nombre, pais, año_inicio FROM artistas
WHERE (pais = 'Colombia' OR pais = 'Puerto Rico')
AND año_inicio < 2015;
```

> ⚠️ Cuando mezcles AND y OR, usa paréntesis para dejar claro el orden de evaluación.

---

### Parte 3 — Actividad práctica (40 min)

Usando `practica.db`, escribe consultas para:

1. Mostrar el título y duración de todas las canciones
2. Artistas que empezaron después del año 2010
3. Canciones lanzadas entre 2017 y 2022 (usando `>=` y `<=`)
4. Artistas que NO son de Estados Unidos
5. Canciones con menos de 200 segundos Y más de 500 millones de reproducciones
6. Usuarios cuyo email termina en "ejemplo.com" (pista: `email LIKE '%ejemplo.com'`)

---

### Resumen de la Sesión 04

✅ `SELECT columnas FROM tabla` es la base de toda consulta.
✅ `WHERE` filtra filas por condición.
✅ Los operadores `=`, `!=`, `>`, `<`, `>=`, `<=` comparan valores.
✅ `AND`, `OR`, `NOT` combinan condiciones.

---
---

## Sesión 05 — SQL Básico: ORDER BY, LIMIT, LIKE, IN, BETWEEN y AS

**Duración:** 2 horas
**Objetivo:** Ampliar el toolkit de consultas con herramientas de ordenamiento, límite y filtros especializados.

---

### Parte 1 — ORDER BY y LIMIT (30 min)

```sql
-- Ordenar de menor a mayor (ascendente, por defecto)
SELECT titulo, reproducciones FROM canciones
ORDER BY reproducciones ASC;

-- Ordenar de mayor a menor (descendente)
SELECT titulo, reproducciones FROM canciones
ORDER BY reproducciones DESC;

-- Ordenar por dos columnas
SELECT titulo, año, reproducciones FROM canciones
ORDER BY año DESC, titulo ASC;

-- Solo las 5 canciones más reproducidas
SELECT titulo, reproducciones FROM canciones
ORDER BY reproducciones DESC
LIMIT 5;

-- Artistas ordenados por nombre
SELECT nombre, pais FROM artistas ORDER BY nombre;
```

---

### Parte 2 — BETWEEN, IN y LIKE (40 min)

#### BETWEEN: rango de valores

```sql
-- Canciones entre 2015 y 2022
SELECT titulo, año FROM canciones
WHERE año BETWEEN 2015 AND 2022;

-- Canciones de 3 a 4 minutos (180 a 240 segundos)
SELECT titulo, duracion_seg FROM canciones
WHERE duracion_seg BETWEEN 180 AND 240;
```

#### IN: lista de valores posibles

```sql
-- Artistas de Colombia, Puerto Rico o España
SELECT nombre, pais FROM artistas
WHERE pais IN ('Colombia', 'Puerto Rico', 'España');

-- Canciones de los géneros 1 (Pop) o 2 (Rock)
SELECT titulo FROM canciones WHERE genero_id IN (1, 2);
```

#### LIKE: búsqueda de texto con patrones

```sql
-- Artistas cuyo nombre empieza con "K"
SELECT nombre FROM artistas WHERE nombre LIKE 'K%';

-- Canciones que contienen "Me" en el título
SELECT titulo FROM canciones WHERE titulo LIKE '%Me%';

-- Usuarios con email de Gmail
SELECT nombre, email FROM usuarios WHERE email LIKE '%@gmail%';

-- El _ representa exactamente un carácter
SELECT titulo FROM canciones WHERE titulo LIKE '_NA%';
-- Encuentra "DNA.", "CAIRO" no, pero "ANA" sí
```

> 💡 `%` = "cualquier cantidad de caracteres" · `_` = "exactamente un carácter"

---

### Parte 3 — Alias con AS y cálculos (30 min)

```sql
-- Renombrar columnas en el resultado
SELECT
    titulo AS "Nombre de la canción",
    duracion_seg / 60 AS "Duración (minutos)",
    reproducciones / 1000000 AS "Reproducciones (M)"
FROM canciones
ORDER BY reproducciones DESC;
```

```sql
-- Alias en tablas (lo usaremos mucho con JOINs)
SELECT c.titulo, c.año
FROM canciones AS c
WHERE c.año > 2020;
```

---

### Parte 4 — Actividad práctica (20 min)

1. Top 3 artistas por año de inicio (los más antiguos)
2. Canciones cuyo título contiene la palabra "Me"
3. Artistas que empezaron entre 2005 y 2015
4. Las 5 canciones más cortas ordenadas de menor a mayor duración, mostrando la duración en minutos
5. Artistas de países de habla inglesa (Estados Unidos, Reino Unido, Australia)

---

### Resumen de la Sesión 05

✅ `ORDER BY columna ASC/DESC` ordena resultados.
✅ `LIMIT n` devuelve solo los primeros n resultados.
✅ `BETWEEN a AND b` filtra por rango.
✅ `IN (lista)` filtra por lista de valores.
✅ `LIKE 'patrón'` busca por patrón de texto (`%` = comodín).
✅ `AS` renombra columnas y permite hacer cálculos en el SELECT.

---
---

## Sesión 06 — SQL Básico: INSERT y UPDATE

**Duración:** 2 horas
**Objetivo:** Aprender a agregar y modificar datos con INSERT y UPDATE, con énfasis en la seguridad y las buenas prácticas.

---

### Parte 1 — INSERT: Agregando datos (50 min)

```sql
INSERT INTO tabla (columna1, columna2, columna3)
VALUES (valor1, valor2, valor3);
```

#### Ejemplos:

```sql
-- Insertar un nuevo artista
INSERT INTO artistas (nombre, pais, año_inicio)
VALUES ('Shakira', 'Colombia', 1995);

-- Insertar una canción (artista_id=4 es Karol G, genero_id=7 es Latin Pop)
INSERT INTO canciones (titulo, artista_id, genero_id, año, duracion_seg, reproducciones)
VALUES ('Amargura', 4, 7, 2023, 210, 150000000);

-- Insertar varios a la vez
INSERT INTO generos (nombre) VALUES
    ('Salsa'),
    ('Vallenato'),
    ('Cumbia');

-- Insertar y ver el resultado inmediatamente
INSERT INTO usuarios (nombre, email) VALUES ('Pedro Ruiz', 'pedro@ejemplo.com');
SELECT * FROM usuarios ORDER BY id DESC LIMIT 1;
```

> ⚠️ No incluyas el `id` si es AUTOINCREMENT. La BD lo asigna sola.
> ⚠️ Si una columna tiene `NOT NULL` y no la incluyes en el INSERT → error.
> ⚠️ Si una columna tiene `UNIQUE` y ya existe ese valor → error de duplicado.

---

### Parte 2 — UPDATE: Modificando datos (50 min)

```sql
UPDATE tabla
SET columna1 = nuevo_valor1, columna2 = nuevo_valor2
WHERE condicion;
```

#### Ejemplos:

```sql
-- Corregir el país de Queen
UPDATE artistas
SET pais = 'Reino Unido'
WHERE id = 3;

-- Actualizar múltiples campos
UPDATE canciones
SET año = 1976, duracion_seg = 360
WHERE id = 3;

-- Operación matemática al actualizar
UPDATE canciones
SET reproducciones = reproducciones + 5000000
WHERE id = 1;

-- Actualizar todos los artistas de un país (¡cuidado, afecta varios registros!)
UPDATE artistas
SET pais = 'Colombia'
WHERE pais = 'colombia';  -- Corregir capitalización inconsistente
```

---

### 🚨 El error más peligroso: UPDATE sin WHERE

```sql
-- ¡ESTO ACTUALIZA TODAS LAS FILAS DE LA TABLA!
UPDATE canciones SET reproducciones = 0;
-- Acabas de poner en cero TODAS las reproducciones de TODAS las canciones
```

**Buena práctica — siempre verifica antes:**
```sql
-- Paso 1: Verifica qué filas vas a afectar
SELECT * FROM canciones WHERE artista_id = 1;

-- Paso 2: Si el resultado es el correcto, ejecuta el UPDATE
UPDATE canciones SET reproducciones = reproducciones + 1000000
WHERE artista_id = 1;
```

---

### Parte 3 — Actividad práctica (20 min)

1. Inserta 2 nuevos artistas que te gusten
2. Inserta 3 canciones de esos artistas
3. Actualiza el año de inicio de uno de tus artistas nuevos
4. Incrementa en 10 millones las reproducciones de todas las canciones del año 2022
5. Verifica el resultado con un SELECT antes y después del UPDATE

---

### Resumen de la Sesión 06

✅ `INSERT INTO tabla (cols) VALUES (vals)` agrega nuevas filas.
✅ No incluyas el `id` en columnas AUTOINCREMENT.
✅ `UPDATE tabla SET col = val WHERE condicion` modifica filas.
✅ **SIEMPRE usa WHERE en UPDATE** o afectarás todas las filas.
✅ Verifica con SELECT antes de ejecutar un UPDATE importante.

---
---

## Sesión 07 — SQL Básico: DELETE, transacciones y agregaciones

**Duración:** 2 horas
**Objetivo:** Completar el CRUD básico de SQL con DELETE seguro, aprender transacciones y las funciones de agregación.

---

### Parte 1 — DELETE: Borrando datos con responsabilidad (30 min)

```sql
DELETE FROM tabla WHERE condicion;
```

```sql
-- Borrar un usuario específico
DELETE FROM usuarios WHERE id = 4;

-- Borrar canciones de un año específico
DELETE FROM canciones WHERE año < 1980;
```

### 🚨 El error más peligroso: DELETE sin WHERE

```sql
-- ¡ESTO BORRA ABSOLUTAMENTE TODAS LAS FILAS!
DELETE FROM canciones;
-- La tabla sigue existiendo pero está completamente vacía
```

**Protocolo de seguridad obligatorio:**
```sql
-- 1. Primero verifica QUÉ vas a borrar
SELECT * FROM canciones WHERE año < 1980;

-- 2. Si el resultado es correcto, entonces borra
DELETE FROM canciones WHERE año < 1980;
```

---

### Parte 2 — Transacciones: El seguro de vida de tu BD (30 min)

Una **transacción** agrupa operaciones. Si algo falla, puedes cancelar todo y volver al estado anterior.

```sql
BEGIN TRANSACTION;

-- Operaciones que van juntas o no van
UPDATE canciones SET reproducciones = reproducciones + 1000 WHERE id = 1;
DELETE FROM canciones WHERE año < 1970;
INSERT INTO canciones (titulo, artista_id, año) VALUES ('Nueva canción', 1, 2024);

-- Si todo está bien:
COMMIT;

-- Si algo salió mal, cancela todo:
-- ROLLBACK;
```

> 💡 Piensa en una transacción como un "borrador": puedes hacer cambios y decidir si guardarlos (COMMIT) o descartarlos (ROLLBACK).

**Caso real:** En una tienda online, cuando alguien compra:
1. Se descuenta del inventario
2. Se carga a la tarjeta
3. Se registra el pedido

Si el paso 2 falla, el paso 1 debe revertirse. Sin transacciones, tendrías un producto descontado sin cobro.

---

### Parte 3 — Funciones de Agregación (40 min)

Las funciones de agregación calculan un valor a partir de un grupo de filas:

```sql
-- Cuántas canciones hay
SELECT COUNT(*) AS total_canciones FROM canciones;

-- Cuántas canciones tienen más de 500M de reproducciones
SELECT COUNT(*) AS canciones_populares FROM canciones
WHERE reproducciones > 500000000;

-- Total de reproducciones de todas las canciones
SELECT SUM(reproducciones) AS total_reproducciones FROM canciones;

-- Promedio de reproducciones
SELECT AVG(reproducciones) AS promedio FROM canciones;

-- Duración máxima y mínima
SELECT
    MAX(duracion_seg) AS mas_larga,
    MIN(duracion_seg) AS mas_corta,
    MAX(duracion_seg) - MIN(duracion_seg) AS diferencia
FROM canciones;

-- Duración promedio en minutos
SELECT ROUND(AVG(duracion_seg) / 60.0, 2) AS promedio_minutos
FROM canciones;
```

---

### Parte 4 — Actividad práctica (20 min)

1. ¿Cuántos artistas hay de cada continente? (agrupa manualmente)
2. ¿Cuál es la suma total de reproducciones de todas las canciones?
3. Borra las playlists del usuario con id=4 (verifica primero con SELECT)
4. Usa una transacción para: insertar una canción y luego borrarla, haciendo ROLLBACK al final
5. ¿Cuántos segundos de música hay en total en la base de datos? ¿Cuántas horas es eso?

---

### Resumen de la Sesión 07

✅ `DELETE FROM tabla WHERE condicion` borra filas.
✅ **SIEMPRE usa WHERE** en DELETE. Verifica con SELECT primero.
✅ Las transacciones (BEGIN / COMMIT / ROLLBACK) protegen operaciones críticas.
✅ `COUNT`, `SUM`, `AVG`, `MAX`, `MIN` son las funciones de agregación básicas.
✅ Con estas 4 sesiones, dominas el CRUD básico de SQL.

---
---

# 🔗 BLOQUE 3 — RELACIONES SQL

---

## Sesión 08 — SQL Relaciones: INNER JOIN con dos tablas

**Duración:** 2 horas
**Objetivo:** Entender el concepto de JOIN y dominar INNER JOIN uniendo exactamente dos tablas.

---

### Parte 1 — El problema: los datos están separados (20 min)

Cuando consultamos canciones, vemos `artista_id` pero no el nombre:

```sql
SELECT titulo, artista_id FROM canciones;
```

| titulo | artista_id |
|--------|-----------|
| Tití Me Preguntó | 1 |
| Anti-Hero | 2 |
| Bohemian Rhapsody | 3 |

Queremos el **nombre** del artista, no su id. Para eso existe **JOIN**.

**Visualizando JOIN:**
```
Tabla canciones          Tabla artistas
-----------------        ---------------
titulo  | artista_id     id | nombre
--------|-----------     ---|---------
TTP     |     1     ───► 1  | Bad Bunny
Anti-H  |     2     ───► 2  | T. Swift
Bohemian|     3     ───► 3  | Queen
```

---

### Parte 2 — INNER JOIN: La unión básica (60 min)

```sql
SELECT tabla1.columna, tabla2.columna
FROM tabla1
INNER JOIN tabla2 ON tabla1.clave_foranea = tabla2.clave_primaria;
```

`INNER JOIN` devuelve solo las filas que tienen **coincidencia en ambas tablas**.

#### Ejemplos progresivos:

```sql
-- 1. El más simple: título y nombre del artista
SELECT canciones.titulo, artistas.nombre
FROM canciones
INNER JOIN artistas ON canciones.artista_id = artistas.id;

-- 2. Con alias para escribir menos
SELECT c.titulo, a.nombre
FROM canciones AS c
INNER JOIN artistas AS a ON c.artista_id = a.id;

-- 3. Más columnas y ordenado
SELECT
    c.titulo,
    a.nombre AS artista,
    a.pais,
    c.año,
    c.reproducciones
FROM canciones AS c
INNER JOIN artistas AS a ON c.artista_id = a.id
ORDER BY c.reproducciones DESC;

-- 4. JOIN + WHERE: canciones de artistas colombianos
SELECT c.titulo, a.nombre AS artista, c.año
FROM canciones AS c
INNER JOIN artistas AS a ON c.artista_id = a.id
WHERE a.pais = 'Colombia'
ORDER BY c.año;

-- 5. JOIN con artistas y géneros (dos JOINs, los veremos mejor la próxima sesión)
SELECT c.titulo, a.nombre AS artista, g.nombre AS genero
FROM canciones AS c
INNER JOIN artistas AS a ON c.artista_id = a.id
INNER JOIN generos AS g ON c.genero_id = g.id
WHERE c.año = 2022;
```

---

### Parte 3 — Entendiendo qué hace INNER JOIN (20 min)

`INNER JOIN` es como una intersección: solo muestra lo que está en **ambos lados**:

```sql
-- Si un artista no tiene canciones, NO aparece en el resultado
-- Si una canción tiene un artista_id que no existe en artistas, tampoco aparece

-- ¿Cuántas filas devuelve esto?
SELECT COUNT(*) FROM canciones INNER JOIN artistas ON canciones.artista_id = artistas.id;
-- La misma cantidad que tiene canciones, porque todas tienen un artista_id válido
```

---

### Parte 4 — Actividad práctica (20 min)

1. Muestra el título, artista y duración en minutos de cada canción
2. Muestra el título, artista y nombre del género de cada canción
3. ¿Qué canciones tienen más de 1000 millones de reproducciones? Muestra el título y el nombre del artista
4. Muestra solo las canciones del género "Reggaeton" con su artista
5. Lista todas las playlists con el nombre del usuario que las creó

---

### Resumen de la Sesión 08

✅ `INNER JOIN` combina filas de dos tablas usando la relación PK ↔ FK.
✅ Solo devuelve filas con coincidencia en **ambas** tablas.
✅ Los alias (`c`, `a`) simplifican las consultas.
✅ Se puede combinar JOIN con WHERE para filtrar el resultado.

---
---

## Sesión 09 — SQL Relaciones: LEFT JOIN y unir tres tablas

**Duración:** 2 horas
**Objetivo:** Aprender LEFT JOIN y dominar la unión de tres o más tablas en una sola consulta.

---

### Parte 1 — INNER JOIN vs LEFT JOIN (40 min)

#### El problema de INNER JOIN

```sql
-- ¿Cuántos géneros hay?
SELECT COUNT(*) FROM generos;  -- 10 géneros

-- ¿Cuántos géneros aparecen en canciones con INNER JOIN?
SELECT g.nombre, COUNT(c.id) AS canciones
FROM generos AS g
INNER JOIN canciones AS c ON c.genero_id = g.id
GROUP BY g.id, g.nombre;
-- Solo muestra los géneros que TIENEN canciones
-- Los géneros 'Salsa', 'Vallenato', 'Cumbia' que insertamos no aparecen
```

#### La solución: LEFT JOIN

`LEFT JOIN` devuelve **TODAS** las filas de la tabla izquierda, tengan o no coincidencia en la derecha. Cuando no hay coincidencia, los campos de la derecha son `NULL`.

```sql
-- Todos los géneros, aunque no tengan canciones
SELECT g.nombre AS genero, COUNT(c.id) AS canciones
FROM generos AS g
LEFT JOIN canciones AS c ON c.genero_id = g.id
GROUP BY g.id, g.nombre
ORDER BY canciones DESC;
```

| genero | canciones |
|--------|-----------|
| Reggaeton | 5 |
| Pop | 4 |
| Hip-Hop | 2 |
| ... | ... |
| Salsa | 0 |
| Vallenato | 0 |

```sql
-- Usar LEFT JOIN para encontrar géneros SIN canciones
SELECT g.nombre AS genero_sin_canciones
FROM generos AS g
LEFT JOIN canciones AS c ON c.genero_id = g.id
WHERE c.id IS NULL;  -- IS NULL detecta los que no tienen coincidencia
```

> 💡 **Cuándo usar cada uno:**
> - `INNER JOIN`: Solo me importan los que tienen relación en ambos lados.
> - `LEFT JOIN`: Quiero todos los de la tabla izquierda, aunque no tengan relación.

---

### Parte 2 — Unir tres o más tablas (60 min)

```sql
-- Título, artista y género de cada canción (3 tablas)
SELECT
    c.titulo,
    a.nombre AS artista,
    a.pais,
    g.nombre AS genero,
    c.año
FROM canciones AS c
INNER JOIN artistas AS a ON c.artista_id = a.id
INNER JOIN generos AS g ON c.genero_id = g.id
ORDER BY a.nombre, c.año;
```

```sql
-- Playlists con su usuario y sus canciones (4 tablas)
SELECT
    u.nombre AS usuario,
    p.nombre AS playlist,
    c.titulo AS cancion,
    pc.orden
FROM usuarios AS u
INNER JOIN playlists AS p ON p.usuario_id = u.id
INNER JOIN playlist_canciones AS pc ON pc.playlist_id = p.id
INNER JOIN canciones AS c ON c.id = pc.cancion_id
ORDER BY u.nombre, p.nombre, pc.orden;
```

```sql
-- Consulta completa: usuario, playlist, canción y artista
SELECT
    u.nombre AS usuario,
    p.nombre AS playlist,
    c.titulo AS cancion,
    a.nombre AS artista
FROM usuarios AS u
INNER JOIN playlists AS p ON p.usuario_id = u.id
INNER JOIN playlist_canciones AS pc ON pc.playlist_id = p.id
INNER JOIN canciones AS c ON c.id = pc.cancion_id
INNER JOIN artistas AS a ON c.artista_id = a.id
ORDER BY u.nombre, p.nombre, pc.orden;
```

---

### Parte 3 — Actividad práctica (20 min)

1. Muestra todos los artistas y, si tienen canciones, cuántas tienen (usa LEFT JOIN)
2. ¿Hay algún usuario sin playlists? Encuéntralo con LEFT JOIN + IS NULL
3. Lista todas las canciones de la playlist llamada "Fiesta" con su artista
4. Muestra el nombre completo de cada canción en cada playlist (usuario → playlist → canción → artista)
5. ¿Cuántas canciones diferentes hay en todas las playlists juntas?

---

### Resumen de la Sesión 09

✅ `LEFT JOIN` incluye todas las filas de la tabla izquierda.
✅ Las filas sin coincidencia tienen `NULL` en los campos de la tabla derecha.
✅ `WHERE campo IS NULL` encuentra los registros sin relación.
✅ Encadenando JOINs podemos unir 3, 4 o más tablas.

---
---

## Sesión 10 — SQL Relaciones: GROUP BY y HAVING

**Duración:** 2 horas
**Objetivo:** Dominar el agrupamiento de datos para obtener estadísticas y resúmenes por categorías.

---

### Parte 1 — GROUP BY: Agrupando para resumir (50 min)

`GROUP BY` agrupa filas con el mismo valor en una columna y aplica funciones de agregación por grupo.

```sql
-- ¿Cuántas canciones tiene cada artista?
SELECT a.nombre, COUNT(c.id) AS total_canciones
FROM artistas AS a
LEFT JOIN canciones AS c ON c.artista_id = a.id
GROUP BY a.id, a.nombre
ORDER BY total_canciones DESC;
```

```sql
-- Reproducciones totales por artista
SELECT a.nombre, SUM(c.reproducciones) AS total_rep
FROM canciones AS c
INNER JOIN artistas AS a ON c.artista_id = a.id
GROUP BY a.id, a.nombre
ORDER BY total_rep DESC;
```

```sql
-- Estadísticas por año
SELECT
    año,
    COUNT(*) AS canciones,
    ROUND(AVG(duracion_seg) / 60.0, 2) AS duracion_prom_min,
    MAX(reproducciones) / 1000000 AS max_rep_millones
FROM canciones
GROUP BY año
ORDER BY año DESC;
```

```sql
-- Canciones por género (con nombre del género)
SELECT
    g.nombre AS genero,
    COUNT(c.id) AS total_canciones,
    SUM(c.reproducciones) / 1000000 AS reproducciones_millones
FROM generos AS g
LEFT JOIN canciones AS c ON c.genero_id = g.id
GROUP BY g.id, g.nombre
ORDER BY total_canciones DESC;
```

---

### Parte 2 — HAVING: Filtrando grupos (40 min)

`WHERE` filtra filas individuales **antes** de agrupar.
`HAVING` filtra grupos **después** de agrupar.

```sql
-- Artistas con más de 2 canciones en la BD
SELECT a.nombre, COUNT(c.id) AS total
FROM artistas AS a
LEFT JOIN canciones AS c ON c.artista_id = a.id
GROUP BY a.id, a.nombre
HAVING total > 2;
```

```sql
-- Géneros con más de 1000 millones de reproducciones totales
SELECT g.nombre, SUM(c.reproducciones) AS total
FROM generos AS g
INNER JOIN canciones AS c ON c.genero_id = g.id
GROUP BY g.id, g.nombre
HAVING total > 1000000000
ORDER BY total DESC;
```

```sql
-- Diferencia clave: WHERE vs HAVING
-- WHERE filtra antes de agrupar (solo cuenta canciones populares)
SELECT a.nombre, COUNT(*) AS canciones_populares
FROM canciones AS c
INNER JOIN artistas AS a ON c.artista_id = a.id
WHERE c.reproducciones > 500000000
GROUP BY a.id, a.nombre;

-- HAVING filtra el grupo resultante (solo muestra artistas con 2+ canciones populares)
SELECT a.nombre, COUNT(*) AS canciones_populares
FROM canciones AS c
INNER JOIN artistas AS a ON c.artista_id = a.id
WHERE c.reproducciones > 500000000
GROUP BY a.id, a.nombre
HAVING COUNT(*) >= 2;
```

---

### Parte 3 — Actividad práctica (30 min)

1. ¿Cuál es el promedio de duración por género en minutos?
2. Artistas con reproducciones totales superiores a 2000 millones
3. ¿Qué años tienen al menos 3 canciones en la base de datos?
4. Géneros con promedio de duración mayor a 3 minutos
5. Usuario con más playlists creadas

---

### Resumen de la Sesión 10

✅ `GROUP BY columna` agrupa filas iguales para aplicar funciones de agregación.
✅ `HAVING condicion` filtra los grupos resultantes.
✅ `WHERE` filtra antes de agrupar; `HAVING` filtra después.
✅ Siempre incluye la columna agrupadora en el `GROUP BY`.

---
---

## Sesión 11 — SQL Relaciones: Subconsultas y repaso general

**Duración:** 2 horas
**Objetivo:** Aprender subconsultas y consolidar todo el SQL aprendido antes de pasar a Python.

---

### Parte 1 — Subconsultas (40 min)

Una **subconsulta** es un SELECT dentro de otro SELECT. La consulta interna se ejecuta primero.

```sql
-- Canciones con reproducciones por encima del promedio
SELECT titulo, reproducciones
FROM canciones
WHERE reproducciones > (SELECT AVG(reproducciones) FROM canciones)
ORDER BY reproducciones DESC;
```

```sql
-- Artistas que tienen canciones de 2022
SELECT nombre FROM artistas
WHERE id IN (
    SELECT DISTINCT artista_id FROM canciones WHERE año = 2022
);
```

```sql
-- La canción más reproducida de cada artista
SELECT c.titulo, a.nombre AS artista, c.reproducciones
FROM canciones AS c
INNER JOIN artistas AS a ON c.artista_id = a.id
WHERE c.reproducciones = (
    SELECT MAX(c2.reproducciones)
    FROM canciones AS c2
    WHERE c2.artista_id = c.artista_id
);
```

```sql
-- Géneros que no tienen ninguna canción (alternativa a LEFT JOIN + IS NULL)
SELECT nombre FROM generos
WHERE id NOT IN (
    SELECT DISTINCT genero_id FROM canciones WHERE genero_id IS NOT NULL
);
```

---

### Parte 2 — El orden completo de SQL (20 min)

Cuando escribes una consulta compleja, el orden importa:

```sql
SELECT   ...     -- 1. Qué columnas mostrar
FROM     ...     -- 2. De qué tabla principal
JOIN     ...     -- 3. Unir con otras tablas
WHERE    ...     -- 4. Filtrar filas individuales (antes de agrupar)
GROUP BY ...     -- 5. Agrupar filas
HAVING   ...     -- 6. Filtrar grupos (después de agrupar)
ORDER BY ...     -- 7. Ordenar el resultado final
LIMIT    ...;    -- 8. Limitar cantidad de resultados
```

#### Ejemplo con todas las cláusulas:

```sql
SELECT
    g.nombre AS genero,
    COUNT(c.id) AS total_canciones,
    SUM(c.reproducciones) / 1000000 AS reproducciones_M
FROM generos AS g
INNER JOIN canciones AS c ON c.genero_id = g.id
INNER JOIN artistas AS a ON c.artista_id = a.id
WHERE a.pais IN ('Colombia', 'Puerto Rico', 'España')
GROUP BY g.id, g.nombre
HAVING COUNT(c.id) >= 2
ORDER BY reproducciones_M DESC
LIMIT 5;
```

---

### Parte 3 — Repaso general: El desafío final de SQL (60 min)

Resuelve estos desafíos usando todo lo aprendido:

**Nivel 1 — Básico**
1. Lista las canciones lanzadas en 2022 ordenadas por reproducciones
2. ¿Cuántos artistas hay por país?
3. Artistas cuyo nombre tiene exactamente 7 caracteres (pista: `LENGTH(nombre) = 7`)

**Nivel 2 — Intermedio**
4. Las 3 playlists con más canciones y el nombre del usuario que las creó
5. Artistas que tienen canciones en más de un género diferente
6. El género con el promedio de reproducciones más alto

**Nivel 3 — Avanzado**
7. Usuarios que tienen canciones de artistas colombianos en alguna de sus playlists
8. Para cada artista, muestra su canción más larga y más corta
9. ¿Qué canciones aparecen en más de una playlist?

---

### Resumen de la Sesión 11 y del Bloque SQL

✅ Las subconsultas permiten usar un SELECT como condición o fuente de datos.
✅ El orden correcto: SELECT → FROM → JOIN → WHERE → GROUP BY → HAVING → ORDER BY → LIMIT.
✅ **Dominas el CRUD completo de SQL**: SELECT, INSERT, UPDATE, DELETE.
✅ **Dominas las relaciones**: INNER JOIN, LEFT JOIN, unión de múltiples tablas.
✅ **Dominas las agregaciones**: COUNT, SUM, AVG, MAX, MIN con GROUP BY y HAVING.

---
---

# 🐍 BLOQUE 4 — PYTHON + BASE DE DATOS

---

## Sesión 12 — Python + SQLite: Conectando Python con una BD

**Duración:** 2 horas
**Objetivo:** Aprender a usar Python para interactuar con SQLite, entendiendo qué hace la BD "por debajo" antes de usar SQLModel.

---

### Parte 1 — El módulo sqlite3 (30 min)

Python incluye `sqlite3` sin necesidad de instalación:

```python
import sqlite3

# 1. Conectar (crea la BD si no existe)
conexion = sqlite3.connect("mi_app.db")

# 2. Crear cursor (el "lápiz" con el que escribimos SQL)
cursor = conexion.cursor()

# 3. Ejecutar SQL
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tareas (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT NOT NULL,
        completada INTEGER DEFAULT 0,
        fecha TEXT DEFAULT (date('now'))
    )
""")

# 4. Confirmar cambios
conexion.commit()

# 5. Cerrar la conexión
conexion.close()
print("¡BD creada!")
```

---

### Parte 2 — CRUD en Python (70 min)

#### ⚠️ Regla de oro: Nunca uses f-strings con SQL

```python
# ❌ PELIGROSO - SQL Injection
nombre = input("Nombre: ")
cursor.execute(f"SELECT * FROM usuarios WHERE nombre = '{nombre}'")
# Si el usuario escribe: ' OR '1'='1  →  ¡accede a toda la tabla!

# ✅ SEGURO - Parámetros
cursor.execute("SELECT * FROM usuarios WHERE nombre = ?", (nombre,))
```

#### CREATE — Insertar

```python
def agregar_tarea(titulo: str) -> int:
    with sqlite3.connect("mi_app.db") as con:
        cursor = con.cursor()
        cursor.execute(
            "INSERT INTO tareas (titulo) VALUES (?)",
            (titulo,)
        )
        con.commit()
        return cursor.lastrowid  # El id asignado automáticamente

id_nueva = agregar_tarea("Estudiar SQL")
print(f"Tarea creada con id: {id_nueva}")
```

#### READ — Leer

```python
def obtener_tareas_pendientes():
    with sqlite3.connect("mi_app.db") as con:
        con.row_factory = sqlite3.Row  # Acceder por nombre de columna
        cursor = con.cursor()
        cursor.execute("SELECT * FROM tareas WHERE completada = 0")
        return cursor.fetchall()

def obtener_tarea(tarea_id: int):
    with sqlite3.connect("mi_app.db") as con:
        con.row_factory = sqlite3.Row
        cursor = con.cursor()
        cursor.execute("SELECT * FROM tareas WHERE id = ?", (tarea_id,))
        return cursor.fetchone()  # Una fila o None

# Usar
tareas = obtener_tareas_pendientes()
for t in tareas:
    print(f"[{t['id']}] {t['titulo']} - {t['fecha']}")
```

#### UPDATE y DELETE

```python
def completar_tarea(tarea_id: int) -> bool:
    with sqlite3.connect("mi_app.db") as con:
        cursor = con.cursor()
        cursor.execute(
            "UPDATE tareas SET completada = 1 WHERE id = ?",
            (tarea_id,)
        )
        con.commit()
        return cursor.rowcount > 0  # True si se actualizó algo

def eliminar_tarea(tarea_id: int) -> bool:
    with sqlite3.connect("mi_app.db") as con:
        cursor = con.cursor()
        cursor.execute("DELETE FROM tareas WHERE id = ?", (tarea_id,))
        con.commit()
        return cursor.rowcount > 0
```

---

### Parte 3 — Mini app de lista de tareas (20 min)

```python
# app_tareas.py
import sqlite3

def setup_db():
    with sqlite3.connect("tareas.db") as con:
        con.execute("""CREATE TABLE IF NOT EXISTS tareas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            titulo TEXT NOT NULL,
            completada INTEGER DEFAULT 0
        )""")

def menu():
    setup_db()
    while True:
        print("\n=== Lista de Tareas ===")
        print("1. Ver tareas pendientes")
        print("2. Agregar tarea")
        print("3. Completar tarea")
        print("4. Salir")
        opcion = input("Opción: ")

        if opcion == "1":
            with sqlite3.connect("tareas.db") as con:
                con.row_factory = sqlite3.Row
                tareas = con.execute("SELECT * FROM tareas WHERE completada=0").fetchall()
                if not tareas:
                    print("¡No hay tareas pendientes!")
                for t in tareas:
                    print(f"  [{t['id']}] {t['titulo']}")

        elif opcion == "2":
            titulo = input("Título de la tarea: ")
            with sqlite3.connect("tareas.db") as con:
                cur = con.execute("INSERT INTO tareas (titulo) VALUES (?)", (titulo,))
                print(f"Tarea #{cur.lastrowid} creada.")

        elif opcion == "3":
            tid = int(input("ID de la tarea: "))
            with sqlite3.connect("tareas.db") as con:
                con.execute("UPDATE tareas SET completada=1 WHERE id=?", (tid,))
                print("¡Tarea completada!")

        elif opcion == "4":
            break

if __name__ == "__main__":
    menu()
```

---

### Resumen de la Sesión 12

✅ `sqlite3` es el módulo nativo de Python para SQLite.
✅ Usa `?` como placeholder, nunca f-strings (SQL Injection).
✅ `with sqlite3.connect(...)` maneja la conexión automáticamente.
✅ `row_factory = sqlite3.Row` permite acceder a columnas por nombre.
✅ `fetchall()` → lista; `fetchone()` → una fila o None.

---
---

## Sesión 13 — Introducción a SQLModel: Modelos como tablas

**Duración:** 2 horas
**Objetivo:** Entender qué es SQLModel, por qué es mejor que sqlite3 puro y cómo define tablas como clases de Python.

---

### Parte 1 — ¿Por qué SQLModel? (20 min)

Con `sqlite3` teníamos varios problemas:
- SQL escrito como strings → errores solo visibles al ejecutar
- Sin autocompletado en el editor
- Las filas son tuplas o diccionarios, no objetos reales

**SQLModel** soluciona esto: defines las tablas como **clases Python** y obtienes:
- ✅ Autocompletado en el editor
- ✅ Validación automática de tipos
- ✅ El SQL se genera solo
- ✅ Los datos son objetos Python reales

> SQLModel fue creado por Sebastián Ramírez (también creó FastAPI). Combina SQLAlchemy y Pydantic.

---

### Parte 2 — Tu primer modelo SQLModel (50 min)

```python
# modelos.py
from typing import Optional
from sqlmodel import Field, SQLModel, create_engine, Session, select

# Esta clase ES la definición de la tabla
class Artista(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str                              # NOT NULL
    pais: Optional[str] = None              # Puede ser NULL
    año_inicio: Optional[int] = None        # Puede ser NULL
    activo: bool = Field(default=True)       # Con valor por defecto
```

Con esta clase, SQLModel genera automáticamente:
```sql
CREATE TABLE artista (
    id INTEGER PRIMARY KEY,
    nombre VARCHAR NOT NULL,
    pais VARCHAR,
    año_inicio INTEGER,
    activo INTEGER NOT NULL DEFAULT 1
)
```

#### Tipos de datos Python → SQL

| Python | SQL |
|--------|-----|
| `str` | VARCHAR |
| `int` | INTEGER |
| `float` | REAL |
| `bool` | BOOLEAN (INTEGER 0/1) |
| `Optional[str]` | VARCHAR nullable |
| `Optional[int]` | INTEGER nullable |

#### Opciones de Field

```python
class EjemploCompleto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str = Field(min_length=1, max_length=100)
    email: str = Field(unique=True)          # No se puede repetir
    codigo: str = Field(index=True)          # Búsquedas más rápidas
    edad: Optional[int] = Field(default=None, ge=0, le=120)  # 0 ≤ edad ≤ 120
    puntuacion: float = Field(default=0.0, ge=0.0, le=5.0)
```

---

### Parte 3 — Creando la base de datos con SQLModel (30 min)

```python
# database.py
from sqlmodel import create_engine, SQLModel

DATABASE_URL = "sqlite:///mi_musica.db"

# echo=True imprime el SQL generado (muy útil para aprender)
engine = create_engine(DATABASE_URL, echo=True)

def crear_tablas():
    # Importar los modelos ANTES de llamar esto
    SQLModel.metadata.create_all(engine)
    print("¡Tablas creadas!")
```

```python
# main.py
from database import crear_tablas
from modelos import Artista  # El import registra el modelo

if __name__ == "__main__":
    crear_tablas()
```

Cuando ejecutes, verás en la consola el SQL generado por SQLModel.

---

### Parte 4 — Actividad: Modelando tu propia app (20 min)

Define los modelos SQLModel para la app que diseñaste en la sesión 02. Incluye:
- Mínimo 2 modelos con `table=True`
- Claves primarias
- Campos opcionales y obligatorios
- Al menos una clave foránea
- Al menos un Field con restricciones (unique, index, ge/le)

---

### Resumen de la Sesión 13

✅ SQLModel define tablas como clases Python con anotaciones de tipo.
✅ `table=True` indica que la clase es una tabla de BD real.
✅ `Optional[tipo]` hace que el campo sea nullable.
✅ `Field()` configura restricciones de la columna.
✅ `create_engine(url)` crea la conexión.
✅ `SQLModel.metadata.create_all(engine)` crea todas las tablas.

---
---

## Sesión 14 — SQLModel: CRUD completo con Sessions

**Duración:** 2 horas
**Objetivo:** Implementar las 4 operaciones CRUD con Sessions de SQLModel.

---

### Parte 1 — El concepto de Session (15 min)

La **Session** es el "espacio de trabajo" donde ocurren todas las operaciones. Funciona como un carrito de compras: acumulas cambios y al final decides si los confirmas (commit) o cancelas (rollback).

```python
from sqlmodel import Session, create_engine

engine = create_engine("sqlite:///musica.db")

with Session(engine) as session:
    # Aquí van todas las operaciones
    pass
    # Al salir del "with": commit automático si no hubo errores
    # Si hubo error: rollback automático
```

---

### Parte 2 — CRUD completo (85 min)

```python
# crud_completo.py
from typing import Optional, List
from sqlmodel import Field, SQLModel, create_engine, Session, select

class Artista(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    pais: Optional[str] = None
    año_inicio: Optional[int] = None

class Cancion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    artista_id: int = Field(foreign_key="artista.id")
    año: Optional[int] = None
    reproducciones: int = 0

engine = create_engine("sqlite:///musica_crud.db", echo=False)
SQLModel.metadata.create_all(engine)

# ── CREATE ─────────────────────────────────────────────────

def crear_artista(nombre: str, pais: str = None, año: int = None) -> Artista:
    artista = Artista(nombre=nombre, pais=pais, año_inicio=año)
    with Session(engine) as session:
        session.add(artista)
        session.commit()
        session.refresh(artista)  # Carga el id asignado por la BD
    return artista

def crear_cancion(titulo: str, artista_id: int, año: int = None) -> Cancion:
    cancion = Cancion(titulo=titulo, artista_id=artista_id, año=año)
    with Session(engine) as session:
        session.add(cancion)
        session.commit()
        session.refresh(cancion)
    return cancion

# ── READ ───────────────────────────────────────────────────

def obtener_artista(artista_id: int) -> Optional[Artista]:
    with Session(engine) as session:
        return session.get(Artista, artista_id)

def listar_artistas() -> List[Artista]:
    with Session(engine) as session:
        return session.exec(select(Artista)).all()

def buscar_canciones(año: int = None, min_rep: int = None) -> List[Cancion]:
    with Session(engine) as session:
        q = select(Cancion)
        if año:
            q = q.where(Cancion.año == año)
        if min_rep:
            q = q.where(Cancion.reproducciones >= min_rep)
        return session.exec(q).all()

# ── UPDATE ─────────────────────────────────────────────────

def actualizar_artista(artista_id: int, nuevo_pais: str = None) -> Optional[Artista]:
    with Session(engine) as session:
        artista = session.get(Artista, artista_id)
        if not artista:
            return None
        if nuevo_pais:
            artista.pais = nuevo_pais
        session.add(artista)
        session.commit()
        session.refresh(artista)
    return artista

def incrementar_reproducciones(cancion_id: int, cantidad: int = 1) -> Optional[Cancion]:
    with Session(engine) as session:
        cancion = session.get(Cancion, cancion_id)
        if not cancion:
            return None
        cancion.reproducciones += cantidad
        session.add(cancion)
        session.commit()
        session.refresh(cancion)
    return cancion

# ── DELETE ─────────────────────────────────────────────────

def eliminar_cancion(cancion_id: int) -> bool:
    with Session(engine) as session:
        cancion = session.get(Cancion, cancion_id)
        if not cancion:
            return False
        session.delete(cancion)
        session.commit()
    return True

# ── Prueba ─────────────────────────────────────────────────

if __name__ == "__main__":
    # Crear
    bb = crear_artista("Bad Bunny", "Puerto Rico", 2016)
    print(f"Creado: {bb.nombre} (id={bb.id})")

    c1 = crear_cancion("Tití Me Preguntó", bb.id, 2022)
    c2 = crear_cancion("Me Porto Bonito", bb.id, 2022)

    # Leer
    artistas = listar_artistas()
    print(f"\nArtistas: {[a.nombre for a in artistas]}")

    # Actualizar
    incrementar_reproducciones(c1.id, 1000000)

    # Verificar
    c = obtener_artista(bb.id)
    print(f"\nArtista recuperado: {c.nombre}")

    # Eliminar
    resultado = eliminar_cancion(c2.id)
    print(f"\nCanción eliminada: {resultado}")
```

---

### Parte 3 — Consultas avanzadas con select() (20 min)

```python
with Session(engine) as session:
    # WHERE múltiple
    q = (select(Cancion)
         .where(Cancion.año >= 2020)
         .where(Cancion.reproducciones > 100000000))
    canciones = session.exec(q).all()

    # ORDER BY
    q = select(Artista).order_by(Artista.nombre)
    artistas = session.exec(q).all()

    # LIMIT
    q = select(Cancion).order_by(Cancion.reproducciones.desc()).limit(5)
    top5 = session.exec(q).all()

    # Obtener uno o None
    q = select(Artista).where(Artista.nombre == "Karol G")
    artista = session.exec(q).first()
```

---

### Resumen de la Sesión 14

✅ La `Session` agrupa operaciones y hace commit/rollback automático.
✅ `session.add(obj)` + `session.commit()` + `session.refresh(obj)` para CREATE/UPDATE.
✅ `session.get(Modelo, id)` obtiene un registro por su PK.
✅ `session.exec(select(...)).all()` ejecuta consultas.
✅ `session.delete(obj)` + `session.commit()` para DELETE.

---
---

## Sesión 15 — SQLModel: Relaciones y separación de modelos

**Duración:** 2 horas
**Objetivo:** Implementar relaciones entre modelos y aprender el patrón de separar modelos Base/Create/Response.

---

### Parte 1 — Relaciones en SQLModel (40 min)

```python
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class Artista(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    pais: Optional[str] = None

    # Un artista tiene muchas canciones
    canciones: List["Cancion"] = Relationship(back_populates="artista")

class Cancion(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    titulo: str
    artista_id: int = Field(foreign_key="artista.id")
    año: Optional[int] = None

    # Una canción pertenece a un artista
    artista: Optional[Artista] = Relationship(back_populates="canciones")
```

```python
# Usando las relaciones
with Session(engine) as session:
    artista = session.get(Artista, 1)
    session.refresh(artista)

    print(f"Canciones de {artista.nombre}:")
    for c in artista.canciones:
        print(f"  - {c.titulo}")

    cancion = session.get(Cancion, 1)
    session.refresh(cancion)
    print(f"Artista de '{cancion.titulo}': {cancion.artista.nombre}")
```

---

### Parte 2 — El patrón Base/Create/Response (50 min)

Este es el patrón más importante que usarás con FastAPI:

```python
# ── Artista ────────────────────────────────────────────────

class ArtistaBase(SQLModel):
    """Atributos comunes a todos los contextos"""
    nombre: str
    pais: Optional[str] = None
    año_inicio: Optional[int] = None

class ArtistaCreate(ArtistaBase):
    """Lo que recibe el usuario al CREAR un artista.
    No incluye id (lo asigna la BD)."""
    pass

class ArtistaUpdate(SQLModel):
    """Lo que recibe el usuario al ACTUALIZAR.
    Todos los campos son opcionales."""
    nombre: Optional[str] = None
    pais: Optional[str] = None
    año_inicio: Optional[int] = None

class Artista(ArtistaBase, table=True):
    """La tabla real en la base de datos."""
    id: Optional[int] = Field(default=None, primary_key=True)
    canciones: List["Cancion"] = Relationship(back_populates="artista")

class ArtistaResponse(ArtistaBase):
    """Lo que DEVOLVEMOS al usuario.
    Siempre incluye el id."""
    id: int

# ── ¿Por qué esta separación? ─────────────────────────────
# ArtistaCreate: el usuario no puede elegir el id
# ArtistaUpdate: puede actualizar solo algunos campos
# Artista (tabla): contiene todo, incluyendo relaciones
# ArtistaResponse: lo que mostramos, controlamos qué exponemos
# Podríamos agregar campos "internos" a la tabla
# (como password_hash) que NO incluimos en ArtistaResponse
```

---

### Parte 3 — Actividad integradora (30 min)

Define el modelo completo (Base, Create, Update, Table, Response) para la app de tu proyecto final. Incluye:
- Mínimo 3 entidades
- Relaciones 1:N entre ellas
- Una relación N:M con tabla intermedia

---

### Resumen de la Sesión 15

✅ `Relationship(back_populates=...)` conecta modelos sin escribir SQL JOIN.
✅ El patrón Base/Create/Update/Table/Response separa responsabilidades.
✅ `Create` no tiene `id`; `Update` tiene todos los campos opcionales; `Response` siempre tiene `id`.
✅ Esta separación es fundamental para construir APIs seguras y correctas.

---
---

# ⚡ BLOQUE 5 — FASTAPI

---

## Sesión 16 — ¡Hola FastAPI! Tu primer servidor web

**Duración:** 2 horas
**Objetivo:** Entender qué es una API REST, instalar FastAPI y crear los primeros endpoints con documentación automática.

---

### Parte 1 — ¿Qué es una API REST? (20 min)

**La analogía del restaurante:**
- Tú (app móvil/web) = cliente
- La cocina (servidor + BD) = donde viven los datos
- El mesero = la **API**

Tú le dices al mesero qué quieres → el mesero va a la cocina → la cocina prepara → el mesero te lo trae.

Una **API REST** es un conjunto de reglas para comunicarse a través de HTTP.

#### Los métodos HTTP y su equivalente SQL

| HTTP | Uso | SQL |
|------|-----|-----|
| `GET` | Obtener datos | `SELECT` |
| `POST` | Crear datos nuevos | `INSERT` |
| `PUT` | Actualizar datos | `UPDATE` |
| `DELETE` | Borrar datos | `DELETE` |

#### Las URLs son los "recursos"

```
GET    /artistas          → Dame todos los artistas
GET    /artistas/5        → Dame el artista con id=5
POST   /artistas          → Crea un nuevo artista
PUT    /artistas/5        → Actualiza el artista con id=5
DELETE /artistas/5        → Borra el artista con id=5
GET    /artistas/5/canciones → Canciones del artista 5
```

---

### Parte 2 — Tu primer servidor FastAPI (50 min)

```python
# main.py
from fastapi import FastAPI
from typing import Optional

app = FastAPI(
    title="Mi API de Música 🎵",
    description="API para gestionar canciones y artistas",
    version="1.0.0"
)

@app.get("/")
def inicio():
    return {"mensaje": "¡Bienvenido a mi API! 🎵"}

@app.get("/artistas")
def listar_artistas():
    # En una app real, esto vendría de la BD
    return [
        {"id": 1, "nombre": "Bad Bunny", "pais": "Puerto Rico"},
        {"id": 2, "nombre": "Taylor Swift", "pais": "Estados Unidos"},
    ]

@app.get("/artistas/{artista_id}")
def obtener_artista(artista_id: int):
    artistas = {
        1: {"id": 1, "nombre": "Bad Bunny"},
        2: {"id": 2, "nombre": "Taylor Swift"},
    }
    if artista_id not in artistas:
        return {"error": "Artista no encontrado"}
    return artistas[artista_id]

@app.get("/buscar")
def buscar(
    nombre: Optional[str] = None,
    pais: Optional[str] = None
):
    return {"buscando": {"nombre": nombre, "pais": pais}}
```

#### Ejecutar:
```bash
uvicorn main:app --reload
```

Abre: **http://127.0.0.1:8000**

---

### Parte 3 — La documentación automática (30 min)

FastAPI genera documentación interactiva automáticamente:

- **http://localhost:8000/docs** → Swagger UI (puedes probar los endpoints directamente)
- **http://localhost:8000/redoc** → ReDoc (mejor para leer)

Prueba en `/docs`:
1. Haz clic en `GET /artistas` → "Try it out" → "Execute"
2. Haz clic en `GET /artistas/{artista_id}` → ingresa `1` → "Execute"
3. Prueba con id=999 para ver el error

---

### Parte 4 — Parámetros de ruta vs Query Parameters (20 min)

```python
# Parámetro de RUTA: va en la URL
# GET /canciones/5
@app.get("/canciones/{cancion_id}")
def obtener_cancion(cancion_id: int):
    return {"id": cancion_id}

# Query PARAMETER: va después del ?
# GET /canciones?año=2022&limite=5
@app.get("/canciones")
def listar_canciones(
    año: Optional[int] = None,
    artista: Optional[str] = None,
    limite: int = 10
):
    return {"filtros": {"año": año, "artista": artista, "limite": limite}}

# Ambos a la vez
# GET /artistas/1/canciones?limite=5
@app.get("/artistas/{artista_id}/canciones")
def canciones_de_artista(artista_id: int, limite: int = 10):
    return {"artista_id": artista_id, "limite": limite}
```

---

### Resumen de la Sesión 16

✅ Una API REST usa métodos HTTP (GET/POST/PUT/DELETE) sobre URLs.
✅ `@app.get("/ruta")` define un endpoint GET.
✅ FastAPI genera documentación automática en `/docs`.
✅ `uvicorn main:app --reload` inicia el servidor de desarrollo.
✅ Parámetros de ruta: `{id}` en la URL. Query params: después del `?`.

---
---

## Sesión 17 — FastAPI + SQLModel: La combinación ganadora

**Duración:** 2 horas
**Objetivo:** Conectar FastAPI con SQLModel usando inyección de dependencias para crear una API con base de datos real.

---

### Parte 1 — Estructura del proyecto (20 min)

```
mi_api_musica/
├── main.py          ← App FastAPI y endpoints
├── database.py      ← Engine y función get_session
├── modelos.py       ← Todos los modelos SQLModel
└── requirements.txt
```

---

### Parte 2 — database.py y modelos.py (30 min)

```python
# database.py
from sqlmodel import create_engine, Session, SQLModel
from typing import Generator

DATABASE_URL = "sqlite:///musica.db"

engine = create_engine(
    DATABASE_URL,
    echo=False,
    connect_args={"check_same_thread": False}  # Necesario para SQLite + FastAPI
)

def crear_tablas():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator:
    """
    Generador que provee una sesión de BD a cada request.
    FastAPI la usará como dependencia.
    """
    with Session(engine) as session:
        yield session
```

```python
# modelos.py
from typing import Optional, List
from sqlmodel import Field, SQLModel, Relationship

class ArtistaBase(SQLModel):
    nombre: str
    pais: Optional[str] = None
    año_inicio: Optional[int] = None

class ArtistaCreate(ArtistaBase):
    pass

class ArtistaUpdate(SQLModel):
    nombre: Optional[str] = None
    pais: Optional[str] = None
    año_inicio: Optional[int] = None

class Artista(ArtistaBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    canciones: List["Cancion"] = Relationship(back_populates="artista")

class ArtistaResponse(ArtistaBase):
    id: int

class CancionBase(SQLModel):
    titulo: str
    artista_id: int
    año: Optional[int] = None
    reproducciones: int = 0

class CancionCreate(CancionBase):
    pass

class CancionUpdate(SQLModel):
    titulo: Optional[str] = None
    artista_id: Optional[int] = None
    año: Optional[int] = None
    reproducciones: Optional[int] = None

class Cancion(CancionBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    artista: Optional[Artista] = Relationship(back_populates="canciones")

class CancionResponse(CancionBase):
    id: int
```

---

### Parte 3 — Inyección de dependencias (50 min)

```python
# main.py
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from typing import List
from contextlib import asynccontextmanager

from database import engine, get_session, crear_tablas
from modelos import Artista, ArtistaCreate, ArtistaResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_tablas()   # Se ejecuta al iniciar la app
    yield
    # Aquí va código de limpieza al cerrar (opcional)

app = FastAPI(title="API de Música 🎵", lifespan=lifespan)

@app.get("/artistas", response_model=List[ArtistaResponse])
def listar_artistas(session: Session = Depends(get_session)):
    #                                   ↑
    # Depends(get_session) le dice a FastAPI:
    # "Antes de ejecutar esta función, llama get_session()
    # y pasa el resultado como 'session'"
    artistas = session.exec(select(Artista)).all()
    return artistas

@app.get("/artistas/{artista_id}", response_model=ArtistaResponse)
def obtener_artista(artista_id: int, session: Session = Depends(get_session)):
    artista = session.get(Artista, artista_id)
    if not artista:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    return artista

@app.post("/artistas", response_model=ArtistaResponse, status_code=201)
def crear_artista(data: ArtistaCreate, session: Session = Depends(get_session)):
    artista = Artista.model_validate(data)
    session.add(artista)
    session.commit()
    session.refresh(artista)
    return artista
```

> 💡 `response_model=ArtistaResponse` le dice a FastAPI qué forma tiene la respuesta. Valida automáticamente y filtra campos que no deben mostrarse.

> 💡 `raise HTTPException(status_code=404, ...)` devuelve el error HTTP correcto.

---

### Parte 4 — Probando la integración (20 min)

```bash
uvicorn main:app --reload
```

En **http://localhost:8000/docs**:
1. `POST /artistas` — Crea 3 artistas
2. `GET /artistas` — Verifica que aparecen
3. `GET /artistas/1` — Obtén el primero
4. `GET /artistas/999` — Verifica el error 404

---

### Resumen de la Sesión 17

✅ `get_session()` con `yield` es el patrón para proveer sesiones a FastAPI.
✅ `Depends(get_session)` inyecta automáticamente la sesión en cada endpoint.
✅ `lifespan` ejecuta código al iniciar/cerrar la app.
✅ `response_model` valida y filtra la respuesta automáticamente.
✅ `HTTPException` devuelve errores HTTP con el código correcto.

---
---

## Sesión 18 — Endpoints GET y POST

**Duración:** 2 horas
**Objetivo:** Implementar todos los endpoints de lectura y creación con validación, filtros y documentación completa.

---

### API completa de GET y POST

```python
# main.py (GET y POST completos)
from fastapi import FastAPI, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import List, Optional
from contextlib import asynccontextmanager

from database import engine, get_session, crear_tablas
from modelos import (
    Artista, ArtistaCreate, ArtistaResponse,
    Cancion, CancionCreate, CancionResponse
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    crear_tablas()
    yield

app = FastAPI(title="API de Música 🎵", lifespan=lifespan)

# ── Artistas: GET ──────────────────────────────────────────

@app.get("/artistas", response_model=List[ArtistaResponse], tags=["Artistas"])
def listar_artistas(
    pais: Optional[str] = Query(default=None, description="Filtrar por país"),
    limite: int = Query(default=20, ge=1, le=100),
    session: Session = Depends(get_session)
):
    """Obtiene todos los artistas. Permite filtrar por país."""
    q = select(Artista)
    if pais:
        q = q.where(Artista.pais == pais)
    q = q.limit(limite)
    return session.exec(q).all()

@app.get("/artistas/{artista_id}", response_model=ArtistaResponse, tags=["Artistas"])
def obtener_artista(artista_id: int, session: Session = Depends(get_session)):
    """Obtiene un artista por su ID."""
    artista = session.get(Artista, artista_id)
    if not artista:
        raise HTTPException(status_code=404, detail=f"Artista {artista_id} no encontrado")
    return artista

@app.get("/artistas/{artista_id}/canciones", response_model=List[CancionResponse], tags=["Artistas"])
def canciones_del_artista(artista_id: int, session: Session = Depends(get_session)):
    """Obtiene todas las canciones de un artista."""
    artista = session.get(Artista, artista_id)
    if not artista:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    q = select(Cancion).where(Cancion.artista_id == artista_id)
    return session.exec(q).all()

# ── Artistas: POST ─────────────────────────────────────────

@app.post("/artistas", response_model=ArtistaResponse, status_code=201, tags=["Artistas"])
def crear_artista(data: ArtistaCreate, session: Session = Depends(get_session)):
    """Crea un nuevo artista."""
    artista = Artista.model_validate(data)
    session.add(artista)
    session.commit()
    session.refresh(artista)
    return artista

# ── Canciones: GET ─────────────────────────────────────────

@app.get("/canciones", response_model=List[CancionResponse], tags=["Canciones"])
def listar_canciones(
    año: Optional[int] = Query(default=None, description="Filtrar por año"),
    min_reproducciones: Optional[int] = Query(default=None, ge=0),
    orden: str = Query(default="titulo", description="titulo | año | reproducciones"),
    limite: int = Query(default=20, ge=1, le=100),
    session: Session = Depends(get_session)
):
    """Lista canciones con filtros y ordenamiento opcionales."""
    q = select(Cancion)
    if año:
        q = q.where(Cancion.año == año)
    if min_reproducciones is not None:
        q = q.where(Cancion.reproducciones >= min_reproducciones)
    if orden == "reproducciones":
        q = q.order_by(Cancion.reproducciones.desc())
    elif orden == "año":
        q = q.order_by(Cancion.año.desc())
    else:
        q = q.order_by(Cancion.titulo)
    return session.exec(q.limit(limite)).all()

@app.get("/canciones/{cancion_id}", response_model=CancionResponse, tags=["Canciones"])
def obtener_cancion(cancion_id: int, session: Session = Depends(get_session)):
    """Obtiene una canción por su ID."""
    cancion = session.get(Cancion, cancion_id)
    if not cancion:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    return cancion

# ── Canciones: POST ────────────────────────────────────────

@app.post("/canciones", response_model=CancionResponse, status_code=201, tags=["Canciones"])
def crear_cancion(data: CancionCreate, session: Session = Depends(get_session)):
    """Crea una nueva canción. El artista_id debe existir."""
    artista = session.get(Artista, data.artista_id)
    if not artista:
        raise HTTPException(
            status_code=404,
            detail=f"Artista con id {data.artista_id} no existe"
        )
    cancion = Cancion.model_validate(data)
    session.add(cancion)
    session.commit()
    session.refresh(cancion)
    return cancion

# ── Endpoint especial ──────────────────────────────────────

@app.get("/estadisticas", tags=["General"])
def estadisticas(session: Session = Depends(get_session)):
    """Resumen estadístico de la base de datos."""
    total_artistas = len(session.exec(select(Artista)).all())
    total_canciones = len(session.exec(select(Cancion)).all())
    return {
        "artistas": total_artistas,
        "canciones": total_canciones,
        "estado": "operativo"
    }
```

---

### Actividad (30 min)

En `/docs`, prueba:
1. Crea 4 artistas (al menos 2 del mismo país)
2. Crea 5 canciones
3. Filtra canciones por año
4. Filtra artistas por país
5. Obtén las canciones de un artista específico
6. Intenta crear una canción con artista_id=999 → verifica el 404

---

### Resumen de la Sesión 18

✅ `Query()` documenta y valida los query parameters.
✅ `tags=["Nombre"]` agrupa endpoints en la documentación.
✅ El docstring de la función se convierte en descripción del endpoint.
✅ Siempre verifica la existencia de recursos relacionados antes de crearlos.
✅ `status_code=201` para creaciones exitosas.

---
---

## Sesión 19 — Endpoints PUT y DELETE + Debugging

**Duración:** 2 horas
**Objetivo:** Completar el CRUD con PUT y DELETE, aprender a manejar errores y resolver los problemas más comunes.

---

### Parte 1 — PUT: Actualizando recursos (40 min)

```python
from modelos import ArtistaUpdate, CancionUpdate

@app.put("/artistas/{artista_id}", response_model=ArtistaResponse, tags=["Artistas"])
def actualizar_artista(
    artista_id: int,
    data: ArtistaUpdate,
    session: Session = Depends(get_session)
):
    """
    Actualiza un artista. Solo envía los campos que quieres cambiar.
    """
    artista = session.get(Artista, artista_id)
    if not artista:
        raise HTTPException(status_code=404, detail="Artista no encontrado")

    # exclude_unset=True → solo los campos que el usuario envió
    campos = data.model_dump(exclude_unset=True)
    for campo, valor in campos.items():
        setattr(artista, campo, valor)

    session.add(artista)
    session.commit()
    session.refresh(artista)
    return artista

@app.put("/canciones/{cancion_id}", response_model=CancionResponse, tags=["Canciones"])
def actualizar_cancion(
    cancion_id: int,
    data: CancionUpdate,
    session: Session = Depends(get_session)
):
    """Actualiza una canción. Solo envía los campos a cambiar."""
    cancion = session.get(Cancion, cancion_id)
    if not cancion:
        raise HTTPException(status_code=404, detail="Canción no encontrada")

    if data.artista_id is not None:
        if not session.get(Artista, data.artista_id):
            raise HTTPException(status_code=404, detail="El artista_id no existe")

    for campo, valor in data.model_dump(exclude_unset=True).items():
        setattr(cancion, campo, valor)

    session.add(cancion)
    session.commit()
    session.refresh(cancion)
    return cancion

# Endpoint especial: reproducir (muy útil en apps reales)
@app.put("/canciones/{cancion_id}/reproducir", response_model=CancionResponse, tags=["Canciones"])
def reproducir(cancion_id: int, session: Session = Depends(get_session)):
    """Incrementa el contador de reproducciones en 1."""
    cancion = session.get(Cancion, cancion_id)
    if not cancion:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    cancion.reproducciones += 1
    session.add(cancion)
    session.commit()
    session.refresh(cancion)
    return cancion
```

---

### Parte 2 — DELETE (20 min)

```python
@app.delete("/artistas/{artista_id}", tags=["Artistas"])
def eliminar_artista(artista_id: int, session: Session = Depends(get_session)):
    """Elimina un artista. ⚠️ Elimina también todas sus canciones."""
    artista = session.get(Artista, artista_id)
    if not artista:
        raise HTTPException(status_code=404, detail="Artista no encontrado")
    nombre = artista.nombre
    session.delete(artista)
    session.commit()
    return {"mensaje": f"'{nombre}' eliminado", "id": artista_id}

@app.delete("/canciones/{cancion_id}", tags=["Canciones"])
def eliminar_cancion(cancion_id: int, session: Session = Depends(get_session)):
    """Elimina una canción."""
    cancion = session.get(Cancion, cancion_id)
    if not cancion:
        raise HTTPException(status_code=404, detail="Canción no encontrada")
    titulo = cancion.titulo
    session.delete(cancion)
    session.commit()
    return {"mensaje": f"'{titulo}' eliminada", "id": cancion_id}
```

---

### Parte 3 — Errores frecuentes y cómo resolverlos (40 min)

Esta sección es nueva y vale la pena dedicarle tiempo completo.

#### Error 1: `Table already exists`
```
sqlalchemy.exc.OperationalError: (sqlite3.OperationalError) table artista already exists
```
**Causa:** Modificaste un modelo pero la tabla antigua sigue en el archivo .db.
**Solución:**
```bash
# Opción rápida: borrar el archivo de BD (pierdes datos)
rm musica.db

# Opción correcta en producción: usar migraciones (Alembic)
# Por ahora, durante desarrollo, borrar el archivo está bien
```

#### Error 2: `check_same_thread`
```
sqlalchemy.exc.ProgrammingError: SQLite objects created in a thread can only be used in that same thread
```
**Causa:** No agregaste `check_same_thread: False` al crear el engine.
**Solución:**
```python
engine = create_engine(url, connect_args={"check_same_thread": False})
```

#### Error 3: `422 Unprocessable Entity`
```
{"detail": [{"type": "missing", "loc": ["body", "nombre"], ...}]}
```
**Causa:** Enviaste datos que no pasan la validación del modelo.
**Solución:** Lee el detalle del error. Indica exactamente qué campo faltó o fue inválido.

#### Error 4: Modelos no registrados
```
sqlalchemy.exc.InvalidRequestError: Could not determine join condition
```
**Causa:** Un modelo no fue importado antes de llamar `create_all()`.
**Solución:**
```python
# En database.py o main.py, importa TODOS los modelos antes de create_all
from modelos import Artista, Cancion  # ← no olvides ninguno
SQLModel.metadata.create_all(engine)
```

#### Error 5: `DetachedInstanceError`
```
sqlalchemy.orm.exc.DetachedInstanceError: Instance is not bound to a Session
```
**Causa:** Intentas acceder a una relación (`artista.canciones`) después de cerrar la Session.
**Solución:** Usa `session.refresh(obj)` mientras la sesión está abierta, o carga la relación dentro del `with Session`.

---

### Resumen de la Sesión 19

✅ `model_dump(exclude_unset=True)` es la clave para actualizaciones parciales.
✅ `setattr(obj, campo, valor)` actualiza campos dinámicamente.
✅ Los 5 errores más comunes y cómo resolverlos.
✅ El CRUD completo de la API está terminado.

---
---

# 🏆 BLOQUE 6 — PROYECTO FINAL

---

## Sesión 20 — Proyecto Final: Diseño e inicio

**Duración:** 2 horas
**Objetivo:** Diseñar la base de datos del proyecto, estructurar el proyecto y comenzar la implementación.

---

### Ideas de proyectos

| Proyecto | Entidades sugeridas |
|----------|-------------------|
| 🎮 Biblioteca de videojuegos | Juego, Género, Desarrollador, Reseña |
| 📚 Club de lectura | Libro, Autor, Usuario, Comentario |
| 🍕 Menú de restaurante | Plato, Categoría, Ingrediente, Pedido |
| ⚽ Liga deportiva | Equipo, Jugador, Partido, Estadística |
| 🎬 Base de películas | Película, Director, Actor, Calificación |
| 🎓 Sistema escolar | Estudiante, Materia, Profesor, Nota |
| 🏋️ Rutinas de ejercicio | Ejercicio, Rutina, Usuario, Progreso |
| 🌮 App de recetas | Receta, Ingrediente, Categoría, Comentario |

---

### Checklist de diseño (45 min)

Antes de escribir código, completa este checklist:

- [ ] Elegí el tema de mi proyecto
- [ ] Identifiqué al menos 3 entidades
- [ ] Definí los atributos de cada entidad con sus tipos
- [ ] Identifiqué todas las relaciones (1:N y N:M)
- [ ] Dibujé el diagrama de la BD en papel
- [ ] Definí las claves primarias y foráneas
- [ ] No hay datos repetidos innecesariamente

---

### Checklist de implementación (75 min)

Sigue este orden estrictamente:

**Paso 1 — `modelos.py`** (25 min)
```
[ ] Modelos Base, Create, Update, Table, Response para cada entidad
[ ] Relaciones con Relationship y back_populates
[ ] Al menos un campo con validación (unique, index, ge/le)
```

**Paso 2 — `database.py`** (5 min)
```
[ ] engine configurado correctamente (con check_same_thread para SQLite)
[ ] get_session() implementado
[ ] crear_tablas() implementado
```

**Paso 3 — `main.py`** (45 min)
```
[ ] App FastAPI con título y descripción
[ ] lifespan configurado (llama crear_tablas)
[ ] Implementar primero solo los GET
[ ] Verificar en /docs que funcionan
[ ] Implementar POST
[ ] Verificar, crear algunos registros
[ ] Seguir con PUT y DELETE
```

---

### Resumen de la Sesión 20

✅ El diseño va primero, siempre.
✅ Seguir el orden: modelos → database → main → verificar → siguiente endpoint.
✅ Probar en `/docs` después de cada endpoint implementado.

---
---

## Sesión 21 — Proyecto Final: Construcción y revisión entre pares

**Duración:** 2 horas
**Objetivo:** Terminar la implementación, agregar el endpoint especial y revisar el código de otro compañero.

---

### Parte 1 — Construcción y refinamiento (60 min)

**Checklist de endpoints mínimos por entidad:**

Para cada una de tus 3+ entidades:
- [ ] `GET /entidad` — Lista todos (con al menos un filtro opcional)
- [ ] `GET /entidad/{id}` — Obtiene uno por id (con 404 si no existe)
- [ ] `POST /entidad` — Crea uno nuevo (con validación de relaciones)
- [ ] `PUT /entidad/{id}` — Actualiza uno (con `exclude_unset=True`)
- [ ] `DELETE /entidad/{id}` — Elimina uno

**Endpoint especial (mínimo 1, idealmente 2):**
- [ ] Un endpoint que combine 2 entidades (ej: `/autores/{id}/libros`)
- [ ] Un endpoint con lógica especial (ej: `/canciones/{id}/reproducir`)
- [ ] Un endpoint de estadísticas o resumen

**Documentación mínima:**
- [ ] Título descriptivo en la app FastAPI
- [ ] Docstring en cada endpoint explicando qué hace
- [ ] `tags` para agrupar los endpoints por entidad

---

### Parte 2 — Revisión entre pares (60 min)

Intercambia tu proyecto con un compañero y completa esta revisión:

```
Proyecto revisado: ________________________
Revisor: __________________________________

FUNCIONALIDAD (marca cada uno que funciona)
[ ] GET /entidad      funciona y devuelve lista
[ ] GET /entidad/{id} devuelve 404 si no existe
[ ] POST /entidad     crea correctamente
[ ] PUT /entidad/{id} actualiza parcialmente
[ ] DELETE            elimina y confirma

DISEÑO DE BD
[ ] Las tablas tienen sentido para el tema elegido
[ ] Las relaciones son correctas
[ ] No hay datos repetidos innecesariamente

UNA cosa que está muy bien implementada:
_____________________________________________

UNA sugerencia de mejora concreta:
_____________________________________________

¿Hay algún bug que encontraste?
_____________________________________________
```

---

### Resumen de la Sesión 21

✅ CRUD completo implementado para todas las entidades.
✅ Al menos un endpoint especial creativo.
✅ Documentación básica en todos los endpoints.
✅ El código fue revisado por un compañero.

---
---

## Sesión 22 — Proyecto Final: Presentaciones y cierre

**Duración:** 2 horas
**Objetivo:** Presentar el proyecto al grupo, recibir retroalimentación y celebrar lo aprendido en el curso.

---

### Estructura de la presentación (8 minutos por equipo)

**1. ¿Qué construí? (1 min)**
- Nombre y descripción del proyecto
- ¿Para qué sirve? ¿A quién le sería útil?

**2. El diseño de la base de datos (2 min)**
- Muestra el diagrama de tus tablas
- Explica las relaciones y por qué tomaste esas decisiones

**3. Demo en vivo en `/docs` (4 min)**
- Crear al menos un registro de cada entidad
- Mostrar un filtro funcionando
- Demostrar el endpoint especial
- Mostrar el manejo de un error 404

**4. Reflexión (1 min)**
- ¿Qué fue lo más difícil?
- ¿Qué agregarías con más tiempo?

---

### Rúbrica de evaluación del proyecto

| Criterio | Excelente (4) | Bien (3) | Regular (2) | Insuficiente (1) |
|----------|--------------|----------|-------------|-----------------|
| **Diseño de BD** | 3+ tablas, relaciones correctas, sin redundancia | 3 tablas, relaciones aceptables | 2 tablas, alguna redundancia | 1 tabla o diseño incorrecto |
| **Funcionalidad** | CRUD completo + 2 endpoints especiales | CRUD completo + 1 especial | CRUD casi completo | CRUD incompleto |
| **Validaciones** | 404 en todos los casos, validaciones de datos | 404 implementado | 404 parcial | Sin manejo de errores |
| **Documentación** | Tags + docstrings + descripción completa | Tags + docstrings | Solo tags | Sin documentación |
| **Presentación** | Clara, demo fluida, reflexión profunda | Clara, demo funciona | Algo confusa, demo parcial | Confusa o sin demo |

---

### Retrospectiva del curso (15 min)

**Lo que aprendiste en 22 sesiones:**

```
Sesiones 01-03 → Pensar en datos y diseñar bases de datos
Sesiones 04-07 → SQL básico: el lenguaje de las bases de datos
Sesiones 08-11 → SQL avanzado: relaciones y agregaciones
Sesiones 12-15 → Python + SQLModel: la BD desde Python
Sesiones 16-19 → FastAPI: exponiendo la BD al mundo
Sesiones 20-22 → Proyecto completo propio
```

**¿A dónde puedes ir desde aquí?**

- 🔐 **Autenticación** — Agregar login con JWT tokens
- 🐘 **PostgreSQL** — De SQLite a una BD de producción
- 🐳 **Docker** — Empaquetar tu app para cualquier servidor
- ☁️ **Deployment** — Publicar en Railway, Render o Fly.io (gratis)
- 🧪 **Testing** — Pruebas automáticas con pytest
- 🌐 **Frontend** — Conectar tu API con React o Vue.js
- 📦 **Alembic** — Migraciones cuando cambies la estructura de la BD

---

### 🎉 ¡Lo lograste!

Pasaste de no saber qué era una base de datos a tener una **API REST completamente funcional** con:

✅ Base de datos con múltiples tablas relacionadas
✅ Consultas SQL complejas con JOINs y agregaciones
✅ Modelos Python elegantes con SQLModel
✅ Validación automática de datos
✅ Documentación interactiva generada automáticamente
✅ CRUD completo con manejo correcto de errores
✅ Un proyecto propio del que puedes estar orgulloso

Eso es exactamente lo que hacen los desarrolladores backend en el mundo real. 🚀

---
---

## 📚 Recursos para seguir aprendiendo

- **SQLModel**: https://sqlmodel.tiangolo.com/
- **FastAPI**: https://fastapi.tiangolo.com/
- **SQLZoo** (práctica SQL): https://sqlzoo.net/
- **DB Fiddle** (SQL en el navegador): https://www.db-fiddle.com/

---

## 🗺️ Cheat Sheet — Referencia rápida

### SQL completo

```sql
-- CRUD
SELECT columnas FROM tabla WHERE cond ORDER BY col DESC LIMIT n;
INSERT INTO tabla (col1, col2) VALUES (val1, val2);
UPDATE tabla SET col = val WHERE id = ?;   -- ¡Siempre WHERE!
DELETE FROM tabla WHERE id = ?;            -- ¡Siempre WHERE!

-- JOINs
SELECT a.col, b.col FROM a INNER JOIN b ON a.fk = b.pk;
SELECT a.col, b.col FROM a LEFT JOIN  b ON a.fk = b.pk;

-- Agregaciones
SELECT col, COUNT(*), SUM(x), AVG(x), MAX(x), MIN(x)
FROM tabla GROUP BY col HAVING COUNT(*) > 1;

-- Orden completo
SELECT FROM JOIN WHERE GROUP BY HAVING ORDER BY LIMIT
```

### SQLModel

```python
class Mi(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    opcional: Optional[str] = None

engine = create_engine("sqlite:///mi.db", connect_args={"check_same_thread": False})
SQLModel.metadata.create_all(engine)

with Session(engine) as s:
    obj = Mi(nombre="x"); s.add(obj); s.commit(); s.refresh(obj)  # CREATE
    obj = s.get(Mi, id)                                             # READ one
    todos = s.exec(select(Mi).where(Mi.nombre == "x")).all()       # READ many
    obj.nombre = "y"; s.add(obj); s.commit()                       # UPDATE
    s.delete(obj); s.commit()                                       # DELETE
```

### FastAPI

```python
app = FastAPI()

@app.get("/items", response_model=List[ItemResponse])
def listar(session: Session = Depends(get_session)):
    return session.exec(select(Item)).all()

@app.get("/items/{id}", response_model=ItemResponse)
def obtener(id: int, session: Session = Depends(get_session)):
    obj = session.get(Item, id)
    if not obj: raise HTTPException(404, "No encontrado")
    return obj

@app.post("/items", response_model=ItemResponse, status_code=201)
def crear(data: ItemCreate, session: Session = Depends(get_session)):
    obj = Item.model_validate(data)
    session.add(obj); session.commit(); session.refresh(obj)
    return obj

@app.put("/items/{id}", response_model=ItemResponse)
def actualizar(id: int, data: ItemUpdate, session: Session = Depends(get_session)):
    obj = session.get(Item, id)
    if not obj: raise HTTPException(404, "No encontrado")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(obj, k, v)
    session.add(obj); session.commit(); session.refresh(obj)
    return obj

@app.delete("/items/{id}")
def eliminar(id: int, session: Session = Depends(get_session)):
    obj = session.get(Item, id)
    if not obj: raise HTTPException(404, "No encontrado")
    session.delete(obj); session.commit()
    return {"ok": True}
```

---

*Curso diseñado para jóvenes programadores de 15-16 años · 22 sesiones · 2 horas cada una*
*Inspirado en la documentación oficial de SQLModel y FastAPI de Sebastián Ramírez*
