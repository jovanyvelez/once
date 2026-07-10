# Capítulo 1: Bienvenida — ¿qué vamos a aprender?

> *"Una hora de estudio bien planificada vale por tres horas de búsqueda en Google."*
> — Proverbio del desarrollador senior

Imagina que tu base de datos es una **bodega gigante llena de estanterías** 📦. Hoy tenés un problema: hablar con esa bodega en SQL puro es como ir a buscar un tornillo en un almacén de 10.000 cajas usando una linterna. Funciona, pero ¿qué tal si pudiéramos simplemente **pedir las cosas por nombre**?

Ahí aparece **SQLAlchemy** 🎩: es un **traductor mágico** que convierte objetos de Python (clases, listas, atributos) en consultas SQL. Y la versión **2.0** reescribió ese traductor casi desde cero, haciendo que el código sea mucho más legible.

---

## 1.1 ¿Qué vas a poder hacer al terminar este manual?

- ✅ Definir tus tablas como clases de Python (sin escribir SQL a mano).
- ✅ Crear, leer, actualizar y borrar datos sin despegarte de Python.
- ✅ Modelar relaciones complejas: uno-a-muchos, muchos-a-muchos, autorreferencias.
- ✅ Reutilizar columnas con **mixins** (DRY sin perder tipado).
- ✅ Aplicar **herencia de modelos** con tres estrategias distintas.
- ✅ Escuchar **eventos** del ORM para auditoría automática, timestamps, validación.
- ✅ Trabajar con `AsyncSession` para apps 100% asíncronas.
- ✅ Conectar todo esto a una API moderna con FastAPI.

---

## 1.2 ¿Por qué *este* manual?

Después de hacer búsquedas en Internet, seguro notaste algo:

- 🟠 **La mayoría de tutoriales en español** están en SQLAlchemy 1.x (sintaxis vieja).
- 🟠 **Los ejemplos actualizados a 2.0** son dispersos y a veces contradictorios.
- 🟠 **FastAPI + SQLAlchemy** suele explicarse sin profundizar en patrones modernos.

Este manual nace precisamente para cubrir esos huecos. Es:

- 📌 **Moderno**: usa exclusivamente SQLAlchemy 2.0 con `Mapped[T]`.
- 📌 **Práctico**: cada capítulo tiene ejemplos copiables y ejecutables.
- 📌 **Integral**: cubre desde cero hasta `AsyncSession` + FastAPI async.
- 📌 **Pedagógico**: se entiende sin haber visto nunca SQLAlchemy.

---

## 1.3 ¿Cómo se lee este manual?

1. 🟢 **En orden**, si sos nuevo. Cada capítulo asume lo anterior.
2. 🟠 **Por secciones**, si tenés experiencia: saltá al capítulo que necesitás.
3. 💻 **Con la terminal abierta**: copiá los ejemplos, ejecutálos, modificalos.

> 🎓 **Consejo**: la mejor forma de aprender es **romper código**. Si todo funciona a la primera, seguramente no lo entendiste del todo. Forzá errores y arreglalos.

---

## 1.4 Mapa mental de lo que viene

```
🟢 FUNDAMENTOS (Caps. 1-6)
   ↓ Aprendés a definir modelos y conectarte a la base
🟡 INTERMEDIO (Caps. 7-12)
   ↓ Reutilizás, heredás, hacés CRUD y consultas reales
🔴 AVANZADO (Caps. 13-16)
   ↓ Dominás relaciones, eventos, async, todo el poder del ORM
⚡ INTEGRACIÓN (Caps. 17-21)
   ↓ Conectás todo a FastAPI y aprendés el patrón de la industria
```

---

## 🎓 Lo que aprendiste

- Este manual te lleva **de cero a senior** en SQLAlchemy 2.0.
- Te enfoca en **lo moderno y práctico**, sin perder el rigor.
- Está organizado para leer **en cualquier orden**.

## 📖 Siguiente

[Capítulo 2: Conceptos previos →](./02-conceptos-previos.md)
