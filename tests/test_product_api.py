from fastapi.testclient import TestClient

from main import app

client = TestClient(app)
# python -m pytest -v
def test_read_root():
   response = client.get("/")
   assert response.status_code == 200
   assert response.json() == {"message": "Welcome to home page"}

def test_get_all_products():
    response = client.get("/products")
    assert response.status_code == 200

def test_get_product_by_id():
    response = client.get("/products/1")
    assert response.status_code == 200