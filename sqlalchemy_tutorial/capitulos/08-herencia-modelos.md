# Capítulo 8: Herencia de modelos — tres estrategias distintas

> Una sola jerarquía Python, **tres formas distintas** de materializarla en SQL. La elección depende de tu modelo de negocio.

---

## 8.1 ¿Qué es la herencia de modelos?

Es un mecanismo que te permite definir una **clase padre** con campos comunes y **clases hijas** que extienden esa estructura.

> 🎓 **Analogía**: pensá en una jerarquía de vehículos. **Vehículo** es el padre (ruedas, motor). **Auto** y **Moto** heredan de él pero cada uno agrega sus particularidades.

### ¿Cómo se materializa esa jerarquía en SQL?

Ahí es donde SQLAlchemy 2.0 ofrece **tres estrategias**, cada una con trade-offs diferentes:

| Estrategia | Tablas SQL | Polimorfismo |
|---|---|---|
| **Joined Table Inheritance** | Una tabla por clase (padre e hijas) | ✅ Sí |
| **Single Table Inheritance** | Una sola tabla para todos | ✅ Sí |
| **Concrete Table Inheritance** | Una tabla por clase hija (no hay tabla padre) | ❌ No |

> 💡 **¿Cuándo usar cada una?** Lo vemos en detalle más abajo.

---

## 8.2 Joined Table Inheritance (la más común)

### Idea

- Una tabla por cada clase de la jerarquía.
- Las tablas hijas tienen una FK hacia la tabla padre.
- Permite queries **polimórficas** (`SELECT * FROM vehiculo` trae autos + motos).

### Implementación

```python
from sqlalchemy import ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship

class Base(DeclarativeBase):
    pass


class Vehiculo(Base):
    """Clase padre."""
    __tablename__ = "vehiculos"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    marca: Mapped[str]
    modelo: Mapped[str]

    # 👈 discriminador: qué tipo de vehículo es cada fila
    __mapper_args__ = {
        "polymorphic_identity": "vehiculo",
        "polymorphic_on": "tipo",
    }
    
    # Columna extra para distinguir el tipo en la misma tabla
    tipo: Mapped[str] = mapped_column(String(50))


class Auto(Vehiculo):
    """Clase hija."""
    __tablename__ = "autos"
    
    id: Mapped[int] = mapped_column(ForeignKey("vehiculos.id"), primary_key=True)
    cantidad_puertas: Mapped[int]
    tiene_aire: Mapped[bool]
    
    __mapper_args__ = {
        "polymorphic_identity": "auto",
    }


class Moto(Vehiculo):
    """Otra hija."""
    __tablename__ = "motos"
    
    id: Mapped[int] = mapped_column(ForeignKey("vehiculos.id"), primary_key=True)
    cilindrada: Mapped[int]
    
    __mapper_args__ = {
        "polymorphic_identity": "moto",
    }
```

### SQL generado

```sql
CREATE TABLE vehiculos (
    id INTEGER NOT NULL PRIMARY KEY,
    marca VARCHAR NOT NULL,
    modelo VARCHAR NOT NULL,
    tipo VARCHAR(50) NOT NULL
);

CREATE TABLE autos (
    id INTEGER NOT NULL PRIMARY KEY,
    cantidad_puertas INTEGER NOT NULL,
    tiene_aire BOOLEAN NOT NULL,
    FOREIGN KEY(id) REFERENCES vehiculos(id)
);

CREATE TABLE motos (
    id INTEGER NOT NULL PRIMARY KEY,
    cilindrada INTEGER NOT NULL,
    FOREIGN KEY(id) REFERENCES vehiculos(id)
);
```

### Uso

```python
with Session(engine) as session:
    auto = Auto(marca="Toyota", modelo="Corolla", cantidad_puertas=4, tiene_aire=True)
    moto = Moto(marca="Honda", modelo="CBR", cilindrada=600)
    
    session.add_all([auto, moto])
    session.commit()

    # Query polimórfica: devuelve objetos Auto y Moto
    vehiculos = session.scalars(select(Vehiculo)).all()
    for v in vehiculos:
        print(type(v).__name__, v.marca)  # Auto Toyota / Moto Honda

    # Query específica
    autos = session.scalars(select(Auto)).all()
```

### ✅ Ventajas y ❌ Desventajas

| Ventajas ✅ | Desventajas ❌ |
|---|---|
| Modelo normalizado, sin nulos innecesarios | JOIN automático en cada query polimórfica |
| Integridad referencial clara | Más tablas en la base |
| Queries SQL claras por clase | Poco performante con jerarquías profundas |

