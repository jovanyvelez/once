# Taller de Plantillas Jinja2 con FastAPI (versión simplificada)

---

## Requisitos previos

```bash
pip install "fastapi[standard]"
```

Estructura del proyecto:

```
mi_taller/
├── main.py
└── templates/
    ├── base.html
    └── ...
```

---

## 1. Hola mundo: renderizar una plantilla simple

### `main.py`

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/hola")
def hola(request: Request):
    return templates.TemplateResponse(request=request, name="hola.html", context={"nombre": "Mundo"})
```

### `templates/hola.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Hola</title>
</head>
<body>
    <h1>Hola {{ nombre }}</h1>
</body>
</html>
```

> `{{ nombre }}` es una **expresión**: imprime el valor de la variable.

---

## 2. Herencia de plantillas: `base.html` + plantilla hija

### `templates/base.html` (plantilla base)

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>{% block titulo %}Mi Sitio{% endblock %}</title>
</head>
<body>
    <header>
        <h1>{% block encabezado %}Bienvenido{% endblock %}</h1>
    </header>

    <nav>
        <a href="/">Inicio</a> |
        <a href="/productos">Productos</a> |
        <a href="/contacto">Contacto</a>
    </nav>

    <main>
        {% block contenido %}
        <p>Contenido por defecto.</p>
        {% endblock %}
    </main>

    <footer>
        <p>&copy; 2026 Mi Sitio</p>
    </footer>
</body>
</html>
```

### `templates/inicio.html` (plantilla hija)

```html
{% extends "base.html" %}

{% block titulo %}Inicio - Mi Sitio{% endblock %}

{% block encabezado %}Página de Inicio{% endblock %}

{% block contenido %}
    <p>Bienvenido, {{ usuario }}. Esta es la página principal.</p>
{% endblock %}
```

### `main.py`

```python
@app.get("/inicio")
def inicio(request: Request):
    return templates.TemplateResponse(request=request, name="inicio.html", context={"usuario": "Carlos"})
```

> **Reglas de herencia:**
> - `{% extends "base.html" %}` debe ser la **primera línea** de la plantilla hija.
> - `{% block nombre %} ... {% endblock %}` define bloques reemplazables.
> - Un hijo puede omitir un bloque; en ese caso se usa el contenido por defecto de la base.

---

## 3. Decisiones `if` / `elif` / `else`

### `templates/calificacion.html`

```html
{% extends "base.html" %}
{% block titulo %}Calificación{% endblock %}
{% block contenido %}
    <h2>Resultado de {{ estudiante }}</h2>
    <p>Nota: {{ nota }}</p>

    {% if nota >= 90 %}
        <p>Excelente, ¡sigue así!</p>
    {% elif nota >= 75 %}
        <p>Buen trabajo.</p>
    {% elif nota >= 60 %}
        <p>Aprobado, pero puedes mejorar.</p>
    {% else %}
        <p>Reprobado. Necesitas estudiar más.</p>
    {% endif %}
{% endblock %}
```

### `main.py`

```python
@app.get("/calificacion/{nota}")
def calificacion(request: Request, nota: int):
    return templates.TemplateResponse(request=request, name="calificacion.html", context={"estudiante": "María", "nota": nota})
```

> Operadores disponibles: `==`, `!=`, `<`, `>`, `<=`, `>=`, `and`, `or`, `not`, `in`, `is`.

---

## 4. Ciclos `for`

### `templates/lista.html`

```html
{% extends "base.html" %}
{% block titulo %}Lista de Frutas{% endblock %}
{% block contenido %}
    <h2>Frutas disponibles</h2>
    <ul>
    {% for fruta in frutas %}
        <li>{{ fruta }}</li>
    {% endfor %}
    </ul>

    <h2>Tabla de frutas</h2>
    <table border="1">
        <tr><th>#</th><th>Fruta</th><th>Primero</th><th>Último</th></tr>
        {% for fruta in frutas %}
        <tr>
            <td>{{ loop.index }}</td>
            <td>{{ fruta }}</td>
            <td>{{ loop.first }}</td>
            <td>{{ loop.last }}</td>
        </tr>
        {% endfor %}
    </table>
{% endblock %}
```

### `main.py`

