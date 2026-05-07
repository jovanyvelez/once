# 🧙‍♂️ La Máquina Mágica
## Curso de FastAPI + Jinja2 para adolescentes

> **¿Para quién?** Para ti que sabes escribir `print("hola")` y crear funciones. Nada más.
> **¿Cuánto dura?** 4 sesiones de 30-40 min. Cada una termina con algo que funciona.
> **La promesa:** Copias, pegas, ejecutas y ENTIENDES. Sin frustraciones.
>
> 💡 **¿Nunca has usado Jinja2?** Empieza por el complemento ultra-simple: [Tu Primera Web con Herencia](./herencia_jinja2_simplificado.md) (15 min, solo herencia pura).

---

## 🌍 Mapa de la aventura

```
SESIÓN 1 ──► Setup + primera ruta funcionando
SESIÓN 2 ──► Jinja2: herencia, base.html, formulario real  
SESIÓN 3 ──► POST, Form(...), redirección, respuesta mágica
SESIÓN 4 ──► Historial, eliminar, bucles, reto final
```

---

# 🧪 SESIÓN 1 — El hechizo inicial

**Objetivo:** Proyecto corriendo. Verás "Hola mundo mágico" en el navegador.

## 1.1 Crea el proyecto

```bash
mkdir maquina_magica && cd maquina_magica
mkdir templates static
pip install "fastapi[standard]"
```

> ⚠️ El comando es `"fastapi[standard]"` con los corchetes. Si pones solo `fastapi` te faltará Jinja2.

## 1.2 Crea `main.py`

```python
from datetime import datetime

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    return templates.TemplateResponse(
        name="formulario.html",
        request=request,
        context={"ano_actual": datetime.now().year},
    )
```

### ¿Qué hace cada línea?

| Línea | Explicación |
|--------|------------|
| `app = FastAPI()` | Crea tu servidor web |
| `app.mount("/static", StaticFiles(directory="static"))` | Sirve archivos desde `static/` (ruta relativa) |
| `templates = Jinja2Templates(directory="templates")` | Activa Jinja2, busca .html en `templates/` (ruta relativa) |
| `@app.get("/")` | Cuando visiten la raíz del sitio, ejecuta esta función |
| `templates.TemplateResponse(...)` | Toma un .html, llénalo con datos, entrégalo |
| `context={"ano_actual": ...}` | La **mochila**: diccionario que viaja de Python al HTML |

## 1.3 Crea `templates/formulario.html` (versión simple)

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Máquina Mágica</title>
</head>
<body>
    <h1>🔮 ¡La Máquina Mágica funciona!</h1>
    <p>Año actual: {{ ano_actual }}</p>
</body>
</html>
```

### 🧠 El primer hechizo Jinja2: `{{ }}`

```python
Python: context={"ano_actual": 2026}
               │
               ▼
HTML:    {{ ano_actual }}
               │
               ▼
