# 📋 Guía del Profesor
## De Cero a tu Primera API: SQL, SQLModel y FastAPI
### Curso para jóvenes de 15-16 años · 22 sesiones · 2 horas cada una

---

> Esta guía acompaña el material del estudiante. Está diseñada para profesores con conocimientos de Python y bases de datos, pero sin experiencia previa enseñando a adolescentes. Cada sesión incluye tiempos sugeridos, posibles confusiones del estudiante, preguntas de verificación de comprensión y consejos pedagógicos específicos para este rango de edad.

---

## 🧭 Filosofía pedagógica del curso

### Por qué este enfoque funciona con adolescentes

Los jóvenes de 15-16 años aprenden mejor cuando:
1. **Ven la utilidad inmediata**: Cada concepto debe responder "¿para qué sirve esto en una app real?"
2. **Construyen algo tangible**: No ejercicios abstractos; una base de datos de música, videojuegos o deportes que ellos diseñaron.
3. **Se equivocan en un ambiente seguro**: Los errores son parte del proceso. Normaliza el debugging desde la primera sesión.
4. **Tienen éxitos frecuentes**: Cada sesión debe terminar con algo funcionando, aunque sea pequeño.
5. **Trabajan con sus propios intereses**: Permite máxima libertad en la elección del proyecto final.

### La progresión pedagógica del curso

```
Concreto → Abstracto → Concreto otra vez

1. Primero: "Aquí hay una tabla de canciones" (concreto)
2. Luego: "Esto se llama relación 1:N" (abstracto)
3. Finalmente: "Tu app de videojuegos necesita esta relación" (concreto otra vez)
```

Nunca presentes la teoría antes de mostrar el problema que resuelve.

---

## 🛠️ Preparación antes del curso

### Configuración técnica del aula

```
Requerimientos mínimos por puesto:
- Python 3.11 o superior instalado
- pip actualizado
- DB Browser for SQLite instalado
- VS Code instalado con la extensión de Python
- Acceso a internet (para instalar paquetes y ver documentación)
```

**Script de verificación** — Pide a los estudiantes que ejecuten esto al inicio:

```bash
python --version
pip install sqlmodel fastapi uvicorn --quiet
python -c "import sqlmodel, fastapi; print('✅ Todo listo')"
```

### Material que debes tener listo

- [ ] El archivo `practica.db` creado con el script de la Sesión 03
- [ ] Los proyectos de ejemplo completos (artistas + canciones) funcionando localmente
- [ ] La documentación de FastAPI abierta en el navegador: https://fastapi.tiangolo.com
- [ ] La documentación de SQLModel: https://sqlmodel.tiangolo.com

### Errores técnicos frecuentes antes de comenzar

| Error | Causa probable | Solución |
|-------|---------------|---------|
| `python` no encontrado | Instalación incorrecta o alias faltante | Intentar con `python3` o reinstalar |
| `pip` no encontrado | Idem | `python -m pip install ...` |
| `ModuleNotFoundError: No module named 'sqlmodel'` | El pip instaló en el Python incorrecto | Usar `python -m pip install sqlmodel` |
| VS Code no encuentra Python | Intérprete no seleccionado | Ctrl+Shift+P → "Select Interpreter" |

---

## 📅 Guía sesión por sesión

---

### SESIÓN 01 — ¿Qué es una base de datos?

**Objetivo de aprendizaje:** Los estudiantes pueden explicar con sus propias palabras para qué sirve una BD y reconocen los términos tabla, fila, columna, clave primaria.

---

#### Guía de tiempos

| Actividad | Tiempo | Notas |
|-----------|--------|-------|
| Bienvenida + presentación del curso | 10 min | Muestra el proyecto final que van a construir |
| El problema que resuelven las BDs | 15 min | Discusión grupal antes de mostrar las opciones |
| Tablas, filas y columnas | 25 min | Usa una hoja de cálculo de Google Sheets proyectada |
| Tipos de datos | 15 min | Relaciona con los tipos de Python que ya conocen |
| DB Browser: exploración guiada | 35 min | Hazlo tú primero, luego ellos repiten |
| Cierre + tarea | 5 min | |

---

#### Cómo presentar la clase

**Al inicio, muestra el producto final antes de empezar a enseñar:**

> "En 22 sesiones, van a construir una API web completa. Esto significa que van a tener una URL que cualquiera puede usar desde su teléfono o computador para consultar, agregar y modificar datos en una base de datos que ustedes diseñaron. Hoy empezamos desde el principio: ¿qué es una base de datos?"

**Para explicar la clave primaria**, usa esta analogía:

> "Imaginen que hay dos estudiantes en el colegio que se llaman Juan García. ¿Cómo los diferencia el sistema escolar? Con el número de documento. El `id` en una tabla es exactamente eso: un número único que nunca se repite, aunque dos canciones tengan el mismo título o dos artistas el mismo nombre."

---

#### Señales de que están entendiendo

- ✅ Pueden decir cuántas filas y columnas tiene una tabla que les muestras
- ✅ Pueden identificar cuál sería la clave primaria de una tabla nueva
- ✅ Pueden dar un ejemplo de por qué una lista en Python no sirve para guardar datos permanentemente

#### Señales de confusión frecuente

- ❓ Confunden "tabla" con "base de datos" (una BD contiene muchas tablas)
- ❓ Creen que el `id` debe ser el nombre o algo descriptivo
- ❓ No entienden para qué sirve el tipo de dato si Python no lo exige

**Respuesta para el punto 3:**

> "Python es flexible con los tipos, pero una base de datos es estricta porque guarda millones de filas y debe ser eficiente. Un número entero ocupa 4 bytes; un texto ocupa mucho más. Si guardamos 'el año 1975' como texto en vez de número, las comparaciones de tipo 'año > 2000' no funcionarán correctamente."

---

#### Actividad en DB Browser — Guía paso a paso para el profesor

1. Abre DB Browser y proyecta tu pantalla
2. Crea `sesion01.db` mientras los estudiantes ven
3. Muestra el botón "New Table" y crea la tabla `canciones` paso a paso
4. Explica cada opción: NOT NULL, PRIMARY KEY, AUTOINCREMENT
5. Inserta 3 registros tú mismo mostrando cómo se hace
6. Ahora deja que ellos lo hagan solos con sus 5 canciones favoritas

> ⚠️ **Problema frecuente:** DB Browser puede dar errores confusos cuando el estudiante no marca AUTOINCREMENT en el `id`. Ten listo el mensaje de error para explicarlo cuando aparezca.

---

#### Pregunta de cierre (verifica comprensión)

"Si tuviéramos una tabla de videojuegos, ¿qué columnas tendría y de qué tipo sería cada una?" — Escucha las respuestas y corrige si algún estudiante propone tipos incorrectos.

---

### SESIÓN 02 — Diseño de tablas

**Objetivo de aprendizaje:** Los estudiantes pueden diseñar una base de datos básica para una aplicación real, identificando entidades, atributos y relaciones.

---

#### Guía de tiempos

| Actividad | Tiempo | Notas |
|-----------|--------|-------|
| Revisión de tarea | 10 min | Cada estudiante explica su app en 1 minuto |
| El proceso de diseño | 10 min | Los 4 pasos |
| Entidades y atributos (librería) | 20 min | Hazlo junto con ellos, no solo en el tablero |
| Tipos de relaciones | 35 min | Cada tipo necesita un ejemplo diferente |
| Las 3 reglas de oro | 15 min | Muestra el mal diseño primero |
| Actividad grupal (series) | 25 min | Grupos de 3-4 personas |
| Presentación de grupos | 5 min | |

---

#### Cómo enseñar las relaciones

Las relaciones son el concepto más difícil de este bloque. La clave es **hacer la pregunta correcta en voz alta** antes de dar la respuesta.

**Para 1:N:**
> "Antes de decirles el nombre, piensen: ¿puede un artista tener varias canciones? Sí. ¿Puede una canción tener varios artistas principales? Depende... pero en nuestra app digamos que no. Entonces un artista tiene MUCHAS canciones, pero cada canción tiene UN artista. A esto le llamamos relación uno a muchos."

**Para N:M:**
> "¿Puede un usuario tener varias playlists? Sí. ¿Puede una canción estar en varias playlists? También sí. Aquí no podemos poner la clave foránea en ninguna de las dos tablas. Si ponemos `playlist_id` en canciones, ¿qué pasa cuando la misma canción está en 3 playlists?"

Espera a que ellos razonen por qué una sola columna no alcanza.

**Para la tabla intermedia:**
> "La solución es una tabla nueva que solo existe para conectar las dos. Cada fila de esa tabla dice: 'esta canción está en esta playlist'. Una canción puede aparecer en muchas filas (muchas playlists), y una playlist puede aparecer en muchas filas (muchas canciones)."

---

#### Errores comunes en el diseño (y cómo abordarlos)

**Error: Poner demasiados atributos en una tabla**

Estudiante: "En mi tabla Usuario quiero poner: nombre, apellido, email, teléfono, dirección, ciudad, país, foto_perfil, descripción, fecha_nacimiento, género musical favorito..."