```python
@app.get("/frutas")
def frutas(request: Request):
    lista_frutas = ["Manzana", "Pera", "Uva", "Naranja", "Kiwi"]
    return templates.TemplateResponse(request=request, name="lista.html", context={"frutas": lista_frutas})
```

> **Variables especiales dentro de `for`:**
>
> | Variable | Descripción |
> |---|---|
> | `loop.index` | Iteración actual (empieza en 1) |
> | `loop.index0` | Iteración actual (empieza en 0) |
> | `loop.first` | `True` si es la primera iteración |
> | `loop.last` | `True` si es la última iteración |
> | `loop.length` | Cantidad total de elementos |
> | `loop.revindex` | Iteraciones restantes (base 1) |
> | `loop.revindex0` | Iteraciones restantes (base 0) |
> | `loop.cycle("a","b")` | Alterna entre valores en cada iteración |

---

## 5. `for` + `if` combinados

### `templates/estudiantes.html`

```html
{% extends "base.html" %}
{% block titulo %}Estudiantes{% endblock %}
{% block contenido %}
    <h2>Lista de estudiantes</h2>
    <table border="1">
        <tr>
            <th>#</th>
            <th>Nombre</th>
            <th>Nota</th>
            <th>Estado</th>
        </tr>
        {% for estudiante in estudiantes %}
        <tr style="background-color: {{ loop.cycle('#ffffff', '#f0f0f0') }}">
            <td>{{ loop.index }}</td>
            <td>{{ estudiante.nombre }}</td>
            <td>{{ estudiante.nota }}</td>
            <td>
                {% if estudiante.nota >= 60 %}
                    Aprobado
                {% else %}
                    Reprobado
                {% endif %}
            </td>
        </tr>
        {% endfor %}
    </table>

    <p>Total de estudiantes: {{ estudiantes|length }}</p>
{% endblock %}
```

### `main.py`

```python
@app.get("/estudiantes")
def estudiantes(request: Request):
    datos = [
        {"nombre": "Ana", "nota": 85},
        {"nombre": "Luis", "nota": 55},
        {"nombre": "Eva", "nota": 92},
        {"nombre": "Pedro", "nota": 48},
        {"nombre": "Sofía", "nota": 73},
        {"nombre": "Juan", "nota": 60},
    ]
    return templates.TemplateResponse(request=request, name="estudiantes.html", context={"estudiantes": datos})
```

---

## 6. `for`-`else`: qué pasa si la lista está vacía

### `templates/busqueda.html`

```html
{% extends "base.html" %}
{% block titulo %}Búsqueda{% endblock %}
{% block contenido %}
    <h2>Resultados para "{{ termino }}"</h2>

    {% if resultados %}
        <ul>
        {% for item in resultados %}
            <li>{{ item }}</li>
        {% endfor %}
        </ul>
    {% else %}
        <p>No se encontraron resultados.</p>
    {% endif %}

    {# También se puede usar for-else #}
    <h3>Con for-else:</h3>
    {% for item in resultados %}
        <p>{{ item }}</p>
    {% else %}
        <p><em>La lista está vacía.</em></p>
    {% endfor %}
{% endblock %}
```

### `main.py`

```python
@app.get("/buscar/{termino}")
def buscar(request: Request, termino: str):
    base_datos = ["manzana", "pera", "uva", "naranja", "sandía"]
    resultados = [f for f in base_datos if termino.lower() in f]
    return templates.TemplateResponse(request=request, name="busqueda.html", context={"termino": termino, "resultados": resultados})
```

---

## 7. Diccionarios anidados con `for`

### `templates/cursos.html`

```html
{% extends "base.html" %}
{% block titulo %}Cursos{% endblock %}
{% block contenido %}
    <h2>Cursos y estudiantes inscritos</h2>

    {% for curso, alumnos in cursos.items() %}
        <h3>{{ loop.index }}. {{ curso }} ({{ alumnos|length }} estudiantes)</h3>

        {% if alumnos %}
            <ol>
            {% for alumno in alumnos %}
                <li>{{ alumno.nombre }} — {{ alumno.edad }} años</li>
            {% endfor %}
            </ol>
        {% else %}
            <p><em>Sin estudiantes inscritos aún.</em></p>
        {% endif %}

        {% if not loop.last %}<hr>{% endif %}
    {% endfor %}
{% endblock %}
```

