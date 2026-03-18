# 📋 Formularios HTML: Conectando con el Mundo

> **Nivel:** Principiante · **Duración:** 4 horas (2 descansos de 15 min) · **Audiencia:** Jóvenes 15–16 años  
> **Prerrequisitos:** Conocimientos básicos de HTML (etiquetas, estructura, atributos)

---

## 🗺️ Mapa de la Jornada

| Bloque | Tiempo | Contenido |
|--------|--------|-----------|
| 🟢 Bloque 1 | 0 – 120 min | Introducción · Etiquetas · Práctica guiada |
| ☕ Descanso 1 | 120 – 135 min | *¡Pausa merecida!* |
| 🔵 Bloque 2 | 135 – 195 min | Taller formulario de contacto · Diseño educativo |
| 🍃 Descanso 2 | 195 – 210 min | *Respira, toma agua* |
| 🟣 Bloque 3 | 210 – 240 min | Accesibilidad · Cierre y reto final |

---

# 🟢 BLOQUE 1 — La Base de Todo Formulario

## ¿Por qué existen los formularios?

Piénsalo: cuando creas una cuenta en Instagram, compras en Rappi, reservas una cancha de fútbol o llevas la hoja de matrícula al colegio… estás llenando un formulario. En la web, **los formularios son el principal medio para que los usuarios se comuniquen con un sitio**.

Sin formularios, la web sería solo de lectura. Con formularios, se convierte en una conversación.

> 💬 **Pregunta para arrancar:** ¿En cuántos formularios (digitales o físicos) has participado esta semana? Comenta con tu compañero durante 2 minutos.

---

## 1. La etiqueta `<form>` — El contenedor principal

La etiqueta `<form>` es la "caja" que agrupa todos los campos. Define hacia dónde van los datos y cómo se envían.

```html
<form action="/enviar-datos" method="post">
  <!-- Aquí van todos los campos del formulario -->
</form>
```

### Atributos clave de `<form>`

| Atributo | ¿Qué hace? | Valores comunes |
|----------|-----------|-----------------|
| `action` | URL a donde se envían los datos | `"/pagina.php"`, `"https://..."` |
| `method` | Método HTTP de envío | `get` / `post` |
| `novalidate` | Desactiva validación automática del navegador | (sin valor) |
| `autocomplete` | Activa o desactiva el autocompletado | `on` / `off` |

### `GET` vs `POST` — ¿Cuál usar?

```
GET  → Los datos viajan en la URL (visibles)
       Ejemplo: buscar.com/?q=formularios+html
       Úsalo para: búsquedas, filtros

POST → Los datos viajan ocultos en el cuerpo del mensaje
       Úsalo para: contraseñas, datos personales, pagos
```

> ⚠️ **Importante:** Nunca envíes contraseñas con `method="get"`. ¡Quedarían expuestas en la URL!

---

## 2. La etiqueta `<label>` — El nombre de cada campo

`<label>` le pone nombre a un campo. Parece simple, pero es una de las etiquetas más importantes para la **accesibilidad y la usabilidad**.

```html
<!-- Forma 1: usando el atributo "for" (recomendada) -->
<label for="nombre">Tu nombre completo:</label>
<input type="text" id="nombre" name="nombre">

<!-- Forma 2: envolviendo el input -->
<label>
  Tu nombre completo:
  <input type="text" name="nombre">
</label>
```

### ¿Por qué `<label>` es tan importante?

1. **Hace clic más fácil:** Al hacer clic en el label, el campo se activa.
2. **Lectores de pantalla:** Usuarios con discapacidad visual escuchan el label.
3. **Claridad:** Sin label, el usuario no sabe qué información pedirle.

> 🧪 **Prueba esto:** Crea un label y un input sin conectarlos con `for`/`id`. ¿El clic en el label activa el campo?

---

## 3. La etiqueta `<input>` — El corazón del formulario

`<input>` es la etiqueta más versátil del HTML. Cambia completamente dependiendo de su atributo `type`.

```html
<input type="text" name="usuario" placeholder="Escribe aquí..." required>
```

### Tipos de `<input>` más usados

