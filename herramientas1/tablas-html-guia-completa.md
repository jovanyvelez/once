# 🗂️ Construcción de Tablas en HTML
### Guía de aprendizaje interactiva — Nivel Introductorio

> 📚 **Dirigido a:** Jóvenes de 15 a 16 años con conocimientos básicos de HTML  
> ⏱️ **Duración total:** 210 minutos de clase + 2 descansos de 15 minutos  
> 🎯 **Objetivo:** Dominar la creación y estructuración de tablas en HTML desde cero

---

## 🗺️ Mapa de la sesión

| Bloque | Actividad | Duración |
|--------|-----------|----------|
| 🟢 Bloque 1 | Introducción y fundamentos de tablas | 30 min |
| 🟢 Bloque 2 | Etiquetas `thead`, `tbody` y `tfoot` | 30 min |
| 🟢 Bloque 3 | Atributos y personalización | 30 min |
| 🟢 Bloque 4 | Taller práctico — Parte 1 | 30 min |
| ☕ **DESCANSO 1** | **Pausa activa** | **15 min** |
| 🔵 Bloque 5 | Simulación de boleta de calificaciones | 45 min |
| ☕ **DESCANSO 2** | **Pausa activa** | **15 min** |
| 🟣 Bloque 6 | Validación de etiquetas anidadas | 45 min |
| 🟣 Bloque 7 | Reto final y cierre | 30 min |

---

# 🟢 BLOQUE 1 — Introducción a las Tablas HTML
### ⏱️ Tiempo estimado: 30 minutos

## ¿Qué es una tabla y para qué sirve?

Imagina que tienes que organizar los resultados de un torneo de videojuegos: jugadores, puntajes y posiciones. ¿Cómo lo harías en papel? Probablemente dibujarías filas y columnas. En HTML, las **tablas** hacen exactamente eso: organizan información en filas y columnas de forma visual y ordenada.

Las tablas en HTML se usan para mostrar:
- Horarios y calendarios
- Resultados deportivos
- Notas académicas (¡como una boleta!)
- Comparativas de productos
- Cualquier dato que tenga estructura de cuadrícula

> ⚠️ **Nota importante:** Las tablas son para **datos tabulares**, no para hacer el diseño de una página web. ¡Ese es el trabajo del CSS!

---

## La etiqueta `<table>`

Todo comienza con la etiqueta `<table>`. Esta es el contenedor principal que le dice al navegador: *"Aquí va a haber una tabla"*.

```html
<table>
  <!-- Aquí van las filas y celdas -->
</table>
```

Por sí sola, `<table>` no muestra nada visible. Necesita sus etiquetas internas para cobrar vida.

---

## La etiqueta `<tr>` — Table Row (Fila)

`<tr>` significa **Table Row** (fila de tabla). Cada `<tr>` representa una fila horizontal dentro de la tabla.

```html
<table>
  <tr><!-- Esta es la fila 1 --></tr>
  <tr><!-- Esta es la fila 2 --></tr>
  <tr><!-- Esta es la fila 3 --></tr>
</table>
```

Piensa en `<tr>` como cada renglón de un cuaderno cuadriculado.

---

## La etiqueta `<td>` — Table Data (Celda de datos)

`<td>` significa **Table Data** (celda de datos). Cada `<td>` es una celda individual dentro de una fila. Es donde realmente va el contenido.

```html
<table>
  <tr>
    <td>Celda 1</td>
    <td>Celda 2</td>
    <td>Celda 3</td>
  </tr>
  <tr>
    <td>Celda 4</td>
    <td>Celda 5</td>
    <td>Celda 6</td>
  </tr>
</table>
```

**Resultado visual:**

```
+----------+----------+----------+
| Celda 1  | Celda 2  | Celda 3  |
+----------+----------+----------+
| Celda 4  | Celda 5  | Celda 6  |
+----------+----------+----------+
```

---

## La etiqueta `<th>` — Table Header (Celda de encabezado)

`<th>` significa **Table Header** (celda de encabezado). Funciona igual que `<td>`, pero el contenido aparece en **negrita** y centrado automáticamente. Se usa para los títulos de las columnas.

```html
<table>
  <tr>
    <th>Jugador</th>
    <th>Puntaje</th>
    <th>Nivel</th>
  </tr>
  <tr>
    <td>Carlos</td>
    <td>9800</td>
    <td>Experto</td>
  </tr>
  <tr>
    <td>Sofía</td>
    <td>11200</td>
    <td>Maestro</td>
  </tr>
</table>
```

---

## 🧪 Ejercicio 1 — Tu primera tabla (10 min)

**Instrucciones:** Crea una tabla con la siguiente información sobre tus 3 series o películas favoritas:

| Columnas requeridas |
|---------------------|
| Nombre de la serie/película |
| Género |
| Calificación del 1 al 10 |

**Plantilla de inicio:**

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Mis favoritos</title>
</head>
<body>

  <h1>Mis series y películas favoritas</h1>

  <table border="1">
    <tr>
      <th>Nombre</th>
      <th>Género</th>
      <th>Calificación</th>
    </tr>
    <!-- Agrega tus 3 filas aquí -->

  </table>

