# 🚀 Clase 1: HTML — El esqueleto de todo lo que ves en internet

> **Duración:** ~60 minutos  
> **Audiencia:** Primerizos de 15 años  
> **Objetivo:** Que al salir de esta clase sepan qué es HTML, para qué existe, de dónde salió, y hayan escrito su primera página web con sus propias manos.

---

## 🎬 Hook inicial (3 minutos)

Levanta la mano quien hoy haya visto al menos una de estas cosas:

- Un video corto en TikTok
- Un meme en Instagram
- Un capítulo en Netflix
- Google, Wikipedia o YouTube
- El chat de WhatsApp Web

**Todas, absolutamente todas, funcionan gracias a HTML.** Ni una sola se salva.

Y aquí va la pregunta interesante: si HTML existe desde 1991… ¿cómo es que sigue viva después de más de 30 años? La respuesta la vamos a descubrir hoy.

> 🧠 *Dato curioso para soltar en clase:* la página web más vieja que todavía existe se puede visitar hoy. Es del CERN y la creó el mismo señor que inventó la web. Más abajo te cuento quién es.

---

## 😤 El problema (5 minutos)

Imagina esto. Estamos en 1989. Eres un científico en el CERN (un laboratorio gigante en Suiza donde se chocan partículas). Todos los días miles de investigadores de distintos países escriben documentos, informes, planos, resultados.

**Problema 1 — Caos total:**  
Cada quien usa programas distintos (Word, MacWrite, etc.) y nadie puede leer el archivo del otro. Es como si un español te mandara una carta en español antiguo, otro en catalán y otro en emojis.

**Problema 2 — Perderse en la información:**  
Hay tantos documentos que es imposible encontrarlos. No hay Google, no hay buscador. Si quieres un paper, tienes que pedirlo por correo o ir a la biblioteca.

**Problema 3 — Trabajar en equipo a distancia:**  
Científicos de Francia, Japón y Brasil necesitan comentar el mismo documento, en vivo, desde sus países.

¿Qué haces?  

Inventas algo nuevo. Eso hizo **Tim Berners-Lee**, un ingeniero británico que trabajaba ahí.

---

## 👨‍🔬 Historia express (10 minutos)

### 1989 — La propuesta
Tim le escribe a su jefe una propuesta titulada *"Information Management: A Proposal"*. Su jefe le responde: *"vague but exciting"* (vaga pero emocionante). Aprobado. 😄

### 1990 — Nace la WWW
Tim crea tres inventos en uno:
1. **HTML** — el lenguaje para escribir páginas
2. **HTTP** — el protocolo para pedirlas y enviarlas
3. **URL** — la dirección única de cada página

Juntos forman la **World Wide Web** (la "telaraña mundial"). Fíjate: él no inventó *internet* (eso ya existía), inventó la **web**, que es la forma bonita y ordenada de usar internet.

### 1991 — La primera página web de la historia
Tim publica la primera página en `info.cern.ch`. Era fea, blanca, con texto azul y enlaces subrayados. Y sigue viva. Búscala si quieres.

### 1993 — El navegador Mosaic
Un chico de 22 años en Illinois, **Marc Andreessen**, crea Mosaic: el primer navegador que muestra **imágenes junto al texto** en la misma página. La web explota.

### 1995 — Netscape e Internet Explorer
Guerra de navegadores. Cada uno añade sus propios inventos. Empieza el caos (y de ahí sale JavaScript, pero eso es historia para otro día).

### 2007 — El iPhone cambia todo
Antes había que escribir HTML pensando en pantallas gigantes. Ahora hay que pensar en pantallas de bolsillo. HTML evoluciona para responder a cualquier tamaño.

### Hoy — HTML5
La versión moderna (HTML5) salió en 2014 y nos trajo video nativo, audio, geolocalización, dibujo en canvas y mucho más. Ya no necesitas Flash ni plugins raros.