```html
<!-- Texto libre -->
<input type="text"     name="nombre"    placeholder="Tu nombre">
<input type="email"    name="correo"    placeholder="correo@ejemplo.com">
<input type="password" name="clave"     placeholder="Contraseña segura">
<input type="number"   name="edad"      min="10" max="99">
<input type="tel"      name="telefono"  placeholder="300 123 4567">
<input type="url"      name="web"       placeholder="https://...">

<!-- Fechas -->
<input type="date"     name="nacimiento">
<input type="time"     name="hora_clase">
<input type="datetime-local" name="evento">

<!-- Selección -->
<input type="checkbox" name="acepto" value="si">  <!-- Múltiple selección -->
<input type="radio"    name="genero" value="M">   <!-- Una sola opción -->

<!-- Archivos y colores -->
<input type="file"     name="foto"      accept="image/*">
<input type="color"    name="favorito">
<input type="range"    name="volumen"   min="0" max="100" step="5">

<!-- Especiales -->
<input type="hidden"   name="token"     value="abc123">
<input type="search"   name="buscar"    placeholder="Buscar...">

<!-- Botones -->
<input type="submit"   value="Enviar formulario">
<input type="reset"    value="Borrar todo">
```

### Atributos útiles de `<input>`

| Atributo | Función |
|----------|---------|
| `name` | Nombre del dato (llega al servidor con este nombre) |
| `id` | Identificador único (para conectar con `label`) |
| `value` | Valor por defecto o valor enviado |
| `placeholder` | Texto de ayuda dentro del campo |
| `required` | Campo obligatorio |
| `disabled` | Campo desactivado |
| `readonly` | Campo de solo lectura |
| `maxlength` | Máximo de caracteres |
| `min` / `max` | Rango para números y fechas |
| `pattern` | Expresión regular para validar |
| `autocomplete` | Sugerencias del navegador |

---

## 4. `<select>` y `<option>` — Listas desplegables

Cuando hay opciones fijas (como departamentos, géneros, cursos), una lista desplegable es más clara que un campo de texto libre.

```html
<label for="departamento">¿De qué departamento eres?</label>
<select id="departamento" name="departamento">
  <option value="">-- Selecciona uno --</option>
  <option value="antioquia">Antioquia</option>
  <option value="cundinamarca">Cundinamarca</option>
  <option value="bolivar">Bolívar</option>
  <option value="valle">Valle del Cauca</option>
</select>
```

### Atributos importantes

```html
<!-- Opción preseleccionada -->
<option value="antioquia" selected>Antioquia</option>

<!-- Selección múltiple (ctrl + clic) -->
<select name="materias" multiple size="4">
  <option value="mat">Matemáticas</option>
  <option value="his">Historia</option>
  <option value="ing">Inglés</option>
  <option value="bio">Biología</option>
</select>

<!-- Agrupación de opciones con <optgroup> -->
<select name="curso">
  <optgroup label="Bachillerato">
    <option value="9">Grado 9°</option>
    <option value="10">Grado 10°</option>
    <option value="11">Grado 11°</option>
  </optgroup>
  <optgroup label="Primaria">
    <option value="5">Grado 5°</option>
  </optgroup>
</select>
```

---

## 5. Etiquetas complementarias

### `<textarea>` — Para textos largos

```html
<label for="mensaje">Tu mensaje:</label>
<textarea 
  id="mensaje" 
  name="mensaje" 
  rows="5" 
  cols="40" 
  placeholder="Escribe tu mensaje aquí..."
  maxlength="500">
</textarea>
```

### `<button>` — Botones más flexibles que `<input type="submit">`

```html
<!-- Envía el formulario (comportamiento por defecto) -->
<button type="submit">✉️ Enviar mensaje</button>

<!-- Limpia el formulario -->
<button type="reset">🗑️ Borrar todo</button>

<!-- Solo ejecuta JavaScript, no envía el formulario -->
<button type="button" onclick="validarManual()">✔️ Verificar</button>
```

### `<fieldset>` y `<legend>` — Agrupación visual y semántica

```html
<fieldset>
  <legend>Información personal</legend>
  
  <label for="fn">Nombre:</label>
  <input type="text" id="fn" name="nombre" required>

  <label for="fe">Email:</label>
  <input type="email" id="fe" name="email" required>
</fieldset>

<fieldset>
  <legend>¿Cómo nos conociste?</legend>

  <input type="radio" id="r1" name="medio" value="redes">
  <label for="r1">Redes sociales</label>

  <input type="radio" id="r2" name="medio" value="amigo">
  <label for="r2">Un amigo</label>

  <input type="radio" id="r3" name="medio" value="otro">
  <label for="r3">Otro</label>
</fieldset>
```

---

## 6. Práctica Guiada — "Mi primer formulario"

Construye el siguiente formulario paso a paso en tu editor:

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Mi Primer Formulario</title>
  <style>
    body {
      font-family: Arial, sans-serif;
      max-width: 500px;
      margin: 30px auto;
      padding: 0 20px;
    }
    label {
      display: block;
      margin-top: 15px;
      font-weight: bold;
    }
    input, select, textarea {
      width: 100%;
      padding: 8px;
      margin-top: 4px;
      border: 1px solid #ccc;
      border-radius: 4px;
      box-sizing: border-box;
    }
    button {
      margin-top: 20px;
      padding: 10px 25px;
      background: #007bff;
      color: white;
      border: none;
      border-radius: 4px;
      cursor: pointer;
    }
  </style>
