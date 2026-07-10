"""
Tests de los endpoints de Producto.
"""
from decimal import Decimal


def test_root(client):
    r = client.get("/")
    assert r.status_code == 200
    assert "docs" in r.json()


def test_health(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json() == {"status": "ok"}


def test_crear_producto(client, categoria_sample):
    payload = {
        "nombre": "Laptop Gamer",
        "sku": "LTG-001",
        "precio": "1299.99",
        "descripcion": "RTX 4080, 32GB RAM",
        "categoria_id": categoria_sample.id,
    }
    r = client.post("/productos/", json=payload)
    assert r.status_code == 201, r.text
    data = r.json()
    assert data["nombre"] == "Laptop Gamer"
    assert data["sku"] == "LTG-001"
    assert Decimal(data["precio"]) == Decimal("1299.99")
    assert data["categoria"]["nombre"] == "Electrónica"
    assert "id" in data
    assert "creado_en" in data


def test_crear_producto_sku_duplicado(client):
    payload = {"nombre": "A", "sku": "DUP-1", "precio": "10"}
    client.post("/productos/", json=payload)
    r = client.post("/productos/", json=payload)
    assert r.status_code == 400
    assert "duplicado" in r.json()["detail"]


def test_listar_productos(client):
    for i in range(3):
        client.post(
            "/productos/",
            json={"nombre": f"P{i}", "sku": f"SKU-{i}", "precio": "10"},
        )
    r = client.get("/productos/")
    assert r.status_code == 200
    assert len(r.json()) == 3


def test_listar_productos_con_filtros(client, categoria_sample):
    # Crear productos con distintas categorías y precios
    for i, precio in enumerate(["100", "500", "1500"]):
        client.post(
            "/productos/",
            json={
                "nombre": f"P{i}",
                "sku": f"SKU-{i}",
                "precio": precio,
                "categoria_id": categoria_sample.id,
            },
        )

    # Filtrar por rango de precio
    r = client.get("/productos/", params={"min_precio": "200", "max_precio": "1000"})
    assert r.status_code == 200
    assert len(r.json()) == 1
    assert Decimal(r.json()[0]["precio"]) == Decimal("500")


def test_obtener_producto(client):
    r = client.post(
        "/productos/",
        json={"nombre": "P", "sku": "X-1", "precio": "10"},
    )
    pid = r.json()["id"]

    r2 = client.get(f"/productos/{pid}")
    assert r2.status_code == 200
    assert r2.json()["nombre"] == "P"


def test_obtener_producto_inexistente(client):
    r = client.get("/productos/9999")
    assert r.status_code == 404


def test_patch_parcial(client):
    r = client.post(
        "/productos/",
        json={"nombre": "Original", "sku": "ORIG-1", "precio": "100"},
    )
    pid = r.json()["id"]

    # Solo actualizamos precio
    r2 = client.patch(f"/productos/{pid}", json={"precio": "200"})
    assert r2.status_code == 200
    assert Decimal(r2.json()["precio"]) == Decimal("200")
    assert r2.json()["nombre"] == "Original"  # sin cambios


def test_borrar_producto(client):
    r = client.post(
        "/productos/",
        json={"nombre": "A", "sku": "BORR-1", "precio": "10"},
    )
    pid = r.json()["id"]

    r2 = client.delete(f"/productos/{pid}")
    assert r2.status_code == 204

    r3 = client.get(f"/productos/{pid}")
    assert r3.status_code == 404


def test_validacion_precio_negativo(client):
    r = client.post(
        "/productos/",
        json={"nombre": "A", "sku": "X-1", "precio": "-10"},
    )
    assert r.status_code == 422  # Unprocessable Entity


def test_validacion_sku_largo(client):
    r = client.post(
        "/productos/",
        json={"nombre": "A", "sku": "X" * 100, "precio": "10"},
    )
    assert r.status_code == 422