</body>
</html>
```

> 💡 **Tip:** El atributo `border="1"` en `<table>` le agrega bordes visibles a la tabla. ¡Sin él, las celdas no tienen borde y es difícil verlas!

---

# 🟢 BLOQUE 2 — Estructura semántica: `<thead>`, `<tbody>` y `<tfoot>`
### ⏱️ Tiempo estimado: 30 minutos

## ¿Por qué organizar la tabla en secciones?

Así como un libro tiene portada, contenido e índice, una tabla HTML bien construida tiene **tres secciones claras**. Esto no es solo por estética: ayuda a los navegadores, lectores de pantalla y herramientas de accesibilidad a entender mejor la información.

Las tres secciones son:

| Etiqueta | Nombre | ¿Dónde va? |
|----------|--------|------------|
| `<thead>` | Table Head | Encabezado — los títulos de las columnas |
| `<tbody>` | Table Body | Cuerpo — los datos principales |
| `<tfoot>` | Table Foot | Pie — totales, resúmenes o notas finales |

---

## La etiqueta `<thead>`

`<thead>` envuelve las filas que forman el **encabezado** de la tabla. Normalmente contiene una fila con etiquetas `<th>`.

```html
<table border="1">
  <thead>
    <tr>
      <th>Materia</th>
      <th>Nota 1</th>
      <th>Nota 2</th>
      <th>Promedio</th>
    </tr>
  </thead>
</table>
```

---

## La etiqueta `<tbody>`

`<tbody>` envuelve todas las filas con los **datos reales** de la tabla. Puede contener tantas filas `<tr>` como necesites.

```html
<table border="1">
  <thead>
    <tr>
      <th>Materia</th>
      <th>Nota 1</th>
      <th>Nota 2</th>
      <th>Promedio</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Matemáticas</td>
      <td>4.2</td>
      <td>3.8</td>
      <td>4.0</td>
    </tr>
    <tr>
      <td>Lengua Castellana</td>
      <td>4.5</td>
      <td>4.7</td>
      <td>4.6</td>
    </tr>
    <tr>
      <td>Ciencias Naturales</td>
      <td>3.9</td>
      <td>4.1</td>
      <td>4.0</td>
    </tr>
  </tbody>
</table>
```

---

## La etiqueta `<tfoot>`

`<tfoot>` envuelve la fila o filas del **pie de la tabla**. Se usa para mostrar totales, promedios generales, o cualquier dato de resumen.

> 🤓 **Dato curioso:** Aunque escribas `<tfoot>` al final del HTML, los navegadores modernos lo procesan correctamente. Sin embargo, semánticamente se recomienda colocarlo **después de `<thead>`** y **antes de `<tbody>`** en algunos proyectos. En esta guía lo pondremos al final por claridad.

```html
<table border="1">
  <thead>
    <tr>
      <th>Materia</th>
      <th>Nota 1</th>
      <th>Nota 2</th>
      <th>Promedio</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Matemáticas</td>
      <td>4.2</td>
      <td>3.8</td>
      <td>4.0</td>
    </tr>
    <tr>
      <td>Lengua Castellana</td>
      <td>4.5</td>
      <td>4.7</td>
      <td>4.6</td>
    </tr>
    <tr>
      <td>Ciencias Naturales</td>
      <td>3.9</td>
      <td>4.1</td>
      <td>4.0</td>
    </tr>
  </tbody>
  <tfoot>
    <tr>
      <td><strong>Promedio General</strong></td>
      <td></td>
      <td></td>
      <td><strong>4.2</strong></td>
    </tr>
  </tfoot>
</table>
```

---

## Tabla completa con las tres secciones — Visualización

```
+--------------------+--------+--------+----------+
|      Materia       | Nota 1 | Nota 2 | Promedio |   ← thead
+--------------------+--------+--------+----------+
| Matemáticas        |  4.2   |  3.8   |   4.0    |   ← tbody
| Lengua Castellana  |  4.5   |  4.7   |   4.6    |
| Ciencias Naturales |  3.9   |  4.1   |   4.0    |
+--------------------+--------+--------+----------+
| Promedio General   |        |        |   4.2    |   ← tfoot
+--------------------+--------+--------+----------+
```

---

## 🧪 Ejercicio 2 — Tabla estructurada (10 min)

**Instrucciones:** Toma la tabla del Ejercicio 1 y agrégale `<thead>`, `<tbody>` y `<tfoot>`. En el `<tfoot>` escribe: `"Total de favoritos: 3"`.

---

# 🟢 BLOQUE 3 — Atributos útiles para las tablas
### ⏱️ Tiempo estimado: 30 minutos

## Atributos de `<table>`

| Atributo | ¿Qué hace? | Ejemplo |
|----------|-----------|---------|
| `border` | Agrega bordes visibles | `border="1"` |
| `width` | Define el ancho de la tabla | `width="500"` o `width="80%"` |
| `cellpadding` | Espacio interno en cada celda | `cellpadding="10"` |
| `cellspacing` | Espacio entre celdas | `cellspacing="5"` |
| `align` | Alineación horizontal de la tabla | `align="center"` |
| `bgcolor` | Color de fondo de la tabla | `bgcolor="#f0f0f0"` |
| `summary` | Descripción para accesibilidad | `summary="Tabla de notas"` |

> ⚠️ **Importante:** Muchos de estos atributos son **obsoletos en HTML5**. Hoy en día se usa CSS para el estilo. Pero como estás aprendiendo, ¡es útil conocerlos!

---

## Atributos de `<td>` y `<th>`

### `colspan` — Unir columnas

`colspan` le dice a una celda que ocupe el espacio de **varias columnas**.

```html
<table border="1">
  <tr>
    <th colspan="3">Resultados del Torneo</th>
  </tr>
  <tr>
    <th>Jugador</th>
    <th>Puntaje</th>
    <th>Posición</th>
  </tr>
  <tr>
    <td>Ana</td>
    <td>8500</td>
    <td>2°</td>
  </tr>