Respuesta sugerida: "Todo eso puede ser válido, pero cuando estamos diseñando por primera vez, pongamos solo lo esencial. ¿Qué necesita saber el sistema sobre un usuario para que la app funcione? Empieza con lo mínimo y agrega después."

**Error: No saber si una relación es 1:N o N:M**

Respuesta sugerida: "Haz las dos preguntas: ¿puede [A] tener muchos [B]? Y: ¿puede [B] tener muchos [A]? Si ambas respuestas son sí, es N:M. Si solo una es sí, es 1:N."

---

#### Actividad grupal — Instrucciones detalladas

Asigna a cada grupo el mismo problema (app de series) o diferentes (si el tiempo lo permite). Los grupos deben:

1. Escribir las entidades en una hoja (5 min)
2. Agregar atributos a cada entidad (5 min)
3. Dibujar las flechas de relación y escribir si es 1:N o N:M (5 min)
4. Presentar brevemente a la clase (10 min)

Evalúa en voz alta mientras cada grupo presenta, destacando lo que está bien y corrigiendo suavemente lo que no.

---

### SESIÓN 03 — Instalación y primera BD

**Objetivo de aprendizaje:** Todos los estudiantes tienen el entorno funcionando y comprenden la estructura de la base de datos de práctica.

---

#### Guía de tiempos

| Actividad | Tiempo | Notas |
|-----------|--------|-------|
| Verificación de instalaciones | 25 min | El tiempo más crítico. No avances si alguien está bloqueado |
| Ejecutar el script SQL de práctica | 25 min | Explica cada bloque del script mientras lo ejecutan |
| Explorar la BD en DB Browser | 30 min | Preguntas guiadas sobre la estructura |
| Verificar que todos tienen la BD lista | 10 min | Pasea por los puestos |
| Vista previa de las próximas sesiones | 10 min | "Con esto vamos a poder hacer consultas complejas" |

---

#### Estrategia para las instalaciones

La instalación es donde más estudiantes se pueden quedar atrás. Estrategia recomendada:

1. **Identifica a los más avanzados** antes de empezar. Pídeles que terminen rápido y luego ayuden a los que tienen problemas.
2. **Ten el script de verificación listo** en el proyector para que todos vean el resultado esperado.
3. **No esperes a que todos terminen para seguir**. Deja a los que tienen el entorno listo que exploren DB Browser mientras ayudas a los que están con problemas.

> ⚠️ **El problema más frecuente en Windows:** Python instalado sin agregar al PATH. Solución: reinstalar Python marcando "Add Python to PATH" en el instalador.

---

#### Cómo presentar el script SQL de práctica

No ejecutes todo el script de una vez. Ejecútalo por partes y explica cada sección:

1. Ejecuta solo el CREATE de `generos`. Muestra la tabla en DB Browser.
2. Ejecuta el CREATE de `artistas`. Explica la diferencia entre `NOT NULL` y `TEXT`.
3. Ejecuta el de `canciones`. Señala las FOREIGN KEY y explica que conectan con las otras tablas.
4. Ejecuta los INSERTs de generos. Muestra que la tabla ahora tiene datos.
5. Continúa con los demás INSERTs.

**Pregunta guía para el cierre de la sesión:**

> "Miren la tabla `playlist_canciones`. ¿Cuántas columnas tiene? ¿Por qué tiene dos claves foráneas? ¿A qué relación corresponde?"

---

### SESIONES 04-07 — Bloque SQL Básico

**Objetivo del bloque:** Los estudiantes pueden escribir consultas SQL de complejidad básica con confianza, sin copiar del material.

---

#### Estrategia general para enseñar SQL

**El patrón "Yo hago → Hacemos juntos → Tú haces" funciona muy bien:**

1. **(10 min)** Tú escribes la consulta en el proyector y explicas cada parte
2. **(10 min)** Escribes la consulta con espacios en blanco y el grupo completa en voz alta
3. **(20-30 min)** Ellos resuelven ejercicios solos, tú circulas por los puestos

**Regla de los 5 minutos:** Si un estudiante lleva más de 5 minutos atascado en el mismo punto, interviene. No dejes que la frustración se acumule.

---

#### Sesión 04 — SELECT y WHERE

**Concepto que más les cuesta:** El orden de evaluación de AND y OR sin paréntesis.

Usa este ejemplo concreto:

```sql
-- ¿Qué devuelve esto?
SELECT * FROM artistas
WHERE pais = 'Colombia' OR pais = 'Puerto Rico' AND año_inicio > 2010;
-- Resultado: todos los colombianos + solo los puertorriqueños post-2010
-- Porque AND tiene mayor precedencia que OR
-- Como en matemáticas: * antes que +
```