Navegador ve:  2026
```

**Los dobles corchetes `{{ }}` son huecos que Jinja2 rellena con datos de Python.** El navegador NUNCA ve `{{ }}` — Jinja2 ya lo reemplazó antes de enviar el HTML.

> 🎒 **La mochila mágica:** Python mete datos en un diccionario. Jinja2 desempaqueta ese diccionario dentro del HTML y coloca cada valor en su `{{ }}` correspondiente.

## 1.4 Ejecuta

```bash
fastapi dev main.py
```

Abre http://127.0.0.1:8000 → Deberías ver el año actual.

### 🐛 ¿Error?

| Problema | Solución |
|----------|----------|
| `ModuleNotFoundError: No module named 'fastapi'` | `pip install "fastapi[standard]"` |
| Error 404 | ¿Existe `templates/formulario.html`? |
| `TemplateNotFound` | ¿El archivo se llama EXACTAMENTE `formulario.html`? |

---

## ✅ Checklist Sesión 1

- [ ] Proyecto creado con `templates/` y `static/`
- [ ] `main.py` y `templates/formulario.html` copiados
- [ ] El servidor arranca y ves algo en el navegador
- [ ] Entiendes `{{ variable }}` (hueco que Jinja2 rellena)

---

# 🧪 SESIÓN 2 — Los pergaminos mágicos

**Objetivo:** Base HTML con herencia Jinja2 + formulario real + estilos.

## 2.1 El CSS minimalista: `static/style.css`

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: system-ui, -apple-system, sans-serif;
    line-height: 1.6;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    background: #0a0a1a;
    color: #f0e6ff;
}

/* Navbar */
.navbar-magica {
    background: rgba(10, 10, 26, 0.95);
    border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    padding: 0.8rem 0;
    position: sticky;
    top: 0;
    z-index: 100;
}

.navbar-magica .container {
    display: flex;
    justify-content: space-between;
    align-items: center;
    max-width: 1000px;
    margin: 0 auto;
    padding: 0 1.5rem;
}

.nav-brand {
    font-size: 1.4rem;
    font-weight: 700;
    color: #e0b0ff;
    text-decoration: none;
}

.nav-links { display: flex; gap: 1rem; }

.nav-links a {
    color: #a89cc8;
    text-decoration: none;
    padding: 0.4rem 0.8rem;
    border-radius: 6px;
    font-size: 0.95rem;
}

.nav-links a:hover {
    color: #f0e6ff;
    background: rgba(255, 255, 255, 0.05);
}

/* Contenido */
.main-content {
    flex: 1;
    max-width: 900px;
    width: 100%;
    margin: 2rem auto;
    padding: 0 1.5rem;
}

/* Títulos */
.titulo-magico {
    font-size: 2rem;
    font-weight: 800;
    text-align: center;
    color: #e0b0ff;
    margin-bottom: 0.5rem;
}

.subtitulo-magico {
    text-align: center;
    color: #a89cc8;
    font-size: 1.05rem;
    margin-bottom: 2rem;
}

/* Cards */
.card-magica {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: 2rem;
}

/* Formulario */
.form-magico label {
    display: block;
    margin-bottom: 0.4rem;
    font-weight: 600;
    color: #e0b0ff;
    font-size: 0.95rem;
}

.form-magico input,
.form-magico textarea {
    width: 100%;
    padding: 0.8rem 1rem;
    margin-bottom: 1rem;
    background: rgba(255, 255, 255, 0.05);
    border: 2px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    font-size: 1rem;
    font-family: inherit;
    color: #f0e6ff;
}

.form-magico input:focus,
.form-magico textarea:focus {
    outline: none;
    border-color: #667eea;
}

/* Botones */
.btn-magico {
    display: inline-flex;
    align-items: center;
    justify-content: center;
    gap: 0.5rem;
    background: linear-gradient(135deg, #4a1a7a, #667eea);
    color: white;
    padding: 0.9rem 2rem;
    border: none;
    border-radius: 8px;
    font-size: 1rem;
    font-weight: 600;
    font-family: inherit;
    cursor: pointer;
    width: 100%;
}

.btn-magico:hover { opacity: 0.9; }

.btn-secundario {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    background: transparent;
    color: #e0b0ff;
    padding: 0.7rem 1.4rem;
    border: 2px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    font-size: 0.95rem;
    font-family: inherit;
    cursor: pointer;
    text-decoration: none;
}

.btn-secundario:hover {
    border-color: #e0b0ff;
    background: rgba(224, 176, 255, 0.08);
}

.btn-peligro {
    background: rgba(231, 76, 60, 0.15);
    color: #ff6b6b;
    padding: 0.5rem 1rem;
    border: 1px solid rgba(231, 76, 60, 0.3);
    border-radius: 6px;
    font-size: 0.85rem;
    font-family: inherit;
    cursor: pointer;
}

.btn-peligro:hover { background: rgba(231, 76, 60, 0.25); }

/* Respuesta */
.respuesta-destacada {
    background: rgba(102, 126, 234, 0.1);
    border: 1px solid rgba(102, 126, 234, 0.3);
    border-radius: 12px;
    padding: 2rem;
    text-align: center;
}

.respuesta-destacada .respuesta-texto {
    font-size: 1.5rem;
    font-weight: 700;
    color: #e0b0ff;
    margin-top: 0.5rem;
}

.respuesta-destacada .etiqueta {
    color: #a89cc8;
    font-size: 0.95rem;
}

/* Historial */
.historial-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
    gap: 1rem;
    margin-top: 1.5rem;
}

.card-historial {
    background: rgba(255, 255, 255, 0.04);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-left: 3px solid #764ba2;
    border-radius: 10px;
    padding: 1.2rem;
}

.card-historial-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 0.6rem;
}

.card-historial-header .nombre {
    font-weight: 600;
    color: #f0e6ff;
}

.card-historial-header .numero {
    background: rgba(102, 126, 234, 0.15);
    color: #667eea;
    padding: 0.15rem 0.6rem;
    border-radius: 12px;
    font-size: 0.8rem;
    font-weight: 600;
}

.card-historial .pregunta {
    color: #a89cc8;
    font-style: italic;
    margin-bottom: 0.6rem;
}

.card-historial .respuesta {
    color: #e0b0ff;
    font-weight: 600;
    margin-bottom: 0.8rem;
}

.card-historial-footer { text-align: right; }

.contador-preguntas {
    color: #a89cc8;
    font-size: 0.9rem;
    margin-bottom: 0.5rem;
}

/* Estado vacío */
.estado-vacio {
    text-align: center;
    padding: 3rem 2rem;
    background: rgba(255, 255, 255, 0.04);
    border: 1px dashed rgba(255, 255, 255, 0.1);
    border-radius: 12px;
}

.estado-vacio .icono {
    font-size: 3.5rem;
    margin-bottom: 0.8rem;
    display: block;
}

.estado-vacio .mensaje {
    font-size: 1.1rem;
    color: #a89cc8;
    margin-bottom: 1.2rem;
}

/* Acciones */
.acciones-centradas {
    display: flex;
    justify-content: center;
    gap: 1rem;
    margin-top: 2rem;
    flex-wrap: wrap;
}

/* Footer */
.footer-magico {
    background: rgba(10, 10, 26, 0.95);
    border-top: 1px solid rgba(255, 255, 255, 0.1);
    text-align: center;
    padding: 1rem;
    margin-top: auto;
}

.footer-magico p { color: #a89cc8; font-size: 0.9rem; }
.footer-magico span { color: #e0b0ff; }

/* Utilidades */
.text-center { text-align: center; }
.mb-3 { margin-bottom: 1.5rem; }
.mt-4 { margin-top: 2rem; }

/* Responsive */
@media (max-width: 600px) {
    .titulo-magico { font-size: 1.5rem; }
    .historial-grid { grid-template-columns: 1fr; }
    .navbar-magica .container { flex-direction: column; gap: 0.5rem; }
    .acciones-centradas { flex-direction: column; align-items: center; }
}
```