</table>
```

Resultado:
```
+----------------------------------+
|      Resultados del Torneo       |  ← ocupa 3 columnas
+----------+-----------+-----------+
| Jugador  | Puntaje   | Posición  |
+----------+-----------+-----------+
| Ana      | 8500      | 2°        |
+----------+-----------+-----------+
```

---

### `rowspan` — Unir filas

`rowspan` hace que una celda ocupe el espacio de **varias filas** hacia abajo.

```html
<table border="1">
  <tr>
    <th>Categoría</th>
    <th>Materia</th>
    <th>Nota</th>
  </tr>
  <tr>
    <td rowspan="2">Ciencias</td>
    <td>Biología</td>
    <td>4.3</td>
  </tr>
  <tr>
    <!-- La celda de Categoría ya ocupa este espacio -->
    <td>Química</td>
    <td>3.9</td>
  </tr>
</table>
```

Resultado:
```
+-----------+----------+------+
| Categoría | Materia  | Nota |
+-----------+----------+------+
|           | Biología | 4.3  |
| Ciencias  +----------+------+
|           | Química  | 3.9  |
+-----------+----------+------+
```

---

### `align` y `valign` en celdas

| Atributo | Valores posibles | Efecto |
|----------|-----------------|--------|
| `align` | `left`, `center`, `right` | Alineación horizontal del texto |
| `valign` | `top`, `middle`, `bottom` | Alineación vertical del texto |

```html
<td align="center" valign="middle">Texto centrado</td>
```

---

## 🧪 Ejercicio 3 — Usando `colspan` y `rowspan` (15 min)

**Instrucciones:** Crea la siguiente tabla usando `colspan` y `rowspan`:

```
+---------------------------+---------+
| Horario Semanal           | Período |
+----------+----------------+---------+
|          | Matemáticas    |   1°    |
| Lunes    +----------------+---------+
|          | Español        |   2°    |
+----------+----------------+---------+
|          | Ciencias       |   1°    |
| Martes   +----------------+---------+
|          | Inglés         |   2°    |
+----------+----------------+---------+
```

**Pista:** El día (`Lunes`, `Martes`) necesita `rowspan="2"`. El título principal necesita `colspan="3"`.

---

# 🟢 BLOQUE 4 — Taller práctico Parte 1
### ⏱️ Tiempo estimado: 30 minutos

## Taller: Tabla de Campeonato Escolar

Vas a construir desde cero una tabla completa para mostrar los resultados de un campeonato de fútbol escolar entre 5 equipos. Deberá incluir:

- Estructura completa con `<thead>`, `<tbody>` y `<tfoot>`
- Al menos un uso de `colspan`
- Los datos de cada equipo
- El campeón destacado en el pie de la tabla

### Datos del campeonato

| Equipo | PJ | PG | PP | PE | GF | GC | Puntos |
|--------|----|----|----|----|----|----|--------|
| Los Dragones | 4 | 3 | 0 | 1 | 9 | 3 | 10 |
| Águilas FC | 4 | 2 | 1 | 1 | 7 | 5 | 7 |
| Tigres United | 4 | 2 | 2 | 0 | 6 | 7 | 6 |
| Leones SC | 4 | 1 | 2 | 1 | 4 | 6 | 4 |
| Panteras CF | 4 | 0 | 3 | 1 | 2 | 7 | 1 |

> PJ = Partidos Jugados | PG = Ganados | PP = Perdidos | PE = Empatados | GF = Goles a Favor | GC = Goles en Contra

### Código base (complétalo):

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Campeonato Escolar</title>
</head>
<body>

  <h1>🏆 Campeonato Escolar de Fútbol</h1>

  <table border="1" cellpadding="8" cellspacing="0" width="700">

    <thead>
      <tr>
        <!-- Título principal que ocupe todas las columnas -->
        <th colspan="___">Tabla de Posiciones — 2024</th>
      </tr>
      <tr>
        <th>Equipo</th>
        <!-- Agrega el resto de encabezados -->
      </tr>
    </thead>

    <tbody>
      <!-- Agrega las 5 filas con los datos -->
    </tbody>

    <tfoot>
      <tr>
        <!-- En el tfoot indica cuál equipo es el campeón -->
        <td colspan="___">🥇 Campeón: <strong>Los Dragones</strong></td>
      </tr>
    </tfoot>

  </table>

</body>
</html>
```

