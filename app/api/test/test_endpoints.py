import pytest
from fastapi.testclient import TestClient
from app.app import app 
from app.api.database import create_product_in_db, delete_product_by_id
from app.api.models.models import ProductCreate

client = TestClient(app)

'''
These tests are commented out while the Item endpoints 
are enabled to avoid generating noise when analyzing the
product test results.

# Test for POST /items/ endpoint
def test_create_item():
    response = client.post("/items/", json={"name": "Test Item", "description": "This is a test item."})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert data["description"] == "This is a test item."
    assert "id" in data

# Test for GET /items/ endpoint
def test_list_items():
    response = client.get("/items/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
'''
# Add more tests for other endpoints...

#Creates a temporary product that is deleted when the test is finished.
#It helps to not add test products in the database permanently.

@pytest.fixture
def create_temporary_product():
    product = ProductCreate(name="Temporary Product", description="Temporary Product Description", price=9.99)
    return  create_product_in_db(product)
        


# Test for POST /api/v1/example/products/ endpoint
def test_create_product():
    response = client.post("/api/v1/example/products/", json={ "name": "Product", "description": "This is a test item.", "price": 12.99})
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Product"
    assert data["description"] == "This is a test item."
    assert data["price"] == 12.99
    delete_product_by_id(data["id"])
    
# Test for GET /api/v1/example/products/ endpoint
def test_list_products():
    response = client.get("/api/v1/example/products/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

# Test for GET /api/v1/example/products/{product_id} endpoint   
def test_get_product(create_temporary_product):
    product_id = create_temporary_product.id
    response = client.get(f"/api/v1/example/products/{product_id}/")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    delete_product_by_id(product_id)

# Test for PATCH /api/v1/example/products/{product_id} endpoint
def test_update_product(create_temporary_product):
    product_id = create_temporary_product.id
    response = client.patch(f"/api/v1/example/products/{product_id}/", json={"name": "Updated Name"})
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id
    assert data["name"] == "Updated Name"
    delete_product_by_id(product_id)

# Test for DELETE /api/v1/example/products/{product_id} endpoint
def test_delete_product(create_temporary_product):
    product_id = create_temporary_product.id
    response = client.delete(f"/api/v1/example/products/{product_id}/")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == product_id