> El CSS es el "traje" de la web. No necesitas entenderlo línea por línea. Lo importante: se enlaza con `<link href="{{ url_for('static', path='style.css') }}">`. `url_for('static', ...)` usa el `name="static"` que definiste en `app.mount("/static", StaticFiles(directory="static"), name="static")`.

## 2.2 La plantilla base: `templates/base.html`

Este es EL corazón de Jinja2. Una plantilla que las demás heredan:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>{% block titulo %}Máquina Mágica{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', path='style.css') }}" />
</head>
<body>
    <header class="navbar-magica">
        <div class="container">
            <a class="nav-brand" href="{{ url_for('inicio') }}">🔮 Máquina Mágica</a>
            <nav class="nav-links">
                <a href="{{ url_for('inicio') }}">Inicio</a>
                <a href="{{ url_for('historial') }}">Historial</a>
            </nav>
        </div>
    </header>

    <main class="main-content">
        {% block contenido %}{% endblock %}
    </main>

    <footer class="footer-magico">
        <p>Hecho con <span>💜</span> — {{ ano_actual }}</p>
    </footer>
</body>
</html>
```

### 🧠 Jinja2 explicado: Herencia y bloques

#### `{% block nombre %}...{% endblock %}` — Los huecos

```
<title>{% block titulo %}Máquina Mágica{% endblock %}</title>
        └──────────────┬──────────────────┘
        Crea un hueco con valor por defecto "Máquina Mágica".
        Las páginas hijas pueden reemplazar ese texto.
```

**Analogía:** Es un formulario con respuesta ya escrita. Puedes borrarla y escribir otra, o dejarla.

#### `{% extends "base.html" %}` — El hechizo de herencia

Cada página hija empieza con esta línea. Significa: _"Copia todo el esqueleto de base.html, pero déjame sobrescribir los bloques."_

**Analogía:** `base.html` es un molde de galletas. `{% extends %}` es usar ese molde. `{% block %}` es la cobertura que pones encima.

#### `{{ ano_actual }}` — Variable en la plantilla base

Como `base.html` es la madre, cualquier variable del `context` está disponible en TODAS las páginas hijas. El año aparece en el footer automáticamente.

#### `{{ url_for('nombre_de_ruta') }}` — Generador de URLs

En vez de escribir rutas a mano (`href="/historial"`), Jinja2 + FastAPI te dan `url_for`:

```html
<!-- SIN url_for (rutas quemadas) -->
<a href="/historial">Historial</a>
<form action="/procesar_pregunta" method="POST">

<!-- CON url_for (rutas dinámicas) -->
<a href="{{ url_for('historial') }}">Historial</a>
<form action="{{ url_for('procesar_pregunta') }}" method="POST">
```

**¿Qué hace `url_for`?** Le dices el nombre de la función de Python y él te devuelve la ruta correcta. Si algún día cambias `@app.get("/historial")` por `@app.get("/archivo")`, NO necesitas cambiar ningún HTML — `url_for` se actualiza solo.

**¿De dónde salen los nombres?** Del nombre de la función en `main.py`:

```python
@app.get("/")                →  url_for('inicio')
@app.get("/historial")       →  url_for('historial')
@app.post("/procesar_pregunta")  →  url_for('procesar_pregunta')
@app.get("/respuesta_magica")    →  url_for('respuesta_magica')
```

**¿Y si la ruta tiene parámetros?** Los pasas como argumentos extra:

```python
@app.post("/eliminar_pregunta/{indice}")  →  url_for('eliminar_pregunta', indice=loop.index0)
```

**¿Y para archivos estáticos como el CSS?** Usas el `name` que pusiste en `app.mount`:

```python
# En main.py
app.mount("/static", StaticFiles(directory="static"), name="static")
#                                                        └──┬──┘
#                                                 este nombre es la clave

# En el HTML
<link href="{{ url_for('static', path='style.css') }}">
<!--                └──┬──┘            └────┬────┘
                mismo name           ruta dentro de static/ -->
```

**Regla simple:** `url_for` siempre usa el `name` que definiste en Python, sea una ruta (`name="static"` del mount) o una función (`inicio`, `historial`).

> 🎒 **Analogía:** `url_for` es como el GPS de tu app. En vez de memorizar calles (`/historial`), le dices el nombre del destino (`'historial'`) y él calcula la ruta. Si algún día cambian las calles, tu GPS se actualiza solo.

## 2.3 El formulario real: actualiza `templates/formulario.html`

Reemplaza el formulario simple de la Sesión 1:

```html
{% extends "base.html" %}

{% block titulo %}Pregunta Mágica{% endblock %}

{% block contenido %}
<div class="text-center mb-3">
    <h1 class="titulo-magico">🔮 Pregunta a la Máquina Mágica</h1>
    <p class="subtitulo-magico">Escribe tu pregunta y recibe una respuesta misteriosa...</p>
</div>

<div style="max-width: 600px; margin: 0 auto;">
    <div class="card-magica">
        <form action="{{ url_for('procesar_pregunta') }}" method="POST" class="form-magico">
            <label for="nombre">Tu nombre</label>
            <input type="text" id="nombre" name="nombre" required
                   placeholder="¿Cómo te llamas?" />

            <label for="pregunta">Tu pregunta</label>
            <textarea id="pregunta" name="pregunta" required
                      placeholder="¿Qué quieres saber?" rows="4"></textarea>

            <button type="submit" class="btn-magico">🎲 Preguntar</button>
        </form>
    </div>
</div>

<div class="acciones-centradas mt-4">
    <a href="{{ url_for('historial') }}" class="btn-secundario">📜 Ver historial</a>
</div>
{% endblock %}
```

### 🧠 Atención: `name="nombre"` debe coincidir con `Form(...)` en Python

```
HTML:  <input name="nombre" ...>      Python: nombre: str = Form(...)
HTML:  <textarea name="pregunta" ...> Python: pregunta: str = Form(...)
       └───────── coinciden ──────────┘
```

**El `name` del HTML es el puente entre formulario y Python.** Si no coinciden exactamente, no funciona.

## 2.4 Verifica

```bash
fastapi dev main.py
```

Abre http://127.0.0.1:8000 → Fondo oscuro, navbar, formulario visible. El botón aún no hace nada (lo arreglamos en Sesión 3).

---

## ✅ Checklist Sesión 2

- [ ] `static/style.css` y `templates/base.html` copiados
- [ ] `templates/formulario.html` actualizado con herencia
- [ ] Entiendes `{% extends %}` (herencia)
- [ ] Entiendes `{% block %}` (huecos reemplazables)
- [ ] Entiendes que `name="..."` en HTML ↔ `Form(...)` en Python

---

# 🧪 SESIÓN 3 — La bola de cristal

**Objetivo:** Formulario funcional. Escribes pregunta → ves respuesta mágica.

## 3.1 `main.py` completo

Reemplaza tu main.py con esta versión final:

```python
import random
from datetime import datetime

from fastapi import FastAPI, Form, Request
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

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
    "Mejor no contar... 👀",
]