</head>
<body>

  <h1>Registro de Estudiante</h1>

  <form action="#" method="post">

    <fieldset>
      <legend>Datos personales</legend>

      <label for="nombre">Nombre completo *</label>
      <input type="text" id="nombre" name="nombre" 
             placeholder="Ej: Ana García" required>

      <label for="email">Correo electrónico *</label>
      <input type="email" id="email" name="email" 
             placeholder="correo@ejemplo.com" required>

      <label for="edad">Edad</label>
      <input type="number" id="edad" name="edad" min="10" max="20">

    </fieldset>

    <fieldset>
      <legend>Información académica</legend>

      <label for="grado">Grado actual *</label>
      <select id="grado" name="grado" required>
        <option value="">-- Selecciona tu grado --</option>
        <option value="9">Noveno (9°)</option>
        <option value="10">Décimo (10°)</option>
        <option value="11">Once (11°)</option>
      </select>

      <label for="materia">Materia favorita</label>
      <select id="materia" name="materia">
        <option value="">-- Elige una --</option>
        <optgroup label="Ciencias">
          <option value="bio">Biología</option>
          <option value="qui">Química</option>
          <option value="fis">Física</option>
        </optgroup>
        <optgroup label="Humanidades">
          <option value="esp">Español</option>
          <option value="his">Historia</option>
          <option value="ing">Inglés</option>
        </optgroup>
        <optgroup label="Tecnología">
          <option value="tec">Tecnología e informática</option>
        </optgroup>
      </select>

    </fieldset>

    <label for="comentario">¿Qué esperas aprender hoy?</label>
    <textarea id="comentario" name="comentario" rows="4"
              placeholder="Escribe aquí tus expectativas..."></textarea>

    <button type="submit">📝 Registrarme</button>
    <button type="reset">🗑️ Borrar</button>

  </form>

</body>
</html>
```

### ✅ Lista de verificación — ¿Lo tienes todo?

- [ ] Cada campo tiene su `<label>` conectado con `for` e `id`
- [ ] El formulario tiene `method` y `action` definidos
- [ ] Los campos obligatorios tienen `required`
- [ ] Los `<select>` tienen una opción vacía al inicio
- [ ] Usaste al menos un `<fieldset>` con `<legend>`
- [ ] Probaste el formulario en el navegador

---

> ⏰ **Marca de tiempo: 120 minutos**

---

# ☕ DESCANSO 1 — 15 minutos

> Levántate, estira los brazos, toma agua. Cuando vuelvas, construiremos algo real.  
> **Reto opcional para el descanso:** ¿Puedes pensar en un formulario de tu colegio que debería existir en la web y no existe todavía?

---

# 🔵 BLOQUE 2 — Taller y Diseño con Propósito

## 🛠️ Taller: Formulario de Contacto Completo

Un formulario de contacto es uno de los más comunes en la web. Toda empresa, organización o portafolio personal lo necesita. Ahora construirás uno desde cero, con **estilo y funcionalidad real**.

### Objetivo del taller

Crear un formulario de contacto funcional y bien estructurado que incluya:

- Campos para nombre, email, asunto y mensaje
- Validación HTML5 nativa
- Selector de tipo de consulta
- Casilla de términos y condiciones
- Diseño limpio con CSS básico

### Paso 1 — Estructura HTML

```html
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Contáctanos</title>
  <link rel="stylesheet" href="contacto.css">
