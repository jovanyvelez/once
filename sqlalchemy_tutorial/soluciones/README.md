# ✅ Soluciones de los Ejercicios Prácticos

> Acá están las **soluciones** de los ejercicios que aparecen al final de cada capítulo.
> **¡Intentalos primero por tu cuenta antes de mirar acá!** El verdadero aprendizaje está en la lucha.

---

## 🎯 Cómo usar esta carpeta

Cada capítulo técnico (3-19, 22-25) tiene ejercicios en su sección final. Las soluciones están acá en archivos separados:

```
soluciones/
├── README.md (este archivo)
├── 03-instalacion.md
├── 04-engine-session.md
├── 05-declarative-base.md
├── 06-anotaciones-mapped.md
├── 07-mixins.md
├── 08-herencia-modelos.md
├── 09-primer-modelo.md
├── 10-crear-tablas.md
├── 11-crud.md
├── 12-consultas.md
├── 13-relaciones.md
├── 14-subconsultas.md
├── 15-eventos.md
├── 16-async-session.md
├── 17-fastapi.md
├── 18-buenas-practicas.md
├── 19-errores-comunes.md
├── 22-pydantic-v2.md
├── 23-alembic.md
├── 24-sqlalchemy-utils.md
└── 25-docker.md
```

---

## 🟢🟡🔴 Sistema de niveles

Cada ejercicio tiene un nivel de dificultad:

- 🟢 **Básico**: para fijar conceptos del capítulo.
- 🟡 **Intermedio**: combinar varios conceptos o aplicarlos a un caso real.
- 🔴 **Avanzado**: explorar bordes, optimizaciones o casos no triviales.

No te frustres si un 🔴 te cuesta. Es normal. Volvé al capítulo, releé, y volvé a intentar.

---

## 🧪 Cómo testear tus soluciones

Para los ejercicios de código, tenés dos opciones:

### Opción 1: el proyecto del manual

```bash
cd ../proyecto/fastapi_sqlalchemy
docker compose up -d
# Probá tus consultas contra http://localhost:8000/docs
```

### Opción 2: un sandbox rápido

```bash
mkdir mi_sandbox && cd mi_sandbox
python -m venv venv && source venv/bin/activate
pip install sqlalchemy fastapi pydantic pydantic-settings
# Creá archivos .py y experimentá
```

---

## 💡 Consejos generales

1. **Escribí primero el código en papel** si no sabés por dónde empezar.
2. **Corré los errores**: leé el traceback de abajo hacia arriba.
3. **Usá `print()` y `echo=True`**: ver lo que pasa es la mitad del aprendizaje.
4. **Modificá los ejemplos del capítulo**: cambiá un número, un nombre, una condición.
5. **Si te trabás más de 15 minutos**: mirá la pista, después la solución, y volvé a intentar sin mirar.

---

## 🤝 Contribuciones

Si encontrás una solución mejor o alternativa, genial. Hay **muchas** formas correctas de resolver cada ejercicio. Lo importante es que funcione y entiendas por qué.

---

¡A romper código! 🚀