@app.get("/", response_class=HTMLResponse)
async def inicio(request: Request):
    return templates.TemplateResponse(
        name="formulario.html",
        request=request,
        context={"ano_actual": datetime.now().year},
    )


@app.post("/procesar_pregunta")
async def procesar_pregunta(nombre: str = Form(...), pregunta: str = Form(...)):
    respuesta = random.choice(respuestas_magicas)
    preguntas_db.append(
        {"nombre": nombre, "pregunta": pregunta, "respuesta": respuesta}
    )
    return RedirectResponse(url="/respuesta_magica", status_code=303)


@app.get("/respuesta_magica", response_class=HTMLResponse)
async def respuesta_magica(request: Request):
    if preguntas_db:
        ultima = preguntas_db[-1]
    else:
        ultima = {"nombre": "", "pregunta": "", "respuesta": ""}
    return templates.TemplateResponse(
        name="respuesta_magica.html",
        request=request,
        context={"request": request, **ultima, "ano_actual": datetime.now().year},
    )


@app.get("/historial", response_class=HTMLResponse)
async def historial(request: Request):
    return templates.TemplateResponse(
        name="historial.html",
        request=request,
        context={
            "request": request,
            "preguntas": preguntas_db,
            "ano_actual": datetime.now().year,
        },
    )