> 🎯 *Moraleja para los chicos:* HTML lleva más de 30 años viva porque sus creadores la hicieron **simple, abierta y adaptable**. No es propiedad de ninguna empresa. Es de todos.

---

## 🧬 Entonces, ¿qué es HTML? (5 minutos)

**HTML** = **H**yper**T**ext **M**arkup **L**anguage (Lenguaje de Marcado de Hipertexto).

Vamos por partes:

- **Hypertext (Hipertexto):** texto que puede saltar a otro texto con un click. El "hiper" es lo que hace que un link te lleve a otra parte.
- **Markup (Marcado):** no programas, no haces cálculos. **Marcar** significa rodear el contenido con etiquetas que le dicen al navegador *"esto es un título"*, *"esto es una imagen"*, *"esto es un párrafo"*.
- **Language (Lenguaje):** tiene reglas, como cualquier idioma. Si las respetas, te entiende. Si no, el navegador se confunde.

### 🍕 La analogía perfecta: la pizza
Imagina que el HTML es la pizza. Pero no la pizza cualquiera, sino la masa con los ingredientes básicos puestos en orden:

```
- masa (estructura)
- salsa (contenido)
- queso (más contenido)
- pepperoni (más contenido)
```

La masa sola no es bonita ni rica, pero sin ella no hay pizza. Eso es HTML: **la base sobre la que va todo lo demás**.

Después viene:
- **CSS** = la decoración (salsa, queso dorado, bordes perfectos)
- **JavaScript** = la interactividad (pide por la app, te llega caliente a la puerta, el queso se derrite solito)

Hoy solo hacemos la masa. Pero sin masa, no hay pizza. 🍕

---

## 🏗️ Anatomía de una página HTML (10 minutos)

Toda página HTML tiene esta estructura mínima:

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8">
    <title>Mi primera página</title>
  </head>
  <body>
    <!-- Aquí va todo lo que se ve -->
    <h1>¡Hola, mundo!</h1>
    <p>Estoy aprendiendo HTML.</p>
  </body>
</html>
```

### Desglosemos pieza por pieza:

| Pieza | Qué hace | Analogía |
|---|---|---|
| `<!DOCTYPE html>` | Le dice al navegador "esto es HTML5, no me confundas" | El sello de un sobre |
| `<html>` | La raíz. Todo vive adentro. | La caja que contiene la pizza |
| `<head>` | Cosas que NO se ven (título, codificación, metadatos) | La parte de atrás de un libro |
| `<body>` | Lo que SÍ se ve en pantalla | Lo que muestra la tele |
| `<h1>`, `<h2>`, … | Títulos, del más importante al menos | Títulos de un periódico |
| `<p>` | Párrafo de texto | Texto normal |
| `<!-- comentario -->` | Notas que no se ven, son para ti | Post-its que no se pegan |

### Las etiquetas más importantes para empezar

```html
<h1>Título principal</h1>
<h2>Subtítulo</h2>

<p>Un párrafo normal de texto.</p>

<a href="https://www.google.com">Link a Google</a>

<img src="foto.jpg" alt="Una foto">

<ul>
  <li>Elemento de lista 1</li>
  <li>Elemento de lista 2</li>
</ul>

<button>¡Clic aquí!</button>
```

**Dato clave:** casi todas las etiquetas van en pares: una abre `<p>` y otra cierra `</p>`. La barra `/` es la que cierra.

### HTML no es programación
Repite conmigo: **HTML NO es un lenguaje de programación**. Es un lenguaje de marcado. No tiene variables, no tiene if, no hace cálculos. Escribes, marcas, y el navegador lo pinta.

---

## 💻 Manos a la obra: tu primera página (20 minutos)

### Paso 1 — Crear el archivo
1. Abre el Bloc de notas (Windows) o TextEdit (Mac).
2. Pega este código:

```html
<!DOCTYPE html>
<html lang="es">
  <head>
    <meta charset="UTF-8">
    <title>Sobre mí</title>
  </head>
  <body>
    <h1>Hola, me llamo [tu nombre]</h1>
    <h2>Cosas que me gustan</h2>
    <ul>
      <li>Los tacos al pastor</li>
      <li>El fútbol</li>
      <li>Los videojuegos</li>
    </ul>
    <h2>Mi canción favorita</h2>
    <p>Por ahora estoy escuchando mucho a [artista].</p>
    <a href="https://www.youtube.com">Escuchar música en YouTube</a>
  </body>