### `main.py`

```python
@app.get("/cursos")
def cursos(request: Request):
    datos = {
        "Matemáticas": [
            {"nombre": "Ana", "edad": 16},
            {"nombre": "Luis", "edad": 17},
            {"nombre": "Eva", "edad": 15},
        ],
        "Historia": [
            {"nombre": "Pedro", "edad": 16},
        ],
        "Arte": [],
        "Ciencias": [
            {"nombre": "Sofía", "edad": 17},
            {"nombre": "Juan", "edad": 16},
            {"nombre": "Marta", "edad": 15},
            {"nombre": "Diego", "edad": 17},
        ],
    }
    return templates.TemplateResponse(request=request, name="cursos.html", context={"cursos": datos})
```

---

## 8. Condicionales con operadores lógicos y el filtro `in`

### `templates/permisos.html`

```html
{% extends "base.html" %}
{% block titulo %}Permisos{% endblock %}
{% block contenido %}
    <h2>Panel de {{ usuario }}</h2>
    <p>Rol: {{ rol }}</p>

    {% if rol == "admin" %}
        <p>Tienes acceso total al sistema.</p>
    {% elif rol == "editor" or rol == "moderador" %}
        <p>Puedes editar contenido.</p>
    {% else %}
        <p>Solo puedes ver contenido. Acceso limitado.</p>
    {% endif %}

    <h3>Permisos asignados:</h3>
    <ul>
    {% for permiso in permisos %}
        <li>
            {{ permiso }}
            {% if "eliminar" in permiso %}
                — CUIDADO: este permiso es delicado
            {% endif %}
        </li>
    {% endfor %}
    </ul>

    {% if "admin" in permisos and rol == "admin" %}
        <p><strong>Acceso a configuración del sistema habilitado.</strong></p>
    {% endif %}
{% endblock %}
```

### `main.py`

```python
@app.get("/permisos")
def permisos(request: Request):
    return templates.TemplateResponse(request=request, name="permisos.html", context={
            "usuario": "Carlos",
            "rol": "admin",
            "permisos": ["ver_usuarios", "crear_contenido", "eliminar_contenido", "admin"]})
```

---

## 9. Múltiples hijos de una misma base

Puedes crear tantas plantillas hijas como necesites, todas extendiendo `base.html`:

```
templates/
├── base.html
├── inicio.html
├── calificacion.html
├── lista.html
├── estudiantes.html
├── busqueda.html
├── cursos.html
├── permisos.html
└── ...
```

Cada una define sus propios bloques `titulo`, `encabezado` y `contenido`.

---

## 10. `include`: reutilizar fragmentos sin herencia

### `templates/_tarjeta.html` (fragmento reutilizable)

```html
<div style="border:1px solid #ccc; padding:10px; margin:5px;">
    <h4>{{ titulo_tarjeta }}</h4>
    <p>{{ descripcion }}</p>
</div>
```

### `templates/tarjetas.html`

```html
{% extends "base.html" %}
{% block titulo %}Tarjetas{% endblock %}
{% block contenido %}
    <h2>Productos</h2>

    {% for producto in productos %}
        {% with titulo_tarjeta=producto.nombre, descripcion=producto.precio %}
            {% include "_tarjeta.html" %}
        {% endwith %}
    {% endfor %}
{% endblock %}
```

### `main.py`

```python
@app.get("/tarjetas")
def tarjetas(request: Request):
    productos = [
        {"nombre": "Laptop", "precio": "$800"},
        {"nombre": "Mouse", "precio": "$25"},
        {"nombre": "Teclado", "precio": "$45"},
    ]
    return templates.TemplateResponse(request=request, name="tarjetas.html", context={"productos": productos})
```

---

## 11. Comentarios en Jinja2

```jinja2
{# Esto es un comentario de una línea. No aparece en el HTML renderizado. #}

{#
  Esto es
  un comentario
  multilínea
#}
```

---

## 12. `if` dentro de `for`: filtrar elementos al iterar

### `templates/numeros_pares.html`

