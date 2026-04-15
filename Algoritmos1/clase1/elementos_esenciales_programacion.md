# Elementos Esenciales de un Lenguaje de Programación

**Duración estimada:** 2 horas de estudio efectivo
**Nivel:** Fundamentos de Programación

---

## Tabla de Contenidos

1. [Elementos Esenciales de un Lenguaje](#1-elementos-esenciales-de-un-lenguaje)
2. [Tipos de Variables](#2-tipos-de-variables)
3. [Operadores](#3-operadores)
4. [Estructuras de Control](#4-estructuras-de-control)
5. [Actividad 1: Ejercicios Básicos en Consola](#5-actividad-1-ejercicios-básicos-en-consola)
6. [Actividad 2: Taller de Identificación y Clasificación de Variables](#6-actividad-2-taller-de-identificación-y-clasificación-de-variables)
7. [Actividad 3: Conversatorio "¿Cómo piensa un programa?"](#7-actividad-3-conversatorio-cómo-piensa-un-programa)
8. [Resumen y Reflexión Final](#8-resumen-y-reflexión-final)

---

## 1. Elementos Esenciales de un Lenguaje

Todo lenguaje de programación, independientemente de su sintaxis, comparte cinco componentes fundamentales:

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
// C# moderno (.NET 10+) - Top-level statements
string Saludar(string nombre) => $"Hola, {nombre}! Bienvenido.";

string mensaje = Saludar("Carlos");
Console.WriteLine(mensaje);
```

### 1.5 Estructuras de Datos

Formas de organizar y almacenar múltiples valores.

```python
# Python con tipos explícitos
from typing import List, Dict

notas: List[int] = [85, 90, 78, 92]                        # Lista
estudiante: Dict[str, int] = {"nombre": 17, "edad": 17}   # Diccionario
```

```csharp
// C# moderno (.NET 10+) - Inferencia de tipos con List
List<int> notas = [85, 90, 78, 92];
Dictionary<string, int> estudiante = ["nombre", 17];
```

---

## 2. Tipos de Variables

### 2.1 Comparación Directa: Python vs C#

| Concepto | Python (con type hints) | C# (moderno .NET 10+) |
|---------|--------|-----|
| Entero | `int` | `int` |
| Decimal | `float` | `float`, `double` |
| Texto | `str` | `string` |
| Booleano | `bool` | `bool` |
| Sin valor | `None` | `null` |

### 2.2 Características Distintivas

#### Python (Tipado Dinámico)

```python
# Python con type hints (anotaciones de tipo)
# El tipo se declara como sugerencia, no como restricción absoluta
x: int = 10        # Se declara tipo int
x = "texto"        # Permite reasignar a otro tipo (tipado dinámico)
x = 3.14           # Permite reasignar a float
```

**Ventaja:** Flexibilidad con o sin type hints, escritura rápida.
**Desventaja:** Errores solo se detectan en ejecución (sin herramienta de análisis estático).

#### C# (Tipado Estático + Inferencia)

```csharp
// C# moderno (.NET 10+) - Inferencia con var
var x = 10;              // Infiere int
var texto = "hola";      // Infiere string
double precio = 19.99;   // Tipo explícito para decimales
```

**Ventaja:** Errores detectados en compilación, mejor rendimiento.
**Desventaja:** Más código requerido (mitigado con `var`).

### 2.3 Tabla Comparativa de Tipos Primitivos

| Tipo | Python | C# (moderno) | Ejemplo Python | Ejemplo C# |
|------|--------|---------------|----------------|------------|
| Entero | `int` | `int` | `x: int = 42` | `var x = 42` |
| Decimal | `float` | `float`, `double` | `x: float = 3.14` | `var x = 3.14` |
| Texto | `str` | `string` | `x: str = "Hola"` | `var x = "Hola"` |
| Booleano | `bool` | `bool` | `x: bool = True` | `var x = true` |
| Carácter | No existe | `char` | N/A | `var x = 'A'` |

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

// C# moderno: target-typed new()
var estudiante = new Dictionary<string, int>
{
    ["nombre"] = 17,
    ["edad"] = 16
};
```

---

## 3. Operadores

### 3.1 Operadores Aritméticos

| Operador | Descripción | Python | C# (moderno) |
|----------|-------------|--------|---------------|
| `+` | Suma | `5 + 3 → 8` | `5 + 3 → 8` |
| `-` | Resta | `5 - 3 → 2` | `5 - 3 → 2` |
| `*` | Multiplicación | `5 * 3 → 15` | `5 * 3 → 15` |
| `/` | División | `5 / 3 → 1.666...` | `5 / 3 → 1` (int) o `1.666...` (float) |
| `%` | Módulo (resto) | `5 % 3 → 2` | `5 % 3 → 2` |
| `**` | Potencia | `5 ** 3 → 125` | `Math.Pow(5, 3)` |
| `//` | División entera | `5 // 3 → 1` | `5 / 3` (int) |

**Diferencia importante en división:**

```python
# Python 3: La división SIEMPRE retorna float
resultado: float = 10 / 3  # 3.3333333333333335
resultado_entero: int = 10 // 3 # 3 (división entera)
```

```csharp
// C# moderno (.NET 10+): Depende del tipo de los operandos
double resultado1 = 10.0 / 3;  // 3.333...
int resultado2 = 10 / 3;       // 3 (trunca el decimal)
```

### 3.2 Operadores de Comparación

| Operador | Descripción | Python | C# (moderno) |
|----------|-------------|--------|---------------|
| `==` | Igual a | `5 == 5` → `True` | `5 == 5` → `true` |
| `!=` | Diferente de | `5 != 3` → `True` | `5 != 3` → `true` |
| `>` | Mayor que | `5 > 3` → `True` | `5 > 3` → `true` |
| `<` | Menor que | `5 < 3` → `False` | `5 < 3` → `false` |
| `>=` | Mayor o igual | `5 >= 5` → `True` | `5 >= 5` → `true` |
| `<=` | Menor o igual | `5 <= 3` → `False` | `5 <= 3` → `false` |

### 3.3 Operadores Lógicos

| Operador | Descripción | Python | C# (moderno) |
|----------|-------------|--------|---------------|
| `and` | Y lógico | `True and False` → `False` | `true && false` → `false` |
| `or` | O lógico | `True or False` → `True` | `true \|\| false` → `true` |
| `not` | Negación | `not True` → `False` | `!true` → `false` |

```python
# Python con tipos explícitos
edad: int = 20
tiene_identificacion: bool = True

if edad >= 18 and tiene_identificacion:
    print("Puede votar")
```

```csharp
// C# moderno (.NET 10+)
int edad = 20;
bool tieneIdentificacion = true;

if (edad >= 18 && tieneIdentificacion)
    Console.WriteLine("Puede votar");
```

| Operador | Descripción | Python | C# (moderno) |
|----------|-------------|--------|---------------|
| `=` | Asignación simple | `x = 5` | `x = 5;` |
| `+=` | Suma y asigna | `x += 3` | `x += 3;` |
| `-=` | Resta y asigna | `x -= 3` | `x -= 3;` |
| `*=` | Multiplica y asigna | `x *= 3` | `x *= 3;` |
| `/=` | Divide y asigna | `x /= 3` | `x /= 3;` |

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

#### Switch Expression (C#) / Match (Python 3.10+)

```python
# Python 3.10+ con tipos explícitos
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
// C# moderno (.NET 10+) - Switch expression
string dia = "lunes";

string mensaje = dia switch
{
    "lunes" => "Inicio de semana",
    "viernes" => "¡Por fin viernes!",
    _ => "Otro día"
};

Console.WriteLine(mensaje);
```

### 4.2 Estructuras Iterativas

#### For Loop

```python
# Python con tipos explícitos - Iterar sobre una secuencia
from typing import List

frutas: List[str] = ["manzana", "pera", "mango"]

for fruta in frutas:
    print(f"Me gusta la {fruta}")

# range() genera una secuencia
for i in range(5):  # 0, 1, 2, 3, 4
    print(i)

for i in range(1, 6):  # 1, 2, 3, 4, 5
    print(i)
```

```csharp
// C# moderno (.NET 10+) - Colecciones e inferencia
List<string> frutas = ["manzana", "pera", "mango"];

foreach (var fruta in frutas)
    Console.WriteLine($"Me gusta la {fruta}");

for (int i = 0; i < 5; i++)
    Console.WriteLine(i);
```

#### While Loop

```python
# Python con tipos explícitos
contador: int = 0

while contador < 5:
    print(f"Contador: {contador}")
    contador += 1
```

```csharp
// C# moderno (.NET 10+)
int contador = 0;

while (contador < 5)
{
    Console.WriteLine($"Contador: {contador}");
    contador++;
}
```

### 4.3 Comparación Visual de Estructuras

```
                    ┌─────────────┐
                    │   INICIO    │
                    └──────┬──────┘
                           │
                    ┌──────▼──────┐
                    │ ¿Condición? │
                    └──────┬──────┘
                           │
              ┌────────────┼────────────┐
              │ SÍ                      │ NO
       ┌──────▼──────┐          ┌──────▼──────┐
       │  Ejecutar   │          │   Continuar  │
       │   bloque    │          │    flujo     │
       └──────┬──────┘          └──────────────┘
              │
       ┌──────▼──────┐
       │ ¿Condición? │──→ (vuelve a evaluar)
       └─────────────┘
```

---

## 5. Actividad 1: Ejercicios Básicos en Consola

### Ejercicio 1.1: Hola Mundo

**Objetivo:** Verificar que el entorno de desarrollo está configurado correctamente.

**Python:**
```python
print("¡Hola, Mundo!")
```

**C#:**
```csharp
// C# moderno (.NET 10+) - Top-level statement
Console.WriteLine("¡Hola, Mundo!");
```

**Prueba:** Ejecuta ambos programas. Deberías ver el mensaje en la consola.

---

### Ejercicio 1.2: Solicitar Datos y Mostrar Resultados

**Objetivo:** Practicar entrada y salida de datos.

**Python:**
```python
# Python con tipos explícitos
# Solicitar el nombre del usuario
nombre: str = input("¿Cómo te llamas? ")

# Solicitar la edad
edad: int = int(input("¿Cuántos años tienes? "))

# Mostrar un mensaje personalizado
print(f"Hola {nombre}, tienes {edad} años.")
print(f"El próximo año tendrás {edad + 1} años.")
```

**C# (moderno .NET 10+):**
```csharp
// Top-level statements con inferencia
Console.Write("¿Cómo te llamas? ");
string nombre = Console.ReadLine();

Console.Write("¿Cuántos años tienes? ");
int edad = int.Parse(Console.ReadLine());

Console.WriteLine($"Hola {nombre}, tienes {edad} años.");
Console.WriteLine($"El próximo año tendrás {edad + 1} años.");
```

---

### Ejercicio 1.3: Calculadora Simple

**Objetivo:** Trabajar con operadores aritméticos y conversión de tipos.

**Python:**
```python
# Calculadora simple en Python con tipos explícitos
from typing import Union

print("=== CALCULADORA ===")

num1: float = float(input("Ingrese el primer número: "))
num2: float = float(input("Ingrese el segundo número: "))

suma: float = num1 + num2
resta: float = num1 - num2
multiplicacion: float = num1 * num2

# Manejar división por cero
division: Union[str, float]
modulo: Union[str, float]

if num2 != 0:
    division = num1 / num2
    modulo = num1 % num2
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

**C# (moderno .NET 10+):**
```csharp
// Top-level statements - Calculadora
Console.WriteLine("=== CALCULADORA ===");

Console.Write("Ingrese el primer número: ");
double num1 = double.Parse(Console.ReadLine());

Console.Write("Ingrese el segundo número: ");
double num2 = double.Parse(Console.ReadLine());

double suma = num1 + num2;
double resta = num1 - num2;
double multiplicacion = num1 * num2;

string division = num2 != 0 ? (num1 / num2).ToString() : "No definida";
double modulo = num2 != 0 ? num1 % num2 : 0;

Console.WriteLine($"\nResultados:");
Console.WriteLine($"{num1} + {num2} = {suma}");
Console.WriteLine($"{num1} - {num2} = {resta}");
Console.WriteLine($"{num1} * {num2} = {multiplicacion}");
Console.WriteLine($"{num1} / {num2} = {division}");
Console.WriteLine($"{num1} % {num2} = {modulo}");
```

---

### Ejercicio 1.4: Clasificador de Número

**Objetivo:** Practicar estructuras condicionales.

**Python:**
```python
# Clasificador de número con tipos explícitos

numero: int = int(input("Ingrese un número: "))

if numero > 0:
    print("El número es POSITIVO")
elif numero < 0:
    print("El número es NEGATIVO")
else:
    print("El número es CERO")

# Clasificar si es par o impar
if numero % 2 == 0:
    print("El número es PAR")
else:
    print("El número es IMPAR")

# Clasificar si está en ciertos rangos
if 1 <= numero <= 100:
    print("El número está entre 1 y 100")
```

**C# (moderno .NET 10+):**
```csharp
// Top-level statements - Clasificador de número
Console.Write("Ingrese un número: ");
int numero = int.Parse(Console.ReadLine());

if (numero > 0)
    Console.WriteLine("El número es POSITIVO");
else if (numero < 0)
    Console.WriteLine("El número es NEGATIVO");
else
    Console.WriteLine("El número es CERO");

if (numero % 2 == 0)
    Console.WriteLine("El número es PAR");
else
    Console.WriteLine("El número es IMPAR");

if (numero >= 1 && numero <= 100)
    Console.WriteLine("El número está entre 1 y 100");
```

---

### Ejercicio 1.5: Tabla de Multiplicar

**Objetivo:** Practicar ciclos y acumuladores.

**Python:**
```python
# Tabla de multiplicar con tipos explícitos

numero: int = int(input("¿Qué tabla desea ver? "))
hasta: int = int(input("¿Hasta qué número? "))

print(f"\n=== TABLA DEL {numero} ===")

for i in range(1, hasta + 1):
    resultado: int = numero * i
    print(f"{numero} x {i} = {resultado}")
```

**C# (moderno .NET 10+):**
```csharp
// Top-level statements - Tabla de multiplicar
Console.Write("¿Qué tabla desea ver? ");
int numero = int.Parse(Console.ReadLine());

Console.Write("¿Hasta qué número? ");
int hasta = int.Parse(Console.ReadLine());

Console.WriteLine($"\n=== TABLA DEL {numero} ===");

for (int i = 1; i <= hasta; i++)
{
    int resultado = numero * i;
    Console.WriteLine($"{numero} x {i} = {resultado}");
}
```

---

## 6. Actividad 2: Taller de Identificación y Clasificación de Variables

### Instrucciones

A continuación se presentan fragmentos de código con variables. Para cada uno:

1. Identifique TODAS las variables declaradas
2. Clasifique cada variable por su **tipo de dato**
3. Clasifique cada variable por su **alcance** (local, global, parámetro)
4. Identifique si hay **errores de tipo** o conversiones necesarias

---

### Ejercicio 2.1: Análisis de Código

**Código a analizar:**

```python
# Sistema de registro de estudiantes con tipos explícitos
from typing import List, Tuple

def calcular_promedio(nombre: str, notas: List[int]) -> Tuple[str, float, str]:
    suma: int = 0
    for nota in notas:
        suma = suma + nota
    promedio: float = suma / len(notas)

    estado: str
    if promedio >= 70:
        estado = "Aprobado"
    else:
        estado = "Reprobado"

    return nombre, promedio, estado

# Programa principal
estudiante: str = input("Nombre del estudiante: ")
calificaciones: List[int] = [85, 90, 78]

nombre: str
promedio: float
estado: str
nombre, promedio, estado = calcular_promedio(estudiante, calificaciones)
print(f"{nombre}: promedio {promedio:.2f} - {estado}")
```

**Hoja de respuestas:**

| Variable | Tipo de Dato | Alcance | Observaciones |
|----------|--------------|---------|---------------|
| `nombre` (parámetro) | str | Parámetro | |
| `notas` | list | Local | Contiene enteros |
| `suma` | int/float | Local | Acumulador |
| `nota` | int | Local | Iterador del for |
| `promedio` | float | Local | Resultado de división |
| `estado` | str | Local | Texto condicional |
| `estudiante` | str | Global | Input del usuario |
| `calificaciones` | list | Global | Lista de enteros |

---

### Ejercicio 2.2: Código en C# Moderno (.NET 10+) a Analizar

```csharp
// C# moderno (.NET 10+) - Programa de cálculos
// No requiere clase Program ni Main() - Top-level statements
// Implicit usings incluye System por defecto

double precioUnitario = 15000.0;
Console.Write("Ingrese la cantidad: ");
int cantidad = int.Parse(Console.ReadLine());
double descuento = 0.15;

double subtotal = precioUnitario * cantidad;
double montoDescuento = subtotal * descuento;
double total = subtotal - montoDescuento;

Console.WriteLine($"Subtotal: {subtotal:C}");
Console.WriteLine($"Descuento: {montoDescuento:C}");
Console.WriteLine($"Total a pagar: {total:C}");
```

**Hoja de respuestas:**

| Variable | Tipo de Dato | Alcance | Observaciones |
|----------|--------------|---------|---------------|
| `precioUnitario` | double | Top-level | Constante en el cálculo |
| `cantidad` | int | Top-level | Conversión de string a int |
| `descuento` | double | Top-level | Porcentaje como decimal |
| `subtotal` | double | Top-level | Resultado del cálculo |
| `montoDescuento` | double | Top-level | Cantidad descontada |
| `total` | double | Top-level | Resultado final |

---

### Ejercicio 2.3: Desafío - Encuentra los Errores

**Código con errores (Python):**

```python
# Código con errores (se muestra para análisis)
nombre: str = "Ana"
edad: int = 16
altura: float = 1.65
es_estudiante: str = "sí"
promedio: float = 85.5

# Error 1: incompatibilidad de tipos
if es_estudiante == sí:  # Error: 'sí' debería ser string "sí"
    print("Es estudiante")

# Error 2: operación entre tipos incompatibles
resultado = nombre + edad  # Error: no se puede sumar string + int

# Error 3: variable no definida
print(EstaVariableNoExiste)  # Error: falta definir o usar comillas

# Error 4: tipo incorrecto para operación
division = promedio // 2  # Funciona pero puede no ser la intención
```

**Solución:**

```python
# Código corregido con tipos explícitos
nombre: str = "Ana"
edad: int = 16
altura: float = 1.65
es_estudiante: str = "sí"  # Era string, está correcto
promedio: float = 85.5

# Corrección 1: usar string
if es_estudiante == "sí":
    print("Es estudiante")

# Corrección 2: convertir int a str
resultado: str = nombre + str(edad)  # "Ana16"

# Corrección 3: definir variable o usar string
print("EstaVariableNoExiste")

# Corrección 4: comentario sobre intención
division: float = promedio / 2  # 42.75 (float), no división entera
```

---

### Ejercicio 2.4: Clasificación Rápida

Clasifica cada variable según su tipo:

```python
a) temperatura: float = 36.5
b) letra: str = 'A'
c) cantidad_hijos: int = 3
d) nombre_producto: str = "Cuaderno"
e) esta_activo: bool = True
f) poblacion: int = 7800000000
g) precio: float = 29.99
h) es_mayor_de_edad: bool = False
```

**Solución:**

| Variable | Tipo Python | Tipo C# |
|----------|------------|---------|
| `temperatura` | float | double/float |
| `letra` | str | char |
| `cantidad_hijos` | int | int |
| `nombre_producto` | str | string |
| `esta_activo` | bool | bool |
| `poblacion` | int | long (por tamaño) |
| `precio` | float | double |
| `es_mayor_de_edad` | bool | bool |

---

## 7. Actividad 3: Conversatorio "¿Cómo piensa un programa?"

### Propósito

Este conversatorio busca desarrollar el **pensamiento computacional**: la forma de analizar y descomponer problemas para que una computadora pueda resolverlos.

### Duración: 25-30 minutos

---

### Parte A: Pensamiento Algorítmico (10 minutos)

**Pregunta detonadora:**
> "Si le dijeras a un extraterrestre cómo preparar un sandwich de jamón, ¿qué le dirías?"

**Discusión guiada:**

Un programa es como una receta:
1. **Ingredientes** = Datos/Variables
2. **Pasos de la receta** = Instrucciones/Algoritmo
3. **Decisiones** ("¿está frío el jamón?") = Estructuras condicionales
4. **Repetir** ("untar hasta que esté cubierto") = Ciclos

**Ejercicio mental:**
¿Qué sucedería si en la receta olvidamos decir "cortar el pan"? ¿Qué tipo de error es?

**Respuesta esperada:**
- Error de lógica (el programa compila pero no hace lo esperado)
- Error en tiempo de ejecución (el programa falla)
- Error silencioso (produce un resultado incorrecto)

---

### Parte B: Descomposición de Problemas (10 minutos)

**Escenario:**
> "Una profesora necesita calcular el promedio de su curso de 30 estudiantes. Cada estudiante tiene 3 notas. Necesita saber cuántos aprobaron y cuántos reprobaron."

**Descomposición paso a paso:**

```
PROBLEMA: Calcular promedio del curso y estadísticas de aprobación

