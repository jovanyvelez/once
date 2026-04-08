# 🎨 Maquetación Moderna con CSS
### Flexbox & CSS Grid — Material de Clase

> **Nivel:** Principiante-Intermedio  
> **Duración total:** 6 horas (2 clases de 3 horas)  
> **Herramientas necesarias:** Navegador web, editor de código (VS Code recomendado), [CodePen](https://codepen.io) o [JSFiddle](https://jsfiddle.net)

---

## 📋 Índice General

**Clase 1 — Flexbox**
1. [El Modelo de la Caja (Box Model)](#1-el-modelo-de-la-caja-box-model)
2. [¿Qué es la maquetación moderna?](#2-qué-es-la-maquetación-moderna)
3. [Introducción a Flexbox](#3-introducción-a-flexbox)
4. [Propiedades del contenedor flex](#4-propiedades-del-contenedor-flex)
5. [Propiedades de los elementos flex](#5-propiedades-de-los-elementos-flex)
6. [Ejemplos prácticos con Flexbox](#6-ejemplos-prácticos-con-flexbox)
7. [⏸️ DESCANSO 1 — 15 minutos](#descanso-1)
8. [🛠️ Taller 1: Flexbox](#taller-1)

**Clase 2 — CSS Grid**
9. [Introducción a CSS Grid](#9-introducción-a-css-grid)
10. [Definir filas y columnas](#10-definir-filas-y-columnas)
11. [Ubicar elementos en el grid](#11-ubicar-elementos-en-el-grid)
12. [Ejemplos prácticos con Grid](#12-ejemplos-prácticos-con-grid)
13. [⏸️ DESCANSO 2 — 15 minutos](#descanso-2)
14. [🛠️ Taller 2: CSS Grid](#taller-2)
15. [Flexbox vs Grid — ¿Cuándo usar cada uno?](#15-flexbox-vs-grid--cuándo-usar-cada-uno)
16. [Recursos para seguir aprendiendo](#16-recursos-para-seguir-aprendiendo)

---

# CLASE 1 — FLEXBOX
> ⏱️ Duración: 3 horas | Bloques: 120 min teoría + 15 min descanso + 60 min taller

---

---

## 1. El Modelo de la Caja (Box Model)

Antes de mover cajas, debemos entender de qué están hechas. En CSS, **todo es una caja**.

### Anatomía de la caja 📦

Cada elemento HTML se visualiza como una caja compuesta por cuatro capas, desde adentro hacia afuera:

1. **Content (Contenido):** Donde aparece el texto, imágenes o hijos.
2. **Padding (Relleno):** El espacio invisible que separa el contenido del borde.
3. **Border (Borde):** La línea (visible o no) que rodea el padding y el contenido.
4. **Margin (Margen):** El espacio exterior que separa esta caja de otras cajas.

**Visualización:**
```text
┌───────────────────────────────────────────┐
│  MARGEN (Exterior)                        │
│  ┌─────────────────────────────────────┐  │
│  │  BORDE                               │  │
│  │  ┌───────────────────────────────┐  │  │
│  │  │  PADDING (Relleno)            │  │  │
│  │  │  ┌─────────────────────────┐  │  │  │
│  │  │  │       CONTENIDO         │  │  │  │
│  │  │  └─────────────────────────┘  │  │  │
│  │  └───────────────────────────────┘  │  │
│  └─────────────────────────────────────┘  │
└───────────────────────────────────────────┘
```

### La propiedad `box-sizing: border-box` ✨

Por defecto (`content-box`), cuando sumas padding o borde, la caja **crece** y rompe tu diseño.

> [!IMPORTANT]
> Los profesionales usamos siempre `border-box`. Esto hace que el ancho (`width`) incluya el padding y el borde, evitando que la caja se "infle".

```css
/* El "reset" que todo proyecto moderno debe tener */
* {
  box-sizing: border-box;
}
```

---

## 2. ¿Qué es la maquetación moderna?

Antes de entrar al código, hay que entender **por qué** existe la maquetación moderna.

### El problema del pasado 🕰️

Imagínate que quieres poner tres cajas una al lado de la otra en una página web. Antes de 2012, los desarrolladores hacían cosas como esta:

```css
/* Método antiguo — NO hagas esto 😅 */
.caja {
  float: left;
  width: 33%;
}
.contenedor::after {
  content: "";
  display: block;
  clear: both;
}
```

Esto era confuso, difícil de mantener y se rompía fácilmente en pantallas pequeñas (celulares). Era como construir una casa con cinta adhesiva.

### La solución moderna ✅

Hoy tenemos dos herramientas poderosas que hacen el trabajo de forma limpia y lógica:

| Herramienta | Ideal para | Dirección |
|-------------|------------|-----------|
| **Flexbox** | Distribuir elementos en **una sola dirección** (fila o columna) | 1D |
| **CSS Grid** | Crear **layouts completos** con filas Y columnas | 2D |

> [!TIP]
> **Dato curioso:** Flexbox fue diseñado por el equipo de CSS en 2009, pero se volvió estable y confiable alrededor de 2015. Grid llegó oficialmente en 2017. ¡Son tecnologías relativamente recientes!

---

## 3. Introducción a Flexbox

### ¿Qué significa "Flex"?

**Flex** viene de *flexible*. La idea es que los elementos dentro de un contenedor se adapten, crezcan o encojan de forma automática según el espacio disponible.

### El modelo mental 🧠

Piensa en Flexbox como una **fila de asientos en un bus**:
- El **bus** es el contenedor (`display: flex`)
- Los **pasajeros** son los elementos hijos
- Puedes decirle a los pasajeros que se acomoden hacia la izquierda, la derecha, el centro, o que llenen todo el espacio disponible

### Activar Flexbox

Solo necesitas **una línea de CSS** en el elemento padre:

```css
.contenedor {
  display: flex;
}
```

¡Eso es todo! Automáticamente, todos los hijos directos se convierten en *flex items* y se acomodan en una fila.

### Ejemplo base

```html
<!-- HTML -->
<div class="contenedor">
  <div class="caja">1</div>
  <div class="caja">2</div>
  <div class="caja">3</div>
</div>
```

```css
/* CSS */
.contenedor {
  display: flex;
  background-color: #f0f0f0;
  padding: 10px;
}

.caja {
  background-color: #4a90e2;
  color: white;
  padding: 20px;
  margin: 5px;
  font-size: 20px;
  font-weight: bold;
}
```

**Resultado:** Las tres cajas aparecen en fila, una al lado de la otra. Sin `display: flex`, estarían apiladas verticalmente.

---

## 4. Propiedades del Contenedor Flex

Estas propiedades se aplican al **elemento padre** (el contenedor).

### 3.1 `flex-direction` — La dirección del flujo

Controla si los elementos van en fila (horizontal) o columna (vertical).

```css
.contenedor {
  display: flex;
  flex-direction: row;           /* → por defecto: izquierda a derecha */
  /* flex-direction: row-reverse;   ← derecha a izquierda */
  /* flex-direction: column;        ↓ arriba hacia abajo */
  /* flex-direction: column-reverse;↑ abajo hacia arriba */
}
```

**Visualización:**

```text
flex-direction: row (por defecto)
[ 1 ] [ 2 ] [ 3 ]

flex-direction: column
[ 1 ]
[ 2 ]
[ 3 ]
```

---

### 3.2 `justify-content` — Alineación en el eje principal

Controla cómo se distribuyen los elementos en la **dirección principal** (horizontal si `flex-direction: row`).

```css
.contenedor {
  display: flex;
  justify-content: flex-start;    /* |[1][2][3]          | */
  /* justify-content: flex-end;      |          [1][2][3]| */
  /* justify-content: center;        |   [1][2][3]       | */
  /* justify-content: space-between; |[1]    [2]    [3]  | */
  /* justify-content: space-around;  | [1]  [2]  [3]    | */
  /* justify-content: space-evenly;  |  [1]  [2]  [3]   | */
}
```

> [!TIP]
> **Tip para recordarlo:** `justify-content` maneja el espacio como un "justificado" de texto — lo mismo que en Word cuando centras o alineas un párrafo.

---

### 3.3 `align-items` — Alineación en el eje secundario

Si `flex-direction: row`, entonces `align-items` controla la alineación **vertical**.

```css
.contenedor {
  display: flex;
  height: 200px;                 /* Necesita altura para que se note */
  align-items: stretch;          /* por defecto: estira los hijos */
  /* align-items: flex-start;       alinea arriba */
  /* align-items: flex-end;         alinea abajo */
  /* align-items: center;           centra verticalmente ✨ */
}
```

> [!IMPORTANT]
> **El truco del centrado perfecto:** ¿Quieres centrar algo horizontal Y verticalmente? Esta es la combinación mágica:

```css
.contenedor {
  display: flex;
  justify-content: center;
  align-items: center;
}
```

---

### 3.4 `flex-wrap` — ¿Se pueden envolver los elementos?

Por defecto, todos los elementos se quedan en **una sola línea**, aunque no quepan. Con `flex-wrap` les damos permiso de pasar a la siguiente fila.

```css
.contenedor {
  display: flex;
  flex-wrap: nowrap;    /* por defecto — todos en una línea */
  /* flex-wrap: wrap;      pasan a la siguiente línea si no hay espacio */
  /* flex-wrap: wrap-reverse; igual pero en orden inverso */
}
```

**Ejemplo visual:**

```text
nowrap (por defecto):
[ 1 ][ 2 ][ 3 ][ 4 ][ 5 ][ 6 ]

wrap (salto de línea):
[ 1 ][ 2 ][ 3 ]
[ 4 ][ 5 ][ 6 ]
```

---

### 3.5 `gap` — Espacio entre elementos

En lugar de usar `margin` en cada hijo, puedes poner el espacio desde el padre:

```css
.contenedor {
  display: flex;
  gap: 16px;          /* espacio igual en todos lados */
  /* gap: 10px 20px;    fila columna (vertical horizontal) */
}
```

---

## 5. Propiedades de los Elementos Flex

Estas propiedades se aplican a los **hijos** del contenedor.

### 4.1 `flex-grow` — ¿Cuánto puede crecer?

Define si un elemento puede ocupar el espacio sobrante, y cuánto.

```css
.elemento-a { flex-grow: 1; }  /* ocupa 1 parte del espacio libre */
.elemento-b { flex-grow: 2; }  /* ocupa 2 partes (el doble que A) */
.elemento-c { flex-grow: 0; }  /* no crece (valor por defecto) */
```

**Resultado visual:**
```text
|  [A (crece 1x)]  |  [B (crece 2x)]  | [C (0)] |
```

---

### 4.2 `flex-shrink` — ¿Cuánto puede encogerse?

El opuesto de `flex-grow`: controla qué tan rápido se encoge un elemento cuando no hay espacio.

```css
.elemento {
  flex-shrink: 1;   /* se encoge normalmente (por defecto) */
  /* flex-shrink: 0;   ¡no se encoge nunca! */
  /* flex-shrink: 2;   se encoge el doble de rápido */
}
```

---

### 4.3 `flex-basis` — Tamaño base

El tamaño "sugerido" del elemento antes de que el navegador reparta el espacio libre.

```css
.elemento {
  flex-basis: 200px;   /* empieza con 200px de ancho */
  /* flex-basis: auto;    usa el ancho del contenido (por defecto) */
  /* flex-basis: 0;       empieza desde cero */
}
```

---

### 4.4 `flex` — La propiedad abreviada ⚡

En lugar de escribir `flex-grow`, `flex-shrink` y `flex-basis` por separado, puedes usar la propiedad abreviada:

```css
.elemento {
  flex: 1;              /* grow:1, shrink:1, basis:0 — muy común */
  /* flex: 0 0 200px;     no crece, no se encoge, 200px fijo */
  /* flex: 2 1 auto;      crece doble, se encoge normal, tamaño auto */
}
```

> [!TIP]
> `flex: 1` es una de las combinaciones más usadas en el mundo real. Significa "ocupa todo el espacio disponible de forma equitativa".

---

### 4.5 `align-self` — Alineación individual

Permite que **un solo elemento** ignore el `align-items` del padre y tenga su propia alineación.

```css
.elemento-especial {
  align-self: flex-end;   /* solo este baja al fondo */
}
```

---

### 4.6 `order` — Cambiar el orden visual

Puedes cambiar el orden en que aparecen los elementos **sin modificar el HTML**.

```css
.primero-visualmente  { order: 1; }
.segundo-visualmente  { order: 2; }
.tercero-visualmente  { order: 3; }
```

> [!WARNING]
> **Cuidado:** Cambiar el orden visual pero no el del HTML puede confundir a los lectores de pantalla (accesibilidad). Úsalo con responsabilidad.

---

## 6. Ejemplos Prácticos con Flexbox

### Ejemplo 1: Barra de navegación

```html
<nav class="navbar">
  <div class="logo">🎮 MiSitio</div>
  <ul class="nav-links">
    <li><a href="#">Inicio</a></li>
    <li><a href="#">Proyectos</a></li>
    <li><a href="#">Contacto</a></li>
  </ul>
</nav>
```

```css
.navbar {
  display: flex;
  justify-content: space-between;  /* logo a la izquierda, links a la derecha */
  align-items: center;             /* centrado vertical */
  background-color: #1a1a2e;
  padding: 0 24px;
  height: 64px;
}

.logo {
  color: white;
  font-size: 1.5rem;
  font-weight: bold;
}

.nav-links {
  display: flex;
  list-style: none;
  gap: 24px;
  margin: 0;
  padding: 0;
}

.nav-links a {
  color: #a0aec0;
  text-decoration: none;
  transition: color 0.2s;
}

.nav-links a:hover {
  color: white;
}
```

---

### Ejemplo 2: Tarjetas de productos

```html
<section class="galeria">
  <div class="tarjeta">
    <img src="https://picsum.photos/seed/a/300/200" alt="Producto 1">
    <div class="info">
      <h3>Producto 1</h3>
      <p>Descripción corta del producto.</p>
      <button>Agregar al carrito</button>
    </div>
  </div>
  <div class="tarjeta">
    <img src="https://picsum.photos/seed/b/300/200" alt="Producto 2">
    <div class="info">
      <h3>Producto 2</h3>
      <p>Descripción corta del producto.</p>
      <button>Agregar al carrito</button>
    </div>
  </div>
  <div class="tarjeta">
    <img src="https://picsum.photos/seed/c/300/200" alt="Producto 3">
    <div class="info">
      <h3>Producto 3</h3>
      <p>Descripción corta del producto.</p>
      <button>Agregar al carrito</button>
    </div>
  </div>
</section>
```

```css
.galeria {
  display: flex;
  flex-wrap: wrap;         /* se adapta a pantallas pequeñas */
  gap: 20px;
  padding: 20px;
  justify-content: center;
}

.tarjeta {
  display: flex;
  flex-direction: column;  /* imagen arriba, info abajo */
  width: 280px;
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 12px rgba(0,0,0,0.1);
  background: white;
}

.tarjeta img {
  width: 100%;
  height: 180px;
  object-fit: cover;
}

.info {
  display: flex;
  flex-direction: column;
  flex: 1;                  /* ocupa todo el espacio disponible */
  padding: 16px;
  gap: 8px;
}

.info button {
  margin-top: auto;         /* empuja el botón al fondo de la tarjeta */
  padding: 10px;
  background-color: #4a90e2;
  color: white;
  border: none;
  border-radius: 6px;
  cursor: pointer;
}
```

> [!NOTE]
> **Observa el truco:** `margin-top: auto` en el botón lo empuja hasta abajo, haciendo que todas las tarjetas tengan el botón alineado, sin importar cuánto texto tengan.

---

### Ejemplo 3: Centrado perfecto — El Santo Grial del CSS

Algo que antes tomaba 10 líneas de CSS:

```css
/* Antes (método antiguo) */
.centrado {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
}

/* Ahora con Flexbox ✨ */
.centrado {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh; /* o cualquier altura */
}
```

---

## 7. ⏸️ DESCANSO 1 — 15 minutos <a name="descanso-1"></a>

> [!TIP]
> **🎮 TIEMPO LIBRE — 15 MINUTOS**
> 
> Levántate, estira las piernas, toma agua o un snack.
> 
> **Reto opcional:** antes de volver, abre CodePen e intenta centrar un div con Flexbox de memoria.

---

## 8. 🛠️ Taller 1: Construye tu Tarjeta de Perfil <a name="taller-1"></a>

> ⏱️ **Tiempo:** 60 minutos  
> 👤 **Trabajo:** Individual  
> 🛠️ **Herramienta:** CodePen, JSFiddle o VS Code

### Descripción del proyecto

Vas a construir una **tarjeta de perfil** similar a las que se ven en redes sociales o portfolios. Toda la maquetación debe hacerse **exclusivamente con Flexbox**.

### Requerimientos obligatorios ✅

Tu tarjeta de perfil debe incluir:

1. **Avatar o imagen de perfil** (puede ser un placeholder de `https://picsum.photos/150/150`)
2. **Nombre y usuario** (ejemplo: "Ana García / @ana.dev")
3. **Una bio corta** (1-2 líneas de texto)
4. **3 estadísticas** en fila: Proyectos, Seguidores, Siguiendo (con número y etiqueta)
5. **2 botones de acción:** "Seguir" y "Mensaje"
6. **3 miniaturas de proyectos** en fila (imágenes pequeñas)

### Requerimientos de Flexbox ✅

Debes usar **al menos** estas propiedades (márcalas cuando las uses):

- [ ] `display: flex` en al menos 3 contenedores distintos
- [ ] `flex-direction` (al menos una vez en columna)
- [ ] `justify-content` (al menos 2 valores distintos)
- [ ] `align-items`
- [ ] `gap`
- [ ] `flex-wrap` (en la sección de miniaturas)
- [ ] `flex: 1` o `flex-grow` (al menos una vez)

### Estructura HTML sugerida (¡puedes modificarla!)

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mi Tarjeta de Perfil</title>
  <style>
    /* Tu CSS aquí */
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    
    body {
      font-family: sans-serif;
      background: #f5f5f5;
      display: flex;
      justify-content: center;
      align-items: center;
      min-height: 100vh;
    }
    
    /* ↓ ESCRIBE TU CSS AQUÍ ↓ */
    
  </style>
</head>
<body>
  
  <div class="tarjeta">
    
    <!-- Sección superior: avatar + nombre -->
    <div class="perfil-header">
      <!-- Tu código aquí -->
    </div>
    
    <!-- Bio -->
    <p class="bio">
      <!-- Tu texto aquí -->
    </p>
    
    <!-- Estadísticas -->
    <div class="estadisticas">
      <!-- Tu código aquí -->
    </div>
    
    <!-- Botones -->
    <div class="botones">
      <!-- Tu código aquí -->
    </div>
    
    <!-- Miniaturas de proyectos -->
    <div class="miniaturas">
      <!-- Tu código aquí -->
    </div>
    
  </div>

</body>
</html>
```

### Criterios de evaluación

| Criterio | Puntos |
|----------|--------|
| Todos los elementos requeridos presentes | 20 pts |
| Uso correcto de las propiedades Flexbox marcadas | 30 pts |
| Diseño visualmente ordenado y coherente | 20 pts |
| La tarjeta se ve bien en ventana reducida (responsive) | 20 pts |
| Creatividad / personalización del diseño | 10 pts |
| **Total** | **100 pts** |

### Recursos de apoyo

- 🎮 [Flexbox Froggy](https://flexboxfroggy.com/#es) — Juego para practicar Flexbox
- 📖 [CSS Tricks: Guía completa de Flexbox](https://css-tricks.com/snippets/css/a-guide-to-flexbox/)
- 🎨 [Coolors](https://coolors.co) — Generador de paletas de colores

---
---

# CLASE 2 — CSS GRID
> ⏱️ Duración: 3 horas | Bloques: 90 min teoría + 15 min descanso + 75 min taller

---

## 9. Introducción a CSS Grid

### ¿Por qué Grid si ya tenemos Flexbox?

Flexbox es genial para **una dimensión** (filas O columnas). Pero, ¿qué pasa cuando necesitas controlar **filas Y columnas al mismo tiempo**?

Imagina el layout de una revista: tienes una cabecera, una barra lateral, el contenido principal, y un pie de página. Hacer eso con Flexbox requiere muchos contenedores anidados y es complicado. Con Grid, lo defines todo desde un solo lugar.

### El modelo mental 🧠

Piensa en Grid como una **hoja de cuadrícula**:
- Defines cuántas columnas y filas quieres
- Los elementos se colocan en las celdas de esa cuadrícula
- Puedes hacer que un elemento ocupe **múltiples celdas**

```
┌────────────┬────────────┬────────────┐
│     1      │     2      │     3      │
├────────────┼────────────┼────────────┤
│     4      │     5      │     6      │
├────────────┼────────────┼────────────┤
│     7      │     8      │     9      │
└────────────┴────────────┴────────────┘
```

### Activar CSS Grid

```css
.contenedor {
  display: grid;
}
```

Sin definir columnas, funciona igual que el flujo normal. La magia viene cuando defines la estructura.

---

## 10. Definir Filas y Columnas

### 9.1 `grid-template-columns` — Definir columnas

```css
.contenedor {
  display: grid;
  
  /* 3 columnas de tamaño fijo */
  grid-template-columns: 200px 200px 200px;
  
  /* Lo mismo con repeat() */
  grid-template-columns: repeat(3, 200px);
  
  /* 3 columnas que se reparten el espacio igual */
  grid-template-columns: 1fr 1fr 1fr;
  
  /* O con repeat */
  grid-template-columns: repeat(3, 1fr);
  
  /* Mezcla: barra lateral fija + contenido flexible */
  grid-template-columns: 250px 1fr;
  
  /* Columna pequeña + grande + pequeña */
  grid-template-columns: 1fr 2fr 1fr;
}
```

> [!TIP]
> **¿Qué es `fr`?** Es una unidad especial de Grid que significa *fracción* del espacio disponible. `1fr 1fr 1fr` divide el espacio en tres partes iguales, igual que `flex: 1` en Flexbox pero para Grid.

---

### 9.2 `grid-template-rows` — Definir filas

```css
.contenedor {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  
  /* 2 filas: primera de 100px, segunda de 300px */
  grid-template-rows: 100px 300px;
  
  /* Altura automática según contenido */
  grid-template-rows: auto auto;
}
```

---

### 9.3 La función `minmax()` — Tamaños flexibles

Una de las funciones más útiles de Grid: define un tamaño **entre un mínimo y un máximo**.

```css
.contenedor {
  display: grid;
  
  /* Columnas de mínimo 200px, máximo que crezcan igual */
  grid-template-columns: repeat(3, minmax(200px, 1fr));
}
```

---

### 9.4 `auto-fill` y `auto-fit` — Columnas automáticas

La combinación de `repeat()` con `auto-fill` o `auto-fit` y `minmax()` es una de las más poderosas del CSS moderno:

```css
.galeria {
  display: grid;
  /* Crea tantas columnas como quepan, cada una de mínimo 250px */
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 16px;
}
```

Esto crea un layout **completamente responsivo** sin una sola media query. Los elementos se acomodan solos según el ancho de la pantalla.

---

### 9.5 `gap` — Espacio entre celdas

Igual que en Flexbox:

```css
.contenedor {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  
  gap: 20px;              /* espacio igual en filas y columnas */
  /* row-gap: 20px;          solo espacio entre filas */
  /* column-gap: 10px;       solo espacio entre columnas */
  /* gap: 20px 10px;         filas columnas */
}
```

---

### 9.6 `grid-template-areas` — Layout con nombres

Esta es la propiedad más visual e intuitiva de Grid. Le das **nombres** a las áreas:

```css
.layout {
  display: grid;
  grid-template-columns: 250px 1fr;
  grid-template-rows: 80px 1fr 60px;
  grid-template-areas:
    "header  header"
    "sidebar main"
    "footer  footer";
  min-height: 100vh;
}

.header  { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main    { grid-area: main; }
.footer  { grid-area: footer; }
```

```
┌──────────────────────────────┐
│           HEADER             │
├──────────┬───────────────────┤
│          │                   │
│ SIDEBAR  │       MAIN        │
│          │                   │
├──────────┴───────────────────┤
│           FOOTER             │
└──────────────────────────────┘
```

> [!TIP]
> Cuando ves las `grid-template-areas`, puedes "dibujar" mentalmente el layout. Si una misma palabra aparece en varias celdas, ese elemento ocupa todas esas celdas.

---

## 11. Ubicar Elementos en el Grid

### 10.1 `grid-column` y `grid-row` — Posicionamiento manual

Puedes decirle a un elemento exactamente en qué **línea** empieza y termina.

Las líneas en Grid se cuentan desde 1:

```
Columnas:  1    2    3    4
           |    |    |    |
           | c1 | c2 | c3 |
```

```css
.elemento {
  /* Ocupa desde la línea 1 hasta la línea 3 (2 columnas) */
  grid-column: 1 / 3;
  
  /* Ocupa desde la línea 1 hasta la línea 2 (1 fila) */
  grid-row: 1 / 2;
}

/* Abreviación con span — "ocupa 2 columnas desde donde esté" */
.elemento {
  /* Ocupa 2 columnas desde donde esté */
  grid-column: span 2;
  /* Ocupa 3 filas desde donde esté */
  grid-row: span 3;
}
```

---

### 10.2 Alineación en Grid

Grid también tiene propiedades de alineación:

```css
/* En el contenedor — afecta a todos los elementos */
.contenedor {
  display: grid;
  justify-items: center;  /* alineación horizontal de cada celda */
  align-items: center;    /* alineación vertical de cada celda */
}

/* En el contenedor — alineación del grid completo */
.contenedor {
  justify-content: center;  /* el grid completo dentro del contenedor */
  align-content: center;
}

/* En el elemento — sobreescribe la alineación del padre */
.elemento {
  justify-self: end;
  align-self: start;
}
```

---

## 12. Ejemplos Prácticos con Grid

### Ejemplo 1: Layout de página completa

```html
<div class="layout">
  <header class="header">🏠 Mi Blog</header>
  <nav class="sidebar">
    <ul>
      <li>Inicio</li>
      <li>Artículos</li>
      <li>Acerca de</li>
    </ul>
  </nav>
  <main class="main">
    <h1>Bienvenido a mi blog</h1>
    <p>Aquí encontrarás artículos sobre tecnología y diseño.</p>
  </main>
  <footer class="footer">© 2024 Mi Blog</footer>
</div>
```

```css
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: sans-serif;
}

.layout {
  display: grid;
  grid-template-columns: 220px 1fr;
  grid-template-rows: 64px 1fr 48px;
  grid-template-areas:
    "header header"
    "sidebar main"
    "footer footer";
  min-height: 100vh;
}

.header {
  grid-area: header;
  background: #1a1a2e;
  color: white;
  display: flex;
  align-items: center;
  padding: 0 24px;
  font-size: 1.4rem;
  font-weight: bold;
}

.sidebar {
  grid-area: sidebar;
  background: #f7f7f7;
  padding: 24px 16px;
  border-right: 1px solid #e0e0e0;
}

.sidebar ul {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.sidebar li {
  padding: 10px 12px;
  border-radius: 6px;
  cursor: pointer;
  transition: background 0.2s;
}

.sidebar li:hover {
  background: #e8e8e8;
}

.main {
  grid-area: main;
  padding: 32px;
}

.footer {
  grid-area: footer;
  background: #1a1a2e;
  color: #a0aec0;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.875rem;
}
```

---

### Ejemplo 2: Galería fotográfica con elementos destacados

```html
<div class="galeria">
  <div class="foto destacada">📸 Foto 1 (destacada)</div>
  <div class="foto">📸 Foto 2</div>
  <div class="foto">📸 Foto 3</div>
  <div class="foto">📸 Foto 4</div>
  <div class="foto wide">📸 Foto 5 (ancha)</div>
  <div class="foto">📸 Foto 6</div>
</div>
```

```css
.galeria {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  padding: 20px;
}

.foto {
  background: #4a90e2;
  color: white;
  padding: 30px;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
}

/* Esta foto ocupa 2 columnas y 2 filas */
.foto.destacada {
  grid-column: span 2;
  grid-row: span 2;
  background: #e24a4a;
  font-size: 1.2rem;
}

/* Esta foto ocupa todo el ancho */
.foto.wide {
  grid-column: 1 / -1;   /* -1 significa "hasta la última línea" */
  background: #4ae24a;
}
```

---

### Ejemplo 3: Grid responsivo sin media queries

```css
.galeria-responsive {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 16px;
}
```

Con esto:
- En una pantalla grande: 4-5 columnas
- En una tablet: 2-3 columnas  
- En un celular: 1-2 columnas

¡Todo automático! 🎉

---

## 13. ⏸️ DESCANSO 2 — 15 minutos <a name="descanso-2"></a>

> [!TIP]
> **🍃 TIEMPO LIBRE — 15 MINUTOS**
> 
> ¡Estamos en la recta final! Descansa la vista, mueve el cuerpo.
> 
> **Reto opcional:** dibuja en papel el layout de tu taller antes de escribir el código.

> 📌 **Nota pedagógica:** Este descanso viene después de los primeros 90 minutos de la segunda clase. En este punto ya tienen la teoría completa de Grid. La pausa les permite consolidar lo aprendido y llegar frescos al taller, que es la parte más creativa y exigente de la sesión.

---

## 14. 🛠️ Taller 2: Diseña una Revista Digital <a name="taller-2"></a>

> ⏱️ **Tiempo:** 75 minutos  
> 👤 **Trabajo:** Individual  
> 🛠️ **Herramienta:** CodePen, JSFiddle o VS Code

### Descripción del proyecto

Vas a crear el **layout de portada de una revista digital** sobre el tema que más te guste (videojuegos, música, deportes, moda, tecnología...). La maquetación debe hacerse **exclusivamente con CSS Grid** (el estilo visual puede incluir Flexbox para detalles internos).

### Requerimientos obligatorios ✅

Tu portada de revista debe incluir:

1. **Cabecera (header):** Nombre de la revista + menú de navegación con al menos 4 secciones
2. **Artículo principal (hero):** Imagen grande + titular + resumen de 2-3 líneas
3. **Artículos secundarios (al menos 3):** Más pequeños, con imagen, título y categoría
4. **Barra lateral (sidebar):** Puede incluir noticias breves, publicidad ficticia, o sección "Lo más leído"
5. **Pie de página (footer):** Nombre de la revista, año, redes sociales (pueden ser íconos de emoji)

### Requerimientos de CSS Grid ✅

Debes usar **al menos** estas propiedades (márcalas cuando las uses):

- [ ] `display: grid` en al menos 2 contenedores distintos
- [ ] `grid-template-columns` con al menos una columna `fr`
- [ ] `grid-template-rows`
- [ ] `grid-template-areas` (para el layout general)
- [ ] `grid-area` (para asignar elementos al área correspondiente)
- [ ] `grid-column: span` o `grid-column: X / Y` (al menos en el artículo principal)
- [ ] `gap`
- [ ] `minmax()` o `auto-fit`/`auto-fill` (en al menos una sección)

### Estructura HTML sugerida (¡es un punto de partida, modifícala!)

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mi Revista Digital</title>
  <style>
    * {
      margin: 0;
      padding: 0;
      box-sizing: border-box;
    }
    
    body {
      font-family: Georgia, serif;
      background: #f9f9f7;
      color: #222;
    }
    
    /* ↓ ESCRIBE TU CSS AQUÍ ↓ */
    
  </style>
</head>
<body>
  
  <!-- LAYOUT PRINCIPAL -->
  <div class="revista">
    
    <header class="header">
      <!-- Nombre de la revista y navegación -->
    </header>
    
    <main class="hero">
      <!-- Artículo principal con imagen grande -->
    </main>
    
    <section class="articulos">
      <!-- Artículos secundarios con grid interno -->
      <article class="articulo"><!-- ... --></article>
      <article class="articulo"><!-- ... --></article>
      <article class="articulo"><!-- ... --></article>
    </section>
    
    <aside class="sidebar">
      <!-- Contenido de barra lateral -->
    </aside>
    
    <footer class="footer">
      <!-- Información del footer -->
    </footer>
    
  </div>

</body>
</html>
```

### Boceto de referencia (una posibilidad)

```
┌────────────────────────────────────────────┐
│               NOMBRE REVISTA               │  ← header
│   Sección1 | Sección2 | Sección3 | Sec4   │
├────────────────────────────┬───────────────┤
│                            │               │
│      ARTÍCULO PRINCIPAL    │   SIDEBAR     │  ← hero + aside
│         (imagen grande)    │   (lo más     │
│         Titular grande     │    leído)     │
│         Resumen...         │               │
├────────────────────────────┤               │
│  [art2]  [art3]  [art4]   │               │  ← artículos
│                            │               │
├────────────────────────────┴───────────────┤
│                  FOOTER                    │
└────────────────────────────────────────────┘
```

> [!TIP]
> **Consejo:** Dibuja tu propio boceto antes de escribir código. Unos 5 minutos de planificación te ahorran 30 minutos de frustración.

### Criterios de evaluación

| Criterio | Puntos |
|----------|--------|
| Todos los elementos requeridos presentes | 20 pts |
| Uso correcto de las propiedades Grid marcadas | 30 pts |
| El layout se asemeja a una revista real | 20 pts |
| Coherencia visual: colores, tipografía, espaciado | 20 pts |
| Creatividad / tema elegido / detalles extra | 10 pts |
| **Total** | **100 pts** |

### Recursos de apoyo

- 🎮 [Grid Garden](https://cssgridgarden.com/#es) — Juego para practicar Grid
- 📖 [CSS Tricks: Guía completa de Grid](https://css-tricks.com/snippets/css/complete-guide-grid/)
- 🖼️ [Lorem Picsum](https://picsum.photos) — Imágenes de placeholder: `https://picsum.photos/400/300`
- 🎨 [Coolors](https://coolors.co) — Paletas de colores

---

## 15. Flexbox vs Grid — ¿Cuándo usar cada uno?

Esta es la pregunta más frecuente después de aprender ambas tecnologías. La respuesta corta es: **se complementan, no compiten**.

### Guía rápida de decisión

| Si necesitas... | Usa... |
| :--- | :--- |
| El **layout general** de la página | **CSS Grid** |
| Acomodar elementos en **una sola dirección** | **Flexbox** |
| Que un elemento ocupe **múltiples filas y columnas** | **CSS Grid** |
| **Centrar** algo rápidamente | **Flexbox** |
| Manejar un número **desconocido** de elementos | **Flexbox** (con wrap) |
| Un diseño con **posiciones precisas** y fijas | **CSS Grid** |

### Tabla comparativa

| Característica | Flexbox | Grid |
|---------------|---------|------|
| Dimensiones | 1D (fila o columna) | 2D (filas y columnas) |
| Control del layout | Los hijos controlan su tamaño | El padre controla el layout |
| Alineación | Excelente para alinear elementos | Bueno, especialmente con `align-items` |
| Responsivo | Con `flex-wrap` y `flex` | Con `auto-fill`, `minmax()` |
| Caso de uso típico | Navbars, botones, tarjetas en fila | Layouts de página, galerias, dashboards |

### El ejemplo definitivo: úsalos juntos

```css
/* Grid para el layout general */
.pagina {
  display: grid;
  grid-template-areas:
    "header header"
    "sidebar main"
    "footer footer";
  grid-template-columns: 250px 1fr;
}

/* Flexbox para el contenido interno del header */
.header {
  grid-area: header;
  display: flex;                 /* ← Flexbox dentro de un área Grid */
  justify-content: space-between;
  align-items: center;
}
```

**Esto es lo que hacen los profesionales:** Grid para la estructura, Flexbox para los detalles.

---

## 16. Recursos para Seguir Aprendiendo

### 🎮 Juegos interactivos (la forma más divertida)
- [Flexbox Froggy](https://flexboxfroggy.com/#es) — Ayuda a una rana a llegar a su hoja con Flexbox
- [CSS Grid Garden](https://cssgridgarden.com/#es) — Riega tus plantas con Grid
- [Flexbox Defense](http://www.flexboxdefense.com/) — Tower defense con Flexbox (en inglés)

### 📖 Documentación y guías
- [MDN Web Docs — Flexbox](https://developer.mozilla.org/es/docs/Learn/CSS/CSS_layout/Flexbox) — En español
- [MDN Web Docs — Grid](https://developer.mozilla.org/es/docs/Learn/CSS/CSS_layout/Grids) — En español
- [CSS Tricks: Guía de Flexbox](https://css-tricks.com/snippets/css/a-guide-to-flexbox/) — La guía visual de referencia
- [CSS Tricks: Guía de Grid](https://css-tricks.com/snippets/css/complete-guide-grid/) — Igual de esencial

### 🛠️ Herramientas de práctica
- [CodePen](https://codepen.io) — Editor online, sin instalar nada
- [CSS Grid Generator](https://cssgrid-generator.netlify.app/) — Genera código Grid visualmente
- [Flexbox Playground](https://flexbox.tech/) — Prueba propiedades en tiempo real

### 📺 Canales de YouTube recomendados
- **Kevin Powell** — El mejor canal de CSS en YouTube (en inglés, subtítulos disponibles)
- **Bluuweb** — Excelente canal en español sobre desarrollo web
- **Hola Mundo** — Canal latinoamericano con tutoriales de HTML/CSS

### 🏆 Próximos pasos sugeridos
1. Completar todos los niveles de Flexbox Froggy y Grid Garden
2. Reconstruir el layout de tu sitio web favorito
3. Aprender **CSS Variables** (`--mi-color: #4a90e2`)
4. Explorar **CSS Animations** y **Transitions**
5. Aprender los fundamentos de **diseño responsivo** y **media queries**

---

## 📝 Resumen — Hoja de Referencia Rápida

### Flexbox

```css
/* Contenedor */
.flex {
  display: flex;
  flex-direction: row | row-reverse | column | column-reverse;
  justify-content: flex-start | flex-end | center | space-between | space-around | space-evenly;
  align-items: stretch | flex-start | flex-end | center | baseline;
  flex-wrap: nowrap | wrap | wrap-reverse;
  gap: valor;
}

/* Elementos */
.flex-item {
  flex-grow: número;    /* cuánto puede crecer */
  flex-shrink: número;  /* cuánto puede encogerse */
  flex-basis: tamaño;   /* tamaño base */
  flex: grow shrink basis; /* abreviado */
  align-self: auto | flex-start | flex-end | center | stretch;
  order: número;
}
```

### CSS Grid

```css
/* Contenedor */
.grid {
  display: grid;
  grid-template-columns: valores | repeat(n, valor) | repeat(auto-fill, minmax(min, max));
  grid-template-rows: valores;
  grid-template-areas: "nombre nombre" "otro otro";
  gap: valor;
  justify-items: start | end | center | stretch;
  align-items: start | end | center | stretch;
}

/* Elementos */
.grid-item {
  grid-column: inicio / fin | span n;
  grid-row: inicio / fin | span n;
  grid-area: nombre;
  justify-self: start | end | center | stretch;
  align-self: start | end | center | stretch;
}
```

---

*Material desarrollado para clases de Desarrollo Web — Maquetación Moderna*  
*Actualizado: 2024 | Licencia: CC BY-SA 4.0 — Libre para usar y adaptar con atribución*