```html
{% extends "base.html" %}
{% block titulo %}Números{% endblock %}
{% block contenido %}
    <h2>Números del 1 al 20</h2>

    <ul>
    {% for n in numeros %}
        {% if n % 2 == 0 %}
            <li><strong>{{ n }}</strong> — par</li>
        {% else %}
            <li>{{ n }} — impar</li>
        {% endif %}
    {% endfor %}
    </ul>

    <h3>Resumen</h3>
    {% set pares = [] %}
    {% set impares = [] %}
    {% for n in numeros %}
        {% if n % 2 == 0 %}
            {% set _ = pares.append(n) %}
        {% else %}
            {% set _ = impares.append(n) %}
        {% endif %}
    {% endfor %}
    <p>Pares: {{ pares|join(", ") }} ({{ pares|length }})</p>
    <p>Impares: {{ impares|join(", ") }} ({{ impares|length }})</p>
{% endblock %}
```

### `main.py`

```python
@app.get("/numeros")
def numeros(request: Request):
    return templates.TemplateResponse(request=request, name="numeros_pares.html", context={"numeros": list(range(1, 21))})
```

---

## `main.py` completo de referencia

```python
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates

app = FastAPI()
templates = Jinja2Templates(directory="templates")


@app.get("/hola")
def hola(request: Request):
    return templates.TemplateResponse(request=request, name="hola.html", context={"nombre": "Mundo"})


@app.get("/inicio")
def inicio(request: Request):
    return templates.TemplateResponse(request=request, name="inicio.html", context={"usuario": "Carlos"})


@app.get("/calificacion/{nota}")
def calificacion(request: Request, nota: int):
    return templates.TemplateResponse(request=request, name="calificacion.html", context={"estudiante": "María", "nota": nota})


@app.get("/frutas")
def frutas(request: Request):
    return templates.TemplateResponse(request=request, name="lista.html", context={"frutas": ["Manzana", "Pera", "Uva", "Naranja", "Kiwi"]})


@app.get("/estudiantes")
def estudiantes(request: Request):
    datos = [
        {"nombre": "Ana", "nota": 85},
        {"nombre": "Luis", "nota": 55},
        {"nombre": "Eva", "nota": 92},
        {"nombre": "Pedro", "nota": 48},
        {"nombre": "Sofía", "nota": 73},
        {"nombre": "Juan", "nota": 60},
    ]
    return templates.TemplateResponse(request=request, name="estudiantes.html", context={"estudiantes": datos})


@app.get("/buscar/{termino}")
def buscar(request: Request, termino: str):
    base_datos = ["manzana", "pera", "uva", "naranja", "sandía"]
    resultados = [f for f in base_datos if termino.lower() in f]
    return templates.TemplateResponse(request=request, name="busqueda.html", context={"termino": termino, "resultados": resultados})


@app.get("/cursos")
def cursos(request: Request):
    datos = {
        "Matemáticas": [
            {"nombre": "Ana", "edad": 16},
            {"nombre": "Luis", "edad": 17},
            {"nombre": "Eva", "edad": 15},
        ],
        "Historia": [
            {"nombre": "Pedro", "edad": 16},
        ],
        "Arte": [],
        "Ciencias": [
            {"nombre": "Sofía", "edad": 17},
            {"nombre": "Juan", "edad": 16},
            {"nombre": "Marta", "edad": 15},
            {"nombre": "Diego", "edad": 17},
        ],
    }
    return templates.TemplateResponse(request=request, name="cursos.html", context={"cursos": datos})


@app.get("/permisos")
def permisos(request: Request):
    return templates.TemplateResponse(request=request, name="permisos.html", context={
            "usuario": "Carlos",
            "rol": "admin",
            "permisos": ["ver_usuarios", "crear_contenido", "eliminar_contenido", "admin"]})


@app.get("/tarjetas")
def tarjetas(request: Request):
    productos = [
        {"nombre": "Laptop", "precio": "$800"},
        {"nombre": "Mouse", "precio": "$25"},
        {"nombre": "Teclado", "precio": "$45"},
    ]
    return templates.TemplateResponse(request=request, name="tarjetas.html", context={"productos": productos})


@app.get("/numeros")
def numeros(request: Request):
    return templates.TemplateResponse(request=request, name="numeros_pares.html", context={"numeros": list(range(1, 21))})
```