---

## ✅ Solución de referencia (¡intenta hacerlo solo primero!)

<details>
<summary>👆 Haz clic aquí para ver la solución</summary>

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Campeonato Escolar</title>
</head>
<body>

  <h1>🏆 Campeonato Escolar de Fútbol</h1>

  <table border="1" cellpadding="8" cellspacing="0" width="700">
    <thead>
      <tr>
        <th colspan="8">Tabla de Posiciones — 2024</th>
      </tr>
      <tr>
        <th>Equipo</th>
        <th>PJ</th>
        <th>PG</th>
        <th>PP</th>
        <th>PE</th>
        <th>GF</th>
        <th>GC</th>
        <th>Puntos</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Los Dragones</td>
        <td>4</td><td>3</td><td>0</td><td>1</td>
        <td>9</td><td>3</td><td>10</td>
      </tr>
      <tr>
        <td>Águilas FC</td>
        <td>4</td><td>2</td><td>1</td><td>1</td>
        <td>7</td><td>5</td><td>7</td>
      </tr>
      <tr>
        <td>Tigres United</td>
        <td>4</td><td>2</td><td>2</td><td>0</td>
        <td>6</td><td>7</td><td>6</td>
      </tr>
      <tr>
        <td>Leones SC</td>
        <td>4</td><td>1</td><td>2</td><td>1</td>
        <td>4</td><td>6</td><td>4</td>
      </tr>
      <tr>
        <td>Panteras CF</td>
        <td>4</td><td>0</td><td>3</td><td>1</td>
        <td>2</td><td>7</td><td>1</td>
      </tr>
    </tbody>
    <tfoot>
      <tr>
        <td colspan="8">🥇 Campeón: <strong>Los Dragones</strong> con 10 puntos</td>
      </tr>
    </tfoot>
  </table>