</head>
<body>

  <main class="contenedor">

    <header class="encabezado">
      <h1>💬 Contáctanos</h1>
      <p>Responderemos en menos de 24 horas.</p>
    </header>

    <form class="formulario-contacto" action="#" method="post" novalidate>

      <!-- Nombre y Email en una fila -->
      <div class="fila-doble">

        <div class="campo">
          <label for="contacto-nombre">
            Nombre completo <span class="obligatorio">*</span>
          </label>
          <input 
            type="text" 
            id="contacto-nombre" 
            name="nombre"
            placeholder="¿Cómo te llamas?"
            required
            autocomplete="name"
            minlength="2"
            maxlength="60">
          <span class="ayuda">Mínimo 2 caracteres</span>
        </div>

        <div class="campo">
          <label for="contacto-email">
            Correo electrónico <span class="obligatorio">*</span>
          </label>
          <input 
            type="email" 
            id="contacto-email" 
            name="email"
            placeholder="correo@ejemplo.com"
            required
            autocomplete="email">
        </div>

      </div>

      <!-- Tipo de consulta -->
      <div class="campo">
        <label for="tipo-consulta">
          Tipo de consulta <span class="obligatorio">*</span>
        </label>
        <select id="tipo-consulta" name="tipo_consulta" required>
          <option value="">-- Selecciona el motivo --</option>
          <optgroup label="Soporte">
            <option value="tecnico">Problema técnico</option>
            <option value="cuenta">Mi cuenta</option>
          </optgroup>
          <optgroup label="Información">
            <option value="precios">Precios y planes</option>
            <option value="servicios">Servicios disponibles</option>
          </optgroup>
          <optgroup label="Otros">
            <option value="sugerencia">Sugerencia o idea</option>
            <option value="otro">Otro motivo</option>
          </optgroup>
        </select>
      </div>

      <!-- Asunto -->
      <div class="campo">
        <label for="asunto">Asunto</label>
        <input 
          type="text" 
          id="asunto" 
          name="asunto"
          placeholder="Resume tu consulta en una frase"
          maxlength="100">
      </div>

      <!-- Mensaje -->
      <div class="campo">
        <label for="mensaje">
          Mensaje <span class="obligatorio">*</span>
        </label>
        <textarea 
          id="mensaje" 
          name="mensaje"
          rows="6"
          placeholder="Describe con detalle tu consulta..."
          required
          minlength="20"
          maxlength="1000">
        </textarea>
        <span class="ayuda">Mínimo 20 caracteres · Máximo 1000</span>
      </div>

      <!-- Cómo prefiere ser contactado -->
      <div class="campo">
        <p class="label-grupo">¿Cómo prefieres que te contactemos?</p>

        <div class="opciones-radio">
          <input type="radio" id="via-email" name="via_contacto" value="email" checked>
          <label for="via-email">📧 Por email</label>

          <input type="radio" id="via-whatsapp" name="via_contacto" value="whatsapp">
          <label for="via-whatsapp">📱 Por WhatsApp</label>

          <input type="radio" id="via-llamada" name="via_contacto" value="llamada">
          <label for="via-llamada">📞 Llamada telefónica</label>
        </div>
      </div>

      <!-- Teléfono condicional -->
      <div class="campo" id="campo-telefono">
        <label for="telefono">Teléfono</label>
        <input 
          type="tel" 
          id="telefono" 
          name="telefono"
          placeholder="300 123 4567"
          pattern="[0-9\s\-\+]{7,15}">
        <span class="ayuda">Solo si elegiste WhatsApp o llamada</span>
      </div>

      <!-- Términos y condiciones -->
      <div class="campo campo-check">
        <input type="checkbox" id="terminos" name="terminos" value="acepto" required>
        <label for="terminos">
          He leído y acepto la 
          <a href="#" target="_blank">política de privacidad</a> 
          y los 
          <a href="#" target="_blank">términos de uso</a>
          <span class="obligatorio">*</span>
        </label>
      </div>

      <!-- Suscripción opcional -->
      <div class="campo campo-check">
        <input type="checkbox" id="newsletter" name="newsletter" value="si">
        <label for="newsletter">
          📬 Quiero recibir novedades y recursos gratuitos
        </label>
      </div>

      <!-- Botones de acción -->
      <div class="acciones">
        <button type="submit" class="btn-primario">
          ✉️ Enviar mensaje
        </button>
        <button type="reset" class="btn-secundario">
          🗑️ Borrar todo
        </button>
      </div>

    </form>

  </main>

</body>
</html>
```

### Paso 2 — Estilos CSS (`contacto.css`)

```css
/* === Variables y reset básico === */
:root {
  --primario: #2563eb;
  --primario-oscuro: #1d4ed8;
  --texto: #1f2937;
  --texto-suave: #6b7280;
  --borde: #d1d5db;
  --fondo: #f9fafb;
  --blanco: #ffffff;
  --error: #dc2626;
  --exito: #16a34a;
  --radio: 8px;
  --sombra: 0 4px 20px rgba(0,0,0,0.08);
}

* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

body {
  font-family: 'Segoe UI', system-ui, sans-serif;
  background: var(--fondo);
  color: var(--texto);
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 30px 20px;
}

/* === Contenedor principal === */
.contenedor {
  background: var(--blanco);
  border-radius: 16px;
  box-shadow: var(--sombra);
  width: 100%;
  max-width: 680px;
  overflow: hidden;
}

/* === Encabezado === */
.encabezado {
  background: var(--primario);
  color: white;
  padding: 30px 40px;
}

.encabezado h1 {
  font-size: 1.8rem;
  margin-bottom: 6px;
}