> 💡 **Analogía que funciona:** "El AND es como la multiplicación y el OR es como la suma en matemáticas. El `*` siempre va antes que el `+` a menos que haya paréntesis."

---

#### Sesión 05 — ORDER BY, LIMIT, LIKE, IN, BETWEEN

**Actividad de consolidación sugerida (adicional al material):**

Pide a los estudiantes que conviertan preguntas en español a SQL:

- "Dame los 3 artistas más recientes" → `SELECT nombre FROM artistas ORDER BY año_inicio DESC LIMIT 3`
- "¿Hay canciones cuyo título empiece con 'B'?" → `SELECT titulo FROM canciones WHERE titulo LIKE 'B%'`
- "Artistas de Colombia, México o Argentina" → `WHERE pais IN ('Colombia', 'México', 'Argentina')`

Este ejercicio de "traducción" es muy efectivo para afianzar la comprensión.

---

#### Sesión 06 — INSERT y UPDATE

**El momento pedagógico más importante de la sesión:**

Antes de mostrar el peligro del UPDATE sin WHERE, ejecuta esto delante de todos:

```sql
-- Primero muestra cuántas canciones hay
SELECT COUNT(*) FROM canciones;  -- Digamos 15

-- Luego ejecuta el UPDATE sin WHERE
UPDATE canciones SET reproducciones = 0;

-- Luego verifica
SELECT * FROM canciones;  -- Todas con 0
```

Ver el efecto en tiempo real tiene mucho más impacto que solo explicarlo. La reacción del grupo ("¡nooo!") refuerza el aprendizaje.

Luego muestra cómo recuperarse (o no) con:

> "Como no hicimos una copia de seguridad, no hay forma de recuperar esos datos. Por eso la regla es: **siempre verifica con un SELECT antes de ejecutar un UPDATE o DELETE importante**."

---

#### Sesión 07 — DELETE, transacciones y agregaciones

**Para enseñar transacciones, usa la analogía bancaria:**

> "Imagina que transfières $50 de tu cuenta a la de tu amigo. Son dos operaciones: restar $50 de tu cuenta y sumar $50 a la suya. Si la primera operación funciona pero la segunda falla (por un error del sistema), ¿qué pasa? Tu dinero desapareció y tu amigo no lo recibió. Las transacciones previenen exactamente eso: o se hacen las dos operaciones o no se hace ninguna."

**Para las funciones de agregación**, empieza siempre mostrando los datos crudos y luego la versión agregada:

```sql
-- Primero: ver todos los valores
SELECT reproducciones FROM canciones;

-- Luego: el resumen
SELECT AVG(reproducciones) FROM canciones;
```

Esto ayuda a entender que AVG "colapsa" todas las filas en un solo valor.

---

### SESIONES 08-11 — Bloque Relaciones SQL

**El tema más difícil del curso.** Planifica más tiempo de soporte individual en estas sesiones.

---

#### Sesión 08 — INNER JOIN

**El error conceptual más frecuente:** Los estudiantes mezclan el orden de las tablas en el ON y no entienden por qué no funciona.

```sql
-- Estas dos consultas son equivalentes (el orden en ON no importa):
SELECT * FROM canciones INNER JOIN artistas ON canciones.artista_id = artistas.id;
SELECT * FROM canciones INNER JOIN artistas ON artistas.id = canciones.artista_id;

-- Pero esta NO funciona (columnas equivocadas):
SELECT * FROM canciones INNER JOIN artistas ON canciones.id = artistas.id;
-- Une por id coincidente, que no tiene sentido semántico
```

**Visualización que funciona bien:** Dibuja dos tablas en el tablero con flechas físicas conectando las filas que coinciden. Es más efectivo que cualquier explicación verbal.

**Pregunta de verificación de comprensión:** "¿Qué pasa si un artista no tiene ninguna canción? ¿Aparece en el resultado del INNER JOIN?" (No aparece — este es el punto clave que diferencia INNER de LEFT JOIN.)

---

#### Sesión 09 — LEFT JOIN y tres tablas

**Estrategia para las consultas de tres tablas:**

Construye la consulta en el proyector de forma incremental:

```sql
-- Paso 1: Solo canciones
SELECT c.titulo FROM canciones AS c;

-- Paso 2: Agrega el artista
SELECT c.titulo, a.nombre
FROM canciones AS c
INNER JOIN artistas AS a ON c.artista_id = a.id;

-- Paso 3: Agrega el género
SELECT c.titulo, a.nombre, g.nombre
FROM canciones AS c
INNER JOIN artistas AS a ON c.artista_id = a.id
INNER JOIN generos AS g ON c.genero_id = g.id;
```