</body>
</html>
```

</details>

---

---

# ☕ DESCANSO 1 — 15 minutos
> ### 🎮 ¡Descansa la vista, estira el cuerpo y toma agua!
> **Actividad sugerida:** Cierra el computador y cuenta a alguien qué aprendiste hasta ahora usando solo tus palabras.

---

---

# 🔵 BLOQUE 5 — Simulación de Boleta de Calificaciones
### ⏱️ Tiempo estimado: 45 minutos

## ¿Qué vamos a construir?

Una **boleta de calificaciones** es el ejemplo perfecto de una tabla HTML real. Tiene encabezados claros, datos estructurados y un resumen al final. ¡Exactamente lo que hemos aprendido!

Vamos a construir una boleta completa que incluya:
- Información del estudiante (con `colspan`)
- Notas por período y materia (con `rowspan`)
- Promedio general en el `<tfoot>`
- Uso correcto de `<thead>`, `<tbody>` y `<tfoot>`

---

## Análisis de la estructura

Antes de escribir código, siempre es buena idea **planear la tabla en papel**:

```
+-------------------------------------------------------+
|            INSTITUCIÓN EDUCATIVA DEMO                 |  ← colspan="7"
+-------------------------------------------------------+
| Estudiante: Juan Pérez     | Grado: 10° | Año: 2024   |  ← colspan mixtos
+--------------------+-------+-------+-------+----------+
|                    |  P1   |  P2   |  P3   |  P4      |  ← thead de notas
|      Materia       +-------+-------+-------+----------+
|                    | Nota  | Nota  | Nota  | Nota     |
+--------------------+-------+-------+-------+----------+
| Matemáticas        |  4.2  |  3.8  |  4.5  |  4.1     |  ← tbody
| Lengua Castellana  |  4.5  |  4.7  |  4.3  |  4.6     |
| Ciencias Naturales |  3.9  |  4.1  |  3.7  |  4.0     |
| Inglés             |  4.0  |  3.5  |  4.2  |  4.4     |
| Educación Física   |  4.8  |  4.9  |  5.0  |  4.7     |
| Informática        |  4.3  |  4.6  |  4.8  |  5.0     |
+--------------------+-------+-------+-------+----------+
| Promedio General   |                        4.35       |  ← tfoot
+--------------------+-----------------------------------+
```

---

## Código completo de la boleta

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Boleta de Calificaciones</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      padding: 20px;
      background-color: #f5f5f5;
    }

    table {
      border-collapse: collapse;
      width: 700px;
      margin: 0 auto;
      background-color: white;
      box-shadow: 0 2px 8px rgba(0,0,0,0.15);
    }

    th, td {
      border: 1px solid #333;
      padding: 10px 14px;
      text-align: center;
    }

    /* Encabezado principal del colegio */
    .encabezado-colegio {
      background-color: #003366;
      color: white;
      font-size: 16px;
      font-weight: bold;
      letter-spacing: 1px;
    }

    /* Información del estudiante */
    .info-estudiante {
      background-color: #e8f0fe;
      text-align: left;
      font-size: 14px;
    }

    /* Encabezados de períodos */
    thead tr:last-child th {
      background-color: #0055aa;
      color: white;
    }

    /* Primera fila del thead (materia + períodos) */
    thead tr:first-child th {
      background-color: #0055aa;
      color: white;
    }

    /* Filas del cuerpo — alternadas */
    tbody tr:nth-child(even) {
      background-color: #f0f7ff;
    }

    tbody tr:hover {
      background-color: #d0e8ff;
    }

    /* Columna de materias */
    tbody td:first-child {
      text-align: left;
      font-weight: bold;
    }

    /* Notas aprobadas */
    .aprobada {
      color: #1a7a1a;
      font-weight: bold;
    }

    /* Notas reprobadas */
    .reprobada {
      color: #cc0000;
      font-weight: bold;
    }

    /* Pie de tabla */
    tfoot td {
      background-color: #003366;
      color: white;
      font-weight: bold;
      font-size: 15px;
    }
  </style>
</head>
<body>

  <table>

    <!-- ===================== THEAD ===================== -->
    <thead>

      <!-- Fila 1: Nombre del colegio -->
      <tr>
        <th class="encabezado-colegio" colspan="6">
          🏫 INSTITUCIÓN EDUCATIVA DEMO
        </th>
      </tr>

      <!-- Fila 2: Datos del estudiante -->
      <tr>
        <td class="info-estudiante" colspan="2">
          <strong>Estudiante:</strong> Juan Camilo Pérez Rodríguez
        </td>
        <td class="info-estudiante">
          <strong>Grado:</strong> 10°A
        </td>
        <td class="info-estudiante">
          <strong>Año:</strong> 2024
        </td>
        <td class="info-estudiante" colspan="2">
          <strong>Docente Director:</strong> Prof. García
        </td>
      </tr>

      <!-- Fila 3: Encabezados de columnas -->
      <tr>
        <th>Asignatura</th>
        <th>Período 1</th>
        <th>Período 2</th>
        <th>Período 3</th>
        <th>Período 4</th>
        <th>Promedio</th>
      </tr>

    </thead>

    <!-- ===================== TBODY ===================== -->
    <tbody>

      <tr>
        <td>Matemáticas</td>
        <td class="aprobada">4.2</td>
        <td class="reprobada">2.8</td>
        <td class="aprobada">4.5</td>
        <td class="aprobada">4.1</td>
        <td class="aprobada">3.9</td>
      </tr>

      <tr>
        <td>Lengua Castellana</td>
        <td class="aprobada">4.5</td>
        <td class="aprobada">4.7</td>
        <td class="aprobada">4.3</td>
        <td class="aprobada">4.6</td>
        <td class="aprobada">4.5</td>
      </tr>

      <tr>
        <td>Ciencias Naturales</td>
        <td class="aprobada">3.9</td>
        <td class="aprobada">4.1</td>
        <td class="reprobada">2.7</td>
        <td class="aprobada">4.0</td>
        <td class="aprobada">3.7</td>
      </tr>

      <tr>
        <td>Inglés</td>
        <td class="aprobada">4.0</td>
        <td class="aprobada">3.5</td>
        <td class="aprobada">4.2</td>
        <td class="aprobada">4.4</td>
        <td class="aprobada">4.0</td>
      </tr>

      <tr>
        <td>Educación Física</td>
        <td class="aprobada">4.8</td>
        <td class="aprobada">4.9</td>
        <td class="aprobada">5.0</td>
        <td class="aprobada">4.7</td>
        <td class="aprobada">4.9</td>
      </tr>

      <tr>
        <td>Informática</td>
        <td class="aprobada">4.3</td>
        <td class="aprobada">4.6</td>
        <td class="aprobada">4.8</td>
        <td class="aprobada">5.0</td>
        <td class="aprobada">4.7</td>
      </tr>

      <tr>
        <td>Historia y Geografía</td>
        <td class="reprobada">2.5</td>
        <td class="aprobada">3.8</td>
        <td class="aprobada">4.0</td>
        <td class="aprobada">3.9</td>
        <td class="aprobada">3.6</td>
      </tr>

    </tbody>

    <!-- ===================== TFOOT ===================== -->
    <tfoot>
      <tr>
        <td colspan="5">📊 Promedio General del Año</td>
        <td>4.18</td>
      </tr>
    </tfoot>

  </table>

</body>
</html>
```

---

## 🧪 Taller de Boleta — Tu turno (20 min)

Crea tu propia boleta de calificaciones con los siguientes requisitos:

### Requisitos obligatorios ✅

1. **Encabezado del colegio** usando `colspan` para que ocupe todas las columnas
2. **Fila con tu nombre, grado y año** — usa `colspan` en al menos una celda
3. **Mínimo 5 materias** con notas en 4 períodos
4. **Columna de promedio** por materia (puedes calcularlo a mano)
5. **`<tfoot>`** con el promedio general
6. Usa `<thead>`, `<tbody>` y `<tfoot>` correctamente