.encabezado p {
  opacity: 0.85;
  font-size: 0.95rem;
}

/* === Formulario === */
.formulario-contacto {
  padding: 35px 40px;
  display: flex;
  flex-direction: column;
  gap: 20px;
}

/* === Fila doble (dos campos lado a lado) === */
.fila-doble {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}

@media (max-width: 520px) {
  .fila-doble {
    grid-template-columns: 1fr;
  }
  .formulario-contacto {
    padding: 25px 20px;
  }
}

/* === Campos individuales === */
.campo {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.campo label,
.label-grupo {
  font-weight: 600;
  font-size: 0.9rem;
  color: var(--texto);
}

.obligatorio {
  color: var(--error);
  margin-left: 3px;
}

/* === Inputs, select, textarea === */
input[type="text"],
input[type="email"],
input[type="tel"],
input[type="url"],
input[type="number"],
select,
textarea {
  width: 100%;
  padding: 10px 14px;
  border: 1.5px solid var(--borde);
  border-radius: var(--radio);
  font-size: 0.95rem;
  color: var(--texto);
  background: var(--blanco);
  transition: border-color 0.2s, box-shadow 0.2s;
  outline: none;
}

input:focus,
select:focus,
textarea:focus {
  border-color: var(--primario);
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.15);
}

input:invalid:not(:placeholder-shown),
textarea:invalid:not(:placeholder-shown) {
  border-color: var(--error);
}

input:valid:not(:placeholder-shown) {
  border-color: var(--exito);
}

textarea {
  resize: vertical;
  min-height: 130px;
}

select {
  cursor: pointer;
}

/* === Texto de ayuda === */
.ayuda {
  font-size: 0.78rem;
  color: var(--texto-suave);
}

/* === Radios y checkboxes === */
.opciones-radio {
  display: flex;
  flex-wrap: wrap;
  gap: 16px;
  margin-top: 4px;
}

.opciones-radio input[type="radio"] {
  width: auto;
  accent-color: var(--primario);
}

.opciones-radio label {
  font-weight: normal;
  cursor: pointer;
}

.campo-check {
  flex-direction: row;
  align-items: flex-start;
  gap: 10px;
}

.campo-check input[type="checkbox"] {
  width: 18px;
  height: 18px;
  margin-top: 2px;
  accent-color: var(--primario);
  flex-shrink: 0;
  cursor: pointer;
}

.campo-check label {
  font-weight: normal;
  font-size: 0.9rem;
  line-height: 1.5;
  cursor: pointer;
}

.campo-check a {
  color: var(--primario);
  text-decoration: underline;
}

/* === Botones === */
.acciones {
  display: flex;
  gap: 12px;
  margin-top: 8px;
  flex-wrap: wrap;
}

.btn-primario,
.btn-secundario {
  padding: 12px 28px;
  border-radius: var(--radio);
  font-size: 0.95rem;
  font-weight: 600;
  cursor: pointer;
  border: none;
  transition: transform 0.1s, box-shadow 0.2s;
}

.btn-primario {
  background: var(--primario);
  color: white;
  box-shadow: 0 2px 8px rgba(37, 99, 235, 0.3);
}

.btn-primario:hover {
  background: var(--primario-oscuro);
  transform: translateY(-1px);
  box-shadow: 0 4px 12px rgba(37, 99, 235, 0.4);
}

.btn-secundario {
  background: transparent;
  color: var(--texto-suave);
  border: 1.5px solid var(--borde);
}

.btn-secundario:hover {
  background: var(--fondo);
}
```

### Paso 3 — Validaciones HTML5 que debes conocer

```html
<!-- Campo requerido -->
<input type="text" required>

<!-- Longitud mínima y máxima de texto -->
<input type="text" minlength="3" maxlength="50">

<!-- Rango numérico -->
<input type="number" min="0" max="100" step="5">

<!-- Patrón personalizado (expresión regular) -->
<!-- Solo letras y espacios -->
<input type="text" pattern="[A-Za-záéíóúÁÉÍÓÚñÑ\s]+" 
       title="Solo letras y espacios">

<!-- Solo números de teléfono colombianos -->
<input type="tel" pattern="[0-9]{10}" 
       title="Ingresa 10 dígitos sin espacios">

<!-- URL válida -->
<input type="url" placeholder="https://...">

<!-- Mensaje personalizado de validación con JavaScript -->
<input type="email" id="correo"
       oninvalid="this.setCustomValidity('Por favor ingresa un correo válido')"
       oninput="this.setCustomValidity('')">