---

## Ejecución

```bash
uvicorn main:app --reload --port 8000
```

Abre `http://localhost:8000/hola`, `http://localhost:8000/inicio`, etc.

---

# 📝 36 Ejercicios propuestos

Cada ejercicio debe resolverse creando:
1. Una ruta en `main.py` (copia el `main.py` de referencia y añade tus rutas).
2. Una plantilla `.html` en `templates/` que extienda `base.html`.
3. Los datos necesarios (listas, diccionarios, variables) pasados desde la ruta.

**Hay 12 grupos de 3 estudiantes. A cada grupo se le asignan 3 ejercicios (ver tabla al final).**

---

## Bloque A: Herencia de plantillas (ejercicios 1–7)

> **Objetivo:** Practicar `{% extends %}`, `{% block %}`, `base.html`.

| # | Ejercicio |
|---|-----------|
| 1 | Ruta `/perfil` que muestre nombre, edad y hobby de un usuario. La plantilla `perfil.html` debe extender `base.html` y sobrescribir los bloques `titulo`, `encabezado` y `contenido`. |
| 2 | Ruta `/mascota` que muestre el nombre, especie y edad de una mascota. Usa herencia de `base.html`. |
| 3 | Ruta `/libro` que muestre título, autor y año de un libro. Extiende `base.html` y cambia los tres bloques. |
| 4 | Ruta `/pais` que muestre nombre del país, capital e idioma. Usa herencia. |
| 5 | Ruta `/pelicula` que muestre título, director y año. Usa `base.html`. |
| 6 | Ruta `/deporte` que muestre nombre del deporte, cantidad de jugadores por equipo y si usa balón (booleano). Extiende `base.html`. |
| 7 | Ruta `/cancion` que muestre el título, artista y duración en segundos de una canción. Usa herencia. |

---

## Bloque B: `if` / `elif` / `else` (ejercicios 8–15)

> **Objetivo:** Practicar condicionales con variables numéricas, texto y booleanas.

| # | Ejercicio |
|---|-----------|
| 8 | Ruta `/edad/{edad}`. Si la edad < 13: "Niño", < 18: "Adolescente", < 65: "Adulto", si no: "Adulto mayor". Muestra el número y la categoría. |
| 9 | Ruta `/temperatura/{grados}`. Si grados < 10: "Frío", < 25: "Templado", < 35: "Caluroso", si no: "Extremo". |
| 10 | Ruta `/clima/{estado}` (recibe "soleado", "nublado", "lluvioso"). Muestra un mensaje distinto para cada caso con `if/elif/else`. Si no coincide con ninguno, muestra "Estado desconocido". |
| 11 | Ruta `/numero/{n}`. Indica si el número es positivo, negativo o cero. Además indica si es par o impar. Usa dos `if` independientes (no anidados). |
| 12 | Ruta `/hora/{hora}`. Si hora < 12: "Buenos días", si < 19: "Buenas tardes", si no: "Buenas noches". Valida que esté entre 0 y 23; si no, muestra "Hora inválida". |
| 13 | Ruta `/calcular/{a}/{b}/{operacion}`. operacion puede ser "suma", "resta", "multiplicacion", "division". Muestra el resultado y el símbolo. Si es división y b=0, muestra "No se puede dividir entre cero". |
| 14 | Ruta `/acceso/{rol}`. Muestra diferentes secciones del menú según el rol: "admin" ve todo, "editor" ve 3 opciones, "visitante" ve solo 1 opción. Usa `if/elif/else` para mostrar listas distintas. |
| 15 | Ruta `/nota/{puntaje}`. 90-100: "A", 80-89: "B", 70-79: "C", 60-69: "D", <60: "F". Muestra la letra y un mensaje distinto para cada rango. Valida que esté entre 0 y 100. |

---

## Bloque C: Ciclos `for` con listas simples (ejercicios 16–21)

> **Objetivo:** Practicar `{% for item in lista %}` con datos planos.