@app.post("/eliminar_pregunta/{indice}")
async def eliminar_pregunta(indice: int):
    if 0 <= indice < len(preguntas_db):
        preguntas_db.pop(indice)
    return RedirectResponse(url="/historial", status_code=303)
```

### 🧠 El viaje completo de los datos (debes LEER esto)

```
1. USUARIO escribe en el formulario y hace clic
        │
2. POST /procesar_pregunta
        │
3. FastAPI recibe los datos con Form(...)
   nombre = "Ana", pregunta = "¿Lloverá?"
        │
4. Python procesa:
   - random.choice() elige respuesta al azar
   - Guarda todo en preguntas_db
   - RedirectResponse → "ve a /respuesta_magica"
        │
5. GET /respuesta_magica
   - Toma la última pregunta: preguntas_db[-1]
   - **ultima desempaca el diccionario en variables sueltas
   - Arma la mochila: {nombre, pregunta, respuesta, ano_actual}
        │
6. Jinja2 abre respuesta_magica.html
   - {{ nombre }}     → "Ana"
   - {{ pregunta }}   → "¿Lloverá?"
   - {{ respuesta }}  → "¡Sí! 🔮"
        │
7. NAVEGADOR recibe HTML limpio (sin {{ }} ni {% %})
```

### Los 3 conceptos nuevos en main.py

| Concepto | Código | Significado |
|----------|--------|-------------|
| `Form(...)` | `nombre: str = Form(...)` | "Este dato viene del formulario HTML. Es obligatorio" |
| `RedirectResponse` | `RedirectResponse(url="/respuesta_magica", status_code=303)` | "Redirige al navegador a otra página" |
| `**ultima` | `**ultima` | Desempaca el diccionario: sus llaves se vuelven variables sueltas |

> ❓ **¿Por qué redirigir en vez de mostrar directo?** Si el usuario recarga la página, un GET es seguro. Un POST recargado enviaría los datos otra vez. Esta técnica se llama Post/Redirect/Get.

## 3.2 Crea `templates/respuesta_magica.html`

```html
{% extends "base.html" %}