```

---

## 🎓 Diseño de Formularios en el Contexto Educativo

Los formularios en entornos escolares tienen desafíos únicos. No es lo mismo un formulario para comprar ropa que uno para que un estudiante pida un cupo en un taller, reporte un problema en el colegio o entregue una tarea.

### Principios de diseño para contextos educativos

#### 1. Claridad antes que todo

```html
<!-- ❌ Confuso -->
<label for="id1">Dato 1:</label>
<input type="text" id="id1" name="d1">

<!-- ✅ Claro -->
<label for="nombre-estudiante">Nombre del estudiante:</label>
<input type="text" id="nombre-estudiante" name="nombre_estudiante"
       placeholder="Ej: Laura Martínez">
```

#### 2. Instrucciones dentro del formulario

```html
<fieldset>
  <legend>📚 Solicitud de material de biblioteca</legend>
  <p class="instruccion">
    Completa este formulario para solicitar un libro prestado. 
    Los campos marcados con <strong>*</strong> son obligatorios.
    Recibirás la confirmación en tu correo institucional.
  </p>
  <!-- campos... -->
</fieldset>
```

#### 3. Formularios cortos y enfocados

Evita pedir más información de la necesaria. Si un estudiante va a registrar una idea para un proyecto, no le pidas su número de teléfono.

```
❌ Formulario de 15 campos para una simple sugerencia
✅ Formulario de 3-4 campos bien pensados
```

#### 4. Mensajes de error amigables

```html
<!-- Usando JavaScript básico -->
<script>
  document.querySelector('form').addEventListener('submit', function(e) {
    const email = document.getElementById('email').value;
    if (!email.includes('@')) {
      e.preventDefault();
      alert('❌ Por favor verifica tu correo electrónico');
    }
  });
</script>
```

### Casos de uso educativos — Practica estos

| Formulario | Campos clave | Tipo de inputs |
|------------|-------------|----------------|
| Inscripción a un club | Nombre, grado, motivación | text, select, textarea |
| Reporte de daño en el colegio | Lugar, descripción, urgencia | text, textarea, radio |
| Encuesta de convivencia | Satisfacción, sugerencias | radio, checkbox, textarea |
| Solicitud de permiso | Fecha, motivo, acudiente | date, text, textarea |
| Entrega de proyecto digital | Nombre, URL, descripción | text, url, textarea |

### 🧩 Mini reto — Formulario educativo

Diseña (en papel o en código) el formulario de **"Inscripción al Semillero de Programación"** de tu colegio. Debe tener:

- Nombre completo y grado
- ¿Por qué quieres inscribirte? (textarea)
- ¿Tienes computador en casa? (radio: sí / no / a veces)
- Materias en las que eres más fuerte (checkbox: Matemáticas, Tecnología, Inglés, Otra)
- Email de contacto

---

> ⏰ **Marca de tiempo: 195 minutos**

---

# 🍃 DESCANSO 2 — 15 minutos

> Has completado la parte más intensa del taller. ¡Bien hecho!  
> Estira los dedos, cierra los ojos un momento.  
> Cuando vuelvas, abordaremos algo que marca la diferencia entre un buen formulario y uno **excelente**.

---

# 🟣 BLOQUE 3 — Accesibilidad: Formularios para Todas las Personas

## ¿Qué es la accesibilidad web?

La accesibilidad web significa que **cualquier persona puede usar un sitio web**, independientemente de sus capacidades físicas, cognitivas o tecnológicas. Esto incluye personas que:

- 👁️ Tienen baja visión o son ciegas (usan lectores de pantalla como NVDA o VoiceOver)
- 🤚 Tienen dificultades motoras (navegan solo con teclado)
- 🧠 Tienen dislexia u otras dificultades cognitivas
- 🔇 Son sordas (no pueden escuchar audio)
- 📱 Usan teléfonos viejos o conexiones lentas

> 💡 **Dato:** Según la OMS, más del 15% de la población mundial vive con algún tipo de discapacidad. Un formulario inaccesible excluye a millones de personas.

---

## Las 4 reglas POUR de accesibilidad

La guía WCAG (Web Content Accessibility Guidelines) agrupa la accesibilidad en 4 principios:

| Principio | Significado | Ejemplo en formularios |
|-----------|------------|----------------------|
| **P**erceptible | La información debe poderse percibir | Labels visibles y asociados |
| **O**perable | Debe poderse usar con cualquier dispositivo | Navegación por teclado |
| **U**nderstandable | El contenido debe ser comprensible | Mensajes de error claros |
| **R**obust | Debe funcionar con tecnologías asistivas | HTML semántico correcto |

---

## Buenas prácticas de accesibilidad en formularios

### 1. Siempre usa `<label>` — nunca solo `placeholder`

```html
<!-- ❌ MAL: El placeholder desaparece al escribir -->
<input type="email" placeholder="Tu correo">

