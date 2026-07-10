# Capítulo 5: Declarative Base — el ADN de tus modelos

> Dejemos de usar SQL literal: aquí aprendés a definir tablas como clases.

Aquí es donde SQLAlchemy 2.0 brilla. Cada **clase** que escribás representa una **tabla** en la base de datos.

---

## 5.1 La nueva sintaxis (`DeclarativeBase`)

```python
from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    """Clase base de la cual heredarán todos nuestros modelos."""
    pass
```

Sí, está vacío. Esa es la idea: solo sirve como "marcador" para que SQLAlchemy sepa qué clases son modelos de base de datos.

> ⚠️ **No confundir** con la antigua función `declarative_base()`. Esa sintaxis vieja **aún funciona** en 2.0, pero se considera obsoleta.

### ¿Por qué `DeclarativeBase` y no `declarative_base()`?

| Aspecto | `declarative_base()` 🟠 | `DeclarativeBase` ✅ |
|---|---|---|
| Tipo de declaración | Función | Clase abstracta |
| Tipado mypy | 🟠 parcial | 🟢 perfecto |
| Herencia Python | 🟠 "mágica" | 🟢 explícita |
| Recomendación oficial | marcada como legacy | preferida |

> 🎓 **Analogía**: `DeclarativeBase` es como una **"raíz de la familia"** 🌳. Todas las clases que tengan el gen "modelo" son sus descendientes.

---

## 5.2 Tu primer modelo

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String

class Base(DeclarativeBase):
    pass

class Usuario(Base):
    __tablename__ = "usuarios"   # 👈 nombre de la tabla en SQL

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(50), unique=True)
```

Vamos a desgranar esto:

- `__tablename__ = "usuarios"` → define cómo se llamará la tabla en SQL.
- `id: Mapped[int] = mapped_column(primary_key=True)` → define una columna `INT PRIMARY KEY`.
- `nombre: Mapped[str] = mapped_column(String(50), unique=True)` → define una columna `VARCHAR(50) UNIQUE`.

---

## 5.3 Anatomía de un modelo

```python
class Producto(Base):
    __tablename__ = "productos"           # 👈 nombre de la tabla en SQL

    # 👇 las columnas de la tabla
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(100))
    sku: Mapped[str] = mapped_column(String(20), unique=True)
    precio: Mapped[float] = mapped_column(Numeric(10, 2))

    def __repr__(self):                    # 👈 opcional pero ÚTIL para debug
        return f"Producto(id={self.id}, nombre={self.nombre!r})"
```

### Partes de la clase

| Parte | Para qué sirve |
|---|---|
| `__tablename__` | Nombre real de la tabla en SQL. |
| Atributos con `Mapped[T]` y `mapped_column` | Las columnas de la tabla. |
| `__repr__` (opcional) | Cómo se imprime el objeto (útil en logs). |
| `__table_args__` | Configuración extra de la tabla (índices, constraints). |

### El superpoder del `__repr__`

```python
p = Producto(id=1, nombre="Cafetera", precio=8500.50, sku="CF-001")
print(p)
# → Producto(id=1, nombre='Cafetera', precio=8500.50)
```

Sin `__repr__`, imprimiría algo como `<Producto object at 0x7f1234>`. Con él, ves los datos.

> 💡 Si tu modelo es relativamente simple, podés ahorrarte el `__repr__` usando `@dataclass`:
>
> ```python
> from dataclasses import dataclass
>
> @dataclass
> class Producto(Base):
>     __tablename__ = "productos"
>     id: Mapped[int] = mapped_column(primary_key=True)
>     nombre: Mapped[str]
> ```

---

## 5.4 Tabla con nombre automático

Si no ponés `__tablename__`, SQLAlchemy genera uno **a partir del nombre de la clase**:

```python
class ProductoSinNombre(Base):
    # sin __tablename__
    id: Mapped[int] = mapped_column(primary_key=True)

# SQLAlchemy genera: __tablename__ = "producto_sin_nombre"
```

> 🎓 **Consejo**: **no dejes el nombre por defecto**. Es explícito, evita confusiones y te da control sobre el SQL generado.

---

## 5.5 `__table_args__`: restricciones a nivel de tabla

Algunas restricciones necesitan verse entre varias columnas. Para eso existe `__table_args__`:

```python
from sqlalchemy import UniqueConstraint, Index