> 🎓 **Cuándo usarla**: cuando necesitás **normalización** (evitar columnas con muchos NULL) y consultás **mezcla de tipos** seguido.

---

## 8.3 Single Table Inheritance (la más performante)

### Idea

- Una **sola tabla** para toda la jerarquía.
- Una columna "tipo" discrimina qué clase es cada fila.
- Las columnas de los hijos quedan en la tabla padre y admiten NULL si no corresponden.

### Implementación

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String

class Base(DeclarativeBase):
    pass


class Empleado(Base):
    """Una sola tabla."""
    __tablename__ = "empleados"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str]
    salario: Mapped[float]
    
    # Columnas específicas de cada hijo (nullable)
    horas_extras: Mapped[int | None] = mapped_column(default=None)
    comision: Mapped[float | None] = mapped_column(default=None)
    
    __mapper_args__ = {
        "polymorphic_identity": "empleado",
        "polymorphic_on": "tipo_discriminador",
    }
    
    tipo_discriminador: Mapped[str] = mapped_column(String(20))


class EmpleadoPlanta(Empleado):
    """Horas extras, salario fijo."""
    __mapper_args__ = {"polymorphic_identity": "planta"}
    
    def __init__(self, **kwargs):
        kwargs.setdefault("horas_extras", 0)
        super().__init__(**kwargs)


class EmpleadoComision(Empleado):
    """Comisión por ventas."""
    __mapper_args__ = {"polymorphic_identity": "comision"}
    
    def __init__(self, **kwargs):
        kwargs.setdefault("comision", 0.0)
        super().__init__(**kwargs)
```

### SQL generado

```sql
CREATE TABLE empleados (
    id INTEGER NOT NULL PRIMARY KEY,
    nombre VARCHAR NOT NULL,
    salario FLOAT NOT NULL,
    horas_extras INTEGER,
    comision FLOAT,
    tipo_discriminador VARCHAR(20) NOT NULL
);
```

### ✅ Ventajas y ❌ Desventajas

| Ventajas ✅ | Desventajas ❌ |
|---|---|
| **Muy performante**: sin JOIN | Muchas columnas nullable |
| Polimorfismo nativo | Menos normalizado |
| Schema simple | Restricciones CHECK no se aplican |

> 🎓 **Cuándo usarla**: cuando consultás **mezcla de tipos seguido** (la query es un solo SELECT). Es lo más rápido.

> ⚠️ **Con PostgreSQL**: podés agregar CHECK constraints para reforzar que `horas_extras` solo exista para `planta` y `comision` para `comision`. Esto se hace en `__table_args__`.

---

## 8.4 Concrete Table Inheritance (cada hijo es independiente)

### Idea

- Cada clase hija tiene **su propia tabla completa**, sin FK al padre.
- La clase padre **no** se mapea a una tabla.
- **No hay polimorfismo** (no podés hacer `SELECT * FROM vehiculo`).

### Implementación

```python
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String


class Base(DeclarativeBase):
    pass


# 👇 clase abstracta (no es tabla, no es heredable por SQLAlchemy)
from sqlalchemy.orm import AbstractConcreteBase


class Vehiculo(AbstractConcreteBase, Base):
    """Sin tabla propia. Sirve solo para compartir estructura."""
    
    marca: Mapped[str]
    modelo: Mapped[str]


class Auto(Vehiculo):
    __tablename__ = "autos_concretos"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    marca: Mapped[str]
    modelo: Mapped[str]
    cantidad_puertas: Mapped[int]


class Moto(Vehiculo):
    __tablename__ = "motos_concretas"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    marca: Mapped[str]
    modelo: Mapped[str]
    cilindrada: Mapped[int]
```

### SQL generado

```sql
CREATE TABLE autos_concretos (
    id INTEGER NOT NULL PRIMARY KEY,
    marca VARCHAR NOT NULL,
    modelo VARCHAR NOT NULL,
    cantidad_puertas INTEGER NOT NULL
);

CREATE TABLE motos_concretas (
    id INTEGER NOT NULL PRIMARY KEY,
    marca VARCHAR NOT NULL,
    modelo VARCHAR NOT NULL,
    cilindrada INTEGER NOT NULL
);
```

> ⚠️ Las columnas `marca` y `modelo` se duplican en ambas tablas (no hay FK al padre).

### ✅ Ventajas y ❌ Desventajas

| Ventajas ✅ | Desventajas ❌ |
|---|---|
| Cada tabla es autónoma | Columnas duplicadas |
| Consultas directas y rápidas | Sin polimorfismo |
| Aislás fallas en una tabla | Updates del padre hay que hacerlos en cada tabla |

> 🎓 **Cuándo usarla**: cuando los hijos son **conceptualmente distintos** y nunca se consultan juntos. Por ejemplo: `ReporteExcel` y `ReportePDF`.

---

## 8.5 Comparación final

```
Joined Table          Single Table             Concrete Table
─────────────────     ─────────────────        ─────────────────
vehiculos (padre)     empleados (todo)         autos_concretos
  ├── autos               (NULLable)          motos_concretas
  └── motos               campos hijos)
