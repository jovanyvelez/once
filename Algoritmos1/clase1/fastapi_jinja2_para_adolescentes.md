# FastAPI + Jinja2: Crea tu Primera Web App Interactiva

**Duración:** 2 horas
**Nivel:** Principiante (adolescentes 15-17 años)
**Requisitos:** Conocer lo básico de Python (variables, funciones, listas)

---

## Tabla de Contenidos

1. [¿Qué vamos a construir hoy?](#1-qué-vamos-a-construir-hoy)
2. [¿Qué es FastAPI y por qué te va a encantar?](#2-qué-es-fastapi-y-por-qué-te-va-a-encantar)
3. [Configurando tu entorno de trabajo](#3-configurando-tu-entorno-de-trabajo)
4. [Tu primera API en 5 minutos](#4-tu-primera-api-en-5-minutos)
5. [Rutas dinámicas: haciéndola personal](#5-rutas-dinámicas-haciéndola-personal)
6. [Jinja2: el arte de crear páginas web](#6-jinja2-el-arte-de-crear-páginas-web)
7. [Proyecto Integrador: Mini Blog Personal](#7-proyecto-integrador-mini-blog-personal)
8. [Desafíos Extra](#8-desafíos-extra)
9. [Resumen y Próximos Pasos](#9-resumen-y-próximos-pasos)

---

## 1. ¿Qué vamos a construir hoy?

### 🎯 El Proyecto: "Pregunta a la Máquina Mágica"

Hoy vas a crear una aplicación web donde:
- Los usuarios pueden hacer preguntas
- La "máquina mágica" responde con frases aleatorias
- Puedes ver todas las preguntas hechas
- ¡Todo se ve bonito con CSS!

**Parece complicado?** En 2 horas vas a entender cómo funcionan apps que usas todos los días como Instagram, TikTok o tus juegos favoritos.

---

## 2. ¿Qué es FastAPI y por qué te va a encantar?

### 2.1 La Analogía del Restaurante

Imagina que abres un restaurante:

```
🍽️ CLIENTE (tú, en el navegador)
       │
       │  "¡Quiero una pizza!"
       ▼
┌─────────────────────────────────────┐
│  COCINA (FastAPI)                    │
│                                      │
│  1. Recibe tu pedido                 │
│  2. Lo procesa                       │
│  3. Prepara la respuesta             │
│  4. Te lo entrega                    │
└─────────────────────────────────────┘
       │
       │  "¡Aquí está tu pizza! 🍕"
       ▼
   CLIENTE
```

FastAPI es como el chef y el mesero combinados:
- **Chef**: Procesa los pedidos (código Python)
- **Mesero**: Entrega resultados rápido (HTTP)

### 2.2 ¿Por qué FastAPI y no otras herramientas?

| Herramienta | Velocidad | Dificultad | Ideal para |
|-------------|-----------|------------|------------|
| **FastAPI** | ⚡⚡⚡⚡⚡ | Fácil | APIs modernas, apps web |
| Django | ⚡⚡⚡ | Media-Alta | Apps grandes (Instagram) |
| Flask | ⚡⚡⚡⚡ | Fácil | APIs simples |
| Node.js | ⚡⚡⚡⚡ | Media | Apps web completas |

### 2.3 ¿Qué es Jinja2?

Jinja2 es un **motor de plantillas**. Piensa en él como un procesador de texto muy inteligente:

```html
<!-- plantilla.html -->
<h1>Hola, {{ nombre }}!</h1>
<p>Tienes {{ edad }} años.</p>
```

Cuando FastAPI le pasa `nombre="Carlos"` y `edad=16`, Jinja2 convierte esto en:

```html
<h1>Hola, Carlos!</h1>
<p>Tienes 16 años.</p>
```

---

## 3. Configurando tu entorno de trabajo

### 3.1 Instalando todo (solo 1 comando)

Abre tu terminal y escribe:

```bash
# Instalar FastAPI con todas las herramientas básicas incluidas
pip install "fastapi[standard]"
```

**¿Qué incluye `fastapi[standard]`?**

| Herramienta | Qué hace |
|-------------|----------|
| **FastAPI** | El framework principal para crear APIs |
| **httpx** | Cliente HTTP para hacer peticiones |
| **uvicorn** | Servidor de desarrollo (lo corre `fastapi dev`) |
| **jinja2** | Motor de plantillas HTML |
| **python-multipart** | Procesamiento de formularios |

`fastapi dev` es el comando que inicia el servidor y detecta cambios automáticamente.

### 3.2 Creando tu carpeta de proyecto

```bash
# Crear carpeta
mkdir mi_magia_web
cd mi_magia_web

# Crear archivo principal
touch main.py
```

### 3.3 Estructura del proyecto

```
mi_magia_web/
├── main.py          # Aquí va todo tu código Python
├── templates/        # Carpeta para archivos HTML
│   └── (crearemos archivos aquí)
└── static/          # Para CSS, imágenes
    └── style.css
```

---

## 4. Tu primera API en 5 minutos

### 4.1 El "Hola Mundo" de FastAPI

Crea un archivo `main.py` con esto:

```python
from fastapi import FastAPI

# Crear la aplicación
app = FastAPI()

# Tu primera ruta - cuando alguien visite /
@app.get("/")
def hola_mundo():
    return {"mensaje": "¡Hola Mundo!", "status": "funcionando"}
```

### 4.2 Ejecutar el servidor

En tu terminal:

```bash
fastapi dev
```

**¿Qué hace `fastapi dev`?**
- Inicia el servidor en http://127.0.0.1:8000
- Detecta cambios en tu código y se reinicia automáticamente
- Muestra logs de cada petición en la terminal

¡Es todo lo que necesitas para desarrollar!

### 4.3 Probar tu API

Abre tu navegador y visita:
- **http://127.0.0.1:8000** → Deberías ver el JSON

También puedes ver documentación automática en:
- **http://127.0.0.1:8000/docs** → Documentación interactiva (¡gratis!)

### 📝 Ejercicio 4.1: Tu Primer Cambio

**Instrucciones:**
1. Cambia el mensaje a "¡Soy el/la mejor programador/a!"
2. Agrega tu nombre y edad al JSON
3. Reinicia (o guarda si usas --reload)
4. Verifica que funciona

**Resultado esperado:**
```python
@app.get("/")
def hola_mundo():
    return {
        "mensaje": "¡Soy el/la mejor programador/a!",
        "nombre": "Tu nombre",
        "edad": 16,
        "status": "funcionando"
    }
```

---

## 5. Rutas dinámicas: haciéndola personal

### 5.1 Rutas con parámetros

El URL puede cambiar según lo que el usuario escriba:

```
/saludo/Carlos    → "Hola Carlos"
/saludo/María      → "Hola María"
```

**Código:**

```python
@app.get("/saludo/{nombre}")
def saludar(nombre: str):
    return {"mensaje": f"¡Hola {nombre}!", "letras": len(nombre)}
```

**Prueba:**
- http://127.0.0.1:8000/saludo/TuNombre
- http://127.0.0.1:8000/saludo/Minecraft

### 5.2 Múltiples parámetros

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
        if num2 != 0:
            resultado = num1 / num2
        else:
            return {"error": "No se puede dividir entre cero"}
    else:
        return {"error": "Operación no válida"}

    return {
        "num1": num1,
        "operacion": operacion,
        "num2": num2,
        "resultado": resultado
    }
```

**Pruébalo:**
- http://127.0.0.1:8000/calculadora/10/suma/5
- http://127.0.0.1:8000/calculadora/25/multiplicacion/4

### 5.3 Rutas POST: recibiendo datos

**GET vs POST - ¿Cuál usar?**

| Método | Uso | Ejemplo |
|--------|-----|---------|
| **GET** | Pedir información (como buscar en Google) | `GET /usuario/Carlos` |
| **POST** | Enviar información nueva (como un formulario) | `POST /crear-usuario` |

**Ejemplo con POST:**

```python
@app.post("/crear_usuario")
def crear_usuario(nombre: str, edad: int, email: str):
    # Aquí normalmente guardarías en una base de datos
    nuevo_usuario = {
        "nombre": nombre,
        "edad": edad,
        "email": email,
        "id": 42  # Simulado
    }
    return {"mensaje": "¡Usuario creado!", "usuario": nuevo_usuario}
```

### 📝 Ejercicio 5.1: Conversor de Monedas

**Instrucciones:**
1. Crea una ruta `GET /convertir/{cantidad}/{de}/{a}`
2. Debe convertir entre USD, EUR y COP
3. Tasas de cambio (aproximadas):
   - USD a EUR: 0.92
   - USD a COP: 4000
   - EUR a COP: 4350

**Ejemplo:**
- `/convertir/100/USD/EUR` → `92 euros`
- `/convertir/50/EUR/COP` → `217500 pesos`

<details>
<summary>💡 ¿Necesitas ayuda? Ver pista</summary>

```python
@app.get("/convertir/{cantidad}/{de}/{a}")
def convertir(cantidad: float, de: str, a: str):
    tasas = {
        "USD_EUR": 0.92,
        "USD_COP": 4000,
        "EUR_COP": 4350,
        # Agrega más...
    }

    clave = f"{de}_{a}"
    if clave in tasas:
        resultado = cantidad * tasas[clave]
        return {"original": f"{cantidad} {de}", "convertido": f"{resultado} {a}"}
    else:
        return {"error": "Conversión no disponible"}
```

</details>

---

## 6. Jinja2: el arte de crear páginas web

### 6.1 La estructura de carpetas

Primero, crea la estructura:

```bash
mkdir -p templates static
touch templates/base.html
touch templates/inicio.html
touch templates/respuestas.html
touch static/style.css
```

### 6.2 Tu primera plantilla HTML

Edita `templates/inicio.html`:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>{{ titulo }}</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <header>
        <h1>{{ titulo }}</h1>
        <p>{{ subtitulo }}</p>
    </header>

    <main>
        <div class="caja">
            <h2>🎤 Formulario de Preguntas</h2>
            <form action="/procesar" method="POST">
                <label for="nombre">Tu nombre:</label>
                <input type="text" name="nombre" required>

                <label for="pregunta">¿Qué quieres preguntar?</label>
                <textarea name="pregunta" required></textarea>

                <button type="submit">¡Enviar! 🚀</button>
            </form>
        </div>
    </main>

    <footer>
        <p>Hecho con 💜 usando FastAPI + Jinja2</p>
    </footer>
</body>
</html>
```

### 6.3 Configurar Jinja2 en FastAPI

Actualiza `main.py`:

```python
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# Crear la aplicación
app = FastAPI()

# Montar archivos estáticos (CSS, imágenes)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Configurar Jinja2
templates = Jinja2Templates(directory="templates")

# Base de datos simulada (en memoria)
preguntas_db = []

# Rutas
@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    return templates.TemplateResponse(
        "inicio.html",
        {"request": request, "titulo": "Pregunta a la Máquina", "subtitulo": "La máquina que responde cualquier cosa"}
    )
```

### 6.4 Procesando formularios

Agrega esta ruta POST:

```python
@app.post("/procesar")
async def procesar_pregunta(
    nombre: str = Form(...),
    pregunta: str = Form(...)
):
    # La máquina mágica da respuestas aleatorias
    respuestas_magicas = [
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
    respuesta = random.choice(respuestas_magicas)

    # Guardar en nuestra "base de datos"
    preguntas_db.append({
        "nombre": nombre,
        "pregunta": pregunta,
        "respuesta": respuesta
    })

    return {
        "nombre": nombre,
        "pregunta": pregunta,
        "respuesta": respuesta
    }
```

### 6.5 Mostrando las respuestas guardadas

Crea `templates/respuestas.html`:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Respuestas Mágicas</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <header>
        <h1>🔮 Todas las Preguntas Mágicas</h1>
        <nav>
            <a href="/">← Volver al inicio</a>
        </nav>
    </header>

    <main>
        {% if preguntas %}
            <p class="contador">Total de preguntas: {{ preguntas|length }}</p>

            <div class="preguntas-lista">
                {% for item in preguntas %}
                    <div class="pregunta-card">
                        <div class="pregunta">
                            <strong>{{ item.nombre }}</strong> preguntó:
                            <br>
                            <em>"{{ item.pregunta }}"</em>
                        </div>
                        <div class="respuesta">
                            💬 {{ item.respuesta }}
                        </div>
                    </div>
                {% endfor %}
            </div>
        {% else %}
            <div class="vacio">
                <p>😢 No hay preguntas aún.</p>
                <a href="/">¡Sé el primero en preguntar!</a>
            </div>
        {% endif %}
    </main>
</body>
</html>
```

Agrega la ruta en `main.py`:

```python
@app.get("/respuestas", response_class=HTMLResponse)
async def ver_respuestas(request: Request):
    return templates.TemplateResponse(
        "respuestas.html",
        {"request": request, "preguntas": preguntas_db}
    )
```

### 📝 Ejercicio 6.1: Personaliza tu Template

**Instrucciones:**
1. Cambia los colores en `style.css` (usa tu color favorito)
2. Agrega tu nombre en el footer
3. Agrega un emoji favorito en el título
4. Crea una nueva página `templates/acerca.html`

**Resultado esperado:** Una página con tu estilo personal.

### 📝 Ejercicio 6.2: Agrega más respuestas mágicas

**Instrucciones:**
1. Agrega 5 respuestas más a la lista `respuestas_magicas`
2. Pueden ser respuestas graciosas, motivacionales, o de tus juegos favoritos
3. Prueba que funcionen enviando varios formularios

---

## 7. Proyecto Integrador: Mini Blog Personal

### 7.1 Lo que vamos a construir

Un blog donde puedes:
- ✅ Ver una lista de publicaciones
- ✅ Crear nuevas publicaciones
- ✅ Cada publicación tiene título, autor y contenido
- ✅ Interfaz bonita con CSS

### 7.2 Paso 1: El HTML del blog

Crea `templates/blog.html`:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Mi Blog Personal</title>
    <link rel="stylesheet" href="/static/style.css">
</head>
<body>
    <nav class="navbar">
        <span class="logo">📝 Mi Blog</span>
        <div class="nav-links">
            <a href="/blog">Inicio</a>
            <a href="/blog/nueva">Nueva Publicación</a>
        </div>
    </nav>

    <main class="container">
        {% block content %}{% endblock %}
    </main>
</body>
</html>
```

Crea `templates/lista_posts.html` (extiende del blog):

```html
{% extends "blog.html" %}

{% block content %}
<h1>📚 Publicaciones del Blog</h1>

{% if posts %}
    <div class="posts-grid">
        {% for post in posts %}
            <article class="post-card">
                <h2>{{ post.titulo }}</h2>
                <p class="autor">Por {{ post.autor }} • {{ post.fecha }}</p>
                <p class="contenido">{{ post.contenido }}</p>
            </article>
        {% endfor %}
    </div>
{% else %}
    <div class="vacio">
        <p>No hay publicaciones todavía.</p>
        <a href="/blog/nueva" class="btn">¡Escribe la primera!</a>
    </div>
{% endif %}
{% endblock %}
```

Crea `templates/nueva_publicacion.html`:

```html
{% extends "blog.html" %}

{% block content %}
<h1>✨ Nueva Publicación</h1>

<form action="/blog/crear" method="POST" class="form-blog">
    <label for="titulo">Título:</label>
    <input type="text" name="titulo" required>

    <label for="autor">Tu nombre:</label>
    <input type="text" name="autor" required>

    <label for="contenido">¿Qué quieres escribir?</label>
    <textarea name="contenido" rows="10" required></textarea>

    <button type="submit" class="btn">Publicar 📤</button>
</form>
{% endblock %}
```

### 7.3 Paso 2: El código Python

Actualiza `main.py`:

```python
from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from datetime import datetime

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Base de datos simulada
posts_db = [
    {
        "titulo": "Mi primer día programando",
        "autor": "Ana",
        "fecha": "2026-04-10",
        "contenido": "Hoy aprendí qué es una variable. ¡Es como una caja donde guardas cosas!"
    },
    {
        "titulo": "Por qué me gusta Python",
        "autor": "Carlos",
        "fecha": "2026-04-11",
        "contenido": "Python es genial porque puedes hacer cosas complejas con poco código."
    }
]

# Rutas del blog
@app.get("/blog", response_class=HTMLResponse)
async def lista_posts(request: Request):
    return templates.TemplateResponse(
        "lista_posts.html",
        {"request": request, "posts": posts_db}
    )

@app.get("/blog/nueva", response_class=HTMLResponse)
async def nueva_publicacion(request: Request):
    return templates.TemplateResponse(
        "nueva_publicacion.html",
        {"request": request}
    )

@app.post("/blog/crear")
async def crear_post(
    titulo: str = Form(...),
    autor: str = Form(...),
    contenido: str = Form(...)
):
    nuevo_post = {
        "titulo": titulo,
        "autor": autor,
        "fecha": datetime.now().strftime("%Y-%m-%d"),
        "contenido": contenido
    }
    posts_db.insert(0, nuevo_post)  # Agregar al inicio
    return RedirectResponse(url="/blog", status_code=303)
```

### 7.4 Paso 3: El CSS

Crea `static/style.css`:

```css
/* Reset básico */
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
    background-color: #f5f5f5;
    color: #333;
    line-height: 1.6;
}

/* Navbar */
.navbar {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 1rem 2rem;
    display: flex;
    justify-content: space-between;
    align-items: center;
    color: white;
}

.logo {
    font-size: 1.5rem;
    font-weight: bold;
}

.nav-links a {
    color: white;
    text-decoration: none;
    margin-left: 1.5rem;
    padding: 0.5rem 1rem;
    border-radius: 5px;
    transition: background 0.3s;
}

.nav-links a:hover {
    background: rgba(255,255,255,0.2);
}

/* Container */
.container {
    max-width: 800px;
    margin: 2rem auto;
    padding: 0 1rem;
}

/* Formularios */
.form-blog {
    background: white;
    padding: 2rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.form-blog label {
    display: block;
    margin-bottom: 0.5rem;
    font-weight: bold;
    color: #555;
}

.form-blog input,
.form-blog textarea {
    width: 100%;
    padding: 0.8rem;
    margin-bottom: 1rem;
    border: 2px solid #ddd;
    border-radius: 5px;
    font-size: 1rem;
    font-family: inherit;
}

.form-blog input:focus,
.form-blog textarea:focus {
    outline: none;
    border-color: #667eea;
}

/* Botones */
.btn {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    padding: 0.8rem 2rem;
    border: none;
    border-radius: 5px;
    font-size: 1rem;
    cursor: pointer;
    text-decoration: none;
    display: inline-block;
    transition: transform 0.2s;
}

.btn:hover {
    transform: translateY(-2px);
}

/* Posts */
.post-card {
    background: white;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
    transition: transform 0.2s;
}

.post-card:hover {
    transform: translateX(5px);
}

.post-card h2 {
    color: #667eea;
    margin-bottom: 0.5rem;
}

.post-card .autor {
    color: #888;
    font-size: 0.9rem;
    margin-bottom: 1rem;
}

.post-card .contenido {
    line-height: 1.8;
}

/* Vacio */
.vacio {
    text-align: center;
    padding: 3rem;
    background: white;
    border-radius: 10px;
}
```

### 📝 Ejercicio 7.1: Personaliza tu Blog

**Instrucciones obligatorias:**
1. Cambia los colores del gradiente a tu paleta favorita
2. Agrega un emoji único al logo
3. Incluye 3 publicaciones tuyas con temas que te interesen (juegos, música, lo que sea)

**Instrucciones opcionales (desafío):**
4. Agrega un campo de "categoría" a cada post
5. Filtra los posts por categoría

---

## 8. Desafíos Extra

¿Terminaste todo? ¡Felicitaciones! Ahora intenta estos desafíos:

### 🌟 Desafío 1: Sistema de Votación

Agrega botones de "Me gusta" a cada pregunta:

```python
# Hint: Agrega un campo likes a cada post
posts_db = [
    {"titulo": "...", "likes": 0, ...}
]
```

### 🌟 Desafío 2: Búsqueda de Posts

Agrega una barra de búsqueda:

```python
@app.get("/blog/buscar")
async def buscar_posts(q: str):
    resultados = [p for p in posts_db if q.lower() in p["titulo"].lower()]
    return resultados
```

### 🌟 Desafío 3: Calculadora de Edades de Perro

Crea una ruta `/perro/{edad_humano}` que convierta años humanos a años de perro:

- Los primeros 2 años = 10.5 años de perro por año humano
- Después = 4 años de perro por año humano

**Ejemplo:** 3 años humanos = 2*10.5 + 1*4 = 25 años de perro

### 🌟 Desafío 4: Lista de Tareas (To-Do)

Construye una app de tareas donde puedas:
- [ ] Agregar tarea
- [ ] Marcar como completada
- [ ] Ver todas las tareas
- [ ] Eliminar tarea

---

## 9. Resumen y Próximos Pasos

### 📚 Lo que aprendiste hoy

| Concepto | Descripción | Ejemplo |
|----------|-------------|---------|
| **FastAPI** | Framework web rápido para APIs | `@app.get("/")` |
| **fastapi dev** | Comando para ejecutar el servidor | `fastapi dev` |
| **Rutas** | URLs que responden a peticiones | `/saludo/{nombre}` |
| **Parámetros** | Datos variables en URLs | `def saludar(nombre: str)` |
| **POST** | Enviar datos al servidor | `Form(...)` |
| **Jinja2** | Motor de plantillas HTML | `{{ variable }}` |
| **Templates** | Archivos HTML con lógica | `{% for %}` |
| **Static files** | CSS, imágenes | `/static/style.css` |

### 🛠️ Herramientas que ahora conoces

- `fastapi dev` - Comando para ejecutar el servidor
- `fastapi` - Framework principal
- `jinja2` - Motor de plantillas HTML
- `StaticFiles` - Archivos estáticos
- `Form` - Datos de formularios

### 🎯 Próximos pasos sugeridos

1. **Base de datos real**: Aprende SQLite o PostgreSQL
2. **Autenticación**: Agrega login/logout con JWT
3. **Despliegue**: Publica tu app en Render o Railway gratis
4. **APIs REST**: Practica con clientes como Postman

### Checklist de Aprendizaje

Antes de decir "ya aprendí", asegúrate de poder responder:

- [ ] ¿Qué es FastAPI y para qué sirve?
- [ ] ¿Cómo crear una ruta GET simple?
- [ ] ¿Cómo recibir datos de un formulario?
- [ ] ¿Qué es Jinja2 y cómo usar sus etiquetas `{{ }}` y `{% %}`?
- [ ] ¿Cómo configurar archivos CSS estáticos?
- [ ] ¿Cómo funciona el ciclo request → procesa → response?

---

## 📁 Archivos del Proyecto

Para que tu proyecto quede organizado:

```
mi_blog/
├── main.py              # Todo tu código Python
├── templates/
│   ├── base.html         # (opcional) Plantilla base
│   ├── inicio.html       # Página de preguntas mágicas
│   ├── respuestas.html   # Ver todas las respuestas
│   ├── blog.html         # Base del blog
│   ├── lista_posts.html  # Ver posts
│   └── nueva_publicacion.html  # Crear post
└── static/
    └── style.css         # Tus estilos
```

---

## ❓ Preguntas Frecuentes

**P: ¿Puedo usar este código en mis proyectos?**
R: ¡Sí! FastAPI usa licencia MIT. Es tuyo para siempre.

**P: ¿Por qué usar `fastapi[standard]` en vez de instalar cada cosa por separado?**
R: Porque viene todo incluido y listo para funcionar. No tienes que preocuparte por versiones compatibles.

**P: ¿Dónde puedo aprender más?**
R: La documentación oficial de FastAPI es excelente: https://fastapi.tiangolo.com/es/

**P: ¿Cómo corrijo errores?**
R:
1. Lee el mensaje de error completo
2. Busca en Google el mensaje exacto
3. Pregunta en foros como Stack Overflow

---

**¡Eso es todo por hoy! 🎉**
Si llegaste hasta aquí, ya sabes crear páginas web interactivas con FastAPI y Jinja2.
El mundo del desarrollo web está a tu alcance.

*¡Nos vemos en la próxima clase! 💻✨*
