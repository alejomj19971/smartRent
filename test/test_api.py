

from src.main import app 
from fastapi.testclient import TestClient

client = TestClient(app)

def test_get_arriendos():
    response = client.get("/")
    assert response.status_code == 200
    assert isinstance(response.json(), list),"Fallo en la obtencion de arriendos"

def test_filtrar_por_rango():
    response = client.get("/casas/filtrar/?precioMin=1000000&precioMax=1200000")
    assert response.status_code == 200
    data = response.json()
    assert all(1000000 <= casa["precio"] <= 1200000 for casa in data),"Fallo en el filtro por rango"

def test_agrupar_por_lugar():
    response = client.get("/casas/agrupar")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    if "Apartamento en Arriendo, Machado" in data:
        assert isinstance(data["Apartamento en Arriendo, Machado"], list),"Fallo en la agrupacion"