| # | Ejercicio |
|---|-----------|
| 16 | Ruta `/dias`. Pasa una lista con los 7 días de la semana. Muestra cada día en una lista `<ul>` numerada usando `loop.index`. |
| 17 | Ruta `/colores`. Pasa una lista de 6 colores. Muestra cada uno en un `<div>` con ese color de fondo (usa el atributo `style`). Usa `loop.cycle()` para alternar entre dos tonos de borde. |
| 18 | Ruta `/planetas`. Pasa una lista con los 8 planetas del sistema solar. Resalta con `<strong>` el primero y el último usando `loop.first` y `loop.last`. |
| 19 | Ruta `/animales`. Pasa una lista de 10 animales. Ordénalos alfabéticamente con `|sort` antes de mostrarlos con un `for`. |
| 20 | Ruta `/tareas`. Pasa una lista de 8 tareas. Muestra el número de iteración inverso (`loop.revindex`) junto a cada tarea. Debajo muestra el total con `loop.length`. |
| 21 | Ruta `/vocales/{frase}`. Recibe una frase por URL. En la ruta Python, convierte la frase en una lista de sus letras. En la plantilla recorre la lista con `for` y resalta con `<strong>` solo las vocales (`a,e,i,o,u`) usando un `if` dentro del `for`. |

---

## Bloque D: Ciclos `for` con listas de diccionarios (ejercicios 22–27)

> **Objetivo:** Practicar iteración sobre estructuras compuestas (lista de dicts).

| # | Ejercicio |
|---|-----------|
| 22 | Ruta `/empleados`. Pasa una lista de 5 empleados con `nombre`, `cargo` y `salario`. Muestra una tabla con columnas: #, Nombre, Cargo, Salario. Usa `loop.index` para la numeración. |
| 23 | Ruta `/productos`. Pasa una lista de 6 productos con `nombre`, `precio` y `stock`. Muestra en una tabla y resalta en rojo las filas donde `stock == 0` usando `if` y el atributo `style`. |
| 24 | Ruta `/ciudades`. Pasa una lista de 5 ciudades con `nombre`, `pais` y `poblacion`. Clasifica cada ciudad como "Grande" (>5M habitantes), "Mediana" (>1M) o "Pequeña" usando `if/elif/else` dentro del `for`. |
| 25 | Ruta `/equipo`. Pasa una lista de 6 jugadores con `nombre`, `posicion` y `goles`. Muestra una tabla con `loop.index`. Al final, calcula y muestra el total de goles desde Python (suma en la ruta). |
| 26 | Ruta `/recetas`. Pasa una lista de 4 recetas con `nombre`, `dificultad` ("fácil", "media", "difícil") y `tiempo` en minutos. Muestra cada receta con color de fondo distinto según dificultad usando `if/elif` dentro del `for`. |
| 27 | Ruta `/paises`. Pasa una lista de 8 países con `nombre`, `continente`, y `idioma`. Agrúpalos visualmente por continente dentro del mismo `for`, mostrando un subtítulo cada vez que cambia el continente (usa `if` comparando con el valor de la iteración anterior mediante `{% set %}`). |

---

## Bloque E: Diccionarios anidados y `for` con `.items()` (ejercicios 28–30)

> **Objetivo:** Iterar sobre diccionarios con `{% for clave, valor in dict.items() %}`.

| # | Ejercicio |
|---|-----------|
| 28 | Ruta `/asignaturas`. Pasa un diccionario donde la clave es el nombre de una asignatura y el valor es una lista de 3 temas. Muestra: "Asignatura: Matemáticas → Temas: Álgebra, Geometría, Cálculo". Usa `for` anidado. |
| 29 | Ruta `/equipos`. Pasa un diccionario donde la clave es el nombre de un equipo deportivo y el valor es una lista con los nombres de sus 5 jugadores titulares. Muestra cada equipo como una sección con su lista numerada de jugadores. |
| 30 | Ruta `/categorias`. Pasa un diccionario donde la clave es una categoría de producto ("Electrónica", "Ropa", "Alimentos") y el valor es una lista de diccionarios con `producto` y `precio`. Muestra cada categoría con su tabla de productos. Si una categoría no tiene productos, muestra "Sin stock". |

---

## Bloque F: `for`-`else` y listas vacías (ejercicios 31–33)

> **Objetivo:** Usar `{% for %}...{% else %}...{% endfor %}` y manejar casos vacíos.