SUBPROBLEMA 1: Ingresar las notas de un estudiante
   → Necesito un lugar para almacenar 3 notas → Lista/Array

SUBPROBLEMA 2: Calcular el promedio de un estudiante
   → Sumar las notas / cantidad de notas

SUBPROBLEMA 3: Determinar si aprobó o reprobó
   → Si promedio >= 70 → Aprobado, sino → Reprobado

SUBPROBLEMA 4: Repetir para los 30 estudiantes
   → Usar un ciclo que se ejecute 30 veces

SUBPROBLEMA 5: Contar aprobados y reprobados
   → Dos contadores que se incrementen según corresponda
```

**Código resultado (Python):**

```python
# Código con tipos explícitos para cálculo de promedio
contador_aprobados: int = 0
contador_reprobados: int = 0

for i in range(1, 4):  # Cambiar a 30 para el curso real
    print(f"\n--- Estudiante {i} ---")
    nota1: float = float(input("Nota 1: "))
    nota2: float = float(input("Nota 2: "))
    nota3: float = float(input("Nota 3: "))

    promedio: float = (nota1 + nota2 + nota3) / 3

    if promedio >= 70:
        print(f"Estudiante {i}: Aprobado ({promedio:.2f})")
        contador_aprobados += 1
    else:
        print(f"Estudiante {i}: Reprobado ({promedio:.2f})")
        contador_reprobados += 1

