# 🌐 HTML Semántico: Construyendo la Web con Sentido

> **Nivel:** Principiante · **Duración total:** 4 horas · **Edad recomendada:** 15–16 años
>
> *"El código que escribes hoy es el mensaje que le dejas al navegador — y a las personas — del mañana."*

---

## 📋 Tabla de Contenidos

1. [¿Qué vamos a aprender hoy?](#-qué-vamos-a-aprender-hoy)
2. [Módulo 1 — Análisis de Estructuras Web](#-módulo-1--análisis-de-estructuras-web)
3. [Módulo 2 — Etiquetas Semánticas en Detalle](#-módulo-2--etiquetas-semánticas-en-detalle)
4. [⏸️ Descanso 1](#%EF%B8%8F-descanso-1--120-minutos)
5. [Módulo 3 — Práctica Guiada](#-módulo-3--práctica-guiada)
6. [⏸️ Descanso 2](#%EF%B8%8F-descanso-2--195-minutos)
7. [Módulo 4 — Código Desorganizado vs. Estructurado](#-módulo-4--código-desorganizado-vs-estructurado)
8. [Proyecto Final del Día](#-proyecto-final-del-día)
9. [Glosario](#-glosario)
10. [Recursos para Seguir Aprendiendo](#-recursos-para-seguir-aprendiendo)

---

## 🎯 ¿Qué vamos a aprender hoy?

### Objetivos de la sesión

Al terminar este taller serás capaz de:

- ✅ Identificar las etiquetas estructurales y semánticas de HTML5
- ✅ Analizar la arquitectura de una página web real
- ✅ Construir un documento HTML correctamente organizado
- ✅ Distinguir entre código desordenado y código profesional
- ✅ Explicar *por qué* la semántica importa más allá del aspecto visual

### ¿Qué necesitas?

| Herramienta | ¿Para qué? | ¿Dónde conseguirla? |
|---|---|---|
| Un navegador web | Ver el resultado | Chrome, Firefox o Edge |
| Un editor de código | Escribir HTML | [VS Code](https://code.visualstudio.com/) (recomendado) |
| Ganas de experimentar | ¡Lo más importante! | Ya las tienes 😄 |

### ¿Cuánto tiempo tenemos?

```
⏱  0:00 - 2:00  →  Módulos 1 y 2
⏸  2:00 - 2:15  →  Descanso 1
⏱  2:15 - 3:15  →  Módulo 3 (práctica guiada)
⏸  3:15 - 3:30  →  Descanso 2
⏱  3:30 - 4:00  →  Módulo 4 + Proyecto final
```

---

## 🔬 Módulo 1 — Análisis de Estructuras Web

> ⏱ **Tiempo estimado: 60 minutos**

### 1.1 Antes de escribir código: ¡Observa!

Antes de crear una página web, los desarrolladores hacen algo que parece simple pero es muy poderoso: **observar otras páginas**. Abre cualquier sitio web (una noticia, una tienda en línea, un blog) y hazte estas preguntas:

- ¿Dónde está el logo y el menú de navegación?
- ¿Dónde está el contenido principal?
- ¿Hay una barra lateral con información extra?
- ¿Dónde están los links de redes sociales o el aviso legal?

Notarás que casi **todas** las páginas web siguen un patrón similar. Eso no es casualidad — es diseño estructural.

---

### 1.2 La Anatomía de una Página Web

Imagina que una página web es como un periódico físico:

```
┌─────────────────────────────────────────────┐
│              NOMBRE DEL PERIÓDICO           │  ← Encabezado (Header)
│         Menú: Noticias | Deportes | Cultura │  ← Navegación (Nav)
├──────────────────────────┬──────────────────┤
│                          │                  │
│   NOTICIA PRINCIPAL      │  Clima hoy       │  ← Artículo + Aside
│   Lorem ipsum dolor...   │  Publicidad      │
│                          │  Últimas noticias│
│   SEGUNDA NOTICIA        │                  │
│   Sit amet consectetur...│                  │
│                          │                  │
├──────────────────────────┴──────────────────┤
│  Contacto | Términos | Redes Sociales       │  ← Pie de página (Footer)
└─────────────────────────────────────────────┘
```

En HTML5, cada una de esas secciones tiene su **propia etiqueta semántica**.

---

### 1.3 HTML Antiguo vs. HTML5: La Revolución Semántica

**¿Sabías que antes todo se hacía con `<div>`?**

Antes de HTML5 (antes de 2014, aproximadamente), los desarrolladores usaban etiquetas genéricas para todo. Así se veía una página típica:

```html
<!-- 🚫 FORMA ANTIGUA — HTML 4 -->
<div id="cabecera">
  <div id="logo">Mi Sitio</div>
  <div id="menu">Inicio | Blog | Contacto</div>
</div>

<div id="contenido-principal">
  <div class="articulo">
    <div class="titulo">Mi primera entrada</div>
    <div class="texto">Aquí va el contenido...</div>
  </div>
</div>

<div id="barra-lateral">
  <div class="widget">Categorías</div>
</div>

<div id="pie">
  <div class="links">Contacto | Privacidad</div>
</div>
```

**¿Cuál es el problema con esto?**

1. 🤖 **Los buscadores no entienden nada.** Google no sabe qué parte es el menú y qué parte es contenido importante.
2. ♿ **Las personas con discapacidad visual tampoco.** Los lectores de pantalla no pueden navegarla bien.
3. 👨‍💻 **Es difícil de mantener.** Cuando el código crece, se vuelve un laberinto de `<div>` anidados.

**Con HTML5, esto cambió:**

```html
<!-- ✅ FORMA MODERNA — HTML5 -->
<header>
  <img src="logo.png" alt="Mi Sitio">
  <nav>Inicio | Blog | Contacto</nav>
</header>

<main>
  <article>
    <h1>Mi primera entrada</h1>
    <p>Aquí va el contenido...</p>
  </article>
</main>

<aside>
  <section>Categorías</section>
</aside>

<footer>
  <p>Contacto | Privacidad</p>
</footer>
```

Mismo resultado visual. Pero ahora el código *habla* — le dice al mundo qué es cada cosa.

---

### 1.4 Actividad: Desarmando una Página Real

> 🛠️ **Tiempo: 20 minutos**

**Instrucciones:**

1. Abre cualquier sitio web en tu navegador (sugerencia: un periódico digital o Wikipedia).
2. Haz clic derecho sobre cualquier parte de la página y selecciona **"Inspeccionar"** o **"Inspeccionar elemento"**.
3. En el panel que aparece, busca estas etiquetas: `<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`, `<footer>`.

**Completa esta tabla en tu cuaderno:**

| Etiqueta encontrada | ¿Qué contenido tiene? | ¿Dónde aparece visualmente? |
|---|---|---|
| `<header>` | | |
| `<nav>` | | |
| `<main>` | | |
| `<article>` | | |
| `<footer>` | | |

**Pregunta para reflexionar:** ¿Encontraste alguna etiqueta que no conocías? ¿Qué crees que hace?

---

### 1.5 El Árbol DOM: Cómo el Navegador Lee tu HTML

Cuando escribes HTML, el navegador no lo lee como texto plano. Lo convierte en una estructura llamada **DOM** (*Document Object Model* — Modelo de Objeto de Documento). Piénsalo como un árbol genealógico:

```
html
├── head
│   ├── meta
│   ├── title
│   └── link
└── body
    ├── header
    │   ├── h1  ←── hijo de header
    │   └── nav
    │       ├── a  ←── hijo de nav
    │       └── a
    ├── main
    │   └── article
    │       ├── h2
    │       └── p
    └── footer
        └── p
```

**Conceptos clave del árbol DOM:**

- **Elemento padre:** el que contiene a otros (ej: `<nav>` es padre de `<a>`)
- **Elemento hijo:** el que está dentro de otro (ej: `<h1>` es hijo de `<header>`)
- **Elementos hermanos:** los que comparten el mismo padre (ej: `<header>`, `<main>` y `<footer>` son hermanos)

> 💡 **Dato curioso:** Los navegadores usan este árbol para saber qué estilos CSS aplicar y cómo responder a los eventos de JavaScript. ¡Todo parte de un buen HTML!

---

## 📖 Módulo 2 — Etiquetas Semánticas en Detalle

> ⏱ **Tiempo estimado: 60 minutos**

### 2.1 El "Esqueleto" Básico de Todo Documento HTML

Antes de hablar de semántica, aquí está la base mínima que **siempre** debe tener un archivo `.html`:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Título de mi página</title>
</head>
<body>
    <!-- Aquí va todo el contenido visible -->
</body>
</html>
```

**Desglose línea a línea:**

| Línea | ¿Qué hace? |
|---|---|
| `<!DOCTYPE html>` | Le dice al navegador: "esto es HTML5" |
| `<html lang="es">` | Inicio del documento; `lang="es"` indica que está en español |
| `<head>` | Información *sobre* la página (no se ve en pantalla) |
| `<meta charset="UTF-8">` | Permite tildes, ñ y caracteres especiales |
| `<meta name="viewport"...>` | Hace la página responsive (adaptable a móvil) |
| `<title>` | El texto que aparece en la pestaña del navegador |
| `<body>` | Todo el contenido que el usuario ve |

---

### 2.2 Etiquetas de Estructura Principal

#### `<header>` — El Encabezado

```html
<header>
    <img src="logo.png" alt="Logo de mi empresa">
    <h1>Mi Sitio Web Increíble</h1>
    <nav>
        <a href="/">Inicio</a>
        <a href="/blog">Blog</a>
        <a href="/contacto">Contacto</a>
    </nav>
</header>
```

**¿Qué va en `<header>`?**
- ✅ Logo del sitio
- ✅ Título principal o nombre de la marca
- ✅ Menú de navegación principal
- ✅ Barra de búsqueda

**¿Qué NO va en `<header>`?**
- ❌ El contenido principal del artículo
- ❌ Formularios de contacto
- ❌ Publicidad

> ⚠️ **Importante:** `<header>` puede aparecer más de una vez en la página. Puede haber un `<header>` para toda la página *y* un `<header>` dentro de un `<article>` (para el encabezado de ese artículo específico).

---

#### `<nav>` — La Navegación

```html
<nav aria-label="Menú principal">
    <ul>
        <li><a href="/">🏠 Inicio</a></li>
        <li><a href="/tutoriales">📚 Tutoriales</a></li>
        <li><a href="/proyectos">💻 Proyectos</a></li>
        <li><a href="/contacto">✉️ Contacto</a></li>
    </ul>
</nav>
```

**¿Para qué sirve `<nav>`?**

No todos los grupos de enlaces son una navegación. `<nav>` se usa específicamente para los **conjuntos de links principales** que permiten moverse por el sitio. No uses `<nav>` para un simple enlace suelto o para links dentro del contenido de un artículo.

**Cuándo usarla:**
- ✅ Menú principal del sitio
- ✅ Menú del pie de página
- ✅ Tabla de contenidos de un artículo largo
- ❌ Un enlace "Haz clic aquí" dentro de un párrafo

---

#### `<main>` — El Contenido Principal

```html
<main>
    <!-- Aquí va lo más importante de la página -->
    <!-- Solo debe haber UN <main> por página -->
    <h1>Bienvenido a mi blog de tecnología</h1>
    <p>Aquí encontrarás tutoriales, noticias y reflexiones sobre el mundo digital.</p>
    
    <article>...</article>
    <article>...</article>
</main>
```

**Reglas de oro de `<main>`:**
1. Solo puede haber **UN** `<main>` por página.
2. No debe estar dentro de `<header>`, `<footer>`, `<aside>` ni `<nav>`.
3. Contiene el contenido único y principal — lo que diferencia *esta* página de las demás.

---

#### `<article>` — El Artículo Independiente

```html
<article>
    <header>
        <h2>Cómo aprendí a programar a los 15 años</h2>
        <p>Publicado el <time datetime="2024-03-15">15 de marzo, 2024</time></p>
        <p>Por <span>Ana García</span></p>
    </header>
    
    <p>Todo empezó cuando mi profesor de informática nos retó a crear nuestra primera página web...</p>
    
    <section>
        <h3>El primer obstáculo</h3>
        <p>Al principio, el código parecía un idioma extraterrestre...</p>
    </section>
    
    <footer>
        <p>Etiquetas: HTML, Programación, Jóvenes</p>
    </footer>
</article>
```

**¿Cómo saber si algo merece ser un `<article>`?**

Hazte esta pregunta: *¿Tendría sentido este contenido si lo copiara y pegara en otro sitio web?*

- Una entrada de blog → ✅ `<article>`
- Una tarjeta de producto en una tienda → ✅ `<article>`
- Un comentario de usuario → ✅ `<article>` (puede estar anidado)
- El menú de navegación → ❌ No es un artículo

---

#### `<section>` — La Sección Temática

```html
<section>
    <h2>Nuestros Servicios</h2>
    
    <article>
        <h3>Diseño Web</h3>
        <p>Creamos sitios modernos y responsivos...</p>
    </article>
    
    <article>
        <h3>Desarrollo de Apps</h3>
        <p>Aplicaciones móviles para iOS y Android...</p>
    </article>
</section>
```

**`<section>` vs. `<article>`: ¿Cuál usar?**

| Característica | `<article>` | `<section>` |
|---|---|---|
| ¿Tiene sentido solo? | Sí, es independiente | No necesariamente |
| ¿Tiene un tema propio? | Sí | Sí |
| Ejemplos | Post de blog, noticia | Capítulo, pestaña, bloque temático |
| ¿Puede contener al otro? | Sí (`<article>` dentro de `<section>`) | Sí (`<section>` dentro de `<article>`) |

> 💡 **Truco mental:** Si le pondrías un título, probablemente merece ser `<section>`. Si funciona solo fuera de contexto, probablemente merece ser `<article>`.

---

#### `<aside>` — El Contenido Complementario

```html
<aside>
    <h3>Artículos relacionados</h3>
    <ul>
        <li><a href="#">5 trucos de CSS que no conocías</a></li>
        <li><a href="#">Cómo organizar tus proyectos en GitHub</a></li>
    </ul>
    
    <h3>Sobre el autor</h3>
    <p>Ana es desarrolladora web con 3 años de experiencia...</p>
</aside>
```

**`<aside>` sirve para contenido que complementa el principal pero no es esencial:**

- Barras laterales (*sidebars*)
- Notas al margen
- Publicidad relacionada con el tema
- Datos curiosos o definiciones
- Biografías de autores

---

#### `<footer>` — El Pie de Página

```html
<footer>
    <section>
        <h3>Contacto</h3>
        <p>📧 hola@misitio.com</p>
        <p>📍 Bogotá, Colombia</p>
    </section>
    
    <section>
        <h3>Síguenos</h3>
        <nav aria-label="Redes sociales">
            <a href="#">Instagram</a>
            <a href="#">Twitter/X</a>
            <a href="#">YouTube</a>
        </nav>
    </section>
    
    <p>© 2024 Mi Sitio Web. Todos los derechos reservados.</p>
</footer>
```

Al igual que `<header>`, `<footer>` puede aparecer tanto a nivel de página como dentro de un `<article>`.

---

### 2.3 Etiquetas de Contenido Semántico

Además de las estructurales, hay etiquetas que dan **significado** a partes específicas del texto:

#### Etiquetas de texto semántico

```html
<!-- Tiempo y fechas -->
<time datetime="2024-12-25">Navidad 2024</time>

<!-- Énfasis importante (no solo negrita visual) -->
<strong>¡Atención! Este es un aviso crítico.</strong>

<!-- Énfasis con énfasis de voz -->
<em>Este término es especialmente relevante.</em>

<!-- Abreviaciones con explicación -->
<abbr title="HyperText Markup Language">HTML</abbr>

<!-- Código dentro de texto -->
<p>Usa la etiqueta <code>&lt;nav&gt;</code> para la navegación.</p>

<!-- Texto marcado/resaltado -->
<p>El concepto más importante es <mark>la semántica web</mark>.</p>

<!-- Texto tachado (ya no es relevante) -->
<p><s>Precio anterior: $50.000</s> Ahora: $35.000</p>

<!-- Citas en bloque -->
<blockquote cite="https://www.w3.org">
    <p>La web está diseñada para funcionar para todas las personas,
    independientemente del hardware, software, idioma o capacidad.</p>
    <footer>— W3C, principios de diseño web</footer>
</blockquote>

<!-- Cita en línea -->
<p>Como dijo Tim Berners-Lee: <q>La web es más una creación social que técnica.</q></p>

<!-- Figura con descripción (imágenes, diagramas, código) -->
<figure>
    <img src="diagrama-html.png" alt="Diagrama de la estructura HTML5">
    <figcaption>Figura 1: Estructura básica de un documento HTML5</figcaption>
</figure>
```

---

### 2.4 El Papel Fundamental de la Semántica

¿Por qué molestarse en todo esto si visualmente se ve igual? Hay tres razones poderosas:

#### 1. 🔍 SEO — Los buscadores te encuentran mejor

Google, Bing y otros buscadores "leen" tu HTML. Un buen uso de semántica les dice:
- Cuál es el **título principal** de la página (`<h1>`)
- Cuál es el **artículo** principal (`<article>`)
- Cuál es el **menú** de navegación (`<nav>`)

Resultado: tu página aparece más arriba en los resultados de búsqueda.

#### 2. ♿ Accesibilidad — La web para todos

Aproximadamente **1 de cada 6 personas** en el mundo vive con algún tipo de discapacidad. Los lectores de pantalla (software que lee el contenido en voz alta) usan las etiquetas semánticas para:
- Saltar directamente al `<main>` sin leer el menú
- Anunciar "navegación principal" cuando encuentran `<nav>`
- Listar todos los `<article>` del documento

**Un código bien escrito puede cambiar la experiencia de alguien.**

#### 3. 👥 Trabajo en equipo — Código que otros entienden

Cuando trabajas en equipo (algo muy común en el mundo laboral), un código semántico es un código que cualquier compañero puede entender sin que se lo expliques. `<article>` habla por sí mismo. `<div class="cosa-principal-2">` no.

---

### 2.5 Mini-Quiz: ¿Qué etiqueta usarías?

Antes de seguir, pon a prueba lo que aprendiste. Para cada situación, piensa qué etiqueta semántica usarías:

1. El menú con links de "Inicio, Nosotros, Blog, Contacto"
2. Un post completo de Instagram que se podría compartir solo
3. La sección de "Últimas noticias" de la página principal de un periódico
4. El pie de página con el copyright y redes sociales
5. Una barra lateral con "Artículos más leídos"
6. El bloque que contiene el logo y el menú superior del sitio
7. El contenido central único de la página

<details>
<summary>🔑 Ver respuestas</summary>

1. `<nav>`
2. `<article>`
3. `<section>` (contiene varios artículos)
4. `<footer>`
5. `<aside>`
6. `<header>`
7. `<main>`

</details>

---

## ⏸️ Descanso 1 — ⏱ 120 minutos

```
╔══════════════════════════════════════════════════════╗
║                                                      ║
║   🎉  ¡Excelente trabajo! Llevas 2 horas aprendiendo ║
║                                                      ║
║   ⏰  Tómate 15 minutos:                             ║
║       • Estira el cuerpo — mueve el cuello y brazos  ║
║       • Hidratación: toma agua 💧                    ║
║       • Aleja la vista de la pantalla 👀             ║
║       • Comenta con un compañero qué etiqueta        ║
║         te pareció más interesante                   ║
║                                                      ║
║   🕐  Continuamos en 15 minutos con la práctica      ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
```

---

## 💻 Módulo 3 — Práctica Guiada

> ⏱ **Tiempo estimado: 60 minutos**

En este módulo vas a construir una página web real, paso a paso. Vamos a crear **el sitio web de una revista de tecnología juvenil**. Al final tendrás una página funcional y correctamente estructurada.

### 3.1 Paso 1: Crear el Archivo

1. Abre VS Code (o tu editor favorito)
2. Crea una nueva carpeta llamada `revista-tech`
3. Dentro de esa carpeta, crea un archivo llamado `index.html`
4. Copia el esqueleto básico:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>TechJoven - La revista de tecnología para jóvenes</title>
</head>
<body>

    <!-- Aquí iremos agregando el contenido -->

</body>
</html>
```

Guarda el archivo (`Ctrl+S`) y ábrelo en el navegador. Verás una página en blanco — ¡normal! Aún no tiene contenido.

---

### 3.2 Paso 2: El Header con Navegación

Reemplaza el comentario dentro de `<body>` por este código:

```html
<header>
    <div>
        <span>💻</span>
        <h1>TechJoven</h1>
        <p>La revista de tecnología para la nueva generación</p>
    </div>
    
    <nav aria-label="Navegación principal">
        <a href="#inicio">Inicio</a>
        <a href="#articulos">Artículos</a>
        <a href="#tutoriales">Tutoriales</a>
        <a href="#comunidad">Comunidad</a>
    </nav>
</header>
```

**Guarda y actualiza el navegador.** ¿Qué ves ahora? El texto aparece, aunque sin estilo. Eso es esperado.

> 🧠 **Para pensar:** ¿Por qué usamos `aria-label="Navegación principal"` en el `<nav>`? Si hubiera otro `<nav>` más abajo (por ejemplo, para el footer), el `aria-label` permite diferenciarlos para los lectores de pantalla.

---

### 3.3 Paso 3: El Contenido Principal

Después del `</header>`, agrega:

```html
<main id="inicio">

    <!-- Artículo destacado -->
    <article id="articulo-destacado">
        <header>
            <h2>Inteligencia Artificial: ¿Amiga o enemiga de los estudiantes?</h2>
            <p>
                Por <span>Carlos Mendoza</span> · 
                <time datetime="2024-11-10">10 de noviembre, 2024</time> · 
                <span>8 min de lectura</span>
            </p>
        </header>
        
        <figure>
            <img src="ia-estudiantes.jpg" alt="Estudiante usando inteligencia artificial en su computadora">
            <figcaption>Cada vez más estudiantes incorporan la IA en su proceso de aprendizaje.</figcaption>
        </figure>
        
        <p>
            La inteligencia artificial ha llegado a las aulas y no parece que se vaya a ir pronto. 
            Herramientas como <strong>ChatGPT, Gemini y Copilot</strong> son ya parte del día a 
            día de millones de estudiantes en todo el mundo. Pero, ¿están ayudando de verdad?
        </p>
        
        <section>
            <h3>Lo que dicen los estudiantes</h3>
            <p>
                En una encuesta realizada a 500 jóvenes de entre 14 y 18 años, el 
                <mark>73% afirmó usar IA al menos una vez a la semana</mark> para tareas escolares.
                Los usos más comunes fueron: resumir textos largos, explicar conceptos difíciles 
                y revisar ortografía.
            </p>
        </section>
        
        <section>
            <h3>El punto de vista de los docentes</h3>
            <p>
                No todos los profesores ven esto con buenos ojos. Según la docente 
                Laura Pérez:
            </p>
            <blockquote>
                <p>
                    "El problema no es la herramienta, sino cómo se usa. 
                    Si el estudiante solo copia y pega sin pensar, no está aprendiendo."
                </p>
            </blockquote>
            <p>
                Sin embargo, otros educadores consideran que enseñar a usar la IA 
                <em>de manera crítica</em> es una habilidad fundamental para el siglo XXI.
            </p>
        </section>
        
        <footer>
            <p>
                Etiquetas: 
                <a href="#">Inteligencia Artificial</a>, 
                <a href="#">Educación</a>, 
                <a href="#">Tecnología</a>
            </p>
        </footer>
    </article>


    <!-- Sección de artículos recientes -->
    <section id="articulos">
        <h2>Artículos Recientes</h2>
        
        <article>
            <header>
                <h3>5 lenguajes de programación que deberías aprender en 2025</h3>
                <time datetime="2024-11-05">5 de noviembre, 2024</time>
            </header>
            <p>
                Python sigue liderando la lista, pero hay sorpresas interesantes 
                entre los lenguajes que más están creciendo este año...
            </p>
            <a href="#">Leer más →</a>
        </article>
        
        <article>
            <header>
                <h3>Cómo crear tu primer repositorio en GitHub paso a paso</h3>
                <time datetime="2024-11-01">1 de noviembre, 2024</time>
            </header>
            <p>
                GitHub es la red social de los programadores. Te enseñamos a 
                subir tu primer proyecto y comenzar a construir tu portafolio...
            </p>
            <a href="#">Leer más →</a>
        </article>
        
        <article>
            <header>
                <h3>Privacidad digital: ¿sabes quién tiene tus datos?</h3>
                <time datetime="2024-10-28">28 de octubre, 2024</time>
            </header>
            <p>
                Cada app que instalas, cada búsqueda que haces... alguien 
                lo está registrando. Descubre cómo protegerte...
            </p>
            <a href="#">Leer más →</a>
        </article>
    </section>

</main>
```

**Guarda y actualiza el navegador.** ¡Ya tienes contenido real!

---

### 3.4 Paso 4: La Barra Lateral

Después del `</main>` y antes de cerrar el `</body>`, agrega:

```html
<aside aria-label="Contenido relacionado">
    
    <section>
        <h3>🔥 Lo más leído</h3>
        <ol>
            <li><a href="#">Hackathon escolar: cómo participar</a></li>
            <li><a href="#">El smartphone del año según expertos</a></li>
            <li><a href="#">Minecraft como herramienta educativa</a></li>
            <li><a href="#">Qué estudiar si quieres trabajar en tecnología</a></li>
        </ol>
    </section>
    
    <section>
        <h3>📅 Próximos Eventos</h3>
        <ul>
            <li>
                <time datetime="2024-11-20">20 nov</time> — 
                Webinar: Introducción a Python
            </li>
            <li>
                <time datetime="2024-11-25">25 nov</time> — 
                Hackathon Estudiantil Online
            </li>
            <li>
                <time datetime="2024-12-01">1 dic</time> — 
                Feria de Ciencias y Tecnología
            </li>
        </ul>
    </section>
    
    <section>
        <h3>💡 ¿Sabías que...?</h3>
        <p>
            El primer sitio web del mundo fue creado por 
            <strong>Tim Berners-Lee</strong> en 1991 y todavía 
            puedes visitarlo hoy en día.
        </p>
        <a href="http://info.cern.ch" target="_blank">Ver el sitio original →</a>
    </section>
    
</aside>
```

---

### 3.5 Paso 5: El Footer

Justo antes del `</body>`, agrega:

```html
<footer>
    
    <section>
        <h3>TechJoven</h3>
        <p>
            Somos una revista digital creada por y para jóvenes 
            apasionados por la tecnología. Nuestro objetivo es 
            hacer la tecnología accesible y emocionante para todos.
        </p>
    </section>
    
    <section>
        <h3>Secciones</h3>
        <nav aria-label="Mapa del sitio">
            <ul>
                <li><a href="#">Inicio</a></li>
                <li><a href="#">Artículos</a></li>
                <li><a href="#">Tutoriales</a></li>
                <li><a href="#">Comunidad</a></li>
                <li><a href="#">Sobre nosotros</a></li>
            </ul>
        </nav>
    </section>
    
    <section>
        <h3>Síguenos</h3>
        <nav aria-label="Redes sociales">
            <a href="#">📸 Instagram</a>
            <a href="#">🐦 Twitter/X</a>
            <a href="#">▶️ YouTube</a>
            <a href="#">💼 LinkedIn</a>
        </nav>
    </section>
    
    <section>
        <h3>Contacto</h3>
        <address>
            <p>📧 <a href="mailto:hola@techjoven.com">hola@techjoven.com</a></p>
            <p>📍 Colombia</p>
        </address>
    </section>
    
    <p>
        <small>
            © <time datetime="2024">2024</time> TechJoven. 
            Contenido libre para uso educativo. 
            <a href="#">Política de privacidad</a> · 
            <a href="#">Términos de uso</a>
        </small>
    </p>
    
</footer>
```

---

### 3.6 Tu Página Completa: Revisión

Abre el archivo en el navegador. Aunque no tiene estilos CSS (eso es otro tema), **tienes una página web completamente estructurada y semántica**. 

Para verificar que la estructura es correcta, puedes usar la herramienta de inspección del navegador:

1. Presiona `F12`
2. Ve a la pestaña **Elements** (Chrome) o **Inspector** (Firefox)
3. Verifica que puedes ver: `<header>`, `<nav>`, `<main>`, `<article>`, `<section>`, `<aside>`, `<footer>`

**Pregunta de reflexión:** ¿Ves cómo el código es legible incluso sin CSS? ¿Podrías explicarle a alguien más lo que hace cada parte?

---

### 3.7 Reto Extra: Agrega tu Propia Sección

Si terminaste antes, agrega dentro del `<main>`, después de la sección de artículos recientes:

```html
<section id="tutoriales">
    <h2>Tutorial Rápido</h2>
    
    <article>
        <header>
            <h3>Tu primera página web en 10 pasos</h3>
        </header>
        
        <ol>
            <li>Instala VS Code</li>
            <li>Crea una carpeta para tu proyecto</li>
            <li>Crea un archivo <code>index.html</code></li>
            <li>Escribe el DOCTYPE y la estructura básica</li>
            <li>Agrega un <code>&lt;header&gt;</code> con tu nombre</li>
            <li>Agrega un <code>&lt;main&gt;</code> con una presentación tuya</li>
            <li>Agrega un <code>&lt;footer&gt;</code> con tu contacto</li>
            <li>Guarda el archivo</li>
            <li>Ábrelo en el navegador</li>
            <li>¡Celebra! Acababas de crear tu primera web 🎉</li>
        </ol>
    </article>
</section>
```

---

## ⏸️ Descanso 2 — ⏱ 195 minutos

```
╔══════════════════════════════════════════════════════╗
║                                                      ║
║   🚀  ¡Construiste tu primera página semántica!      ║
║                                                      ║
║   ⏰  Tómate otros 15 minutos:                       ║
║       • Levántate y camina un poco 🚶                ║
║       • Respira profundo — ya falta poco 💪          ║
║       • Muéstrale tu página a alguien 😄             ║
║       • Piensa: ¿qué pregunta tienes sobre           ║
║         lo que viste hasta ahora?                    ║
║                                                      ║
║   🕐  Último bloque: comparaciones y proyecto final  ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
```

> 💡 **Nota pedagógica:** Este segundo descanso ocurre después de 75 minutos de práctica intensa. Es el momento ideal para pausar porque los estudiantes acaban de lograr algo concreto (construir la página), lo que hace que el descanso sea un refuerzo positivo natural. El bloque final es más analítico y reflexivo, por lo que comenzar descansados favorece la comprensión profunda.

---

## ⚖️ Módulo 4 — Código Desorganizado vs. Estructurado

> ⏱ **Tiempo estimado: 20 minutos**

Este módulo es uno de los más importantes porque te permite ver, de forma directa, la diferencia entre hacer las cosas bien y hacerlas "más o menos".

### 4.1 El Caso de Estudio: La Página de Eventos

Vamos a ver dos versiones del mismo contenido: una página que anuncia los eventos de un club de programación escolar.

---

#### ❌ VERSIÓN DESORGANIZADA

```html
<!DOCTYPE html>
<html>
<head>
<title>eventos</title>
</head>
<body>
<div>
<div><b>CLUB DE PROGRAMACIÓN</b></div>
<div>inicio | eventos | contacto | nosotros</div>
</div>
<div>
<div><b><font size="5">PRÓXIMOS EVENTOS</font></b></div>
<div>
<div>
<b>Hackathon Estudiantil</b><br>
el evento es el 15 de noviembre de 2024 a las 9am<br>
ven y participa en nuestro hackathon donde podrás...<br>
se realizará en el salón de informática del colegio<br>
cupos limitados! inscribete ya
</div>
<div>
<b>Taller de Python</b><br>
22 nov 2024, 2pm<br>
aprende python desde cero con nuestros monitores...<br>
sala de computo, piso 2<br>
gratis para estudiantes
</div>
</div>
<div>
<div>próximos eventos importantes: ver calendario</div>
<div>contacto: clubprog@colegio.edu.co</div>
</div>
</div>
<div>
hecho por el club de programación 2024 - contacto - privacidad
</div>
</body>
</html>
```

**Problemas de esta versión:**

| Problema | Descripción |
|---|---|
| `<html>` sin `lang` | El navegador no sabe el idioma del contenido |
| `<meta charset>` ausente | Los tildes y la ñ pueden verse mal |
| Sin etiquetas semánticas | Todo es `<div>` — no hay significado |
| Uso de `<font>` y `<b>` para estilo | Estas etiquetas mezclan contenido con diseño (mala práctica) |
| Texto sin estructura | Datos como fecha, lugar e inscripción mezclados en texto plano |
| Sin `<nav>` | El menú no es reconocible para buscadores ni lectores de pantalla |
| Sin `<main>` | Google no puede identificar el contenido principal |
| Minúsculas inconsistentes | El texto mezcla mayúsculas y minúsculas sin criterio |
| Sin `<time>` | Las fechas no son legibles por máquinas |
| Sin `<address>` | El email de contacto no tiene semántica de contacto |

---

#### ✅ VERSIÓN ESTRUCTURADA

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Próximos Eventos — Club de Programación Escolar</title>
    <meta name="description" content="Hackathon, talleres y actividades del club de programación estudiantil.">
</head>
<body>

    <header>
        <h1>Club de Programación</h1>
        <p>Donde el código cobra vida</p>
        <nav aria-label="Menú principal">
            <ul>
                <li><a href="/">Inicio</a></li>
                <li><a href="/eventos" aria-current="page">Eventos</a></li>
                <li><a href="/nosotros">Nosotros</a></li>
                <li><a href="/contacto">Contacto</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <h2>Próximos Eventos</h2>
        <p>Actividades abiertas para todos los estudiantes del colegio.</p>

        <section aria-labelledby="titulo-noviembre">
            <h3 id="titulo-noviembre">Noviembre 2024</h3>

            <article>
                <header>
                    <h4>Hackathon Estudiantil</h4>
                    <p>
                        <time datetime="2024-11-15T09:00">
                            Viernes 15 de noviembre, 9:00 a.m.
                        </time>
                    </p>
                </header>
                
                <p>
                    Pon a prueba tus habilidades en equipo. En 8 horas, 
                    deberás crear una solución digital a un problema real 
                    de tu comunidad. <strong>¡Cupos limitados!</strong>
                </p>
                
                <footer>
                    <p>📍 Salón de Informática — Piso 3</p>
                    <p>
                        <a href="/inscripcion/hackathon">
                            Inscribirte ahora →
                        </a>
                    </p>
                </footer>
            </article>

            <article>
                <header>
                    <h4>Taller de Python para Principiantes</h4>
                    <p>
                        <time datetime="2024-11-22T14:00">
                            Viernes 22 de noviembre, 2:00 p.m.
                        </time>
                    </p>
                </header>
                
                <p>
                    ¿Nunca has programado? Este taller es para ti. 
                    Aprenderás los fundamentos de Python con el apoyo 
                    de monitores estudiantiles. Sin requisitos previos.
                </p>
                
                <footer>
                    <p>📍 Sala de Cómputo — Piso 2</p>
                    <p>🎟️ <em>Entrada gratuita para estudiantes del colegio</em></p>
                    <p>
                        <a href="/inscripcion/python">
                            Reservar mi lugar →
                        </a>
                    </p>
                </footer>
            </article>
        </section>
    </main>

    <aside aria-label="Información de contacto">
        <h3>¿Tienes preguntas?</h3>
        <address>
            <p>Escríbenos a: 
                <a href="mailto:clubprog@colegio.edu.co">
                    clubprog@colegio.edu.co
                </a>
            </p>
        </address>
        <p>
            <a href="/calendario">Ver calendario completo de eventos →</a>
        </p>
    </aside>

    <footer>
        <p>
            <small>
                © <time datetime="2024">2024</time> Club de Programación. 
                <a href="/contacto">Contacto</a> · 
                <a href="/privacidad">Privacidad</a>
            </small>
        </p>
    </footer>

</body>
</html>
```

---

### 4.2 Comparación Visual: Las Diferencias que Importan

```
╔══════════════════════════════════════════════════════════════════╗
║  CRITERIO           │ DESORGANIZADO     │ ESTRUCTURADO           ║
╠══════════════════════════════════════════════════════════════════╣
║  Líneas de código   │ ~30               │ ~80                    ║
║  ¿Se ve diferente? │ NO (igual en web) │ NO (igual en web)      ║
╠══════════════════════════════════════════════════════════════════╣
║  SEO (buscadores)  │ ❌ Confuso        │ ✅ Claro               ║
║  Accesibilidad     │ ❌ Ilegible       │ ✅ Completamente legible║
║  Mantenimiento     │ ❌ Laberinto      │ ✅ Autodescriptivo      ║
║  Trabajo en equipo │ ❌ Confuso        │ ✅ Fácil de entender    ║
║  Estándares web    │ ❌ No cumple      │ ✅ HTML5 válido         ║
╚══════════════════════════════════════════════════════════════════╝
```

> 🔑 **La lección más importante del día:** Visualmente, ambas versiones pueden lucir idénticas en el navegador. La diferencia no es lo que *ves* — es lo que el código *comunica* a buscadores, tecnologías de asistencia y otros desarrolladores.

---

### 4.3 Actividad: Detecta los Errores

Aquí tienes un fragmento de código "roto". Identifica **al menos 5 problemas semánticos** y escribe cómo los corregirías:

```html
<html>
<head>
<title>blog</title>
</head>
<body>
<div id="top">
    <div class="name"><font size="6"><b>MI BLOG</b></font></div>
    <div class="menu">
        <a href="/">inicio</a>
        <a href="/posts">posts</a>
        <a href="/about">sobre mi</a>
    </div>
</div>

<div id="wrap">
    <div class="post">
        <div class="post-title"><b>Mi viaje a Cartagena</b></div>
        <div class="post-meta">Carlos · 10 octubre 2024 · 5 min</div>
        <div class="post-content">
            El viaje empezó desde muy temprano en la mañana...
            <img src="cartagena.jpg">
        </div>
    </div>
    
    <div class="sidebar">
        <div class="widget-title">Entradas recientes</div>
        <div>
            <a href="#">Bogotá en fotos</a>
            <a href="#">Recetas de mi abuela</a>
        </div>
    </div>
</div>

<div id="bottom">
    <div>© 2024 Mi Blog</div>
</div>
</body>
</html>
```

<details>
<summary>🔑 Ver solución comentada</summary>

```html
<!DOCTYPE html>                           <!-- Faltaba el DOCTYPE -->
<html lang="es">                          <!-- Faltaba lang -->
<head>
    <meta charset="UTF-8">               <!-- Faltaba charset -->
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mi Blog de Viajes</title>      <!-- Título más descriptivo -->
</head>
<body>

<header>                                  <!-- div#top → header -->
    <h1>Mi Blog</h1>                      <!-- font+b → h1 -->
    <nav aria-label="Navegación principal">  <!-- div.menu → nav -->
        <a href="/">Inicio</a>
        <a href="/posts">Posts</a>
        <a href="/about">Sobre mí</a>
    </nav>
</header>

<main>                                    <!-- div#wrap necesitaba main -->
    <article>                             <!-- div.post → article -->
        <header>
            <h2>Mi viaje a Cartagena</h2>  <!-- div.post-title → h2 -->
            <p>
                Carlos · 
                <time datetime="2024-10-10">10 de octubre, 2024</time> · 
                5 min de lectura                <!-- <time> para la fecha -->
            </p>
        </header>
        <p>
            El viaje empezó desde muy temprano en la mañana...
            <img src="cartagena.jpg" alt="Vista de Cartagena al amanecer"> <!-- faltaba alt -->
        </p>
    </article>
    
    <aside>                               <!-- div.sidebar → aside -->
        <h3>Entradas recientes</h3>       <!-- div.widget-title → h3 -->
        <nav aria-label="Entradas recientes">
            <ul>
                <li><a href="#">Bogotá en fotos</a></li>
                <li><a href="#">Recetas de mi abuela</a></li>
            </ul>
        </nav>
    </aside>
</main>

<footer>                                  <!-- div#bottom → footer -->
    <p><small>© <time datetime="2024">2024</time> Mi Blog</small></p>
</footer>

</body>
</html>
```

**Los 5+ problemas:**
1. Faltaba `<!DOCTYPE html>`
2. Faltaba `lang` en `<html>`
3. Faltaba `<meta charset="UTF-8">`
4. Usaba `<font>` y `<b>` para estilos (deprecated)
5. Todo con `<div>` sin semántica
6. La imagen no tenía atributo `alt`
7. La fecha no usaba `<time>`

</details>

---

## 🏆 Proyecto Final del Día

> ⏱ **Tiempo estimado: 10 minutos**

### Tu Tarjeta de Presentación en HTML

Crea un nuevo archivo `presentacion.html` con tu página personal. Debe incluir **obligatoriamente**:

- `<!DOCTYPE html>` con `lang` correcto
- `<meta charset>` y `<meta viewport>`
- Un `<header>` con tu nombre y una frase que te represente
- Un `<main>` con al menos dos `<section>`:
  - **Sección 1:** Sobre ti (quién eres, qué te gusta)
  - **Sección 2:** Tus habilidades o pasatiempos (puedes usar una lista `<ul>`)
- Un `<footer>` con tu información de contacto usando `<address>`
- Al menos una fecha usando `<time>`
- Al menos un uso de `<strong>` o `<em>` con propósito real (no solo para negrita)

**Criterios de evaluación:**

| Criterio | Puntos |
|---|---|
| Estructura básica completa (DOCTYPE, html, head, body) | 20 |
| Uso correcto de header, main, footer | 30 |
| Al menos 2 section con h2 o h3 | 20 |
| Uso semántico de etiquetas de texto (time, strong, em, etc.) | 20 |
| El HTML es válido (sin errores en el inspector) | 10 |
| **Total** | **100** |

---

## 📚 Glosario

| Término | Definición |
|---|---|
| **Semántica** | El significado detrás de las palabras o etiquetas. En HTML, una etiqueta semántica comunica *qué es* el contenido. |
| **DOM** | Document Object Model. La representación en árbol que hace el navegador del documento HTML. |
| **Etiqueta** | Elemento de HTML encerrado entre `< >`. Ejemplo: `<header>` |
| **Atributo** | Información adicional dentro de una etiqueta. Ejemplo: `lang="es"` |
| **SEO** | Search Engine Optimization. Técnicas para aparecer mejor en buscadores como Google. |
| **Accesibilidad** | Diseño web que permite que personas con discapacidades puedan usar el contenido. |
| **`aria-label`** | Atributo que proporciona una etiqueta descriptiva para tecnologías de asistencia. |
| **`<time>`** | Etiqueta para fechas/horas legibles por máquinas. El atributo `datetime` usa formato estándar. |
| **`<address>`** | Etiqueta para información de contacto del autor o de la organización. |
| **Responsive** | Diseño que se adapta a cualquier tamaño de pantalla (móvil, tablet, computador). |
| **HTML5** | La versión actual de HTML, lanzada oficialmente en 2014, que introdujo las etiquetas semánticas. |
| **Deprecated** | Etiqueta o atributo que ya no se recomienda usar. Ejemplo: `<font>`, `<center>` |

---

## 🌐 Recursos para Seguir Aprendiendo

### Documentación oficial (en español)
- 📖 [MDN Web Docs — Elementos HTML](https://developer.mozilla.org/es/docs/Web/HTML/Element) — La referencia más completa y confiable
- 📖 [HTML Semántico en MDN](https://developer.mozilla.org/es/docs/Glossary/Semantics) — Explicación detallada del concepto

### Herramientas prácticas
- 🛠️ [Validador W3C](https://validator.w3.org/) — Verifica si tu HTML es correcto
- 🛠️ [CodePen](https://codepen.io/) — Escribe y prueba HTML/CSS directamente en el navegador
- 🛠️ [Can I Use](https://caniuse.com/) — Verifica qué navegadores soportan cada etiqueta

### Para practicar más
- 🎮 [freeCodeCamp](https://www.freecodecamp.org/espanol/) — Lecciones interactivas gratuitas
- 🎮 [The Odin Project](https://www.theodinproject.com/) — Ruta de aprendizaje completa (en inglés)

### Conceptos para explorar después
- **CSS** — Cómo darle estilo visual a tu HTML semántico
- **Accesibilidad web (WCAG)** — Estándares para hacer la web inclusiva
- **Open Graph** — Metaetiquetas para compartir en redes sociales

---

## ✅ Checklist Final del Día

Antes de irte, confirma que puedes:

- [ ] Explicar qué es una etiqueta semántica y para qué sirve
- [ ] Nombrar al menos 6 etiquetas estructurales de HTML5
- [ ] Distinguir cuándo usar `<article>` vs. `<section>`
- [ ] Identificar el árbol DOM básico de un documento
- [ ] Crear un documento HTML con estructura semántica válida
- [ ] Corregir código HTML desorganizado
- [ ] Argumentar por qué la semántica importa más allá del aspecto visual

---

> 💬 **Reflexión final:** Hoy aprendiste que el código no solo es para los navegadores — es para las personas. Un HTML bien escrito es más accesible, más fácil de mantener y más honesto. Cada `<article>` que usas correctamente es una decisión de respeto hacia quien use tu página y hacia quien lea tu código.
>
> **¡Sigue construyendo!** 🚀

---

*Material desarrollado con fines educativos. Nivel: Fundamentos de Desarrollo Web. HTML5 — 2024.*