</html>
```

3. Guarda como `sobre-mi.html` (importante: la extensión debe ser `.html`, no `.txt`).
4. Ábrelo con doble click. **¡Boom! Ya tienes tu primera página web.**

### Paso 2 — Ver el código
En la página abierta, presiona `Ctrl + U` (o click derecho → "Ver código fuente"). Verás tu propio HTML ahí. Eso mismo ve el navegador.

### Paso 3 — Inspecionar como pro
Presiona `F12` o click derecho → "Inspeccionar". Se abre un panel con mil cosas. **No te asustes.** Solo mira que del lado izquierdo está tu HTML y del derecho los estilos. Lo usaremos mucho.

### Paso 4 — Romper cosas a propósito
Borra una etiqueta de cierre. Guarda y recarga. ¿Qué pasó?  
Cambia `<h1>` por `<h6>`. ¿Qué cambió?  
Pon el texto fuera de cualquier etiqueta. ¿Se ve?  
**Romper es aprender.** Si no rompes nada, no estás experimentando lo suficiente.

---

## 🎯 Reto de la clase (10 minutos)

**Reto: "Mi tarjeta de presentación digital"**

Crea una página HTML que tenga:

- [ ] Tu nombre en un `<h1>`
- [ ] Tu edad y ciudad en un párrafo
- [ ] Una lista con 3 cosas que te gustan
- [ ] Un link a tu red social favorita
- [ ] Un emoji directo en el HTML (sí, se puede: `🎮`)
- [ ] Un comentario HTML con tu nombre como autor

**Bonus:**  
- Cambia el color de fondo de la página (spoiler: necesitas CSS, lo vemos la próxima clase). Si alguien lo logra hoy, aplausos. 👏
- Agrega una imagen con `<img src="...">` apuntando a una URL pública.

Tiempo: 10 minutos. Cuando terminen, comparten pantalla y vemos las más creativas.

---

## 🧠 Repaso relámpago (5 minutos)

Pregunta rápida a todo el grupo:

1. ¿Qué significa la H de HTML?  
2. ¿Quién inventó la World Wide Web?  
3. ¿HTML es un lenguaje de programación? (trampa)  
4. ¿Para qué sirve la etiqueta `<body>`?  
5. Si quiero un enlace, ¿qué etiqueta uso?  

(Respuestas al final del documento por si las necesitas 😉)

---

## 📦 ¿Qué viene la próxima clase?

> Hoy hicimos la masa.  
> La próxima clase vamos a ponerle los ingredientes: **colores, fuentes, tamaños, posiciones.**  
> Eso es CSS. Y es la clase favorita de todos. Prepárense.

---

## 📚 Para los curiosos (tarea opcional)

- Lee: [La propuesta original de Tim Berners-Lee (1989)](https://www.w3.org/History/1989/proposal.html) — corta, curiosa y firmada por él.
- Visita: la primera página web de la historia, todavía en línea.
- Experimenta: cambia todo lo que se te ocurra en tu archivo `sobre-mi.html`. Guarda y refresca. Repite hasta que te aburras.

---

## 🔑 Respuestas del repaso

1. **Hypertext**
2. **Tim Berners-Lee**
3. **No.** Es un lenguaje de marcado.
4. **Para contener todo lo que se ve en la página.**
5. **`<a href="...">`.**

---

> ✨ *Frase para cerrar la clase:* "Hoy no aprendieron a programar. Aprendieron a hablar un idioma que entienden los navegadores. Y eso, literalmente, les dio un superpoder."