Esta construcción incremental reduce significativamente la confusión.

---

#### Sesión 10 — GROUP BY y HAVING

**El error más frecuente:** Usar columnas en el SELECT que no están en el GROUP BY.

```sql
-- Error: nombre no está en el GROUP BY
SELECT nombre, COUNT(*) FROM canciones GROUP BY artista_id;
-- SQLite puede aceptar esto pero da resultados incorrectos

-- Correcto:
SELECT a.nombre, COUNT(c.id)
FROM artistas AS a
LEFT JOIN canciones AS c ON c.artista_id = a.id
GROUP BY a.id, a.nombre;
```

**Para explicar la diferencia WHERE vs HAVING**, usa esta visualización mental:

> "Imagina que GROUP BY es como poner en grupos todas las canciones de la misma manera que clasificarías ropa en pilas por color. WHERE es como no dejar entrar cierta ropa a la lavandería antes de clasificarla. HAVING es como después de hacer las pilas, tirar las pilas pequeñas (las que tienen menos de 2 prendas)."

---

#### Sesión 11 — Subconsultas y repaso

**Para el repaso general**, considera convertirlo en un mini-concurso:

Divide la clase en equipos de 2-3 personas. Proyecta las preguntas una por una. El primer equipo en tener la consulta correcta funcionando gana un punto. Esto introduce competencia amistosa y hace el repaso más dinámico.

Los desafíos de nivel 3 son intencionalmente difíciles. No esperes que todos los resuelvan; funcionan como extensión para los más avanzados.

---

### SESIONES 12-15 — Bloque Python + SQLModel

---

#### Sesión 12 — Python + sqlite3

**Por qué esta sesión es importante aunque luego usemos SQLModel:**

> Explícales esto directamente: "Vamos a aprender sqlite3 puro aunque después usaremos SQLModel, que hace todo esto automáticamente. El motivo es que cuando algo falle con SQLModel, necesitan entender qué está pasando por debajo. Es como aprender a calcular manualmente antes de usar la calculadora."

**El tema de SQL Injection requiere atención especial:**

Muestra el ataque en vivo (en la base de datos de práctica, no en producción):

```python
import sqlite3

con = sqlite3.connect("practica.db")
cur = con.cursor()

# Simula un formulario de login
nombre_usuario = "' OR '1'='1"  # Entrada maliciosa

# Con f-string (VULNERABLE)
query = f"SELECT * FROM usuarios WHERE nombre = '{nombre_usuario}'"
print("Query peligrosa:", query)
# Muestra: SELECT * FROM usuarios WHERE nombre = '' OR '1'='1'
# ¡Devuelve TODOS los usuarios!
resultado = cur.execute(query).fetchall()
print(f"Registros devueltos: {len(resultado)}")  # Todos los usuarios

# Con parámetros (SEGURO)
resultado_seguro = cur.execute(
    "SELECT * FROM usuarios WHERE nombre = ?",
    (nombre_usuario,)
).fetchall()
print(f"Con parámetros: {len(resultado_seguro)}")  # 0 registros
```

Ver el ataque funcionar en tiempo real hace que recuerden la lección.

---

#### Sesión 13 — Introducción a SQLModel

**Cómo presentar SQLModel sin abrumar:**

Empieza con la comparación directa sqlite3 vs SQLModel:

```python
# Con sqlite3 (lo que ya saben)
cursor.execute("""
    CREATE TABLE IF NOT EXISTS artista (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        pais TEXT
    )
""")

# Con SQLModel (lo que aprenderán hoy)
class Artista(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    pais: Optional[str] = None
```

Pregunta: "¿Cuál es más fácil de leer? ¿Cuál parece más código Python?"

**Para el ejercicio de modelar su app**, circulas constantemente. Los puntos de dificultad más frecuentes:
- Olvidar `table=True`
- Poner `Optional` en campos que deben ser obligatorios
- Olvidar importar `Optional` de `typing`

---

#### Sesión 14 — CRUD con Sessions

**El concepto de Session es el más abstracto de esta sesión.** La analogía del carrito de compras funciona bien:

> "Cuando agregas cosas al carrito de Amazon no se están comprando todavía. Recién cuando haces clic en 'Comprar' se confirma la transacción. La Session funciona igual: puedes hacer `session.add()` varias veces y recién cuando haces `session.commit()` los cambios se guardan en la base de datos."

**¿Por qué `session.refresh()`?** Esto confunde mucho:

> "Después del commit, el objeto que tienes en Python tiene el `id = None` porque lo creaste con `id = None`. La base de datos le asignó un id (digamos 1), pero el objeto en Python no sabe eso todavía. `session.refresh()` le dice al objeto: 've a la base de datos y trae los valores actuales'."

