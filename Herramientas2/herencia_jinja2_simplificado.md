# 🏠 Tu Primera Web — El poder de la herencia
## Complemento ultra-simple de Jinja2 + FastAPI

> **¿Para qué es esto?** Para que vivas en carne propia POR QUÉ existe la herencia de plantillas. Primero harás las cosas "a la antigua" (copiar y pegar código en cada página), sentirás el dolor... y luego descubrirás `{% extends %}` como un superpoder.
>
> **Duración:** 20 minutos. 3 páginas. 3 rutas GET. Cero lógica.
>
> **La promesa:** Al terminar, NUNCA vas a querer volver a copiar un `<nav>` a mano.

---

## 🌍 Las 3 fases de esta misión

```
FASE 1 — SIN herencia (10 min)
   Creas 3 páginas COMPLETAS, cada una con su propio <nav> y <footer>.
   Funciona... pero repetiste código 3 veces.
        │
        ▼
FASE 2 — La revelación (2 min)
   "¿Y si tuvieras 20 páginas? ¿Editarías el footer en 20 archivos?"
   Comparación visual lado a lado del desastre.
        │
        ▼
FASE 3 — CON herencia (8 min)
   Creas base.html UNA vez. Refactorizas las 3 páginas a 4 líneas.
   Momento "¡ahá!" garantizado.
```

---

# 🧱 FASE 1 — Sin herencia (la forma dolorosa)

## 1.1 Crea el proyecto

```bash
mkdir mi_primera_web && cd mi_primera_web
mkdir templates static
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# En Windows: .venv\Scripts\activate
pip install "fastapi[standard]"
```

## 1.2 `main.py`

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
        request=request, name="inicio.html", context={"ano_actual": datetime.now().year},
    )


@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(
        request=request, name="about.html", context={"ano_actual": datetime.now().year},
    )


@app.get("/contacto", response_class=HTMLResponse)
async def contacto(request: Request):
    return templates.TemplateResponse(
        request=request, name="contacto.html", context={"ano_actual": datetime.now().year},
    )
```

## 1.3 `static/style.css`

```css
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}

body {
    font-family: system-ui, sans-serif;
    line-height: 1.6;
    min-height: 100vh;
    display: flex;
    flex-direction: column;
    background: #f5f5f5;
    color: #333;
}

nav {
    background: #4a1a7a;
    padding: 1rem 2rem;
    display: flex;
    gap: 2rem;
}

nav a {
    color: #e0b0ff;
    text-decoration: none;
    font-weight: 600;
}

nav a:hover {
    color: white;
}

main {
    flex: 1;
    max-width: 700px;
    width: 100%;
    margin: 2rem auto;
    padding: 0 1.5rem;
}

h1 {
    color: #4a1a7a;
    margin-bottom: 1rem;
}

footer {
    text-align: center;
    padding: 1rem;
    background: #333;
    color: #aaa;
    font-size: 0.9rem;
}
```

## 1.4 Las 3 páginas — cada una completa, con su propio `<nav>` y `<footer>`

### `templates/inicio.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Inicio — Mi Web</title>
    <link rel="stylesheet" href="{{ url_for('static', path='style.css') }}">
</head>
<body>
    <nav>
        <a href="/">🏠 Inicio</a>
        <a href="/about">🙋 Sobre mí</a>
        <a href="/contacto">📧 Contacto</a>
    </nav>

    <main>
        <h1>👋 ¡Bienvenido a mi primera web!</h1>
        <p>Esta página fue creada con <strong>FastAPI</strong> y <strong>Jinja2</strong>.</p>
        <p>El año actual es: <strong>{{ ano_actual }}</strong></p>
    </main>

    <footer>
        <p>© {{ ano_actual }} — Hecho con FastAPI + Jinja2</p>
    </footer>
</body>
</html>
```

### `templates/about.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sobre mí — Mi Web</title>
    <link rel="stylesheet" href="{{ url_for('static', path='style.css') }}">