{% block titulo %}Respuesta Mágica{% endblock %}

{% block contenido %}
<div class="text-center mb-3">
    <h1 class="titulo-magico">✨ ¡Tu pregunta fue procesada!</h1>
</div>

<div style="max-width: 600px; margin: 0 auto;">
    <div class="card-magica mb-3">
        <p class="text-center" style="color: #a89cc8; margin-bottom: 0.5rem;">
            {{ nombre }} preguntó:
        </p>
        <p class="text-center" style="font-size: 1.15rem; font-style: italic;">
            "{{ pregunta }}"
        </p>
    </div>

    <div class="respuesta-destacada">
        <p class="etiqueta">La máquina mágica responde:</p>
        <p class="respuesta-texto">{{ respuesta }}</p>
    </div>

    <div class="acciones-centradas mt-4">
        <a href="{{ url_for('inicio') }}" class="btn-magico" style="width: auto;">Hacer otra pregunta</a>
        <a href="{{ url_for('historial') }}" class="btn-secundario">📜 Ver historial</a>
    </div>
</div>
{% endblock %}
```

### 🧠 Jinja2: `{{ variable }}` desde diccionario desempacado

```python
# Python hace:
ultima = {"nombre": "Ana", "pregunta": "¿Lloverá?", "respuesta": "¡Sí! 🔮"}
context = {"request": request, **ultima, "ano_actual": 2026}

# La mochila queda:
# {"request": ..., "nombre": "Ana", "pregunta": "¿Lloverá?", "respuesta": "¡Sí! 🔮", "ano_actual": 2026}
```

Sin `**`, tendrías que escribir `{{ ultima.nombre }}` en vez de `{{ nombre }}`.

## 3.3 ¡Pruébalo!

```bash
fastapi dev main.py
```

1. Abre http://127.0.0.1:8000
2. Escribe nombre y pregunta
3. Clic en "🎲 Preguntar"
4. Ves tu pregunta y la respuesta mágica

> 🎮 **Minijuego:** Escribe la misma pregunta 5 veces. ¿Sale siempre igual? (No — `random.choice` elige al azar.)

---

## ✅ Checklist Sesión 3

- [ ] main.py con todas las rutas
- [ ] `respuesta_magica.html` creado
- [ ] El formulario funciona: ves la respuesta
- [ ] Entiendes `Form(...)`, `RedirectResponse`, `**diccionario`
- [ ] Entiendes el viaje: HTML → POST → Python → mochila → Jinja2 → HTML limpio

---

# 🧪 SESIÓN 4 — La biblioteca ancestral

**Objetivo:** Historial con todas las preguntas, botón de eliminar, y reto final.

## 4.1 Crea `templates/historial.html`

```html
{% extends "base.html" %}

{% block titulo %}Historial de Preguntas{% endblock %}