### Requisitos de desafío 🌟

- Agrega una columna `Estado` que diga `✅ Aprobado` o `❌ Reprobado` según si el promedio es mayor o menor a 3.0
- Usa `bgcolor` o estilos básicos para darle color al encabezado

---

# ☕ DESCANSO 2 — 15 minutos
> ### 🧠 ¡Bien hecho! Ya llevas más de dos horas aprendiendo. Mereces este descanso.
> **Actividad sugerida:** Muéstrale tu boleta a un compañero y explícale qué hace cada etiqueta.

---

---

# 🟣 BLOQUE 6 — Validación de Etiquetas Anidadas
### ⏱️ Tiempo estimado: 45 minutos

## ¿Qué es el anidamiento?

En HTML, **anidar** significa poner una etiqueta dentro de otra. Las tablas tienen reglas muy específicas sobre qué puede ir dentro de qué. Si las rompes, el navegador puede mostrar resultados inesperados o la tabla puede verse completamente mal.

---

## Reglas de anidamiento en tablas HTML

### ✅ Estructura correcta

```
<table>
  └── <thead>        (opcional pero recomendado)
       └── <tr>
            └── <th> o <td>
  └── <tbody>        (opcional pero recomendado)
       └── <tr>
            └── <td>
  └── <tfoot>        (opcional pero recomendado)
       └── <tr>
            └── <td>
```

### 🚫 Errores comunes de anidamiento

---

#### ❌ Error 1: `<td>` directamente dentro de `<table>`

```html
<!-- INCORRECTO ❌ -->
<table>
  <td>Esto está mal</td>
</table>

<!-- CORRECTO ✅ -->
<table>
  <tr>
    <td>Esto está bien</td>
  </tr>
</table>
```

**¿Por qué falla?** Las celdas `<td>` SIEMPRE deben estar dentro de una fila `<tr>`. Sin `<tr>`, la tabla no sabe dónde poner la celda.

---

#### ❌ Error 2: `<tr>` dentro de `<tr>`

```html
<!-- INCORRECTO ❌ -->
<table>
  <tr>
    <td>Celda 1</td>
    <tr>                    <!-- ERROR: tr dentro de tr -->
      <td>Celda 2</td>
    </tr>
  </tr>
</table>

<!-- CORRECTO ✅ -->
<table>
  <tr>
    <td>Celda 1</td>
  </tr>
  <tr>
    <td>Celda 2</td>
  </tr>
</table>
```

---

#### ❌ Error 3: `<table>` dentro de `<tr>` (sin `<td>`)

```html
<!-- INCORRECTO ❌ -->
<table>
  <tr>
    <table>...</table>      <!-- ERROR: tabla directamente en tr -->
  </tr>
</table>

<!-- CORRECTO ✅ -->
<table>
  <tr>
    <td>
      <table>...</table>   <!-- Tabla anidada dentro de td ✅ -->
    </td>
  </tr>
</table>
```

---

#### ❌ Error 4: `<thead>` y `<tbody>` mezclados incorrectamente

```html
<!-- INCORRECTO ❌ -->
<table>
  <tr>
    <th>Encabezado</th>
  </tr>
  <thead>                   <!-- thead DESPUÉS de una fila suelta -->
    <tr><th>Otro</th></tr>
  </thead>
</table>

<!-- CORRECTO ✅ -->
<table>
  <thead>
    <tr>
      <th>Encabezado</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Dato</td>
    </tr>
  </tbody>
</table>
```

---

#### ❌ Error 5: Etiquetas no cerradas correctamente

```html
<!-- INCORRECTO ❌ -->
<table>
  <tr>
    <td>Celda 1
    <td>Celda 2
  </tr>
</table>

<!-- CORRECTO ✅ -->
<table>
  <tr>
    <td>Celda 1</td>
    <td>Celda 2</td>
  </tr>
</table>
```

> 💡 **Nota:** Algunos navegadores son tan tolerantes que pueden mostrar la versión incorrecta sin errores visibles, pero esto es una **mala práctica** que puede causar problemas en diferentes dispositivos o navegadores.

---

## Tablas anidadas (tablas dentro de tablas)

Las tablas pueden contener otras tablas **dentro de una `<td>`**. Esto a veces es necesario para layouts complejos.

```html
<table border="1">
  <tr>
    <th>Información General</th>
    <th>Detalle de Notas</th>
  </tr>
  <tr>
    <td>
      <strong>Estudiante:</strong> María López<br>
      <strong>Grado:</strong> 11°
    </td>
    <td>
      <!-- Tabla anidada dentro de una celda -->
      <table border="1">
        <tr>
          <th>Materia</th>
          <th>Nota</th>
        </tr>
        <tr>
          <td>Matemáticas</td>
          <td>4.5</td>
        </tr>
        <tr>
          <td>Inglés</td>
          <td>4.0</td>
        </tr>
      </table>
    </td>
  </tr>
</table>
```