class Empleado(Base):
    __tablename__ = "empleados"
    __table_args__ = (
        UniqueConstraint("nombre", "departamento", name="uq_empleado_dep"),
        Index("ix_empleado_salario", "salario"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    departamento: Mapped[str]
    salario: Mapped[float]
```

- `UniqueConstraint("a", "b")` → combinación `a + b` debe ser única.
- `Index("ix_...", "col")` → crea un índice (acelera búsquedas).

---

## 5.6 Convivencia: `Base` global vs `Base` por módulo

### Estilo 1 — `Base` global (recomendado para empezar)

```python
# src/database.py
class Base(DeclarativeBase):
    pass

# src/models.py
from src.database import Base

class Producto(Base):
    ...
```

✅ Simple y claro.

### Estilo 2 — Cada sistema con su propia `Base`

```python
class BaseAuth(DeclarativeBase):
    """Solo para el sistema de autenticación."""
    pass

class BaseEcommerce(DeclarativeBase):
    """Solo para el sistema de tienda."""
    pass

class Usuario(BaseAuth):
    ...

class Producto(BaseEcommerce):
    ...
```

✅ Útil en proyectos grandes con módulos bien separados (cada sistema puede usar `Base.metadata.create_all()` independiente).

> 💡 En la mayoría de los casos, **un solo `Base`** es suficiente.

---

## 🛠️ Ejercicios prácticos

### 🟢 Ejercicio 5.1: Tu primer modelo

Definí un modelo `Cliente` para una base de datos de e-commerce:

- Tabla: `"clientes"`.
- Columnas: `id` (PK), `email` (VARCHAR(120), único), `nombre` (VARCHAR(80)), `fecha_registro` (server_default `NOW()`).

**Restricción**: usá `class Base(DeclarativeBase)` y la sintaxis moderna `Mapped[T]`.

**Solución**: [soluciones/05-declarative-base.md](../soluciones/05-declarative-base.md#ejercicio-51)

---

### 🟢 Ejercicio 5.2: `__repr__` útil

Agregá un `__repr__` al modelo `Cliente` del ejercicio anterior que muestre `id`, `email` y `nombre`.

Verificá que `print(cliente)` muestre algo legible, no `<Cliente object at 0x...>`.

**Solución**: [soluciones/05-declarative-base.md](../soluciones/05-declarative-base.md#ejercicio-52)

---

### 🟡 Ejercicio 5.3: `__table_args__` con índice único compuesto

Modelá una tabla `Matriculacion(estudiante_id, curso_id, fecha)`. Ningún estudiante debería estar matriculado dos veces en el mismo curso.

Ayudita: `Mapped[tuple[int, int]]` no existe. Vas a tener que usar `__table_args__` con `UniqueConstraint`.

**Solución**: [soluciones/05-declarative-base.md](../soluciones/05-declarative-base.md#ejercicio-53)

---

### 🟡 Ejercicio 5.4: Diagnóstico

Este modelo tiene **dos** errores que impedirán que SQLAlchemy lo reconozca. Encontrá ambos:

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String

class Base(DeclarativeBase):
    pass

class Libro():
    __tablename__ = "libros"
    id: Mapped[int] = mapped_column(primary_key=True)
    titulo: Mapped[str] = mapped_column(String(200))
    isbn: Mapped[str] = mapped_column(String(13), unique=True)
```

**Solución**: [soluciones/05-declarative-base.md](../soluciones/05-declarative-base.md#ejercicio-54)

---

### 🔴 Ejercicio 5.5: Múltiples `Base`

En un proyecto con dos dominios separados (Auth + Biblioteca), creá dos `Base` distintas y un modelo en cada una. Pensá y respondé:

1. ¿Cómo evitarías que `Base.metadata.create_all()` de un dominio toque las tablas del otro?
2. ¿Tiene sentido tener múltiples `Base` para una app monolítica?

**Solución**: [soluciones/05-declarative-base.md](../soluciones/05-declarative-base.md#ejercicio-55)

---

## 🎓 Lo que aprendiste

- `class Base(DeclarativeBase)` es el ADN de tus modelos.
- `__tablename__` define el nombre de la tabla en SQL.
- Los atributos con `Mapped[T]` y `mapped_column(...)` son las columnas.
- `__repr__` sirve para debug.
- `__table_args__` permite restricciones a nivel de tabla.

## 📖 Siguiente

[Capítulo 6: Anotaciones `Mapped[T]` →](./06-anotaciones-mapped.md)