{% block contenido %}
<div class="text-center mb-3">
    <h1 class="titulo-magico">📜 Todas las Preguntas Mágicas</h1>
</div>

{% if preguntas %}
    <p class="contador-preguntas text-center">
        Total de preguntas: {{ preguntas|length }}
    </p>

    <div class="historial-grid">
        {% for item in preguntas %}
            <div class="card-historial">
                <div class="card-historial-header">
                    <span class="nombre">{{ item.nombre }}</span>
                    <span class="numero">#{{ loop.index }}</span>
                </div>
                <p class="pregunta">"{{ item.pregunta }}"</p>
                <p class="respuesta">💬 {{ item.respuesta }}</p>
                <div class="card-historial-footer">
                    <form action="{{ url_for('eliminar_pregunta', indice=loop.index0) }}" method="POST" style="display: inline;">
                        <button type="submit" class="btn-peligro">🗑️ Eliminar</button>
                    </form>
                </div>
            </div>
        {% endfor %}
    </div>
{% else %}
    <div class="estado-vacio">
        <span class="icono">🔮</span>
        <p class="mensaje">No hay preguntas todavía.</p>
        <a href="{{ url_for('inicio') }}" class="btn-magico" style="width: auto;">¡Sé el primero en preguntar!</a>
    </div>
{% endif %}

<div class="acciones-centradas mt-4">
    <a href="{{ url_for('inicio') }}" class="btn-secundario">← Volver al inicio</a>
</div>
{% endblock %}
```

### 🧠 Jinja2 explicado: 4 herramientas nuevas

#### 1. `{% if condicion %}...{% else %}...{% endif %}` — Decisiones

```jinja2
{% if preguntas %}
    ... mostrar historial ...
{% else %}
    ... mostrar "no hay preguntas" ...
{% endif %}
```

**Regla:** Lista vacía = `False`. Lista con elementos = `True`.

#### 2. `{% for item in lista %}...{% endfor %}` — Bucles

```jinja2
{% for item in preguntas %}
    <div>{{ item.nombre }} preguntó: "{{ item.pregunta }}"</div>
    <div>Respuesta: {{ item.respuesta }}</div>
{% endfor %}
```

En cada vuelta, `item` es UN diccionario de la lista. Todo lo que está entre `{% for %}` y `{% endfor %}` se repite.

#### 3. `loop.index` y `loop.index0` — Contador mágico

Dentro de un `{% for %}`, Jinja2 te regala la variable `loop`:

| Variable | Empieza en | Valores |
|----------|-----------|---------|
| `loop.index` | 1 | 1, 2, 3, 4... |
| `loop.index0` | 0 | 0, 1, 2, 3... |

```jinja2
#{{ loop.index }}              ← Muestra #1, #2, #3 (para humanos)
eliminar_pregunta/{{ loop.index0 }}  ← Pasa 0, 1, 2 a Python (índices reales)
```

¿Por qué `loop.index0` para eliminar? Porque `preguntas_db.pop(0)` elimina el primer elemento. `loop.index0` coincide con los índices de Python.

#### 4. `{{ lista|length }}` — Filtros

La barra `|` aplica un filtro. El valor de la izquierda pasa por la tubería y se transforma:

```
[item1, item2, item3]  →  |length  →  3
"ana"                   →  |upper   →  "ANA"
[3, 1, 2]              →  |reverse →  [2, 1, 3]
```

## 4.2 ¿Cómo funciona eliminar?

```
1. Usuario clic en "🗑️ Eliminar"
        │
2. <form> envía POST a /eliminar_pregunta/0
        │
3. FastAPI recibe indice=0 de la URL
        │
4. preguntas_db.pop(0) borra el primer elemento
        │
5. RedirectResponse → vuelve a /historial
        │
