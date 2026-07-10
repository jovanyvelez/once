# Soluciones — Capítulo 3: Instalación y entorno

[Volver al capítulo 3](../capitulos/03-instalacion.md)

---

## Ejercicio 3.1

**Setup completo**

```bash
# 1. Crear entorno
python -m venv mi_entorno

# 2. Activar (Linux/macOS)
source mi_entorno/bin/activate

# 2'. (Windows PowerShell)
.\mi_entorno\Scripts\Activate.ps1

# 3. Instalar SQLAlchemy
pip install "sqlalchemy>=2.0"

# 4. Verificar versión
python -c "import sqlalchemy; print(sqlalchemy.__version__)"
# Debe mostrar algo como '2.0.27'

# 5. Ejecutar el test
python test.py
```

[Volver al ejercicio ↑](../capitulos/03-instalacion.md#%C2%B0-ejercicio-31)

---

## Ejercicio 3.2

**URL de base de datos**

1. SQLite en memoria: `"sqlite:///:memory:"`
2. SQLite en archivo: `"sqlite:///./biblioteca.db"`
3. PostgreSQL: `"postgresql://app:secreta123@db.local:5432/biblioteca"`
4. MySQL: `"mysql+pymysql://app:xyz@mysql.servidor.com:3306/biblioteca"`

[Volver al ejercicio ↑](../capitulos/03-instalacion.md#%C2%B0-ejercicio-32)

---

## Ejercicio 3.3

**Estructura de carpetas**

```bash
mkdir mi_proyecto
cd mi_proyecto
mkdir -p src/routers
touch src/__init__.py
touch src/routers/__init__.py

# Verificar
find . -type d
```

Luego, en `mi_proyecto/`:

```bash
python -c "import sys; sys.path.insert(0, '.'); from src import __name__; print('OK')"
```

Debe imprimir `OK` sin errores.

[Volver al ejercicio ↑](../capitulos/03-instalacion.md#%C2%B1-ejercicio-33)

---

## Ejercicio 3.4

**Probá drivers**

```python
# ¿Está psycopg2 instalado?
python -c "import psycopg2; print(f'psycopg2 versión {psycopg2.__version__}')"
```

Si no tenés una DB PostgreSQL corriendo, **podés** verificar que el driver **importa** sin errores con `import psycopg2`. Lo que NO podés verificar sin DB real es que **funcione** efectivamente.

```python
# Verificar sin conexión real
try:
    import psycopg2
    print(f"✅ psycopg2 {psycopg2.__version__} disponible")
except ImportError:
    print("❌ psycopg2 no instalado. Instalá con: pip install psycopg2-binary")
```

[Volver al ejercicio ↑](../capitulos/03-instalacion.md#%C2%B1-ejercicio-34)
