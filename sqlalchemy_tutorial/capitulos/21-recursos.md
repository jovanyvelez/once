# Capítulo 21: Recursos y siguiente paso

> El manual termina, pero tu camino recién empieza.

---

## 21.1 Documentación oficial

- 📖 [SQLAlchemy 2.0 ORM Quickstart](https://docs.sqlalchemy.org/en/20/orm/quickstart.html) — la fuente de este manual.
- 📖 [SQLAlchemy 2.0 Unified Tutorial](https://docs.sqlalchemy.org/en/20/tutorial/index.html) — más profundo, cubre herencia, Mapped, eventos.
- 📖 [SQLAlchemy API Reference](https://docs.sqlalchemy.org/en/20/orm/) — búsqueda de funciones específicas.
- 📖 [FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/) — la referencia para FastAPI.
- 📖 [Pydantic v2 Docs](https://docs.pydantic.dev/latest/) — la librería de validación.

---

## 21.2 Alembic: migraciones para tu DB

`Base.metadata.create_all(engine)` está perfecto para dev. En producción, la tabla evoluciona: agregás columnas, renombrás, etc. Para eso existen las **migraciones**.

### Instalación

```bash
pip install alembic
alembic init alembic
```

### Configurar `alembic.ini`

```ini
sqlalchemy.url = sqlite:///./tienda.db   # o tu URL real
```

### Crear la primera migración

```bash
alembic revision --autogenerate -m "inicial"
```

Alembic detecta los cambios entre los modelos actuales y la DB, y genera un script de migración.

### Aplicar migraciones

```bash
alembic upgrade head
```

### Flujo de uso típico

```bash
# 1. Modificás un modelo (ej: agregar columna)
# 2. Detectás los cambios:
alembic revision --autogenerate -m "agregar telefono"

# 3. Revisás el archivo en alembic/versions/ para confirmar
# 4. Aplicás:
alembic upgrade head

# 5. Si hay problemas, volvés atrás:
alembic downgrade -1
```

> 🎓 **Consejo**: en CI/CD, las migraciones se ejecutan **antes** de levantar la app. Nunca en medio de producción caliente.

---

## 21.3 Bases de datos: cuándo usar cada una

| DB | Usala si... |
|---|---|
| **SQLite** | Dev, tests, demos, apps pequeñas. No concurrencia alta. |
| **PostgreSQL** | Producción típica. JSONB, full-text, geodatos, etc. |
| **MySQL** | Web apps que crecieron en PHP, ecosistema LAMP. |
| **SQL Server** | Empresas que ya lo tienen (Microsoft stack). |
| **Oracle** | Enterprise pesado (consultá a tu DBA 😉). |

---

## 21.4 Temas avanzados para seguir aprendiendo

Cuando te sientas cómodo con este manual, podés seguir con:

| Tema | Para qué sirve |
|---|---|
| **Alembic** | Migraciones de base de datos. |
| **Pytest + fixtures para DB** | Tests unitarios confiables. |
| **Mapeo asíncrono con `asyncpg`** | Mayor concurrencia. |
| **Patrón Unit of Work** | Diseño avanzado de transacciones. |
| **CQRS** | Separar escrituras y lecturas. |
| **Event Sourcing** | Almacenar eventos en vez de estado. |
| **Outbox Pattern** | Eventos + DB para consistencia. |
| **SQLAlchemy + GraphQL** | Otros tipos de API. |
| **Database connection pooling** | Optimización de performance. |
| **Database sharding** | Escalar horizontalmente. |

---

## 21.5 Herramientas útiles

| Herramienta | Para qué sirve |
|---|---|
| **PgAdmin / DBeaver** | Explorador visual de bases de datos. |
| **Alembic** | Migraciones. |
| **SQLAlchemy-Utils** | Extensiones útiles (assert_matches, instrumentación). |
| **pytest** | Framework de tests. |
| **Hypothesis** | Property-based testing para queries. |
| **Rich** | Logging bonito en consola. |
| **Sentry** | Monitoring de errores en producción. |

---

## 21.6 Tu siguiente paso: armar tu propio proyecto

La mejor forma de consolidar este conocimiento es **construir**:

### Idea 1 — API de una tienda

- Productos, categorías, usuarios, carritos, pedidos.
- CRUD completo + relación N—M (producto ↔ categoría).
- Endpoints `/api/products/`, `/api/categories/`, `/api/orders/`.

### Idea 2 — Blog personal

- Usuarios, posts, comentarios, tags (N—M), categorías.
- Endpoints para listar posts con filtros por tag/fecha.
- Soft delete para borrado.

### Idea 3 — Sistema de votos (estilo Reddit)

- Usuarios, posts, votos (1—N), comentarios anidados.
- Un usuario puede votar muchos posts.
- Implementar el "karma" con agregaciones.

> 🎓 **Regla**: hacé uno **terminado**, no diez a medias. Un CRUD completo vale más que tres abandonados.

---

## 21.7 Libros recomendados

- 📘 *Essential SQLAlchemy* (por Jason Myers & Rick Copeland).
- 📘 *Architecture Patterns with Python* (Cosentino, sobre patrones).
- 📘 *Head First Design Patterns* (por Freeman, sobre patrones de diseño en general).
- 📘 *Clean Architecture* (Robert C. Martin).
- 📘 *Refactoring* (Martin Fowler).

---

## 21.8 Comunidades donde aprender

- 🌐 [StackOverflow](https://stackoverflow.com/questions/tagged/sqlalchemy) — preguntas frecuentes.
- 🌐 [Reddit: r/learnpython](https://www.reddit.com/r/learnpython/).
- 🌐 [Discord de Python Argentina](https://discord.gg/pythonargentina).
- 🌐 [FastAPI Discord](https://discord.gg/fastapi).
- 🌐 [SQLAlchemy GitHub](https://github.com/sqlalchemy/sqlalchemy).

---

## 21.9 Tu plan de acción

| Semana | Tema | Ejercicio |
|---|---|---|
| 1 | Caps. 1-12 | Armar CRUD básico con SQLite. |
| 2 | Cap. 13 | Agregar relaciones entre 3 modelos. |
| 3 | Cap. 17 | Conectar a FastAPI con `SessionDep`. |
| 4 | Cap. 14-16 | Hacer un query complejo + async. |
| 5 | Cap. 18-19 | Buenas prácticas + errores comunes. |
| 6 | Cap. 15 | Implementar auditoría con eventos. |
| 7 | Alembic | Configurar migraciones. |
| 8 | Proyecto final | Tu propia API con tests y deploy. |

> 🎓 **Consejo final del profesor**: leí este manual al menos **dos veces**. La primera para familiarizarte, la segunda para **escribir código propio**. La diferencia entre saber y dominar es la práctica.

---

## 🎓 Palabras finales

Recorriste un camino largo, pero ahora:

- ✅ Podés definir modelos modernos con `Mapped[T]`.
- ✅ Reutilizás columnas con **mixins**.
- ✅ Aplicás tres estrategias de **herencia de modelos**.
- ✅ Escribís queries eficientes evitando el problema N+1.
- ✅ Dominás relaciones 1—N, 1—1, N—M y recursivas.
- ✅ Usás **eventos** para auditoría, timestamps, validación.
- ✅ Trabajás con `AsyncSession` cuando hace falta.
- ✅ Integrás todo con FastAPI usando el patrón `get_db()` con `yield` y `SessionDep`.
- ✅ Evitás errores comunes que pasan juniors.
- ✅ Usás buenas prácticas de la industria.

Eso es **exactamente** lo que vas a usar en tus proyectos profesionales. Lo que falta es práctica: armar un mini proyecto, romper cosas, arreglarlas, leer errores. Esa es la verdadera formación.

¡Mucho éxito! 🚀🐍

---

> **Créditos y agradecimientos**: este manual se basa en [SQLAlchemy 2.0 ORM Quickstart](https://docs.sqlalchemy.org/en/20/orm/quickstart.html) y la documentación oficial de [FastAPI](https://fastapi.tiangolo.com/tutorial/), sintetizados con un enfoque pedagógico para estudiantes hispanohablantes. Los capítulos 7 (Mixins), 8 (Herencia), 15 (Eventos) y 16 (AsyncSession) son contenido adicional para profundizar el dominio del ORM.
>
> _Última revisión: 2026._