| # | Ejercicio |
|---|-----------|
| 31 | Ruta `/buscar_alumno/{nombre}`. Ten una lista fija de 6 alumnos (lista de strings). Si el nombre buscado existe (coincidencia exacta), muestra los datos del alumno. Si no, muestra "Alumno no encontrado" con `for-else`. |
| 32 | Ruta `/inscritos/{curso}`. Define un diccionario con 4 cursos y sus listas de estudiantes. Si el curso existe y tiene estudiantes, muéstralos. Si el curso no existe, muestra "Curso no encontrado". Si existe pero no tiene estudiantes, muestra "Sin inscritos" con `for-else`. |
| 33 | Ruta `/pendientes`. Pasa una lista de tareas, donde cada tarea es un dict con `descripcion` y `completada` (bool). Muestra en una sección las pendientes y en otra las completadas (filtra con `if` dentro del `for`). Si alguna sección queda vacía, muestra "No hay pendientes" o "No hay completadas" usando `for-else`. |

---

## Bloque G: `include` y comentarios (ejercicios 34–36)

> **Objetivo:** Usar `{% include %}`, `{% with %}` y `{# comentarios #}`.

| # | Ejercicio |
|---|-----------|
| 34 | Ruta `/personas`. Crea un fragmento `_ficha.html` que muestre nombre y edad. En la plantilla principal `personas.html` recorre una lista de 4 personas e incluye el fragmento con `{% include %}` y `{% with %}` para pasarle las variables de cada persona. |
| 35 | Ruta `/servicios`. Crea un fragmento `_servicio.html` que reciba `nombre` y `activo` (bool). En la plantilla principal recorre una lista de 5 servicios. Dentro del fragmento usa `if` para mostrar "(Disponible)" o "(No disponible)" según `activo`. Usa `{% include %}` dentro del `for`. |
| 36 | Ruta `/comentada`. Crea una plantilla que use comentarios `{# #}` de una y múltiples líneas explicando qué hace cada parte del código. La plantilla debe mostrar datos normales (nombre, lista de hobbies) pero con comentarios que documenten cada bloque `if`, `for` y cada variable. |

---

## 📋 Asignación de ejercicios por grupo

| Grupo | Integrantes | Ejercicio 1 | Ejercicio 2 | Ejercicio 3 |
|-------|-------------|:-----------:|:-----------:|:-----------:|
| **1** | Estudiante 1A, 1B, 1C | 1 | 13 | 25 |
| **2** | Estudiante 2A, 2B, 2C | 2 | 14 | 26 |
| **3** | Estudiante 3A, 3B, 3C | 3 | 15 | 27 |
| **4** | Estudiante 4A, 4B, 4C | 4 | 16 | 28 |
| **5** | Estudiante 5A, 5B, 5C | 5 | 17 | 29 |
| **6** | Estudiante 6A, 6B, 6C | 6 | 18 | 30 |
| **7** | Estudiante 7A, 7B, 7C | 7 | 19 | 31 |
| **8** | Estudiante 8A, 8B, 8C | 8 | 20 | 32 |
| **9** | Estudiante 9A, 9B, 9C | 9 | 21 | 33 |
| **10** | Estudiante 10A, 10B, 10C | 10 | 22 | 34 |
| **11** | Estudiante 11A, 11B, 11C | 11 | 23 | 35 |
| **12** | Estudiante 12A, 12B, 12C | 12 | 24 | 36 |

> Cada grupo recibe **3 ejercicios**, uno de un bloque distinto, para cubrir diferentes temas.

---

## ⚠️ Reglas para el taller

1. Cada grupo resuelve únicamente los 3 ejercicios asignados.
2. Todos los ejercicios deben extender `base.html`.
3. La ruta de FastAPI debe llamar a la plantilla con `templates.TemplateResponse`.
4. Los datos deben pasarse desde Python (no hardcodearlos en el HTML).
5. Entrega por grupo: archivo `.py` con las 3 rutas + 3 archivos `.html` (o más si usan `include`).
6. El profesor verificará que cada grupo entregue ejercicios distintos.

---

*Taller generado para aprendizaje progresivo de Jinja2 + FastAPI — 12 grupos × 3 ejercicios.*
