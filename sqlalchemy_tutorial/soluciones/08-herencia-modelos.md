# Soluciones — Capítulo 8: Herencia de modelos

[Volver al capítulo 8](../capitulos/08-herencia-modelos.md)

---

## Ejercicio 8.1

**Single Table básico**

```python
from sqlalchemy import String, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Persona(Base):
    __tablename__ = "personas"

    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80))
    email: Mapped[str] = mapped_column(String(120))

    tipo: Mapped[str] = mapped_column(String(20))

    __mapper_args__ = {
        "polymorphic_identity": "persona",
        "polymorphic_on": "tipo",
    }


class Estudiante(Persona):
    legajo: Mapped[int] = mapped_column(Integer, nullable=True)

    __mapper_args__ = {"polymorphic_identity": "estudiante"}


class Profesor(Persona):
    catedra: Mapped[str] = mapped_column(String(80), nullable=True)

    __mapper_args__ = {"polymorphic_identity": "profesor"}
```

**SQL generado** (una sola tabla):

```sql
CREATE TABLE personas (
    id INTEGER NOT NULL PRIMARY KEY,
    nombre VARCHAR(80) NOT NULL,
    email VARCHAR(120) NOT NULL,
    tipo VARCHAR(20) NOT NULL,
    legajo INTEGER,
    catedra VARCHAR(80)
);
```

`legajo` y `catedra` quedan NULL para los tipos que no les corresponden.

[Volver al ejercicio ↑](../capitulos/08-herencia-modelos.md#%C2%B0-ejercicio-81)

---

## Ejercicio 8.2

**Joined Table**

```python
class Persona(Base):
    __tablename__ = "personas"
    id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80))
    email: Mapped[str] = mapped_column(String(120))
    tipo: Mapped[str] = mapped_column(String(20))

    __mapper_args__ = {
        "polymorphic_identity": "persona",
        "polymorphic_on": "tipo",
    }


class Estudiante(Persona):
    __tablename__ = "estudiantes"
    id: Mapped[int] = mapped_column(ForeignKey("personas.id"), primary_key=True)
    legajo: Mapped[int]

    __mapper_args__ = {"polymorphic_identity": "estudiante"}


class Profesor(Persona):
    __tablename__ = "profesores"
    id: Mapped[int] = mapped_column(ForeignKey("personas.id"), primary_key=True)
    catedra: Mapped[str]

    __mapper_args__ = {"polymorphic_identity": "profesor"}
```

**Tablas creadas**:

```python
print(len(Base.metadata.sorted_tables))  # -> 3
for t in Base.metadata.sorted_tables:
    print(t.name)  # personas, estudiantes, profesores
```

[Volver al ejercicio ↑](../capitulos/08-herencia-modelos.md#%C2%B1-ejercicio-82)

---

## Ejercicio 8.3

**Query polimórfica**

```python
from sqlalchemy.orm import with_polymorphic
from sqlalchemy import select


# Sin importar subclases — todo desde Persona
todas = session.scalars(select(Persona)).all()
for p in todas:
    print(type(p).__name__, p.nombre)
# -> Estudiante Ana
# -> Profesor Pedro
# -> Estudiante Lucía
```

**Con `with_polymorphic`** (más eficiente, hace un solo JOIN):

```python
PersonaAll = with_polymorphic(Persona, [Estudiante, Profesor])

stmt = select(PersonaAll)
for p in session.scalars(stmt):
    # p es una tupla con los datos de Persona + los específicos
    print(p.Persona.nombre, getattr(p, "legajo", None), getattr(p, "catedra", None))
```

[Volver al ejercicio ↑](../capitulos/08-herencia-modelos.md#%C2%B1-ejercicio-83)

---

## Ejercicio 8.4

**Elegí la estrategia**

1. **`Vehiculo → Auto / Moto / Camioneta`**: **Joined Table**. Cada vehículo tiene muchos campos específicos (cilindrada, capacidad, tipo_combustible). No querés una tabla con muchos NULLs.

2. **`TipoNotificacion → Email / SMS / Push`**: **Single Table**. Pocos campos específicos; consultas todo junto frecuentemente. Performance es prioridad.

3. **`Reporte → ReporteExcel / ReportePDF / ReporteCSV`**: **Concrete Table**. Nunca se consultan juntos; cada reporte es independiente.

[Volver al ejercicio ↑](../capitulos/08-herencia-modelos.md#%C2%B1-ejercicio-84)

---

## Ejercicio 8.5

**Concrete Table**

```python
from sqlalchemy.orm import AbstractConcreteBase
from sqlalchemy import ForeignKey


class Vehiculo(AbstractConcreteBase, Base):
    """Sin tabla propia."""
    marca: Mapped[str]
    modelo: Mapped[str]


class Auto(Vehiculo):
    __tablename__ = "autos_concretos"
    id: Mapped[int] = mapped_column(primary_key=True)
    marca: Mapped[str]
    modelo: Mapped[str]
    puertas: Mapped[int]


class Moto(Vehiculo):
    __tablename__ = "motos_concretas"
    id: Mapped[int] = mapped_column(primary_key=True)
    marca: Mapped[str]
    modelo: Mapped[str]
    cilindrada: Mapped[int]


# Verificar
Base.metadata.create_all(engine)
print([t.name for t in Base.metadata.sorted_tables])
# -> ['autos_concretos', 'motos_concretas']
# NO hay tabla 'vehiculos'.
```

[Volver al ejercicio ↑](../capitulos/08-herencia-modelos.md#%F0%9F%94%B4-ejercicio-85)