<!-- ✅ BIEN: El label siempre está visible -->
<label for="email">Correo electrónico:</label>
<input type="email" id="email" name="email" placeholder="correo@ejemplo.com">
```

### 2. Agrupa campos relacionados con `<fieldset>` y `<legend>`

```html
<!-- Un lector de pantalla anunciará: 
     "Grupo: Dirección de envío. Campo: Calle principal" -->
<fieldset>
  <legend>Dirección de envío</legend>
  <label for="calle">Calle principal</label>
  <input type="text" id="calle" name="calle">
  <label for="ciudad">Ciudad</label>
  <input type="text" id="ciudad" name="ciudad">
</fieldset>
```

### 3. Indica los campos obligatorios claramente

```html
<!-- ❌ Solo con color (los daltónicos no lo verán) -->
<label style="color: red">Email</label>

<!-- ✅ Con símbolo Y texto alternativo -->
<label for="email">
  Email 
  <span class="obligatorio" aria-label="obligatorio">*</span>
</label>

<!-- ✅ Aún mejor: explicar al inicio del formulario -->
<p>Los campos marcados con <strong>(*)</strong> son obligatorios.</p>
```

### 4. Mensajes de error descriptivos y accesibles

```html
<!-- ❌ Error genérico e inútil -->
<span style="color:red">Error</span>

<!-- ✅ Error específico y accesible -->
<div role="alert" aria-live="polite" class="mensaje-error">
  ⚠️ El correo debe tener el formato: nombre@dominio.com
</div>

<!-- Vinculando el error al campo -->
<input type="email" id="email" 
       aria-describedby="email-error"
       aria-invalid="true">
<span id="email-error" role="alert">
  Por favor ingresa un correo válido
</span>
```

### 5. Atributos ARIA para mayor accesibilidad

```html
<!-- aria-label: descripción adicional cuando el label no es suficiente -->
<input type="search" aria-label="Buscar en el catálogo de la biblioteca">

<!-- aria-required: redundante con required, pero ayuda a lectores viejos -->
<input type="text" required aria-required="true">

<!-- aria-describedby: referencia a texto de ayuda o error -->
<input type="password" id="pass" 
       aria-describedby="pass-ayuda pass-error">
<span id="pass-ayuda">Mínimo 8 caracteres</span>
<span id="pass-error" role="alert"></span>

<!-- aria-live: anuncia cambios dinámicos -->
<div aria-live="polite" id="contador">
  Caracteres restantes: <span>1000</span>
</div>

<!-- role="alert": para mensajes urgentes -->
<div role="alert">
  ✅ ¡Formulario enviado correctamente!
</div>
```

### 6. Navegación por teclado — ¡Pruébalo ahora!

Abre tu formulario y navega **solo con el teclado**:

| Tecla | Acción |
|-------|--------|
| `Tab` | Avanza al siguiente campo |
| `Shift + Tab` | Retrocede al campo anterior |
| `Espacio` | Marca/desmarca checkbox |
| `↑ ↓` | Navega entre opciones radio y select |
| `Enter` | Envía el formulario / activa botón |

```css
/* ✅ Nunca elimines el foco visible sin reemplazarlo */

/* ❌ NO hagas esto */
*:focus { outline: none; }

/* ✅ Haz esto en cambio */
*:focus {
  outline: 3px solid #2563eb;
  outline-offset: 2px;
}

