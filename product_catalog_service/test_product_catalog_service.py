import pytest
from flask import json
from product_catalog_service import app, products, categories


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# Test getting an empty list of categories
def test_get_empty_categories(client):
    response = client.get('/categories')
    assert response.status_code == 200
    assert response.json == []


# Test creating a new category
def test_create_category(client):
    data = {'name': 'Electronics'}
    response = client.post('/categories', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 201
    assert response.json == {'id': 1, 'name': 'Electronics'}
    assert categories == {1: {'id': 1, 'name': 'Electronics'}}


# Test getting the list of categories with one category
def test_get_categories(client):
    response = client.get('/categories')
    assert response.status_code == 200
    assert response.json == [{'id': 1, 'name': 'Electronics'}]


# Test getting an empty list of products
def test_get_empty_products(client):
    response = client.get('/products')
    assert response.status_code == 200
    assert response.json == []


# Test creating a new product
def test_create_product(client):
    data = {'name': 'Smartphone', 'description': 'A cool smartphone', 'category_id': 1}
    response = client.post('/products', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 201
    assert response.json == {'id': 1, 'name': 'Smartphone', 'description': 'A cool smartphone', 'category_id': 1}
    assert products == {1: {'id': 1, 'name': 'Smartphone', 'description': 'A cool smartphone', 'category_id': 1}}


# Test getting the list of products with one product
def test_get_products(client):
    response = client.get('/products')
    assert response.status_code == 200
    assert response.json == [{'id': 1, 'name': 'Smartphone', 'description': 'A cool smartphone', 'category_id': 1}]


# Test getting a specific product
def test_get_product(client):
    response = client.get('/products/1')
    assert response.status_code == 200
    assert response.json == {'id': 1, 'name': 'Smartphone', 'description': 'A cool smartphone', 'category_id': 1}


# Test getting a non-existent product
def test_get_product_not_found(client):
    response = client.get('/products/2')
    assert response.status_code == 404
    assert response.json == {'message': 'Product not found'}


# Test updating a product
def test_update_product(client):
    data = {'name': 'Updated Smartphone', 'description': 'An updated cool smartphone', 'category_id': 1}
    response = client.put('/products/1', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert response.json == {'id': 1, 'name': 'Updated Smartphone', 'description': 'An updated cool smartphone',
                             'category_id': 1}


# Test deleting a product
def test_delete_product(client):
    response = client.delete('/products/1')
    assert response.status_code == 200
    assert response.json == {'message': 'Product deleted'}