</head>
<body>
    <nav>
        <a href="/">🏠 Inicio</a>
        <a href="/about">🙋 Sobre mí</a>
        <a href="/contacto">📧 Contacto</a>
    </nav>

    <main>
        <h1>🙋 Sobre mí</h1>
        <p>Estoy aprendiendo a crear páginas web con Python.</p>
        <p>Antes pensaba que hacer una web requería saber 10 lenguajes.</p>
    </main>

    <footer>
        <p>© {{ ano_actual }} — Hecho con FastAPI + Jinja2</p>
    </footer>
</body>
</html>
```

### `templates/contacto.html`

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contacto — Mi Web</title>
    <link rel="stylesheet" href="{{ url_for('static', path='style.css') }}">
</head>
<body>
    <nav>
        <a href="/">🏠 Inicio</a>
        <a href="/about">🙋 Sobre mí</a>
        <a href="/contacto">📧 Contacto</a>
    </nav>

    <main>
        <h1>📧 Contacto</h1>
        <p>¿Te gustó lo que viste? Escríbeme:</p>
        <ul>
            <li>Email: aprendiz@fastapi.dev</li>
            <li>GitHub: github.com/aprendiz</li>
        </ul>
    </main>

    <footer>
        <p>© {{ ano_actual }} — Hecho con FastAPI + Jinja2</p>
    </footer>
</body>
</html>
```

## 1.5 Ejecuta

```bash
fastapi dev main.py
```

Visita las 3 páginas:
- http://127.0.0.1:8000 → Inicio
- http://127.0.0.1:8000/about → Sobre mí
- http://127.0.0.1:8000/contacto → Contacto

Funciona. Todo bien. Pero...

---

# 💡 FASE 2 — La revelación

**Mira con atención las 3 páginas que escribiste:**

```
inicio.html     about.html      contacto.html
───────────     ───────────     ──────────────
<nav>           <nav>           <nav>
  ...links...     ...links...     ...links...
</nav>          </nav>          </nav>
<main>          <main>          <main>
  ÚNICO que       ÚNICO que       ÚNICO que
  CAMBIA          CAMBIA          CAMBIA
</main>         </main>         </main>
<footer>        <footer>        <footer>
  © 2026          © 2026          © 2026
</footer>       </footer>       </footer>
```

**El `<nav>` y el `<footer>` son IDÉNTICOS en las 3 páginas.** Lo único que cambia es lo que está dentro de `<main>`.

### 🤔 Ahora imagina...

| Si tuvieras... | Editar el footer implicaría... |
|----------------|-------------------------------|
| 3 páginas | Editar 3 archivos |
| 10 páginas | Editar 10 archivos |
| 50 páginas | Editar 50 archivos |
| Una red social con 200 páginas | 😱 Pesadilla |

Cada vez que quieras cambiar el color del navbar, agregar un link, o modificar el footer... toca ir archivo por archivo.

**Esto es un problema real.** Y Jinja2 lo resuelve con herencia.

---

# ✨ FASE 3 — Con herencia (la solución elegante)

## 3.1 El antes y el después (un vistazo)

```
                           ANTES                                  DESPUÉS
                    ┌──────────────────┐              ┌──────────────────────────┐
                    │ inicio.html      │              │ base.html                │
                    │  - nav (copiado) │              │  - nav (1 sola vez)      │
                    │  - contenido     │              │  - footer (1 sola vez)   │
                    │  - footer        │              │  - {% block contenido %} │
                    └──────────────────┘              └──────┬────────┬──────────┘
                    ┌──────────────────┘                     │        │
                    │ about.html                  ┌──────────┘  ┌─────┴──────────┐
                    │  - nav (copiado)            ▼             ▼                ▼
                    │  - contenido          inicio.html    about.html     contacto.html
                    │  - footer             (4 líneas)     (4 líneas)      (4 líneas)
                    └──────────────────┘
                    ┌──────────────────┘
                    │ contacto.html
                    │  - nav (copiado)
                    │  - contenido
                    │  - footer
                    └──────────────────┘

    ~70 líneas de HTML en total                     ~40 líneas de HTML en total
    Nav repetido 3 veces                           Nav escrito 1 sola vez
```