---

#### Sesión 15 — Relaciones y separación de modelos

**El patrón Base/Create/Update/Table/Response es el más importante para FastAPI.** Dedica tiempo a explicar por qué cada uno existe:

| Modelo | ¿Por qué existe? |
|--------|-----------------|
| `Base` | Evita repetir los mismos campos en todos los modelos |
| `Create` | El usuario no puede asignar el `id` ni campos internos |
| `Update` | Todo es opcional; no debería obligar a enviar todos los campos |
| `Table` | El único que tiene `table=True`; contiene relaciones SQLAlchemy |
| `Response` | Controla exactamente qué se devuelve; nunca expone passwords |

**Pregunta provocadora:** "¿Por qué sería peligroso devolver el modelo `Table` directamente en vez de un `Response`?"

Respuesta esperada: Podrías exponer campos sensibles como contraseñas, tokens internos o relaciones que no quieres que el usuario vea.

---

### SESIONES 16-19 — Bloque FastAPI

---

#### Sesión 16 — Hola FastAPI

**Momento de asombro:** Cuando ejecuten el servidor por primera vez y abran `/docs`, espera la reacción. La documentación automática siempre sorprende a quienes vienen de backends más tradicionales.

> "Esto se genera completamente automático. No escribieron ni una línea de HTML ni JavaScript. FastAPI leyó el código Python y generó la documentación. Esto es lo que hace que FastAPI sea tan popular."

**Para el 'Try it out' en Swagger**, guía a toda la clase al mismo tiempo la primera vez. Muchos estudiantes no saben qué hacer con la interfaz inicialmente.

---

#### Sesión 17 — FastAPI + SQLModel

**Inyección de dependencias — el concepto clave:**

La inyección de dependencias es conceptualmente difícil para este grupo de edad. Usa esta explicación:

> "Imagina que tienes una función que necesita una conexión a internet. Hay dos formas de dársela: (1) La función crea la conexión ella misma cada vez que se llama. (2) Alguien externo le pasa la conexión cuando la llama. La segunda opción es 'inyección de dependencias'. FastAPI hace la segunda opción: antes de ejecutar tu endpoint, llama a `get_session()` y le pasa el resultado. Tú no tienes que preocuparte de abrir o cerrar la sesión."

**Verificación de que entendieron `Depends`:**

Pregunta: "Si quitáramos `Depends(get_session)` y pusiéramos directamente `Session(engine)`, ¿qué pasaría?"

Respuesta esperada: Funcionaría, pero habría que abrir y cerrar la sesión manualmente en cada endpoint. Con `Depends`, FastAPI lo hace automáticamente.

---

#### Sesión 18 — GET y POST

**Para los query parameters con `Query()`**, muestra la diferencia en la documentación:

```python
# Sin Query() - aparece en docs pero sin descripción ni validación
@app.get("/items")
def listar(limite: int = 10):
    pass

# Con Query() - aparece documentado y validado
@app.get("/items")
def listar(limite: int = Query(default=10, ge=1, le=100, description="Máximo de resultados")):
    pass
```

Muestra en `/docs` cómo el segundo tiene más información y cómo el `ge=1, le=100` previene que alguien pida `limite=-1` o `limite=999999`.

---

#### Sesión 19 — PUT, DELETE y Debugging

**Esta sesión es deliberadamente diferente.** La mitad es código nuevo (PUT y DELETE) y la mitad es debugging. Alterna entre los dos para que no sea monótona.

**Para la sección de debugging**, el mejor enfoque es reproducir los errores en tiempo real:

1. Crea un modelo nuevo y ejecuta sin `check_same_thread` → muestra el error
2. Corrígelo y ejecuta → muestra que funciona
3. Comete el error de importar un modelo después de `create_all` → muestra el error
4. Corrígelo

**Ver los errores y las soluciones en tiempo real es más valioso que leer sobre ellos.**

**Para el `model_dump(exclude_unset=True)`, muestra la diferencia:**

```python
from modelos import ArtistaUpdate

# El usuario solo envía el país
data = ArtistaUpdate(pais="España")

# Sin exclude_unset: todos los campos, incluso los None
print(data.model_dump())
# {'nombre': None, 'pais': 'España', 'año_inicio': None}

# Con exclude_unset: solo lo que el usuario envió
print(data.model_dump(exclude_unset=True))
# {'pais': 'España'}
```

Si no usáramos `exclude_unset=True`, actualizar solo el país pondría el nombre en `None`.

---

### SESIONES 20-22 — Proyecto Final

---

#### Sesión 20 — Diseño e inicio