print(f"\n=== RESUMEN ===")
print(f"Aprobados: {contador_aprobados}")
print(f"Reprobados: {contador_reprobados}")
```

**Preguntas para reflexión:**

1. ¿Por qué inicializamos los contadores en 0?
2. ¿Qué sucedería si un estudiante tiene promedio de 69.9?
3. ¿Cómo cambiaría el código para que también diga el promedio general del curso?

---

### Parte C: Patrones y Abstracción (10 minutos)

**Pregunta central:**
> "En un juego de buscaminas, ¿cómo determinarías si el jugador perdió?"

**Identificación de patrones:**

```
PERDIÓ = jugador pisó una mina
      = hizo clic en una celda
      = esa celda contenía una mina
      = el tablero ya sabía dónde estaban las minas
```

**Abstracción:**
No necesitamos saber CÓMO se generó el tablero, solo que tiene información sobre dónde están las minas.

**Analogía con programación:**

```python
# Nivel de abstracción ALTO (simple)
tablero: List[List[str]] = [[" ", " ", "mina"], [" ", " ", " "], [" ", " ", " "]]
fila: int = 0
columna: int = 0

if tablero[fila][columna] == "mina":
    print("¡Perdiste!")

# Nivel de abstracción BAJO (complejo internamente)
# Incluye: generación aleatoria, validación de límites,
# actualización de celdas vecinas, conteo de minas adyacentes
```

**Ejercicio de reflexión:**
¿Qué otros ejemplos de la vida diaria tienen niveles de abstracción?

| Actividad | Abstracción alta | Abstracción baja |
|-----------|-----------------|------------------|
| Conducir | "Girar el volante" | Combustión, transmisión, hidráulica |
| Enviar mensaje | "Escribir y enviar" | Protocolos TCP/IP, señales eléctricas |
| Cocinar arroz | "Poner arroz en olla" | Temperatura de ebullición, tiempo absorción |

---

### Guía para el Facilitador

**Para iniciar la discusión:**
- "¿Alguien ha tenido que dar instrucciones muy detalladas a alguien?"
- "¿Qué pasó cuando faltó un paso?"

**Para profundizar:**
- "¿Cómo sabe un programa qué decisión tomar?"
- "¿Las computadoras realmente 'piensan'?"

**Para cerrar:**
- "¿Siguieron todos los pasos de manera secuencial?"
- "¿Hubo momentos donde tuvieron que 'decidir' algo?"

---

## 8. Resumen y Reflexión Final

### Conceptos Clave

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
| Declarar variables | `x: int = 10` (con hints) | `var x = 10` o `int x = 10` |
| Fin de instrucción | Nueva línea | Punto y coma `;` |
| Bloques de código | Indentación | Llaves `{}` o expresión single-line |
| Booleanos | `True`/`False` | `true`/`false` |
| Entrada por consola | `input()` | `Console.ReadLine()` |
| Salida por consola | `print()` | `Console.WriteLine()` |
| Type hints / Declaraciones | `def f(x: int) -> str:` | `string f(int x) => ...` |
| Estructura del programa | Código en cualquier orden | Top-level statements |
| Listas | `List[int] = [1, 2, 3]` | `List<int> = [1, 2, 3]` |

### Checklist de Aprendizaje

Antes de continuar, asegúrate de poder responder:

- [ ] ¿Qué es una variable y qué tipos de datos puede almacenar?
- [ ] ¿Cuál es la diferencia entre `=` y `==`?
- [ ] ¿Cuándo usarías un `if` en lugar de un `while`?
- [ ] ¿Qué significa que Python tenga tipado dinámico y cómo ayudan los type hints?
- [ ] ¿Qué diferencia hay entre el estilo tradicional de C# y el moderno de .NET 10+?
- [ ] ¿Cómo solicitarías datos al usuario en ambos lenguajes?

### Próximos Pasos Sugeridos

1. **Funciones:** Aprende a crear tus propios métodos para reutilizar código
2. **Estructuras de datos avanzadas:** Listas, diccionarios, conjuntos
3. **Manejo de archivos:** Leer y escribir información persistente
4. **Programación orientada a objetos:** Clases, objetos, herencia

---

**Material elaborado para estudio efectivo de 2 horas**
*Si completaste todas las actividades, ¡felicitaciones! Has dado tus primeros pasos en el mundo de la programación.*
