# 🌐 Introducción a HTML5: Tu Primera Página Web

> **Nivel:** Principiante | **Duración:** 4 horas (incluye 30 min de descanso) | **Edad:** 16 años

---

## 📋 Tabla de Contenidos

1. [¿Qué es HTML5?](#qué-es-html5)
2. [Herramientas que usaremos](#herramientas-que-usaremos)
3. [Estructura básica de HTML5](#estructura-básica-de-html5)
4. [Etiquetas esenciales](#etiquetas-esenciales)
5. [🛠️ Taller: Mi primera página web](#️-taller-mi-primera-página-web)
6. [☕ DESCANSO - 30 minutos](#-descanso---30-minutos)
7. [🔍 Revisión por pares](#-revisión-por-pares)
8. [Retos extra](#retos-extra)
9. [Recursos para seguir aprendiendo](#recursos-para-seguir-aprendiendo)

---

## ⏱️ Agenda de la clase

| Hora | Actividad |
|------|-----------|
| 0:00 – 0:30 | ¿Qué es HTML5? Conceptos clave |
| 0:30 – 1:30 | Etiquetas esenciales con ejemplos en vivo |
| 1:30 – 2:15 | 🛠️ Taller: Edición de tu primera página web |
| 2:15 – 2:45 | ☕ **DESCANSO** |
| 2:45 – 3:30 | 🔍 Revisión por pares del código |
| 3:30 – 4:00 | Presentación de páginas + cierre |

---

## ¿Qué es HTML5?

**HTML** son las siglas de *HyperText Markup Language* (Lenguaje de Marcado de Hipertexto). Es el lenguaje que usan los navegadores (Chrome, Firefox, Edge) para mostrar páginas web.

Piénsalo así:

```
🏠 Una página web es como una casa:
   - HTML  → La estructura (paredes, puertas, ventanas)
   - CSS   → La decoración (colores, muebles, estilo)
   - JS    → La electricidad (lo que hace que las cosas funcionen)
```

> **HTML5** es la versión más reciente y moderna de HTML. Fue lanzada en 2014 y es el estándar actual.

### ¿Cómo funciona?

1. Escribes código HTML en un archivo `.html`
2. Abres ese archivo en un navegador
3. ¡El navegador lo convierte en una página visual!

---

## Herramientas que usaremos

### Opción A – Sin instalación (recomendada para hoy)
- 🌐 **[CodePen](https://codepen.io)** — Escribe y ve el resultado en tiempo real
- 🌐 **[Replit](https://replit.com)** — Editor en línea completo

### Opción B – En tu computador
- 📝 **Visual Studio Code** — El editor más popular del mundo (gratuito)
  - Descarga: [code.visualstudio.com](https://code.visualstudio.com)
  - Extensión recomendada: *Live Server* (recarga automática)

### Para abrir tu archivo HTML
Solo arrastra el archivo `.html` a tu navegador, ¡así de fácil!

---

## Estructura básica de HTML5

Todo archivo HTML5 tiene esta estructura base. ¡Memorízala! 🧠

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Mi primera página</title>
  </head>
  <body>
    <!-- Aquí va todo lo que el usuario puede VER -->
    <h1>¡Hola, mundo!</h1>
  </body>
</html>
```

### Desglose línea por línea

| Código | ¿Qué hace? |
|--------|-----------|
| `<!DOCTYPE html>` | Le dice al navegador: "esto es HTML5" |
| `<html lang="es">` | Inicio del documento. `lang="es"` indica que está en español |
| `<head>` | Sección invisible: configuración, título, estilos |
| `<meta charset="UTF-8">` | Permite usar tildes y ñ correctamente |
| `<meta name="viewport"...>` | Hace que se vea bien en celulares |
| `<title>` | El texto que aparece en la pestaña del navegador |
| `</head>` | Cierra la sección de configuración |
| `<body>` | Todo lo que se muestra en pantalla va aquí |
| `</body>` | Cierra el cuerpo de la página |
| `</html>` | Cierra el documento HTML |

### 🔑 Regla de oro de las etiquetas

La mayoría de etiquetas tienen **apertura** y **cierre**:

```html
<etiqueta> contenido </etiqueta>
   👆                    👆
 Abre               Cierra (tiene /)
```

Los **comentarios** no se muestran en pantalla, solo sirven para ti:
```html
<!-- Esto es un comentario, el navegador lo ignora -->
```

---

## Etiquetas esenciales

### 1. 📝 `<html>` — La raíz de todo

```html
<html lang="es">
  <!-- Todo el documento va aquí dentro -->
</html>
```

- Es como el contenedor principal de todo
- El atributo `lang` ayuda a los lectores de pantalla y al SEO

---

### 2. 🧠 `<head>` — La cabeza (invisible)

```html
<head>
  <meta charset="UTF-8">
  <title>Mi sitio web</title>
</head>
```

- **No se muestra** en la pantalla
- Contiene información sobre la página
- Aquí van los estilos CSS y configuraciones

---

### 3. 👀 `<body>` — El cuerpo (visible)

```html
<body>
  <h1>Todo lo que el usuario ve</h1>
  <p>va dentro del body</p>
</body>
```

- **Todo lo visible** va dentro de `<body>`
- Solo puede haber **un** `<body>` por página

---

### 4. 🔤 Encabezados `<h1>` al `<h6>`

Los encabezados organizan el contenido como títulos de un libro.

```html
<h1>Título principal (el más grande)</h1>
<h2>Subtítulo</h2>
<h3>Sección dentro del subtítulo</h3>
<h4>Sub-sección</h4>
<h5>Nivel 5</h5>
<h6>Nivel 6 (el más pequeño)</h6>
```

> ⚠️ **Regla:** Usa solo **un** `<h1>` por página. Es el título más importante.

---

### 5. 📖 `<p>` — Párrafo

La etiqueta más usada para texto normal.

```html
<p>Este es un párrafo de texto. Puede ser tan largo como necesites.</p>

<p>Cada etiqueta p crea un nuevo párrafo con espacio entre ellos.</p>
```

**Resultado visual:**

> Este es un párrafo de texto. Puede ser tan largo como necesites.
>
> Cada etiqueta p crea un nuevo párrafo con espacio entre ellos.

---

### 6. 🔗 `<a>` — Enlace (anchor)

Los enlaces conectan páginas entre sí. ¡Son la esencia de internet!

```html
<!-- Enlace a otra página web -->
<a href="https://www.google.com">Ir a Google</a>

<!-- Enlace que abre en pestaña nueva -->
<a href="https://github.com" target="_blank">GitHub (nueva pestaña)</a>

<!-- Enlace a otra sección de la misma página -->
<a href="#contacto">Ir a la sección contacto</a>

<!-- Enlace de correo electrónico -->
<a href="mailto:hola@ejemplo.com">Envíame un correo</a>
```

#### Atributos importantes de `<a>`:

| Atributo | ¿Para qué sirve? | Ejemplo |
|----------|-----------------|---------|
| `href` | La URL a donde lleva el enlace | `href="https://..."` |
| `target="_blank"` | Abre en pestaña nueva | `target="_blank"` |
| `title` | Texto que aparece al pasar el mouse | `title="Ver más"` |

---

### 7. 🖼️ `<img>` — Imagen

Las imágenes son **etiquetas de cierre automático** (no necesitan `</img>`).

```html
<!-- Imagen desde internet -->
<img src="https://picsum.photos/400/300" alt="Imagen aleatoria">

<!-- Imagen desde tu computador (mismo directorio) -->
<img src="foto.jpg" alt="Mi foto de perfil">

<!-- Imagen con tamaño definido -->
<img src="logo.png" alt="Logo de mi empresa" width="200" height="100">
```

#### Atributos importantes de `<img>`:

| Atributo | ¿Para qué sirve? | ¿Obligatorio? |
|----------|-----------------|---------------|
| `src` | La ruta o URL de la imagen | ✅ Sí |
| `alt` | Texto alternativo (accesibilidad y SEO) | ✅ Sí |
| `width` | Ancho en píxeles | No |
| `height` | Alto en píxeles | No |

> ♿ **¿Por qué es importante el `alt`?** Las personas que usan lectores de pantalla (usuarios con discapacidad visual) dependen del texto `alt` para saber qué hay en la imagen.

---

### 8. Etiquetas de organización

```html
<!-- Línea horizontal (separador visual) -->
<hr>

<!-- Salto de línea -->
<br>

<!-- Texto en negrita -->
<strong>Texto importante en negrita</strong>

<!-- Texto en cursiva -->
<em>Texto con énfasis en cursiva</em>
```

---

## 🛠️ Taller: Mi primera página web

> ⏱️ **Tiempo:** 45 minutos | 👥 **Individual**

### 📌 Objetivo

Crear una página web personal que incluya: tu nombre, una foto, una descripción tuya y al menos un enlace.

---

### Paso 1: Crea tu archivo

1. Abre tu editor (VS Code o CodePen)
2. Crea un nuevo archivo llamado `index.html`
3. Escribe la estructura base (puedes copiarla de arriba)

---

### Paso 2: Completa la plantilla

Copia este código y **reemplaza todo lo que está en MAYÚSCULAS** con tu información:

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Página de TU_NOMBRE</title>
  </head>
  <body>

    <!-- SECCIÓN 1: Tu presentación -->
    <h1>Hola, soy TU_NOMBRE 👋</h1>
    <p>Tengo EDAD años y vivo en TU_CIUDAD.</p>

    <!-- SECCIÓN 2: Sobre ti -->
    <h2>Sobre mí</h2>
    <p>ESCRIBE 2 O 3 ORACIONES SOBRE TI. Por ejemplo: qué te gusta hacer, tu hobbie favorito, tu comida preferida.</p>

    <!-- SECCIÓN 3: Tu foto -->
    <h2>Mi foto</h2>
    <img 
      src="https://api.dicebear.com/7.x/avataaars/svg?seed=TU_NOMBRE" 
      alt="Avatar de TU_NOMBRE"
      width="200"
    >

    <!-- SECCIÓN 4: Mis intereses -->
    <h2>Mis intereses</h2>
    <p>Algunas cosas que me gustan:</p>
    <p>⭐ INTERÉS 1</p>
    <p>⭐ INTERÉS 2</p>
    <p>⭐ INTERÉS 3</p>

    <!-- SECCIÓN 5: Un enlace -->
    <h2>Encuéntrame en</h2>
    <p>
      <a href="URL_DE_TU_RED_SOCIAL" target="_blank">
        Mi perfil en NOMBRE_RED_SOCIAL
      </a>
    </p>

    <!-- PIE DE PÁGINA -->
    <hr>
    <p>Hecho con ❤️ por TU_NOMBRE — AÑO</p>

  </body>
</html>
```

---

### Paso 3: Mejora tu página (si terminas antes)

Agrega cualquiera de estas secciones extra:

```html
<!-- Lista de tus películas favoritas -->
<h2>🎬 Mis películas favoritas</h2>
<p>1. PELÍCULA 1</p>
<p>2. PELÍCULA 2</p>
<p>3. PELÍCULA 3</p>

<!-- Una imagen de algo que te guste -->
<h2>🎮 Mi juego favorito</h2>
<img src="URL_DE_IMAGEN" alt="Descripción de la imagen" width="300">
<p>Me encanta este juego porque RAZÓN.</p>
```

---

### ✅ Checklist del taller

Antes de terminar, verifica que tu página tiene:

- [ ] Estructura base completa (`DOCTYPE`, `html`, `head`, `body`)
- [ ] Título en la pestaña del navegador (`<title>`)
- [ ] Al menos un `<h1>` con tu nombre
- [ ] Al menos dos `<h2>` como subtítulos
- [ ] Al menos tres `<p>` con texto
- [ ] Una `<img>` con `src` y `alt`
- [ ] Al menos un `<a>` con `href`
- [ ] Un `<hr>` separador
- [ ] Comentarios explicando las secciones

---

## ☕ DESCANSO — 30 minutos

```
 ██████████████████████████████████
 █                                █
 █   ☕  ¡Hora de descansar!  ☕   █
 █                                █
 █   Vuelven en 30 minutos.       █
 █   Guarden su trabajo antes     █
 █   de alejarse del computador.  █
 █                                █
 ██████████████████████████████████
```

---

## 🔍 Revisión por pares

> ⏱️ **Tiempo:** 45 minutos | 👥 **En parejas**

La revisión por pares es una práctica real que usan los programadores profesionales. Se llama **Code Review** y sirve para encontrar errores y aprender del código de otros.

---

### ¿Cómo funciona?

1. **Busca un compañero** (o el profe los asigna en parejas)
2. **Intercambien sus archivos** `index.html` (por correo, USB o compartan pantalla)
3. **Revisen el código** usando la guía de abajo
4. **Den retroalimentación** de forma respetuosa y constructiva
5. **Corrijan** su propio código con los comentarios recibidos

---

### 📋 Guía de revisión — ¿Qué revisar?

#### 🔴 Errores críticos (el código no funciona)

```
¿Tienen todas las etiquetas su cierre? Ejemplo:
  ✅ <p>Texto</p>
  ❌ <p>Texto       ← falta el </p>

¿Están bien escritas las etiquetas? Ejemplo:
  ✅ <body>
  ❌ <bodi> o <BODY> o < body>

¿Los atributos tienen comillas? Ejemplo:
  ✅ <img src="foto.jpg" alt="Mi foto">
  ❌ <img src=foto.jpg alt=Mi foto>
```

#### 🟡 Buenas prácticas (el código funciona pero puede mejorar)

```
¿Hay un solo <h1> por página?
¿Las imágenes tienen atributo alt con descripción?
¿Los enlaces tienen href válido?
¿Hay comentarios explicando las secciones?
¿El indentado (sangría) está bien? Ejemplo:

  ✅ Bien indentado:           ❌ Mal indentado:
  <body>                       <body>
    <h1>Título</h1>            <h1>Título</h1>
    <p>Texto</p>               <p>Texto</p>
  </body>                      </body>
```

#### 🟢 Creatividad y contenido

```
¿La página tiene información interesante?
¿Se ve organizada y fácil de leer?
¿Usó alguna etiqueta extra que no vimos en clase?
```

---

### 💬 Cómo dar retroalimentación constructiva

| ❌ No digas | ✅ Di mejor |
|------------|------------|
| "Tu código está mal" | "En la línea 15, falta cerrar la etiqueta `<p>`" |
| "No entendiste nada" | "Aquí podrías agregar un `alt` a la imagen para mejorar la accesibilidad" |
| "Está feo" | "¿Qué tal si agregas más espacios entre secciones con `<hr>`?" |
| "Está perfecto, no cambies nada" | "Me gustó que usaste emojis 😄 Podrías también probar con `<strong>` para resaltar palabras" |

---

### 📝 Formulario de revisión

Usa esta plantilla para dar tu retroalimentación por escrito:

```
REVISIÓN DE CÓDIGO — [Nombre del revisor] → [Nombre del autor]
Fecha: ___________

✅ COSAS QUE HIZO BIEN:
1. 
2. 
3. 

🔧 ERRORES ENCONTRADOS:
1. (Línea aproximada): 
2. (Línea aproximada): 

💡 SUGERENCIAS DE MEJORA:
1. 
2. 

⭐ PUNTUACIÓN GENERAL: ___/10

💬 COMENTARIO FINAL:
```

---

### 🔄 Después de recibir tu revisión

1. **Lee** todos los comentarios con atención
2. **Pregunta** si no entiendes algún comentario
3. **Corrige** los errores críticos primero
4. **Implementa** al menos una sugerencia de mejora
5. **Agradece** a tu compañero/a

---

## Retos extra

¿Terminaste todo? ¡Aquí van desafíos para los más rápidos!

### 🥉 Nivel Bronce
Agrega a tu página:
```html
<!-- Tu canción favorita con enlace a YouTube -->
<h2>🎵 Mi canción favorita</h2>
<p>
  <a href="URL_DE_YOUTUBE" target="_blank">
    NOMBRE DE LA CANCIÓN - ARTISTA
  </a>
</p>
```

### 🥈 Nivel Plata
Investiga y usa estas etiquetas nuevas:
```html
<!-- Lista no ordenada (bullets) -->
<ul>
  <li>Elemento 1</li>
  <li>Elemento 2</li>
  <li>Elemento 3</li>
</ul>

<!-- Lista ordenada (números) -->
<ol>
  <li>Primer lugar</li>
  <li>Segundo lugar</li>
  <li>Tercer lugar</li>
</ol>
```

### 🥇 Nivel Oro
Intenta crear una segunda página y enlazarla:

**Archivo: `index.html`**
```html
<a href="hobbies.html">Ver mis hobbies</a>
```

**Archivo: `hobbies.html`** (nuevo archivo)
```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8">
    <title>Mis hobbies</title>
  </head>
  <body>
    <h1>Mis hobbies</h1>
    <p>En esta página hablo de mis actividades favoritas...</p>
    <a href="index.html">← Volver al inicio</a>
  </body>
</html>
```

---

## 📚 Resumen de etiquetas vistas hoy

| Etiqueta | ¿Para qué? | Ejemplo |
|----------|-----------|---------|
| `<html>` | Raíz del documento | `<html lang="es">` |
| `<head>` | Metadatos (invisible) | `<head>...</head>` |
| `<body>` | Contenido visible | `<body>...</body>` |
| `<h1>`–`<h6>` | Títulos y subtítulos | `<h1>Mi título</h1>` |
| `<p>` | Párrafo de texto | `<p>Mi texto</p>` |
| `<a>` | Enlace | `<a href="url">Click</a>` |
| `<img>` | Imagen | `<img src="foto.jpg" alt="foto">` |
| `<hr>` | Línea separadora | `<hr>` |
| `<br>` | Salto de línea | `<br>` |
| `<strong>` | Texto en negrita | `<strong>importante</strong>` |
| `<em>` | Texto en cursiva | `<em>énfasis</em>` |

---

## Recursos para seguir aprendiendo

### 📖 Documentación oficial (en español)
- [MDN Web Docs en Español](https://developer.mozilla.org/es/docs/Web/HTML) — La biblia del desarrollo web
- [W3Schools HTML Tutorial](https://www.w3schools.com/html/) — Con ejemplos interactivos

### 🎮 Aprende jugando
- [Flexbox Froggy](https://flexboxfroggy.com/#es) — Para cuando aprendan CSS
- [CSS Diner](https://flukeout.github.io/) — Para practicar selectores

### 🎬 Videos recomendados
- Busca en YouTube: **"HTML5 desde cero en español"**
- Canal recomendado: **Fazt**, **MiduDev**, **HolaMundo**

### 💻 Práctica
- [CodePen](https://codepen.io) — Crea y comparte código en línea
- [GitHub Pages](https://pages.github.com) — ¡Publica tu página web gratis!

---

## 🏆 Logros de la clase

Al terminar esta clase, puedes decir que sabes:

- [x] Qué es HTML5 y para qué sirve
- [x] Cuál es la estructura básica de un documento HTML
- [x] Crear y usar las etiquetas `<html>`, `<head>`, `<body>`
- [x] Crear párrafos con `<p>` y títulos con `<h1>`-`<h6>`
- [x] Crear enlaces con `<a>` e imágenes con `<img>`
- [x] Editar tu primera página web personal
- [x] Revisar el código de otra persona de forma constructiva

---

*Material creado para clase de introducción a HTML5 · Nivel secundaria · 4 horas*

*Licencia: [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.es) — Libre para usar y modificar con atribución*