**Tu rol en esta sesión es principalmente el de asesor individual**, no de instructor frontal.

**Los primeros 45 minutos son críticos:** Si un estudiante empieza a implementar con un diseño deficiente, su proyecto entero sufrirá. Pasa por todos los puestos durante el diseño y verifica:

1. ¿Tiene al menos 3 entidades con sentido?
2. ¿Las relaciones son correctas?
3. ¿Los tipos de datos son apropiados?

**Señales de un diseño problemático que debes corregir:**

| Problema | Sugerencia |
|---------|-----------|
| Una tabla con 20+ columnas | Dividir en 2 entidades |
| Columnas calculadas (ej: `promedio_notas`) | Los cálculos se hacen en código, no se guardan |
| Relaciones en la dirección incorrecta | Hacer las dos preguntas "¿puede X tener muchos Y?" |
| No hay ninguna relación entre tablas | "¿Cómo se conectan estas entidades en la vida real?" |

**Para los últimos 75 minutos**, circula constantemente. El orden de implementación correcto es importante; asegúrate de que todos sigan: modelos → database → main (solo GET primero).

---

#### Sesión 21 — Construcción y revisión entre pares

**La revisión entre pares** tiene dos objetivos: que el revisor aprenda a leer código ajeno, y que el revisado reciba retroalimentación externa.

**Instrucciones para la revisión:**

> "No se trata de encontrar errores para ganar. Se trata de aprender mutuamente. Si encuentran un bug, ayuden a resolverlo, no solo anoten 'hay un bug'. Si algo está muy bien implementado, digan específicamente qué está bien y por qué."

**Señales de que un proyecto necesita ayuda urgente:**

- El servidor no inicia
- Los endpoints devuelven errores 500 (error interno)
- No hay ningún endpoint POST funcionando

En estos casos, interviene directamente antes de la revisión entre pares.

---

#### Sesión 22 — Presentaciones y cierre

**Para las presentaciones**, establece estas reglas desde el inicio:

1. El demo es en vivo, desde cero (no prepares datos de antemano)
2. Los errores hacen parte; si algo falla, explica por qué y cómo lo resolverías
3. No se permiten interrupciones durante la demo
4. Las preguntas van al final de cada presentación

**Rol del público:** Pide a los estudiantes que llenen la rúbrica durante cada presentación. Esto los mantiene atentos y produce retroalimentación escrita valiosa.

**Cierre del curso — lo que funciona:**

Termina la sesión preguntando: "¿Qué es lo más útil que aprendieron en este curso?" No por tema o tecnología, sino en términos generales de cómo piensan sobre los datos y los sistemas. Las respuestas suelen sorprender.

---

## 📊 Evaluación

### Evaluación continua (durante el curso)

| Criterio | Frecuencia | Peso sugerido |
|----------|-----------|---------------|
| Actividades prácticas de cada sesión | Cada sesión | 30% |
| Participación y resolución de ejercicios | Continua | 20% |
| Tarea de diseño de BD (Sesión 02) | Una vez | 10% |
| Proyecto final | Sesiones 20-22 | 40% |

### Rúbrica del proyecto final

| Criterio | 4 - Excelente | 3 - Bien | 2 - Regular | 1 - Insuficiente |
|----------|--------------|---------|-------------|-----------------|
| **Diseño de BD** (20%) | 3+ tablas, relaciones correctas, sin redundancias | 3 tablas, relaciones mayormente correctas | 2 tablas o relaciones incorrectas | 1 tabla o diseño irreconocible |
| **Funcionalidad** (30%) | CRUD completo + 2 endpoints especiales, sin errores | CRUD completo + 1 endpoint especial | CRUD mayormente completo | CRUD muy incompleto |
| **Calidad del código** (20%) | Modelos Base/Create/Response, manejo de 404, `exclude_unset` | La mayoría de patrones bien aplicados | Código funcional pero sin patrones | Código que apenas funciona |
| **Documentación** (15%) | Tags + docstrings descriptivos + README | Tags + docstrings básicos | Solo tags | Sin documentación |
| **Presentación** (15%) | Demo fluida, explicación clara, reflexión profunda | Demo funciona, explicación aceptable | Demo con problemas, explicación confusa | Demo no funciona |

---

## 🧩 Diferenciación — Estudiantes con distintos ritmos

### Para estudiantes que van más rápido

Extensiones sugeridas para no aburrirlos:

**Durante el bloque SQL:**
- Investigar y enseñar a sus compañeros: índices (`CREATE INDEX`), vistas (`CREATE VIEW`)
- Optimización: comparar el rendimiento de consultas con y sin índices

**Durante el bloque SQLModel:**
- Implementar validaciones más complejas con `@validator`
- Explorar cómo SQLModel maneja migraciones de datos