## 3.2 Crea `templates/base.html` — UNA sola vez

**Borra los `<nav>` y `<footer>` de las 3 páginas** y ponlos aquí:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block titulo %}Mi Web{% endblock %}</title>
    <link rel="stylesheet" href="{{ url_for('static', path='style.css') }}">
</head>
<body>
    <nav>
        <a href="/">🏠 Inicio</a>
        <a href="/about">🙋 Sobre mí</a>
        <a href="/contacto">📧 Contacto</a>
    </nav>

    <main>
        {% block contenido %}{% endblock %}
    </main>

    <footer>
        <p>© {{ ano_actual }} — Hecho con FastAPI + Jinja2</p>
    </footer>
</body>
</html>
```

### 🧠 ¿Qué es `{% block %}`?

```
{% block titulo %}Mi Web{% endblock %}
└─────┬─────┘  └──┬──┘  └────┬────┘
 "Esto es un  "valor por  "fin del
  bloque"      defecto"    bloque"
```

**Traducción:** "Aquí va el título. Si ninguna página hija dice lo contrario, será 'Mi Web'."

```
{% block contenido %}{% endblock %}
└──────┬──────┘      └────┬────┘
 "Aquí va el         "vacío por
  cuerpo"             defecto"
```

**Traducción:** "Aquí va el contenido de cada página. Por defecto no hay nada."

> 🧩 **Analogía:** `base.html` es un molde de galletas. Tiene la forma base (nav + footer). `{% block contenido %}` es el espacio donde cada página pone su "cobertura" (chocolate, vainilla, fresa).

## 3.3 Refactoriza las 3 páginas — de ~25 líneas a ~8 líneas cada una

### `templates/inicio.html` (reemplaza TODO el contenido anterior)

```html
{% extends "base.html" %}

{% block titulo %}Inicio — Mi Web{% endblock %}

{% block contenido %}
<h1>👋 ¡Bienvenido a mi primera web!</h1>
<p>Esta página fue creada con <strong>FastAPI</strong> y <strong>Jinja2</strong>.</p>
<p>El año actual es: <strong>{{ ano_actual }}</strong></p>
{% endblock %}
```

### `templates/about.html` (reemplaza TODO)

```html
{% extends "base.html" %}

{% block titulo %}Sobre mí — Mi Web{% endblock %}

{% block contenido %}
<h1>🙋 Sobre mí</h1>
<p>Estoy aprendiendo a crear páginas web con Python.</p>
{% endblock %}
```

### `templates/contacto.html` (reemplaza TODO)

```html
{% extends "base.html" %}

{% block titulo %}Contacto — Mi Web{% endblock %}

{% block contenido %}
<h1>📧 Contacto</h1>
<p>¿Te gustó lo que viste? Escríbeme:</p>
<ul>
    <li>Email: aprendiz@fastapi.dev</li>
    <li>GitHub: github.com/aprendiz</li>
</ul>
{% endblock %}
```

## 3.4 Ejecuta y compara

```bash
fastapi dev main.py
```

Visita las 3 páginas. **Se ven EXACTAMENTE IGUAL que antes.** Pero ahora:

- El `<nav>` está en 1 archivo, no en 3
- El `<footer>` está en 1 archivo, no en 3
- Cada página solo tiene **4 líneas de Jinja2 + su contenido único**

## 3.5 La prueba definitiva — cambia algo y mira

En `base.html`, cambia el color del nav (línea del `background`):

```css
/* En base.html, dentro del <nav style="..."> */
style="background: #e74c3c;"
```

O mejor, cambia el texto del footer:

```html
<footer>
    <p>© {{ ano_actual }} — Creado por [TU NOMBRE] con FastAPI</p>