6. Historial se recarga SIN la pregunta borrada
```

## 4.3 Tu app completa

Ejecuta `fastapi dev main.py`. Ya tienes todo:

| Ruta | Método | ¿Qué hace? |
|------|--------|------------|
| `/` | GET | Formulario para preguntar |
| `/procesar_pregunta` | POST | Recibe datos, elige respuesta al azar |
| `/respuesta_magica` | GET | Muestra la última respuesta |
| `/historial` | GET | Todas las preguntas guardadas |
| `/eliminar_pregunta/{indice}` | POST | Borra una pregunta |

---

## 🏆 Reto final — Agrega un campo nuevo

Demuestra que entiendes el flujo completo. Agrega un campo `ciudad`:

**1. En `main.py`, agrega el parámetro:**

```python
async def procesar_pregunta(
    nombre: str = Form(...),
    pregunta: str = Form(...),
    ciudad: str = Form(...),       # NUEVO
):
    ...
    preguntas_db.append({
        "nombre": nombre,
        "pregunta": pregunta,
        "respuesta": respuesta,
        "ciudad": ciudad,           # NUEVO
    })
```

**2. En `formulario.html`, agrega el input (antes del botón):**

```html
<label for="ciudad">Tu ciudad</label>
<input type="text" id="ciudad" name="ciudad" required
       placeholder="Ej: Bogotá, Lima, Madrid..." />
```

**3. En `respuesta_magica.html`, muestra la ciudad:**

```html
<p class="text-center" style="color: #a89cc8;">📍 {{ ciudad }}</p>
```

**4. En `historial.html`, muestra la ciudad en cada card:**

```html
<p style="color: #a89cc8; font-size: 0.85rem;">📍 {{ item.ciudad }}</p>
```

Si tu campo nuevo aparece en respuesta e historial... **¡dominaste el flujo!**

---

## 📋 Hoja de trucos Jinja2

| Sintaxis | Qué hace |
|----------|----------|
| `{{ variable }}` | Inserta valor de Python |
| `{{ item.propiedad }}` | Campo de un diccionario |
| `{% if x %}...{% endif %}` | Condición simple |
| `{% if x %}...{% else %}...{% endif %}` | Condición con alternativa |
| `{% for x in lista %}...{% endfor %}` | Bucle |
| `loop.index` | Índice base 1 (1,2,3...) |
| `loop.index0` | Índice base 0 (0,1,2...) |
| `{% extends "base.html" %}` | Hereda plantilla base |
| `{% block nombre %}...{% endblock %}` | Define/reemplaza bloque |
| `{{ url_for('ruta') }}` | Genera URL desde nombre de función |
| `{# comentario #}` | Comentario invisible |
| `|length` | Cantidad de elementos |
| `|reverse` | Invierte lista |
| `|upper` | A mayúsculas |
| `|default("?")` | Valor si no existe |

## 🧠 Los 5 conceptos para siempre

| Concepto | En español | En código |
|----------|-----------|-----------|
| **Mochila (context)** | Diccionario que viaja Python→Jinja2 | `{"nombre": "Ana"}` |
| **Herencia** | Molde que reutilizas | `{% extends "base.html" %}` |
| **Bloques** | Huecos que llenas a tu manera | `{% block contenido %}` |
| **url_for** | GPS de rutas: nombre de función → URL | `url_for('historial')` |
| **Filtros** | Transforman valor al vuelo | `|reverse`, `|length` |
| **Form(...)** | Lee datos del formulario | `nombre: str = Form(...)` |

## 🗺️ Estructura final

```
maquina_magica/
├── main.py
├── static/
│   └── style.css
└── templates/
    ├── base.html
    ├── formulario.html
    ├── respuesta_magica.html
    └── historial.html
```

## 🚀 ¿Y después?

1. **Refuerza herencia** — haz el complemento [Tu Primera Web con Herencia](./herencia_jinja2_simplificado.md) (15 min)
2. **Guardar en archivo JSON** — que los datos sobrevivan al reinicio
3. **Base de datos SQLite** — el siguiente paso natural
4. **Desplegar en Vercel** (gratis) — para que tus amigos lo usen
5. **Agregar más magia** — fecha de nacimiento, signo zodiacal...

---

**🎉 ¡Felicidades!** Construiste tu primera app web con Python, FastAPI y Jinja2. No solo copiaste — entendiste cada paso.
