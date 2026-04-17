# FastAPI + Jinja2: Mini Curso Completo (4 Horas)

**Duración:** 4 horas (240 minutos)
**Nivel:** Principiante (adolescentes 15-17 años)
**Requisitos:** Conocer lo básico de Python (variables, funciones, listas, diccionarios)

---

## Tabla de Contenidos

1. [Bienvenida y Objetivos](#1-bienvenida-y-objetivos)
2. [Fundamentos de FastAPI](#2-fundamentos-de-fastapi)
3. [Rutas y Parámetros](#3-rutas-y-parámetros)
4. [Parámetros de Query](#4-parámetros-de-query)
5. [Introducción a Jinja2](#5-introducción-a-jinja2)
6. [Herencia de Plantillas](#6-herencia-de-plantillas)
7. [Integración FastAPI + Jinja2](#7-integración-fastapi-jinja2)
8. [Proyecto Final: Sistema de Preguntas y Respuestas](#8-proyecto-final-sistema-de-preguntas-y-respuestas)
9. [Evaluación de Conocimientos](#9-evaluación-de-conocimientos)

---

## 1. Bienvenida y Objetivos

### 🎯 ¿Qué vas a aprender en 4 horas?

| Hora | Tema | Al terminar podrás |
|------|------|-------------------|
| **Hora 1** | Fundamentos de FastAPI | Crear tu primera API y entender el flujo request-response |
| **Hora 2** | Rutas y Parámetros | Crear rutas dinámicas con path y query parameters |
| **Hora 3** | Jinja2 | Crear plantillas HTML con variables y lógica |
| **Hora 4** | Integración + Proyecto | Combinar FastAPI + Jinja2 en una app real |

### 🎯 El Proyecto Final

Construirás un **Sistema de Preguntas y Respuestas** donde:
- Los usuarios envían preguntas via formulario
- La "máquina mágica" responde con frases aleatorias
- Se muestra un historial de todas las preguntas
- Todo con interfaz web bonita usando CSS

---

## 2. Fundamentos de FastAPI

### 2.1 ¿Qué es FastAPI?

**FastAPI** es un framework web moderno para construir APIs con Python. Es rápido, fácil de aprender y genera documentación automática.

**Analogía del Restaurante:**

```
🍽️ CLIENTE (tú, en el navegador)
         │
         │  "¡Quiero una pizza!"
         ▼
┌──────────────────────────────────────┐
│  COCINA (FastAPI)                    │
│                                      │
│  1. Recibe tu pedido (request)       │
│  2. Lo procesa (código Python)       │
│  3. Prepara la respuesta             │
│  4. Te lo entrega (response)         │
└──────────────────────────────────────┘
         │
         │  "¡Aquí está tu pizza! 🍕"
         ▼
      CLIENTE
```

### 2.2 Instalación

```bash
# Instalar FastAPI con todas las herramientas incluidas
pip install "fastapi[standard]"
```

**¿Qué incluye `fastapi[standard]`?**

| Herramienta | Qué hace |
|-------------|----------|
| **FastAPI** | El framework principal |
| **httpx** | Cliente HTTP para pruebas |
| **uvicorn** | Servidor de desarrollo |
| **jinja2** | Motor de plantillas HTML |
| **python-multipart** | Procesamiento de formularios |

### 2.3 Tu primera API

Crea `main.py`:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def hola_mundo():
    return {"mensaje": "¡Hola Mundo!", "status": "funcionando"}
```

**Ejecutar el servidor:**

```bash
fastapi dev
```

**Probar tu API:**
- http://127.0.0.1:8000 → JSON de respuesta
- http://127.0.0.1:8000/docs → Documentación interactiva (¡gratis!)

### 2.4 Estructura del proyecto

```
mi_proyecto/
├── main.py              # Todo tu código Python
├── templates/            # Archivos HTML (Jinja2)
│   └── .html
└── static/              # CSS, imágenes
    └── style.css
```

### 📝 Ejercicio 2.1 (10 min)

1. Crea una carpeta `mi_primera_api`
2. Crea el archivo `main.py` con el código de arriba
3. Ejecuta `fastapi dev`
4. Abre http://127.0.0.1:8000/docs
5. Modifica el mensaje a tu gusto y actualiza

### 2.5 ¿GET vs POST?

| Método | Uso | Cuándo usar |
|--------|-----|-------------|
| **GET** | Leer información | Buscar, ver datos |
| **POST** | Enviar información nueva | Crear, enviar formularios |

---

## 3. Rutas y Parámetros

### 3.1 ¿Qué es una ruta?

Una **ruta** es una URL que el servidor "escucha". Cuando un usuario visita esa URL, FastAPI ejecuta la función correspondiente.

```
/                      → página de inicio
/saludo/Carlos         → saludo personalizado
/blog/2026/04/17       → entrada de blog de una fecha
```

### 3.2 Parámetros de Path (parámetros en la URL)

Los **parámetros de path** van dentro de las llaves `{ }` en la URL:

```python
@app.get("/saludo/{nombre}")
def saludar(nombre: str):
    return {"mensaje": f"¡Hola {nombre}!"}
```

**Prueba:**
- http://127.0.0.1:8000/saludo/Carlos
- http://127.0.0.1:8000/saludo/María

### 3.3 Múltiples parámetros de path

```python
@app.get("/calculadora/{num1}/{operacion}/{num2}")
def calculadora(num1: float, operacion: str, num2: float):
    if operacion == "suma":
        resultado = num1 + num2
    elif operacion == "resta":
        resultado = num1 - num2
    elif operacion == "multiplicacion":
        resultado = num1 * num2
    elif operacion == "division":
        if num2 == 0:
            return {"error": "No se puede dividir entre cero"}
        resultado = num1 / num2
    else:
        return {"error": "Operación no válida. Use: suma, resta, multiplicacion, division"}

    return {
        "num1": num1,
        "operacion": operacion,
        "num2": num2,
        "resultado": resultado
    }
```

**Prueba:**
- http://127.0.0.1:8000/calculadora/10/suma/5
- http://127.0.0.1:8000/calculadora/25/multiplicacion/4
- http://127.0.0.1:8000/calculadora/10/division/0

### 3.4 Parámetros de path con tipos específicos

Puedes especificar el tipo del parámetro:

```python
@app.get("/usuarios/{user_id}")
def get_usuario(user_id: int):
    return {"user_id": user_id, "tipo": type(user_id).__name__}
```

Si escribes `/usuarios/abc`, FastAPI devolverá error 422 porque `abc` no es un entero.

### 3.5 Parámetros opcionales y valores por defecto

```python
@app.get("/saludo/{nombre}")
def saludar(nombre: str, exclamar: bool = True):
    mensaje = f"¡Hola {nombre}!"
    if exclamar:
        mensaje += " 🎉"
    return {"mensaje": mensaje}
```

**Prueba:**
- http://127.0.0.1:8000/saludo/Carlos?exclamar=true
- http://127.0.0.1:8000/saludo/María?exclamar=false

### 📝 Ejercicio 3.1 (15 min)

**Crea una ruta `/perro/{edad_humana}`** que convierta edad humana a edad de perro:

```
Reglas:
- Primeros 2 años humanos: 10.5 años de perro por año
- Años siguientes: 4 años de perro por año

Ejemplo: 3 años humanos = 2*10.5 + 1*4 = 25 años de perro
```

**Prueba:**
- http://127.0.0.1:8000/perro/3
- http://127.0.0.1:8000/perro/10

<details>
<summary>💡 ¿Necesitas ayuda?</summary>

```python
@app.get("/perro/{edad_humana}")
def edad_perro(edad_humana: int):
    if edad_humana <= 0:
        return {"error": "La edad debe ser positiva"}

    if edad_humana <= 2:
        edad_perro = edad_humana * 10.5
    else:
        edad_perro = 2 * 10.5 + (edad_humana - 2) * 4

    return {
        "edad_humana": edad_humana,
        "edad_perro": edad_perro
    }
```

</details>

---

## 4. Parámetros de Query

### 4.1 ¿Qué son los parámetros de query?

Los **parámetros de query** van después del `?` en la URL:

```
/buscar?q=python&orden=reciente
/buscar?q=fastapi&pagina=2
```

Se definen como **parámetros de función** (no dentro de la ruta):

```python
@app.get("/buscar")
def buscar(q: str, orden: str = "reciente"):
    return {"busqueda": q, "orden": orden, "resultados": []}
```

**Prueba:**
- http://127.0.0.1:8000/buscar?q=python
- http://127.0.0.1:8000/buscar?q=fastapi&orden=popular

### 4.2 Parámetros opcionales

Todos los parámetros de query son opcionales si tienen valor por defecto:

```python
@app.get("/productos")
def listar_productos(
    categoria: str = None,
    precio_min: float = None,
    precio_max: float = None,
    disponibles: bool = True
):
    filtros = []
    if categoria:
        filtros.append(f"Categoría: {categoria}")
    if precio_min:
        filtros.append(f"Precio mínimo: ${precio_min}")
    if precio_max:
        filtros.append(f"Precio máximo: ${precio_max}")
    filtros.append(f"Solo disponibles: {disponibles}")

    return {"filtros": filtros}
```

**Prueba:**
- http://127.0.0.1:8000/productos
- http://127.0.0.1:8000/productos?categoria=electronica&precio_min=100

### 4.3 Conversión automática de tipos

FastAPI convierte automáticamente los valores de query:

```python
@app.get("/calcular")
def calcular(x: int, y: int, operacion: str = "suma"):
    if operacion == "suma":
        resultado = x + y
    elif operacion == "resta":
        resultado = x - y
    elif operacion == "multiplicacion":
        resultado = x * y
    else:
        return {"error": "Operación no válida"}

    return {"x": x, "y": y, "operacion": operacion, "resultado": resultado}
```

**Prueba:**
- http://127.0.0.1:8000/calcular?x=10&y=5&operacion=suma
- http://127.0.0.1:8000/calcular?x=10&y=5&operacion=multiplicacion

### 4.4 Parámetros de query obligatorios

Si un parámetro no tiene valor por defecto, es **obligatorio**:

```python
@app.get("/saludar")
def saludar(nombre: str):  # nombre es obligatorio
    return {"mensaje": f"¡Hola {nombre}!"}
```

Si llamas `/saludar` sin `?nombre=...`, obtendrás error 422.

### 📝 Ejercicio 4.1 (15 min)

**Crea una ruta `/filtrar_numeros`** que reciba una lista de números y permetros:

```
Parámetros:
- numeros: list[int] (query params separados por coma)
- criterio: str = "todos" (todos, pares, impares)

Ejemplos:
/filtrar_numeros?numeros=1,2,3,4,5&criterio=pares
/filtrar_numeros?numeros=10,15,20,25&criterio=impares
```

<details>
<summary>💡 ¿Necesitas ayuda?</summary>

```python
from typing import List

@app.get("/filtrar_numeros")
def filtrar_numeros(
    numeros: str,  # Se recibe como string "1,2,3,4,5"
    criterio: str = "todos"
):
    # Convertir string a lista de enteros
    lista = [int(n.strip()) for n in numeros.split(",")]

    if criterio == "pares":
        resultado = [n for n in lista if n % 2 == 0]
    elif criterio == "impares":
        resultado = [n for n in lista if n % 2 != 0]
    else:
        resultado = lista

    return {
        "original": lista,
        "criterio": criterio,
        "resultado": resultado
    }
```

</details>

### 4.5 Combinando path y query parameters

```python
@app.get("/usuarios/{user_id}/posts")
def get_posts_usuario(
    user_id: int,
    publicado: bool = True,
    limite: int = 10
):
    return {
        "user_id": user_id,
        "publicado": publicado,
        "limite": limite,
        "posts": []
    }
```

**Prueba:**
- http://127.0.0.1:8000/usuarios/1/posts
- http://127.0.0.1:8000/usuarios/1/posts?publicado=false&limite=5

---

## 5. Introducción a Jinja2

### 5.1 ¿Qué es Jinja2?

**Jinja2** es un motor de plantillas (template engine). Permite crear archivos HTML dinámicos donde puedes:
- Insertar variables: `{{ variable }}`
- Usar lógica: `{% if %}`, `{% for %}`
- Heredar plantillas: `{% extends %}`

**Analogía:** Es como un procesador de texto inteligente:

```html
<!-- plantilla.html -->
<h1>Hola, {{ nombre }}!</h1>
<p>Tienes {{ edad }} años.</p>
```

Se convierte en:
```html
<h1>Hola, Carlos!</h1>
<p>Tienes 16 años.</p>
```

### 5.2 Configuración inicial

**Estructura de carpetas:**

```bash
mkdir -p templates static
touch main.py
```

**Archivo `main.py`:**

```python
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

# Montar archivos estáticos (CSS, imágenes)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar Jinja2
templates = Jinja2Templates(directory="templates")
```

### 5.3 Variables en plantillas

Crea `templates/saludo.html`:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>{{ titulo }}</title>
</head>
<body>
    <h1>{{ mensaje }}</h1>
    <p>Bienvenido, {{ nombre }}!</p>
    <p>Tienes {{ edad }} años.</p>
</body>
</html>
```

**Ruta en `main.py`:**

```python
@app.get("/saludo", response_class=HTMLResponse)
async def saludo(request: Request):
    return templates.TemplateResponse(
        "saludo.html",
        {
            "request": request,
            "titulo": "Saludo Personalizado",
            "mensaje": "¡Hola desde FastAPI!",
            "nombre": "Carlos",
            "edad": 16
        }
    )
```

### 5.4 Estructuras de control: if / for

**Crea `templates/lista.html`:**

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Lista de Productos</title>
</head>
<body>
    <h1>🛒 {{ titulo }}</h1>

    {% if productos %}
        <p>Tenemos {{ productos|length }} productos:</p>
        <ul>
        {% for producto in productos %}
            <li>
                <strong>{{ producto.nombre }}</strong>
                - ${{ producto.precio }}
                {% if producto.en_stock %}
                    <span class="disponible">✓ Disponible</span>
                {% else %}
                    <span class="agotado">✗ Agotado</span>
                {% endif %}
            </li>
        {% endfor %}
        </ul>
    {% else %}
        <p>😢 No hay productos disponibles.</p>
    {% endif %}
</body>
</html>
```

**Ruta en `main.py`:**

```python
@app.get("/productos", response_class=HTMLResponse)
async def lista_productos(request: Request):
    productos = [
        {"nombre": "Cuaderno", "precio": 15000, "en_stock": True},
        {"nombre": "Lápiz", "precio": 2000, "en_stock": True},
        {"nombre": "Borrador", "precio": 1000, "en_stock": False},
    ]
    return templates.TemplateResponse(
        "lista.html",
        {"request": request, "titulo": "Mis Productos", "productos": productos}
    )
```

### 5.5 Filtros de Jinja2

Los **filtros** transforman el valor de una variable:

| Filtro | Descripción | Ejemplo |
|--------|-------------|---------|
| `upper` | Mayúsculas | `{{ nombre\|upper }}` |
| `lower` | Minúsculas | `{{ nombre\|lower }}` |
| `length` | Cantidad de elementos | `{{ lista\|length }}` |
| `default` | Valor por defecto | `{{ valor\|default("N/A") }}` |
| `sort` | Ordenar lista | `{{ numeros\|sort }}` |

```html
<p>Tu nombre en mayúsculas: {{ nombre|upper }}</p>
<p>Cantidad de productos: {{ productos|length }}</p>
<p>Precio formateado: ${{ precio|default(0) }}</p>
```

### 5.6 Comentarios en Jinja2

```html
{# Esto es un comentario que no aparece en el HTML #}
<h1>{{ titulo }}</h1>
```

### 📝 Ejercicio 5.1 (20 min)

**Crea una página de perfil de estudiante:**

1. Crea `templates/perfil.html` que muestre:
   - Nombre del estudiante (variable `nombre`)
   - Edad (variable `edad`)
   - Lista de materias (variable `materias`)
   - Promedio general (variable `promedio`)
   - Si el promedio >= 4.0: mostrar "⭐ Destacado"
   - Si no: mostrar "📚 En mejora"

2. Crea la ruta `/perfil/{nombre}` que muestre el perfil

3. Agrega CSS básico en `static/style.css`

<details>
<summary>💡 Solución básica</summary>

```python
# main.py
@app.get("/perfil/{nombre}", response_class=HTMLResponse)
async def perfil(request: Request, nombre: str):
    datos = {
        "Ana": {"edad": 16, "materias": ["Matemáticas", "Física"], "promedio": 4.5},
        "Carlos": {"edad": 17, "materias": ["Historia", "Arte"], "promedio": 3.8},
    }
    info = datos.get(nombre, {"edad": 0, "materias": [], "promedio": 0})

    return templates.TemplateResponse(
        "perfil.html",
        {
            "request": request,
            "nombre": nombre,
            "edad": info["edad"],
            "materias": info["materias"],
            "promedio": info["promedio"]
        }
    )
```

</details>

---

## 6. Herencia de Plantillas

### 6.1 ¿Por qué usar herencia?

La **herencia de plantillas** permite crear una plantilla "base" con la estructura común y que otras plantillas hereden y personalicen solo partes específicas.

**Analogía:** Es como un molde de galletas. El molde define la forma general, y cada galleta puede tener un glaseado diferente.

### 6.2 La plantilla base (layout)

Crea `templates/base.html`:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block titulo %}Mi App{% endblock %}</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <header>
        <nav>
            <a href="/">🏠 Inicio</a>
            <a href="/productos">🛒 Productos</a>
            <a href="/acerca">ℹ️ Acerca</a>
        </nav>
    </header>

    <main>
        {% block contenido %}
        {# Este contenido será reemplazado por las páginas que hereden #}
        {% endblock %}
    </main>

    <footer>
        <p>Hecho con 💜 - {{ ano_actual }}</p>
    </footer>
</body>
</html>
```

### 6.3 Extender la plantilla base

Crea `templates/inicio.html`:

```html
{% extends "base.html" %}

{% block titulo %}Inicio - Mi App{% endblock %}

{% block contenido %}
<div class="hero">
    <h1>🎉 ¡Bienvenido!</h1>
    <p>Esta es la página de inicio de mi aplicación.</p>
</div>

<div class="features">
    <div class="card">
        <h3>🚀 Rápido</h3>
        <p>Construido con FastAPI</p>
    </div>
    <div class="card">
        <h3>🎨 Bonito</h3>
        <p>Diseños con CSS moderno</p>
    </div>
    <div class="card">
        <h3>📱 Responsive</h3>
        <p>Funciona en todos los dispositivos</p>
    </div>
</div>
{% endblock %}
```

### 6.4 La plantilla de productos

Crea `templates/productos.html`:

```html
{% extends "base.html" %}

{% block titulo %}Productos - Mi App{% endblock %}

{% block contenido %}
<h1>🛒 Mis Productos</h1>

{% if productos %}
    <div class="productos-grid">
    {% for producto in productos %}
        <div class="producto-card">
            <h2>{{ producto.nombre }}</h2>
            <p class="precio">${{ producto.precio }}</p>
            <p class="descripcion">{{ producto.descripcion }}</p>
        </div>
    {% endfor %}
    </div>
{% else %}
    <p>No hay productos disponibles.</p>
{% endif %}
{% endblock %}
```

### 6.5 Actualizar main.py

```python
from datetime import datetime

@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    return templates.TemplateResponse(
        "inicio.html",
        {"request": request, "ano_actual": datetime.now().year}
    )

@app.get("/productos", response_class=HTMLResponse)
async def productos(request: Request):
    productos = [
        {"nombre": "Laptop", "precio": 2500000, "descripcion": "Para programación"},
        {"nombre": "Mouse", "precio": 85000, "descripcion": " inalámbrico"},
    ]
    return templates.TemplateResponse(
        "productos.html",
        {"request": request, "productos": productos, "ano_actual": datetime.now().year}
    )

@app.get("/acerca", response_class=HTMLResponse)
async def acerca(request: Request):
    return templates.TemplateResponse(
        "acerca.html",
        {"request": request, "ano_actual": datetime.now().year}
    )
```

### 6.6 El archivo CSS base

Crea `static/style.css`:

```css
/* Reset y variables */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, sans-serif;
    line-height: 1.6;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
}

/* Header */
header {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem 2rem;
    color: white;
}

header nav a {
    color: white;
    text-decoration: none;
    margin-right: 1.5rem;
    padding: 0.5rem 1rem;
    border-radius: 5px;
}

header nav a:hover {
    background: rgba(255,255,255,0.2);
}

/* Main */
main {
    flex: 1;
    max-width: 800px;
    margin: 2rem auto;
    padding: 0 1rem;
}

/* Footer */
footer {
    background: #333;
    color: white;
    text-align: center;
    padding: 1rem;
    margin-top: auto;
}

/* Cards */
.card, .producto-card {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    margin-bottom: 1rem;
}
```

### 📝 Ejercicio 6.1 (20 min)

**Crea una página "Acerca de" y una página de contacto:**

1. Crea `templates/acerca.html` que extienda `base.html`
2. Incluye información sobre ti y sobre la app
3. Crea `templates/contacto.html` con un formulario de contacto
4. Agrega las rutas en `main.py`

---

## 7. Integración FastAPI + Jinja2

### 7.1 Formularios con POST

El verdadero poder de FastAPI + Jinja2 es procesar formularios. Vamos a crear el sistema de preguntas.

**Crea `templates/formulario.html`:**

```html
{% extends "base.html" %}

{% block titulo %}Pregunta Mágica{% endblock %}

{% block contenido %}
<div class="pregunta-container">
    <h1>🔮 Pregunta a la Máquina Mágica</h1>
    <p>Escribe tu pregunta y la máquina te dará una respuesta misteriosa...</p>

    <form action="/procesar_pregunta" method="POST" class="form-magico">
        <label for="nombre">Tu nombre:</label>
        <input type="text" name="nombre" required placeholder="¿Cómo te llamas?">

        <label for="pregunta">Tu pregunta:</label>
        <textarea name="pregunta" required placeholder="¿Qué quieres saber?"></textarea>

        <button type="submit" class="btn-magico">🎲 Preguntar</button>
    </form>

    <div class="historial">
        <h2>📜 Historial de Preguntas</h2>
        <a href="/historial" class="btn">Ver todas las preguntas →</a>
    </div>
</div>
{% endblock %}
```

### 7.2 Procesar el formulario

Agrega en `main.py`:

```python
from fastapi import Form
from fastapi.responses import RedirectResponse

# Base de datos simulada (en memoria)
preguntas_db = []

@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    return templates.TemplateResponse(
        "formulario.html",
        {"request": request}
    )

@app.post("/procesar_pregunta")
async def procesar_pregunta(
    nombre: str = Form(...),
    pregunta: str = Form(...)
):
    # Respuestas mágicas aleatorias
    respuestas = [
        "¡Sí, definitivamente! 🔮",
        "No lo creo... 🤔",
        "Pregunta de nuevo mañana 🌙",
        "¡Absolutamente sí! ✨",
        "Las estrellas dicen que no... ⭐",
        "¡Tal vez! Eso depende de ti 🎯",
        "Lo más probable es que sí 🎲",
        "Solo el tiempo lo dirá ⏳"
    ]

    import random
    respuesta = random.choice(respuestas)

    # Guardar en base de datos simulada
    preguntas_db.append({
        "nombre": nombre,
        "pregunta": pregunta,
        "respuesta": respuesta
    })

    return RedirectResponse(url="/respuesta_magica", status_code=303)
```

### 7.3 Mostrar resultado (página de respuesta individual)

Crea `templates/respuesta_magica.html`:

```html
{% extends "base.html" %}

{% block titulo %}Respuesta Mágica{% endblock %}

{% block contenido %}
<div class="respuesta-container">
    <h1>✨ ¡Tu pregunta fue procesada!</h1>

    <div class="pregunta-box">
        <p class="etiqueta">{{ nombre }} preguntó:</p>
        <p class="pregunta">"{{ pregunta }}"</p>
    </div>

    <div class="respuesta-box">
        <p class="etiqueta">La máquina mágica responde:</p>
        <p class="respuesta">{{ respuesta }}</p>
    </div>

    <div class="acciones">
        <a href="/" class="btn">← Hacer otra pregunta</a>
        <a href="/historial" class="btn">📜 Ver historial</a>
    </div>
</div>
{% endblock %}
```

Agrega la ruta:

```python
@app.get("/respuesta_magica", response_class=HTMLResponse)
async def respuesta_magica(request: Request):
    # Obtener la última pregunta
    if preguntas_db:
        ultima = preguntas_db[-1]
    else:
        ultima = {"nombre": "", "pregunta": "", "respuesta": ""}

    return templates.TemplateResponse(
        "respuesta_magica.html",
        {
            "request": request,
            "nombre": ultima["nombre"],
            "pregunta": ultima["pregunta"],
            "respuesta": ultima["respuesta"]
        }
    )
```

### 7.4 Página de historial

Crea `templates/historial.html`:

```html
{% extends "base.html" %}

{% block titulo %}Historial de Preguntas{% endblock %}

{% block contenido %}
<h1>📜 Todas las Preguntas Mágicas</h1>

{% if preguntas %}
    <p class="contador">Total de preguntas: {{ preguntas|length }}</p>

    <div class="preguntas-lista">
    {% for item in preguntas %}
        <div class="pregunta-item">
            <div class="pregunta-header">
                <strong>{{ item.nombre }}</strong>
                <span class="numero">#{{ loop.index }}</span>
            </div>
            <div class="pregunta-texto">
                <em>"{{ item.pregunta }}"</em>
            </div>
            <div class="respuesta-texto">
                💬 {{ item.respuesta }}
            </div>
        </div>
    {% endfor %}
    </div>
{% else %}
    <div class="vacio">
        <p>😢 No hay preguntas aún.</p>
        <a href="/" class="btn">¡Sé el primero en preguntar!</a>
    </div>
{% endif %}
{% endblock %}
```

Agrega la ruta:

```python
@app.get("/historial", response_class=HTMLResponse)
async def historial(request: Request):
    return templates.TemplateResponse(
        "historial.html",
        {"request": request, "preguntas": preguntas_db}
    )
```

### 7.5 CSS para el formulario

Agrega a `static/style.css`:

```css
/* Formulario mágico */
.form-magico {
    background: white;
    padding: 2rem;
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

.form-magico label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: bold;
    color: #555;
}

.form-magico input,
.form-magico textarea {
    width: 100%;
    padding: 1rem;
    margin-bottom: 1rem;
    border: 2px solid #ddd;
    border-radius: 8px;
    font-size: 1rem;
    font-family: inherit;
}

.form-magico input:focus,
.form-magico textarea:focus {
    outline: none;
    border-color: #667eea;
}

.btn-magico {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 1rem 2rem;
    border: none;
    border-radius: 8px;
    font-size: 1.1rem;
    cursor: pointer;
    width: 100%;
    transition: transform 0.2s;
}

.btn-magico:hover {
    transform: translateY(-3px);
}

/* Preguntas */
.pregunta-container, .respuesta-container {
    text-align: center;
}

.pregunta-box, .respuesta-box {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    margin: 1rem 0;
    text-align: left;
}

.etiqueta {
    color: #888;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}

.pregunta-texto {
    font-size: 1.2rem;
    color: #333;
}

.respuesta-texto {
    color: #667eea;
    font-size: 1.3rem;
    font-weight: bold;
    margin-top: 0.5rem;
}

.preguntas-lista {
    margin-top: 2rem;
}

.pregunta-item {
    background: white;
    padding: 1.5rem;
    border-radius: 10px;
    margin-bottom: 1rem;
    border-left: 4px solid #667eea;
}

.pregunta-header {
    display: flex;
    justify-content: space-between;
    margin-bottom: 0.5rem;
}

.numero {
    color: #888;
}
```

### 📝 Ejercicio 7.1 (20 min)

**Agrega la funcionalidad de eliminar preguntas:**

1. Crea una ruta `POST /eliminar_pregunta/{indice}` que quite una pregunta del historial
2. Agrega un botón "Eliminar" en cada pregunta del historial
3. Asegúrate de que el índice sea válido antes de eliminar

<details>
<summary>💡 Pista</summary>

```python
@app.post("/eliminar_pregunta/{indice}")
async def eliminar_pregunta(indice: int):
    if 0 <= indice < len(preguntas_db):
        preguntas_db.pop(indice)
    return RedirectResponse(url="/historial", status_code=303)
```

En la plantilla:
```html
<form action="/eliminar_pregunta/{{ loop.index0 }}" method="POST">
    <button type="submit" class="btn-eliminar">🗑️ Eliminar</button>
</form>
```

</details>

---

## 8. Proyecto Final: Sistema de Preguntas y Respuestas

### 8.1 Lo que vamos a construir

Un sistema completo con:
- ✅ Página principal con formulario
- ✅ Procesamiento de preguntas
- ✅ Respuestas aleatorias
- ✅ Historial de preguntas
- ✅ Diseño moderno con CSS

### 8.2 Estructura final del proyecto

```
sistema_preguntas/
├── main.py              # Todo el código FastAPI
├── templates/
│   ├── base.html         # Plantilla base
│   ├── formulario.html   # Página principal
│   ├── respuesta_magica.html  # Resultado individual
│   └── historial.html    # Lista de preguntas
└── static/
    └── style.css         # Estilos
```

### 8.3 Código completo de main.py

```python
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import random

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Base de datos simulada
preguntas_db = []
respuestas_magicas = [
    "¡Sí, definitivamente! 🔮",
    "No lo creo... 🤔",
    "Pregunta de nuevo mañana 🌙",
    "¡Absolutamente sí! ✨",
    "Las estrellas dicen que no... ⭐",
    "¡Tal vez! Eso depende de ti 🎯",
    "Lo más probable es que sí 🎲",
    "Solo el tiempo lo dirá ⏳",
    "¡Sin duda alguna! 🌟",
    "Mejor no contar... 👀"
]

# Rutas
@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    return templates.TemplateResponse("formulario.html", {"request": request})

@app.post("/procesar_pregunta")
async def procesar_pregunta(nombre: str = Form(...), pregunta: str = Form(...)):
    respuesta = random.choice(respuestas_magicas)
    preguntas_db.append({
        "nombre": nombre,
        "pregunta": pregunta,
        "respuesta": respuesta
    })
    return RedirectResponse(url="/respuesta_magica", status_code=303)

@app.get("/respuesta_magica", response_class=HTMLResponse)
async def respuesta_magica(request: Request):
    if preguntas_db:
        ultima = preguntas_db[-1]
    else:
        ultima = {"nombre": "", "pregunta": "", "respuesta": ""}
    return templates.TemplateResponse(
        "respuesta_magica.html",
        {"request": request, **ultima}
    )

@app.get("/historial", response_class=HTMLResponse)
async def historial(request: Request):
    return templates.TemplateResponse(
        "historial.html",
        {"request": request, "preguntas": preguntas_db}
    )

@app.post("/eliminar_pregunta/{indice}")
async def eliminar_pregunta(indice: int):
    if 0 <= indice < len(preguntas_db):
        preguntas_db.pop(indice)
    return RedirectResponse(url="/historial", status_code=303)
```

### 📝 Desafíos extra (para después de la clase)

1. **Agregar likes**: Cada pregunta puede tener un contador de "me gusta"
2. **Búsqueda**: Filtra el historial por nombre o contenido
3. **Categorías**: Clasifica preguntas por tema
4. **Persistencia**: Guarda las preguntas en un archivo JSON

---

## 9. Evaluación de Conocimientos

**Duración:** 20 minutos | **Puntaje total:** 100 puntos

---

### SECCIÓN A: Conceptos (25 puntos)

**PREGUNTA A1 (8 puntos):** Explica con tus propias palabras qué es FastAPI y para qué sirve.

```
Respuesta:
___________________________________________________________________
___________________________________________________________________
```

**PREGUNTA A2 (9 puntos):** ¿Cuál es la diferencia entre parámetros de path y parámetros de query? Da un ejemplo de cada uno.

```
Respuesta:
___________________________________________________________________
___________________________________________________________________
___________________________________________________________________
```

**PREGUNTA A3 (8 puntos):** ¿Qué es Jinja2 y cuál es su propósito en el desarrollo web?

```
Respuesta:
___________________________________________________________________
```

---

### SECCIÓN B: Código (35 puntos)

**PREGUNTA B1 (12 puntos):** Escribe el código FastAPI para una ruta `GET /saludo/{nombre}` que devuelva un JSON con el mensaje `"¡Hola {nombre}!"` y la cantidad de letras del nombre.

```python
# Tu código aquí
```

**PREGUNTA B2 (12 puntos):** Escribe el código de una plantilla Jinja2 `lista.html` que muestre una lista de productos usando un loop `{% for %}` y muestre "No hay productos" si la lista está vacía.

```html
<!-- Tu código aquí -->
```

**PREGUNTA B3 (11 puntos):** Completa el código para procesar un formulario con POST:

```python
@app.post("/crear_usuario")
async def crear_usuario(
    # Completa los parámetros
):
    nuevo_usuario = {
        "nombre": nombre,
        "edad": edad
    }
    return {"mensaje": "Usuario creado", "usuario": nuevo_usuario}
```

---

### SECCIÓN C: Práctico (40 puntos)

**PREGUNTA C1 (20 puntos):** Crea un mini sistema de notas con:
- Ruta `GET /` que muestre una plantilla con la lista de notas
- Ruta `POST /agregar_nota` que reciba `titulo` y `contenido` del formulario y agregue a la lista
- Una plantilla `notas.html` que muestre todas las notas

**PREGUNTA C2 (20 puntos):** Usando el concepto de herencia de plantillas:
1. Crea una plantilla base `base.html` con header y footer
2. Crea una página `inicio.html` que extienda de base.html
3. Muestra cómo usar `{% block contenido %}` y `{% endblock %}`

---

## Respuestas de la Evaluación (Para el docente)

### SECCIÓN A:
- **A1:** FastAPI es un framework web moderno para construir APIs con Python. Permite crear endpoints, procesar datos, renderizar páginas web.
- **A2:** Path params van en la URL (`/saludo/{nombre}`), query params van después del `?` (`/buscar?q=python`). Los path params son parte de la ruta, los query son opcionales.
- **A3:** Jinja2 es un motor de plantillas que permite crear HTML dinámico con variables (`{{ }}`) y lógica (`{% %}`).

### SECCIÓN B:
- **B1:**
```python
@app.get("/saludo/{nombre}")
def saludar(nombre: str):
    return {"mensaje": f"¡Hola {nombre}!", "letras": len(nombre)}
```
- **B2:** (Ver ejemplo en sección 5.4)
- **B3:**
```python
async def crear_usuario(nombre: str = Form(...), edad: int = Form(...)):
```

### SECCIÓN C:
- **C1-C2:** El código completo depende de la estructura del proyecto. Ver ejemplos en secciones 7 y 8.

---

## Resumen de Conceptos Clave

| Concepto | Descripción | Ejemplo |
|----------|-------------|---------|
| **FastAPI** | Framework web para APIs | `@app.get("/")` |
| **Ruta** | URL que responde a peticiones | `@app.get("/saludo/{nombre}")` |
| **Path param** | Parámetro en la URL | `/usuario/{id}` |
| **Query param** | Parámetro después del `?` | `/buscar?q=python` |
| **POST** | Enviar datos al servidor | `Form(...)` |
| **Jinja2** | Motor de plantillas HTML | `{{ variable }}` |
| **Herencia** | Reutilizar plantillas base | `{% extends "base.html" %}` |
| **Block** | Sección reemplazable | `{% block contenido %}...{% endblock %}` |

---

## Distribución del Tiempo

| Módulo | Duración | Contenido |
|--------|----------|-----------|
| **Hora 1** | 60 min | Fundamentos de FastAPI, primera API, GET/POST |
| **Hora 2** | 60 min | Rutas con path params, query params, ejercicios |
| **Hora 3** | 60 min | Jinja2: variables, if/for, filtros, herencia |
| **Hora 4** | 60 min | Integración FastAPI+Jinja2, proyecto final, evaluación |
| **Total** | **240 min** | 4 horas |

---

**¡Felicitaciones por completar el curso! 🎉**

Ahora sabes crear aplicaciones web interactivas con FastAPI y Jinja2. El siguiente paso es aprender bases de datos y autenticación.

*Material elaborado para uso educativo — FastAPI + Jinja2 Mini Curso*
*Duración: 4 horas | Nivel: Principiante*