</footer>
```

Recarga las 3 páginas. **Las 3 cambiaron.** Tocaste 1 archivo, se actualizaron todas.

> 🎉 **Acabas de vivir el "¡ahá!" de la herencia.** Editando 1 archivo (`base.html`), impactaste 3 páginas. Con 50 páginas, el impacto sería el mismo: editas 1, se actualizan 50.

---

## 🧠 `{% extends %}` explicado línea por línea

```html
{% extends "base.html" %}
└──────┬──────┘
  "Copia TODO el HTML de base.html como punto de partida"

{% block titulo %}Inicio — Mi Web{% endblock %}
└──────┬──────┘  └──────┬──────┘  └────┬────┘
 "Voy a         "Este es el    "Terminé"
  cambiar..."     nuevo valor"

{% block contenido %}
<h1>Mi HTML aquí</h1>
{% endblock %}
└──────┬──────┘
 "Lo que sea que ponga aquí, reemplaza
  el bloque vacío de base.html"
```

| Sintaxis | Traducción para humanos |
|----------|------------------------|
| `{% extends "base.html" %}` | "Esta página usa el molde base.html" |
| `{% block titulo %}...{% endblock %}` | "Cambio el título que está en el molde" |
| `{% block contenido %}...{% endblock %}` | "Lleno el cuerpo que el molde dejó vacío" |
| `{{ ano_actual }}` | "Python, pásame el año por la mochila" |

---

## 🔗 `url_for`: el GPS de tus rutas

En vez de escribir rutas a mano que se rompen si las cambias:

Mira el `name` en `app.mount` para archivos estáticos:

```python
# En main.py
app.mount("/static", StaticFiles(directory="static"), name="static")

# En base.html
<link href="{{ url_for('static', path='style.css') }}">
```

> 🎒 **Analogía:** Es como guardar un contacto en el celular. En vez de memorizar el número, le pones nombre y el celular marca solo.

---

## 🏆 Reto: Pasa tu nombre desde Python

En `main.py`, modifica la ruta `/about`:

```python
@app.get("/about", response_class=HTMLResponse)
async def about(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="about.html",
        context={
            "ano_actual": datetime.now().year,
            "nombre": "TU NOMBRE AQUI",
        },
    )
```

En `about.html`, usa la variable:

```html
{% block contenido %}
<h1>🙋 Sobre mí</h1>
<p>Me llamo <strong>{{ nombre }}</strong> y estoy aprendiendo a crear webs con Python.</p>
{% endblock %}
```

¡Acabas de cerrar el círculo: Python → mochila → Jinja2 → HTML!

---

## 📋 Resumen: lo que te llevas

### El antes y el después en números

| | Sin herencia | Con herencia |
|---|-------------|-------------|
| Líneas totales | ~70 | ~40 |
| `<nav>` escrito | 3 veces | 1 vez |
| `<footer>` escrito | 3 veces | 1 vez |
| Cambiar el footer | Editar 3 archivos | Editar 1 archivo |
| Agregar una página nueva | Copiar 20 líneas | Escribir 6 líneas |

### Las 4 sintaxis clave

| Sintaxis | Significado |
|----------|-------------|
| `{% extends "base.html" %}` | "Uso el molde base.html" |
| `{% block nombre %}...{% endblock %}` | "Cambio/lleno esta parte del molde" |
| `{{ variable }}` | "Python, pásame este dato" |
| `{{ url_for('ruta') }}` | "Dame la URL de esta función" |

---

## 🔗 ¿Y ahora?

Ya entendiste POR QUÉ existe la herencia. Ahora aprende a usarla en una app de verdad: **[La Máquina Mágica](./fastapi_jinja2_para_adolescentes.md)** — formularios, POST, bucles, condiciones y una bola de cristal digital.