/* ✅ O esto para un estilo personalizado */
input:focus,
select:focus,
textarea:focus,
button:focus {
  outline: none;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.4);
}
```

### 7. Contraste de color — ¿Se puede leer bien?

Las pautas WCAG exigen:
- **Texto normal:** ratio de contraste mínimo de **4.5:1**
- **Texto grande (+18px):** ratio mínimo de **3:1**

```css
/* ❌ Bajo contraste — difícil de leer */
.ayuda { color: #bbbbbb; background: #ffffff; }  /* ratio: 1.9:1 */

/* ✅ Contraste adecuado */
.ayuda { color: #6b7280; background: #ffffff; }  /* ratio: 4.6:1 */
```

> 🔧 **Herramienta:** [WebAIM Contrast Checker](https://webaim.org/resources/contrastchecker/) — Pega dos colores y te dice si cumplen WCAG.

---

## 🔍 Análisis de accesibilidad — Actividad práctica

Examina el siguiente fragmento de código y encuentra **al menos 5 problemas de accesibilidad**:

```html
<!-- ¿Cuántos problemas encuentras? -->
<form>
  <p style="color: red">* Campos requeridos</p>
  
  <div>
    <input type="text" placeholder="Nombre" style="border: 1px solid #eee">
  </div>
  
  <div>
    <p>Sexo:</p>
    <input type="radio" name="sexo" value="m"> Masculino
    <input type="radio" name="sexo" value="f"> Femenino
  </div>
  
  <div>
    ¿Acepta términos?
    <input type="checkbox">
  </div>
  
  <input type="submit" value="ok">
</form>
```

### Solución comentada

```html
<!-- Problema 1: No hay <label> para el campo de texto
     Problema 2: El input no tiene id ni name
     Problema 3: Los radio no tienen <label> ni id
     Problema 4: El checkbox no tiene <label> ni id
     Problema 5: El botón "ok" no es descriptivo
     Problema 6: El color rojo solo no comunica obligatoriedad
     Problema 7: No hay <fieldset> para agrupar los radio buttons -->

<form action="#" method="post">
  <p>Los campos marcados con <strong>(*)</strong> son requeridos.</p>

  <div class="campo">
    <label for="nombre">Nombre completo <span aria-label="requerido">*</span></label>
    <input type="text" id="nombre" name="nombre" required>
  </div>

  <fieldset>
    <legend>Género</legend>
    <input type="radio" id="masculino" name="genero" value="m">
    <label for="masculino">Masculino</label>
    <input type="radio" id="femenino" name="genero" value="f">
    <label for="femenino">Femenino</label>
    <input type="radio" id="prefiero-no" name="genero" value="no-indicar">
    <label for="prefiero-no">Prefiero no indicar</label>
  </fieldset>

  <div class="campo campo-check">
    <input type="checkbox" id="terminos" name="terminos" required>
    <label for="terminos">Acepto los términos y condiciones *</label>
  </div>

  <button type="submit">Enviar formulario</button>
</form>
```

---

## 🏁 Cierre — Reto Final

### Proyecto integrador

Crea un **formulario de matrícula para un torneo deportivo del colegio**, aplicando todo lo aprendido:

**Requisitos mínimos:**
- [ ] Estructura con `<form>`, `<fieldset>` y `<legend>`
- [ ] Campos: nombre, email, grado (select), deporte (select), nivel (radio), condición médica relevante (textarea)
- [ ] Todos los campos con `<label>` correctamente vinculados
- [ ] Al menos un campo con validación HTML5 (`required`, `minlength`, `pattern`, etc.)
- [ ] Diseño CSS básico (legible, ordenado)
- [ ] Sin problemas de accesibilidad visibles
- [ ] Navegación funcional solo con teclado

**Puntos extra:**
- [ ] Uso de `aria-describedby` para al menos un campo
- [ ] Contraste de colores verificado
- [ ] Formulario responsivo (se ve bien en móvil y escritorio)
- [ ] Campo de archivo para subir foto del participante

---

## 📚 Recursos para seguir aprendiendo

| Recurso | Qué encontrarás | URL |
|---------|----------------|-----|
| MDN Web Docs | Documentación completa de cada etiqueta | developer.mozilla.org |
| W3Schools | Tutoriales con ejemplos editables | w3schools.com |
| WebAIM | Guías de accesibilidad web | webaim.org |
| WCAG 2.1 en español | Estándar oficial de accesibilidad | wcag.iau.org |
| Can I Use | Compatibilidad de navegadores | caniuse.com |

---

## 🧠 Resumen del día

```
FORMULARIOS HTML — Lo que aprendiste hoy
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

<form>         → Contenedor principal (action, method)
<label>        → Nombre accesible para cada campo
<input>        → Campo versátil (text, email, password,
                  checkbox, radio, file, date, range...)
<select>       → Lista desplegable de opciones
<option>       → Cada opción dentro del select
<optgroup>     → Agrupa opciones con un título
<textarea>     → Texto libre y largo
<button>       → Acción (submit, reset, button)
<fieldset>     → Agrupa campos relacionados
<legend>       → Título del grupo fieldset

ACCESIBILIDAD
━━━━━━━━━━━━━
✔ Siempre usa <label> con for/id
✔ Usa fieldset + legend para grupos
✔ Indica errores con texto, no solo color
✔ Verifica la navegación por teclado
✔ Comprueba el contraste de colores
✔ Los placeholder no reemplazan los labels
✔ aria-describedby y role="alert" para mensajes
```

---

> 🎉 **¡Felicitaciones!** Completaste el taller de Formularios HTML.  
> Ahora tienes las herramientas para construir formularios que no solo funcionan, sino que son **accesibles e inclusivos para todas las personas**.

---

*Material elaborado para jóvenes de 15–16 años · Duración: 4 horas · Publicado bajo licencia [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.es)*