> ⚠️ **Precaución:** Las tablas muy anidadas pueden volverse difíciles de leer y mantener. Úsalas solo cuando sea realmente necesario.

---

## 🔍 Taller de Validación — Encuentra los errores (20 min)

Los siguientes fragmentos de código tienen **errores de anidamiento**. Encuéntralos y corrígelos:

### Código 1 — Encuentra los 2 errores

```html
<table border="1">
  <thead>
    <td>Nombre</td>
    <td>Edad</td>
  </thead>
  <tbody>
    <tr>
      <td>Ana</td>
      <td>15</td>
    </tr>
  </tbody>
</table>
```

<details>
<summary>Ver respuesta</summary>

**Error:** Dentro de `<thead>` hay `<td>` pero falta el `<tr>` que las contenga. Además, los encabezados deberían ser `<th>`, no `<td>`.

```html
<!-- SOLUCIÓN -->
<table border="1">
  <thead>
    <tr>                   <!-- ✅ Agregamos el tr -->
      <th>Nombre</th>      <!-- ✅ Usamos th para encabezados -->
      <th>Edad</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Ana</td>
      <td>15</td>
    </tr>
  </tbody>
</table>
```
</details>

---

### Código 2 — Encuentra los 3 errores

```html
<table border="1">
  <tr>
    <th colspan="2">Mi Horario</th>
  </tr>
  <tbody>
    <tr>
      <td>Lunes</td>
      <td>Matemáticas</td>
    <tr>
      <td>Martes</td>
      <td>Inglés</td>
    </tr>
  </tbody>
  <thead>
    <tr>
      <th>Día</th>
      <th>Materia</th>
    </tr>
  </thead>
</table>
```

<details>
<summary>Ver respuesta</summary>

**Error 1:** La primera fila `<tr>` está flotando fuera de `<thead>` o `<tbody>`.  
**Error 2:** La segunda fila `<tr>` no está cerrada (`</tr>` faltante).  
**Error 3:** El `<thead>` está al final cuando debería estar al principio.

```html
<!-- SOLUCIÓN -->
<table border="1">
  <thead>                              <!-- ✅ thead al inicio -->
    <tr>
      <th colspan="2">Mi Horario</th>
    </tr>
    <tr>
      <th>Día</th>
      <th>Materia</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Lunes</td>
      <td>Matemáticas</td>
    </tr>                             <!-- ✅ tr cerrado correctamente -->
    <tr>
      <td>Martes</td>
      <td>Inglés</td>
    </tr>
  </tbody>
</table>
```
</details>

---

### Código 3 — El más difícil (4 errores)

```html
<table>
  <thead>
    <tr>
      <th rowspan="2">Categoría</th>
      <th>SubCat A</th>
    </tr>
    <th>SubCat B</th>    
  </thead>
  <tbody>
    <tr>
      <td rowspan="2">Frutas</td>
      <td>Manzana</td>
    </tr>
    <tr>
      <td>Pera</td>
    </tr>
    <td>Verduras</td>    
    <tr>
      <td>Zanahoria</td>
    </tr>
  </tbody>
</table>
```

<details>
<summary>Ver respuesta</summary>

**Error 1:** El segundo `<th>SubCat B</th>` está fuera de un `<tr>`.  
**Error 2:** El `<td>Verduras</td>` está directamente en `<tbody>` sin `<tr>`.  
**Error 3:** La fila de "Verduras" debería tener `rowspan="2"` para cubrir la fila de "Zanahoria".  
**Error 4:** La fila de "Zanahoria" tiene solo 1 celda pero necesita alinearse con la estructura.

```html
<!-- SOLUCIÓN -->
<table border="1">
  <thead>
    <tr>
      <th rowspan="2">Categoría</th>
      <th>SubCat A</th>
    </tr>
    <tr>                               <!-- ✅ th dentro de tr -->
      <th>SubCat B</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td rowspan="2">Frutas</td>
      <td>Manzana</td>
    </tr>
    <tr>
      <td>Pera</td>
    </tr>
    <tr>                               <!-- ✅ td dentro de tr -->
      <td rowspan="2">Verduras</td>    <!-- ✅ rowspan para cubrir siguiente fila -->
      <td>Zanahoria</td>
    </tr>
    <tr>
      <td>Brócoli</td>                 <!-- ✅ fila adicional para completar rowspan -->
    </tr>
  </tbody>
</table>
```
</details>

---

## Lista de verificación de tablas HTML ✅

Antes de entregar cualquier tabla, revisa esta lista:

```
ESTRUCTURA GENERAL
  ☐ ¿La tabla comienza con <table> y termina con </table>?
  ☐ ¿Usé <thead>, <tbody> y <tfoot> correctamente?
  ☐ ¿Cada sección tiene al menos una fila <tr>?

FILAS Y CELDAS
  ☐ ¿Todas las <td> y <th> están dentro de un <tr>?
  ☐ ¿Todos los <tr> están dentro de <table>, <thead>, <tbody> o <tfoot>?
  ☐ ¿Cerré correctamente todas las etiquetas?

ATRIBUTOS ESPECIALES
  ☐ Si usé colspan, ¿el número coincide con las columnas que debería ocupar?
  ☐ Si usé rowspan, ¿eliminé las celdas que ese espacio ocupa en las filas siguientes?
  ☐ ¿Mis colspan y rowspan no crean "huecos" en la tabla?

SEMÁNTICA
  ☐ ¿Usé <th> para los encabezados y <td> para los datos?
  ☐ ¿La información está organizada de forma lógica?
  ☐ ¿El <tfoot> tiene información de resumen?
```

---

# 🟣 BLOQUE 7 — Reto Final y Cierre
### ⏱️ Tiempo estimado: 30 minutos

## 🏆 Reto Final — Sistema de Torneos con Tabla Compleja

Construye una tabla de **clasificación de un torneo de videojuegos** que cumpla con todos estos requisitos:

### Especificaciones técnicas

| Requisito | Descripción |
|-----------|-------------|
| `colspan` | El título principal debe abarcar todas las columnas |
| `rowspan` | Agrupa los equipos por **región** (al menos 2 regiones con 2 equipos cada una) |
| `<thead>` | Con título y subencabezados de columnas |
| `<tbody>` | Con al menos 4 equipos (2 por región) |
| `<tfoot>` | Con el campeón y la cantidad total de participantes |
| CSS básico | Al menos 3 estilos diferentes aplicados |
| Semántica | Todo validado según la lista de verificación |

### Datos sugeridos

**Región Norte:** Equipo Alpha (980 pts), Equipo Beta (870 pts)  
**Región Sur:** Equipo Gamma (920 pts), Equipo Delta (750 pts)

### Columnas sugeridas

`Región | Equipo | J | G | P | Puntos | Estado`

---

## 📝 Repaso general — Mapa mental de etiquetas

```
TABLE
├── CAPTION ..................... Título de la tabla (encima o debajo)
├── THEAD ....................... Sección de encabezado
│   └── TR ...................... Fila de encabezado
│       ├── TH .................. Celda de encabezado (negrita, centrado)
│       └── TD .................. También puede usarse aquí
├── TBODY ....................... Sección principal de datos
│   └── TR ...................... Filas de datos
│       └── TD .................. Celda de datos
│           └── [colspan] ....... Extiende la celda horizontalmente
│           └── [rowspan] ....... Extiende la celda verticalmente
└── TFOOT ....................... Sección de pie/resumen
    └── TR ...................... Fila de resumen
        └── TD .................. Celda de resumen
```

---

## 🎯 Resumen de lo aprendido hoy

| Etiqueta | Función | Uso principal |
|----------|---------|---------------|
| `<table>` | Contenedor de la tabla | Siempre necesaria |
| `<tr>` | Fila | Dentro de table, thead, tbody o tfoot |
| `<td>` | Celda de datos | Dentro de tr, en el cuerpo |
| `<th>` | Celda de encabezado | Dentro de tr, en thead o primera columna |
| `<thead>` | Sección de encabezado | Agrupa filas del encabezado |
| `<tbody>` | Sección de datos | Agrupa filas de datos principales |
| `<tfoot>` | Sección de pie | Agrupa filas de resumen/totales |
| `colspan` | Unir columnas | Atributo de td/th |
| `rowspan` | Unir filas | Atributo de td/th |

---

## 📚 Referencias y recursos para seguir aprendiendo

- **MDN Web Docs:** [developer.mozilla.org/es/docs/Web/HTML/Element/table](https://developer.mozilla.org/es/docs/Web/HTML/Element/table)
- **W3Schools HTML Tables:** [w3schools.com/html/html_tables.asp](https://www.w3schools.com/html/html_tables.asp)
- **Validador de HTML:** [validator.w3.org](https://validator.w3.org) — ¡pega tu código aquí para verificar errores!
- **CodePen:** [codepen.io](https://codepen.io) — Prueba tu código HTML en línea

---

## 🏅 Criterios de evaluación

| Criterio | Porcentaje |
|----------|-----------|
| Estructura correcta `<table>`, `<tr>`, `<td>` | 20% |
| Uso de `<thead>`, `<tbody>`, `<tfoot>` | 20% |
| Uso correcto de `colspan` y/o `rowspan` | 20% |
| Boleta de calificaciones funcional | 20% |
| Validación de etiquetas (sin errores) | 10% |
| Creatividad y presentación visual | 10% |
| **Total** | **100%** |

---

> 🎉 **¡Felicitaciones!** Hoy aprendiste a construir tablas HTML profesionales desde cero. Las tablas son una herramienta fundamental para organizar datos en la web. Con práctica constante, pronto podrás hacer tablas mucho más complejas combinando HTML con CSS avanzado y hasta JavaScript. ¡Sigue adelante! 💪

---

*Guía elaborada para Educación Media — Área de Tecnología e Informática*  
*Contenido alineado con estándares HTML5 — Versión 1.0*
