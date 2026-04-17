# Fundamentos de Programación — Guía Completa

**Duración total:** 3 horas 45 minutos (225 minutos)
**Nivel:** Fundamentos de Programación — 10º grado (15-16 años)

---

## Tabla de Contenidos

1. [Elementos Esenciales de un Lenguaje](#1-elementos-esenciales-de-un-lenguaje)
2. [Tipos de Variables](#2-tipos-de-variables)
3. [Operadores y Expresiones](#3-operadores-y-expresiones)
4. [Estructuras de Control](#4-estructuras-de-control)
5. [Actividades Prácticas](#5-actividades-prácticas)
6. [Evaluación Final](#6-evaluación-final)

---

## 1. Elementos Esenciales de un Lenguaje

Todo lenguaje de programación comparte cinco componentes fundamentales:

### 1.1 Variables y Tipos de Datos

Son contenedores que almacenan información en la memoria del computador.

```python
# Python con tipos explícitos
nombre: str = "María"        # String (texto)
edad: int = 16               # Integer (entero)
altura: float = 1.65         # Float (decimal)
es_estudiante: bool = True   # Boolean (booleano)
```

```csharp
// C# moderno (.NET 10+)
string nombre = "María";
int edad = 16;
double altura = 1.65;
bool esEstudiante = true;
```

### 1.2 Operadores

Símbolos que indican al computador qué operación realizar.

```
+   -   *   /   %     (aritméticos)
==  !=  >   <   >=  <= (comparación)
&&  ||  !              (lógicos)
=   +=  -=             (asignación)
```

### 1.3 Estructuras de Control

Mecanismos que permiten modificar el flujo de ejecución del programa.

- **Secuenciales:** Ejecutan instrucciones una después de otra
- **Selectivas (condicionales):** Permiten tomar decisiones (if, switch)
- **Iterativas:** Repiten bloques de código (for, while, do-while)

### 1.4 Funciones/Métodos

Bloques de código reutilizables que realizan una tarea específica.

```python
# Python con tipos explícitos
def saludar(nombre: str) -> str:
    return f"Hola, {nombre}! Bienvenido."

mensaje: str = saludar("Carlos")
print(mensaje)
```

```csharp
// C# moderno (.NET 10+)
string Saludar(string nombre) => $"Hola, {nombre}! Bienvenido.";
string mensaje = Saludar("Carlos");
Console.WriteLine(mensaje);
```

### 1.5 Estructuras de Datos

Formas de organizar y almacenar múltiples valores.

```python
# Python con tipos explícitos
from typing import List, Dict

notas: List[int] = [85, 90, 78, 92]
estudiante: Dict[str, int] = {"nombre": 17, "edad": 16}
```

```csharp
// C# moderno (.NET 10+)
List<int> notas = [85, 90, 78, 92];
Dictionary<string, int> estudiante = ["nombre", 17];
```

---

## 2. Tipos de Variables

### 2.1 Comparación Directa: Python vs C#

| Concepto | Python (type hints) | C# (moderno .NET 10+) |
|----------|---------------------|------------------------|
| Entero | `int` | `int` |
| Decimal | `float` | `float`, `double` |
| Texto | `str` | `string` |
| Booleano | `bool` | `bool` |
| Sin valor | `None` | `null` |

### 2.2 Características Distintivas

#### Python (Tipado Dinámico)

```python
x: int = 10        # Se declara tipo int
x = "texto"        # Permite reasignar a otro tipo
x = 3.14           # Permite reasignar a float
```

**Ventaja:** Flexibilidad con o sin type hints.
**Desventaja:** Errores solo se detectan en ejecución.

#### C# (Tipado Estático + Inferencia)

```csharp
var x = 10;              // Infiere int
var texto = "hola";      // Infiere string
double precio = 19.99;   // Tipo explícito para decimales
```

**Ventaja:** Errores detectados en compilación.
**Desventaja:** Más código requerido (mitigado con `var`).

### 2.3 Tabla Comparativa de Tipos Primitivos

| Tipo | Python | C# (moderno) | Ejemplo Python | Ejemplo C# |
|------|--------|---------------|----------------|------------|
| Entero | `int` | `int` | `x: int = 42` | `var x = 42` |
| Decimal | `float` | `float`, `double` | `x: float = 3.14` | `var x = 3.14` |
| Texto | `str` | `string` | `x: str = "Hola"` | `var x = "Hola"` |
| Booleano | `bool` | `bool` | `x: bool = True` | `var x = true` |

### 2.4 Conversión de Tipos (Casting)

```python
# Python con tipos explícitos
edad: int = int("25")        # str a int
precio: float = float("19.99") # str a float
texto: str = str(100)        # int a str
```

```csharp
// C# moderno (.NET 10+)
int edad = int.Parse("25");
double precio = double.Parse("19.99");
string texto = 100.ToString();

// Alternativa segura con TryParse
bool exitoso = int.TryParse("abc", out int resultado); // exitoso = false
```

---

## 3. Operadores y Expresiones

### 3.1 Operadores Aritméticos

| Operador | Descripción | Ejemplo | Resultado |
|----------|-------------|---------|-----------|
| `+` | Suma | `7 + 4` | `11` |
| `-` | Resta | `10 - 3` | `7` |
| `*` | Multiplicación | `6 * 5` | `30` |
| `/` | División | `15 / 4` | `3.75` |
| `%` | Módulo (resto) | `15 % 4` | `3` |
| `**` | Potenciación | `2 ** 5` | `32` |
| `//` | División entera | `5 // 3` | `1` |

**Diferencia importante en división:**

```python
# Python 3: La división SIEMPRE retorna float
resultado: float = 10 / 3  # 3.3333333333333335
resultado_entero: int = 10 // 3 # 3 (división entera)
```

```csharp
// C# moderno (.NET 10+)
double resultado1 = 10.0 / 3;  // 3.333...
int resultado2 = 10 / 3;       // 3 (trunca)
```

### 3.2 El operador de módulo (%) — Entendiéndolo profundamente

El módulo devuelve el **residuo** de una división entera.

```
Ejemplo visual:
15 ÷ 4 = 3 con residuo 3
         ↑
15 % 4 = 3
```

**¿Cuándo usamos el residuo en la vida real?**

- **Par o impar:** Si `numero % 2 == 0` → par
- **Reloj de 12 horas:** Las 13:00 son las 1:00 PM porque `13 % 12 = 1`
- **Ciclos repetitivos:** Cada 3 días hacer algo

### 3.3 Operadores de Comparación (Relacionales)

| Operador | Descripción | Ejemplo | Resultado |
|----------|-------------|---------|-----------|
| `==` | Igual a | `5 == 5` | `True` / `true` |
| `!=` | Diferente de | `5 != 3` | `True` / `true` |
| `>` | Mayor que | `5 > 3` | `True` / `true` |
| `<` | Menor que | `5 < 3` | `False` / `false` |
| `>=` | Mayor o igual | `5 >= 5` | `True` / `true` |
| `<=` | Menor o igual | `5 <= 3` | `False` / `false` |

> **Error clásico:** Confundir `=` (asignación) con `==` (comparación). `=` significa "guardar este valor", no "preguntar si son iguales".

### 3.4 Operadores Lógicos

| Operador | Nombre | Descripción | Python | C# |
|----------|--------|-------------|--------|-----|
| `and` / `&&` | Y | Ambas condiciones deben ser verdaderas | `True and False` → `False` | `true && false` → `false` |
| `or` / `\|\|` | O | Al menos una condición debe ser verdadera | `True or False` → `True` | `true \|\| false` → `true` |
| `not` / `!` | NO | Invierte el valor de verdad | `not True` → `False` | `!true` → `false` |

### 3.5 Tablas de Verdad

#### AND (Y) — Necesita TODAS verdaderas

| A | B | A AND B |
|---|---|---------|
| V | V | **V** |
| V | F | F |
| F | V | F |
| F | F | F |

#### OR (O) — Necesita AL MENOS una verdadera

| A | B | A OR B |
|---|---|---------|
| V | V | **V** |
| V | F | **V** |
| F | V | **V** |
| F | F | F |

#### NOT (NO) — Invierte el valor

| A | NOT A |
|---|-------|
| V | F |
| F | V |

### 3.6 Precedencia de Operadores

El orden de evaluación de las operaciones.

| Precedencia | Operadores | Descripción |
|-------------|------------|--------------|
| 1 (más alta) | `()` | Paréntesis |
| 2 | `**` | Potenciación |
| 3 | `*`, `/`, `%` | Multiplicación, División, Módulo |
| 4 | `+`, `-` | Suma y Resta |
| 5 | `>`, `<`, `>=`, `<=` | Relacionales |
| 6 | `==`, `!=` | Igual y Diferente |
| 7 | `NOT` | Negación lógica |
| 8 | `AND` | Conjunción |
| 9 (más baja) | `OR` | Disyunción |

**Regla mnemotécnica:** "Por favor, mi estimada maestra Rita" (Paréntesis, Potencia, Multiplicación, División, Adición, Sustracción... y así sucesivamente para cada nivel).

### 3.7 Resolución de Expresiones Complejas

#### Ejemplo 1: `3 + 4 * 2`

```
Paso 1: Multiplicación primero
        3 + (4 * 2) = 3 + 8

Paso 2: Suma
        11
```

#### Ejemplo 2: `(3 + 4) * 2`

```
Paso 1: Paréntesis primero
        (7) * 2 = 14

Resultado: 14
```

#### Ejemplo 3: `2 ** 3 + 12 / 3 - 1`

```
Paso 1: Potencias
        8 + 12 / 3 - 1

Paso 2: División
        8 + 4 - 1

Paso 3: Suma y resta
        11

Resultado: 11
```

#### Ejemplo 4: `10 > 5 && 3 + 2 == 5`

```
Paso 1: Aritméticos
        10 > 5 && 5 == 5

Paso 2: Comparaciones
        VERDADERO && VERDADERO

Paso 3: AND
        VERDADERO
```

---

## 4. Estructuras de Control

### 4.1 Estructuras Selectivas (Condicionales)

#### If - Else

```python
# Python con tipos explícitos
nota: int = int(input("Ingrese su nota: "))

if nota >= 90:
    print("Excelente")
elif nota >= 70:
    print("Aprobado")
else:
    print("Reprobado")
```

```csharp
// C# moderno (.NET 10+)
Console.Write("Ingrese su nota: ");
int nota = int.Parse(Console.ReadLine());

if (nota >= 90)
    Console.WriteLine("Excelente");
else if (nota >= 70)
    Console.WriteLine("Aprobado");
else
    Console.WriteLine("Reprobado");
```

#### Match (Python 3.10+) / Switch (C#)

```python
# Python 3.10+
dia: str = "lunes"

match dia:
    case "lunes":
        print("Inicio de semana")
    case "viernes":
        print("¡Por fin viernes!")
    case _:
        print("Otro día")
```

```csharp
// C# moderno (.NET 10+)
string dia = "lunes";

string mensaje = dia switch
{
    "lunes" => "Inicio de semana",
    "viernes" => "¡Por fin viernes!",
    _ => "Otro día"
};
```

### 4.2 Estructuras Iterativas

#### For Loop

```python
# Python - range() genera una secuencia
for i in range(1, 6):  # 1, 2, 3, 4, 5
    print(i)

frutas: list[str] = ["manzana", "pera", "mango"]
for fruta in frutas:
    print(f"Me gusta la {fruta}")
```

```csharp
// C# moderno (.NET 10+)
for (int i = 1; i <= 5; i++)
    Console.WriteLine(i);

List<string> frutas = ["manzana", "pera", "mango"];
foreach (var fruta in frutas)
    Console.WriteLine($"Me gusta la {fruta}");
```

#### While Loop

```python
# Python
contador: int = 0

while contador < 5:
    print(f"Contador: {contador}")
    contador += 1
```

```csharp
// C#
int contador = 0;

while (contador < 5)
{
    Console.WriteLine($"Contador: {contador}");
    contador++;
}
```

---

## 5. Actividades Prácticas

### Actividad 1: Calculadora Simple (20 min)

**Objetivo:** Practicar operadores aritméticos y entrada/salida.

```python
# Calculadora simple en Python
print("=== CALCULADORA ===")

num1: float = float(input("Ingrese el primer número: "))
num2: float = float(input("Ingrese el segundo número: "))

suma: float = num1 + num2
resta: float = num1 - num2
multiplicacion: float = num1 * num2

if num2 != 0:
    division: float = num1 / num2
    modulo: float = num1 % num2
else:
    division = "No definida"
    modulo = "No definido"

print(f"\nResultados:")
print(f"{num1} + {num2} = {suma}")
print(f"{num1} - {num2} = {resta}")
print(f"{num1} * {num2} = {multiplicacion}")
print(f"{num1} / {num2} = {division}")
print(f"{num1} % {num2} = {modulo}")
```

### Actividad 2: Clasificador de Número (15 min)

**Objetivo:** Practicar condicionales y operadores de comparación.

```python
numero: int = int(input("Ingrese un número: "))

if numero > 0:
    print("El número es POSITIVO")
elif numero < 0:
    print("El número es NEGATIVO")
else:
    print("El número es CERO")

if numero % 2 == 0:
    print("El número es PAR")
else:
    print("El número es IMPAR")
```

### Actividad 3: Tabla de Multiplicar (15 min)

**Objetivo:** Practicar ciclos y acumuladores.

```python
numero: int = int(input("¿Qué tabla desea ver? "))
hasta: int = int(input("¿Hasta qué número? "))

print(f"\n=== TABLA DEL {numero} ===")

for i in range(1, hasta + 1):
    resultado: int = numero * i
    print(f"{numero} x {i} = {resultado}")
```

### Actividad 4: Evaluación de Condiciones Lógicas (20 min)

**Para cada escenario, escribe la condición y evalúa si es VERDADERO o FALSO:**

```
ESCENARIO A: Acceso a fiesta
- Tienes invitación Y no has sido expulsado
- Eres miembro del comité OR eres estudiante de 10º

Carlos: invitación = SÍ, expulsado = NO, comité = SÍ, grado = 10º
Daniela: invitación = SÍ, expulsado = SÍ, comité = NO, grado = 11º

Condición: ________________________
Carlos: ___  Daniela: ___
```

```
ESCENARIO B: Préstamo de biblioteca
- No tienes multas O tienes autorización especial
- Eres usuario activo

Laura: multas = SÍ, autorización = SÍ, usuario activo = SÍ
Andrés: multas = NO, autorización = NO, usuario activo = SÍ

Condición: ________________________
Laura: ___  Andrés: ___
```

### Actividad 5: Resolución de Expresiones (15 min)

**Resuelve mostrando cada paso:**

```
EXPRESIÓN A: 5 + 3 * 2
Paso 1: _______________
Paso 2: _______________
Resultado: ___________
```

```
EXPRESIÓN B: (5 + 3) * 2
Paso 1: _______________
Paso 2: _______________
Resultado: ___________
```

```
EXPRESIÓN C: 2 ** 3 + 12 / 3 - 1
Paso 1: _______________
Paso 2: _______________
Paso 3: _______________
Resultado: ___________
```

```
EXPRESIÓN D: 8 > 3 + 5 && 10 / 2 == 5
Paso 1: _______________
Paso 2: _______________
Paso 3: _______________
Resultado: ___________
```

### Actividad 6: Sistema de Calificaciones (25 min)

**Implementa la siguiente lógica:**

```
REGLAS:
1. Para aprobar: asistencia >= 80% Y promedio >= 60
2. Honorífica: promedio >= 90 Y asistencia >= 95
3. Reprobado automático: promedio < 60 (sin importar asistencia)
4. Reprobado automático: asistencia < 60% (sin importar promedio)

EVALÚA:
- María: asistencia 85%, promedio 78
- Pedro: asistencia 97%, promedio 92
- Luisa: asistencia 55%, promedio 75
- Andrés: asistencia 88%, promedio 58
- Sofía: asistencia 72%, promedio 95
```

---

## 6. Evaluación Final

**Duración:** 30 minutos | **Puntaje total:** 100 puntos

---

### SECCIÓN A: Conocimiento Conceptual (20 puntos)

**PREGUNTA A1 (6 puntos):** Explique qué es un operador y cuál es la diferencia entre operadores aritméticos y relacionales. Proporcione un ejemplo de cada uno.

```
Respuesta:
___________________________________________________________________
___________________________________________________________________
___________________________________________________________________
```

**PREGUNTA A2 (7 puntos):** ¿Qué es la precedencia de operadores? Si no existiera, ¿cómo se evaluaría `8 + 4 * 2`? ¿Cómo se evalúa realmente?

```
Respuesta:
___________________________________________________________________
___________________________________________________________________
___________________________________________________________________
```

**PREGUNTA A3 (7 puntos):** ¿Cuándo usaría `&&` en lugar de `||`? Dé un ejemplo real donde cada uno sea la elección correcta.

```
Respuesta:
___________________________________________________________________
```

---

### SECCIÓN B: Resolución de Expresiones (30 puntos)

**PREGUNTA B1 (5 puntos):** Resuelva mostrando cada paso:

```
Expresión: 15 + 3 * 4 - 10 / 2

Paso 1: _______________
Paso 2: _______________
Paso 3: _______________
Resultado: ___________
```

**PREGUNTA B2 (5 puntos):** Resuelva mostrando cada paso:

```
Expresión: (20 - 5) * (3 + 2) / 5

Paso 1: _______________
Paso 2: _______________
Paso 3: _______________
Resultado: _______________
```

**PREGUNTA B3 (5 puntos):** Resuelva mostrando cada paso:

```
Expresión: 2 ** 3 + 7 % 3

Paso 1: _______________
Paso 2: _______________
Paso 3: _______________
Resultado: _______________
```

**PREGUNTA B4 (5 puntos):** Evalúe si es VERDADERO o FALSO:

```
Expresión: 10 > 5 && 3 + 2 != 5

Paso 1: _______________
Paso 2: _______________
Paso 3: _______________
Resultado: ___________
```

**PREGUNTA B5 (5 puntos):** Evalúe si es VERDADERO o FALSO:

```
Expresión: !(8 < 10) || 15 % 4 == 3

Paso 1: _______________
Paso 2: _______________
Paso 3: _______________
Paso 4: _______________
Resultado: ___________
```

**PREGUNTA B6 (5 puntos):** Evalúe si es VERDADERO o FALSO:

```
Expresión: (5 >= 5) && (10 / 2 == 5) || !(3 < 2)

Paso 1: _______________
Paso 2: _______________
Paso 3: _______________
Paso 4: _______________
Paso 5: _______________
Resultado: ___________
```

---

### SECCIÓN C: Construcción de Condiciones (25 puntos)

**PREGUNTA C1 (12 puntos):** Escriba la condición lógica para cada escenario:

```
ESCENARIO A: Un estudiante puede participar en torneo si:
- Promedio >= 4.0 Y no tiene sanciones

Condición: _____________________________________________


ESCENARIO B: Un cliente recibe descuento 20% si:
- Es miembro OR compra > $200.000
- NO es miembro nuevo (antigüedad > 1 año)

Condición: _____________________________________________


ESCENARIO C: Un video se muestra si:
- Usuario no lo ha visto Y NO es contenido "oculto"
- (Tiene > 1000 vistas OR es de creador preferido)

Condición: _____________________________________________
```

**PREGUNTA C2 (13 puntos):** Evalúe cada condición:

```
DATOS:
- edad = 17
- tiene_credencial = VERDADERO
- esta_en_lista = FALSO
- tiene_suscripcion = FALSO

Condición 1: edad > 16 && tiene_credencial
→ ¿VERDADERO o FALSO? _______

Condición 2: esta_en_lista || tiene_suscripcion
→ ¿VERDADERO o FALSO? _______

Condición 3: !esta_en_lista && (edad >= 16 || tiene_credencial)
→ ¿VERDADERO o FALSO? _______

Condición 4: tiene_credencial && !esta_en_lista && !tiene_suscripcion
→ ¿VERDADERO o FALSO? _______
```

---

### SECCIÓN D: Análisis de Escenarios (25 puntos)

**PREGUNTA D1 (25 puntos):** Evalúe cada estudiante según las reglas:

```
REGLAS:
1. Aprobar: asistencia >= 80% Y promedio >= 60
2. Honorífica: promedio >= 90 Y asistencia >= 95
3. Reprobado automático: promedio < 60
4. Reprobado automático: asistencia < 60%

ESTUDIANTE 1: María — Asistencia: 85%, Promedio: 78
¿Aprueba? ___ ¿Honorífica? ___ Estado: _______________

ESTUDIANTE 2: Pedro — Asistencia: 97%, Promedio: 92
¿Aprueba? ___ ¿Honorífica? ___ Estado: _______________

ESTUDIANTE 3: Luisa — Asistencia: 55%, Promedio: 75
¿Aprueba? ___ ¿Honorífica? ___ Estado: _______________

ESTUDIANTE 4: Andrés — Asistencia: 88%, Promedio: 58
¿Aprueba? ___ ¿Honorífica? ___ Estado: _______________

ESTUDIANTE 5: Sofía — Asistencia: 72%, Promedio: 95
¿Aprueba? ___ ¿Honorífica? ___ Estado: _______________
```

---

## Respuestas de la Evaluación (Para el docente)

**SECCIÓN B:**
- B1: 15 + 12 - 5 = 22
- B2: 15 * 5 / 5 = 15
- B3: 8 + 1 = 9
- B4: V && V = V (VERDADERO)
- B5: F || V = V (VERDADERO)
- B6: V && V || V = V (VERDADERO)

**SECCIÓN C:**
- C2:
  - Condición 1: V && V = V
  - Condición 2: F || F = F
  - Condición 3: V && (V || V) = V
  - Condición 4: V && V && V = V

**SECCIÓN D:**
- María: Aprueba, No Honorífica, Aprobado
- Pedro: Aprueba, Sí Honorífica, Honorífica
- Luisa: No Aprueba, No Honorífica, Reprobado por asistencia
- Andrés: No Aprueba, No Honorífica, Reprobado por promedio
- Sofía: No Aprueba, No Honorífica, Reprobado por asistencia

---

## Resumen de Conceptos Clave

| Concepto | Definición | Ejemplo |
|----------|------------|---------|
| Variable | Espacio de memoria con nombre y tipo | `edad: int = 16` |
| Tipo de dato | Categoría del valor almacenado | int, str, bool |
| Operador | Símbolo para operaciones | `+`, `-`, `==` |
| Condicional | Bifurcación según condición | `if-else` |
| Ciclo | Repetición de un bloque | `for`, `while` |
| Función | Bloque de código reutilizable | `def saludar() -> str:` |

### Diferencias Fundamentales: Python vs C#

| Aspecto | Python | C# (moderno .NET 10+) |
|---------|--------|------------------------|
| Tipado | Dinámico (con hints opcionales) | Estático con inferencia |
| Booleanos | `True`/`False` | `true`/`false` |
| Entrada | `input()` | `Console.ReadLine()` |
| Salida | `print()` | `Console.WriteLine()` |
| Listas | `List[int] = [1, 2, 3]` | `List<int> = [1, 2, 3]` |

---

## Distribución del Tiempo

| Actividad | Tiempo |
|-----------|--------|
| Sesión 1: Elementos esenciales + Variables | 45 min |
| Sesión 2: Operadores aritméticos y relacionales | 40 min |
| Sesión 3: Operadores lógicos + Precedencia | 45 min |
| Sesión 4: Estructuras de control + Actividades | 45 min |
| Evaluación Final | 30 min |
| **Total** | **225 min (3h 45min)** |

---

*Material elaborado para uso educativo*
*Fundamentos de Programación — 10º grado*
*Contenido combinado: Elementos Esenciales + Operadores y Expresiones*