**Durante el bloque FastAPI:**
- Agregar autenticación básica con API keys
- Implementar paginación real (offset + limit)
- Explorar el concepto de middleware

**Proyecto final:**
- Agregar un cliente Python simple que consuma la API
- Desplegar en Railway o Render (gratuito)

---

### Para estudiantes que van más lento

**En SQL:** Permite que usen la base de datos de práctica pre-construida sin tener que crearla ellos mismos. Enfócate en que entiendan SELECT + WHERE; las subconsultas son opcionales para este grupo.

**En SQLModel:** La transición desde sqlite3 puede ser confusa. Muéstrales explícitamente la equivalencia:

```python
# sqlite3 (ya lo conocen)
cursor.execute("INSERT INTO artista (nombre) VALUES (?)", ("Queen",))

# SQLModel (mismo resultado)
artista = Artista(nombre="Queen")
session.add(artista)
session.commit()
```

**En FastAPI:** Prioriza que entiendan GET y POST. PUT y DELETE pueden simplificarse o incluso omitirse en el proyecto si el tiempo es limitado.

---

## ❓ Preguntas frecuentes de los estudiantes

**"¿Por qué aprendemos SQLite si en producción se usa PostgreSQL?"**

> "SQLite y PostgreSQL usan el mismo lenguaje SQL, con diferencias menores. Todo lo que aprendes aquí funciona en PostgreSQL casi sin cambios. Usamos SQLite porque no requiere instalación de servidor, lo que nos permite enfocarnos en el SQL en sí. Cuando hagas tu primer trabajo real, el cambio a PostgreSQL será de 5 minutos."

**"¿Por qué no usamos MongoDB o una base de datos NoSQL?"**

> "Las bases de datos relacionales manejan la gran mayoría de aplicaciones del mundo (bancos, e-commerce, redes sociales). MongoDB y NoSQL son excelentes para casos específicos, pero si sabes SQL, tienes la herramienta que funciona para el 80% de los proyectos. Además, entender datos relacionales te ayuda a entender cualquier tipo de base de datos."

**"¿FastAPI es mejor que Django o Flask?"**

> "Son herramientas distintas para cosas distintas. Django incluye todo: autenticación, panel de administración, ORM propio. Flask es muy minimalista. FastAPI es moderno, muy rápido y tiene la mejor documentación automática. Para aprender cómo funciona una API, FastAPI es ideal porque el código es muy explícito y claro. Luego pueden aprender Django si quieren el paquete completo."

**"¿Cómo pongo mi API en internet para que la vean mis amigos?"**

> "Esa es la pregunta perfecta para el siguiente paso. El servicio gratuito más fácil para esto es Railway (railway.app) o Render (render.com). Ambos permiten desplegar aplicaciones FastAPI gratis en minutos con solo conectar tu cuenta de GitHub."

---

## 📌 Notas finales para el profesor

### Lo que más importa

Al final del curso, lo más valioso que los estudiantes se llevan no es saber la sintaxis de SQL ni los nombres de los métodos de SQLModel. Lo más valioso es que **piensan diferente sobre cómo se organiza la información**. Si un estudiante puede mirar una aplicación cualquiera (Spotify, Instagram, un sistema de notas del colegio) y razonar qué tablas tendría su base de datos, el curso fue un éxito.

### Lo que funciona menos de lo esperado

- Las lecturas largas del material. Los estudiantes de esta edad aprenden haciendo, no leyendo. Usa el material como referencia, no como guión.
- Los ejercicios que no tienen contexto real. "Crea una tabla con los campos X, Y, Z" funciona menos que "Imagina que eres el desarrollador de Spotify..."
- Avanzar cuando hay dudas sin resolver. Es mejor tomarse 5 minutos adicionales para aclarar un concepto que seguir dejando a la mitad del grupo atrás.

### Lo que funciona mejor de lo esperado

- La documentación automática de FastAPI. Siempre genera asombro y motivación.
- Los errores en tiempo real. Ver un DELETE sin WHERE borrar toda la tabla es más efectivo que cualquier advertencia verbal.
- La revisión entre pares en la sesión 21. Los estudiantes son sorprendentemente buenos dando retroalimentación útil cuando se les da estructura para hacerlo.
- Dejar que cada estudiante elija el tema de su proyecto. El nivel de motivación y detalle en los proyectos elegidos libremente es notablemente mayor.

---

*Guía del Profesor — Versión 1.0*
*Curso: De Cero a tu Primera API: SQL, SQLModel y FastAPI*
*Diseñada para docentes de programación, educación media técnica y bootcamps juveniles*
