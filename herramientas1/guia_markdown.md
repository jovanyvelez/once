# Guía Rápida de Markdown para Entregas

Markdown es un lenguaje de marcado ligero que te permite dar formato a un texto de manera sencilla utilizando caracteres de puntuación. Es el estándar utilizado en plataformas como GitHub y es ideal para escribir documentación técnica o apuntes de programación.

Para tu resumen sobre HTML, CSS y JavaScript, necesitarás dominar los siguientes elementos:

## 1. Encabezados (Jerarquía del documento)
Para estructurar tu documento y separar los diferentes temas (como "1. ¿Cómo funciona Internet?", "2. Protocolo HTTP", etc.), utiliza el símbolo de numeral (`#`). Entre más símbolos agregues, más pequeño será el encabezado.

**Cómo lo escribes:**
```markdown
# Título Principal del Documento
## Tema Principal (Ej. HTML)
### Subtema (Ej. Etiquetas y Atributos)
```

## 2. Énfasis (Negritas y Cursivas)
Para resaltar palabras clave en tu resumen (como **TCP/IP**, **DOM** o **Bootstrap**), envuelve el texto con asteriscos.

**Cómo lo escribes:**
```markdown
El protocolo **HTTP** es fundamental.
El atributo *href* se usa en los enlaces.
```

## 3. Listas (Viñetas y Numeradas)
Las listas son esenciales para organizar ideas, como cuando enumeres las diferencias entre GET y POST, o los códigos de estado HTTP.

**Listas sin orden (Viñetas):** Utiliza un guion `-` o un asterisco `*` seguido de un espacio.
```markdown
* Código 200: OK
* Código 404: Not Found
```

**Listas ordenadas:** Utiliza números seguidos de un punto y un espacio.
```markdown
1. HTML da la estructura.
2. CSS aporta el diseño visual.
3. JavaScript agrega la interactividad.
```

## 4. Código y Etiquetas
Dado que este es un curso de desarrollo web, deberás mencionar etiquetas HTML o escribir pequeños ejemplos de código.

**Código en línea:** Para mencionar una etiqueta o comando dentro de un párrafo, usa acentos graves simples.

**Cómo lo escribes:**
```markdown
Para crear un párrafo usamos la etiqueta `<p>`.
```

**Bloques de código:** Para mostrar un fragmento de código de varias líneas, usa tres acentos graves antes y después del bloque. Puedes indicar el lenguaje de programación al inicio para resaltar la sintaxis.

**Cómo lo escribes:**
```html
<form action="/submit" method="POST">
    <input type="text" name="usuario">
    <button type="submit">Enviar</button>
</form>
```

## 5. Enlaces
Si deseas hacer referencia a una página externa o a una documentación, utiliza corchetes `[]` para el texto que será visible, seguidos inmediatamente por paréntesis `()` con la URL.

**Cómo lo escribes:**
```markdown
Puedes leer más sobre esto en la [Documentación de Mozilla](https://developer.mozilla.org/es/).
```

---
**Tip:** Presta mucha atención a los espacios y saltos de línea. En Markdown, para que un salto de línea se refleje en el documento final, generalmente debes dejar una línea en blanco entre párrafos.

### Actividad
Elabora un archivo Markdown utilizando los conceptos que aprendiste en esta guía. Incluye al menos un título, una lista, un bloque de código y un enlace. Este será entregado como parte de tu evaluación.