```

| Estrategia | # Tablas | JOIN | Polimorfismo | Mejor para... |
|---|---|---|---|---|
| **Joined** | 1 por clase | Sí | Sí | Jerarquías con consultas mixtas |
| **Single** | 1 | No | Sí | Performance, queries polimórficas |
| **Concrete** | 1 por clase | No | No | Hijos independientes |

> 🎓 **Consejo**: para empezar, usá **Single Table** si no tenés muchos campos específicos en hijos, o **Joined** si te importa la normalización. Concrete Table es para casos puntuales.

---

## 8.6 Mixins vs Herencia: ¿cuál usar?

| Caso | Usá |
|---|---|
| Varios modelos comparten columnas independientes (id, timestamps). | **Mixin** |
| Hay una **jerarquía real** (Auto ⊂ Vehículo). | **Herencia** |
| Compartís lógica de negocio entre clases no relacionadas. | **Mixin con métodos** |
| Compartís comportamiento entre clases relacionadas. | **Herencia** |

Reglas prácticas:

1. Si podés decir "es un": **herencia** (Auto **es un** Vehículo).
2. Si podés decir "tiene": **mixin** (Producto **tiene** Timestamp).
3. Si dudás: empezá con mixin y, si después necesitás jerarquía, migrás.

---

## 🛠️ Ejercicios prácticos

### 🟢 Ejercicio 8.1: Single Table básico

Modelá una jerarquía `Persona` con dos subclases `Estudiante` y `Profesor` usando **Single Table**:

- Todos tienen `id`, `nombre`, `email`.
- `Estudiante` tiene `legajo` (int).
- `Profesor` tiene `catedra` (string).

**Pista**: `__mapper_args__ = {"polymorphic_identity": "..."}`.

**Solución**: [soluciones/08-herencia-modelos.md](../soluciones/08-herencia-modelos.md#ejercicio-81)

---

### 🟡 Ejercicio 8.2: Joined Table

Repetí el ejercicio anterior pero usando **Joined Table**. ¿Cuántas tablas se crean? Verificá con `Base.metadata.sorted_tables`.

**Solución**: [soluciones/08-herencia-modelos.md](../soluciones/08-herencia-modelos.md#ejercicio-82)

---

### 🟡 Ejercicio 8.3: Query polimórfica

Dado cualquiera de las jerarquías anteriores, escribí una query que traiga **todas las personas** (Estudiantes + Profesores) en una sola consulta.

**Pista**: `select(Persona)` con `with_polymorphic("*")`.

**Solución**: [soluciones/08-herencia-modelos.md](../soluciones/08-herencia-modelos.md#ejercicio-83)

---

### 🟡 Ejercicio 8.4: Elegí la estrategia

Para cada caso, decidí qué estrategia usarías y por qué:

1. Una jerarquía `Vehiculo → Auto / Moto / Camioneta` con muchos campos específicos en cada hijo.
2. Una jerarquía `TipoNotificacion → Email / SMS / Push` con muy pocos campos específicos.
3. Una jerarquía `Reporte → ReporteExcel / ReportePDF / ReporteCSV` que nunca se consultan juntos.

**Solución**: [soluciones/08-herencia-modelos.md](../soluciones/08-herencia-modelos.md#ejercicio-84)

---

### 🔴 Ejercicio 8.5: Concrete Table

Implementá el ejemplo del capítulo 8.4 (Concrete Table) con `Vehiculo` como clase abstracta padre y `Auto`, `Moto` como concretas. Verificá con `Base.metadata.create_all(engine)` que se crean las tablas correctas.

**Solución**: [soluciones/08-herencia-modelos.md](../soluciones/08-herencia-modelos.md#ejercicio-85)

---

## 🎓 Lo que aprendiste

- Hay tres estrategias: **Joined**, **Single Table** y **Concrete**.
- Cada una resuelve un trade-off entre normalización y performance.
- **Mixin** es para columnas sueltas, **herencia** es para jerarquías.
- `polymorphic_identity` y `polymorphic_on` permiten queries polimórficas.

## 📖 Siguiente

[Capítulo 9: El primer modelo completo →](./09-primer-modelo.md)