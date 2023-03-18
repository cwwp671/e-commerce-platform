import pytest
from flask import json
from inventory_service import app, inventory


# Define a fixture for creating a test client for the Flask app
@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# Test getting an empty inventory list
def test_get_empty_inventory(client):
    response = client.get('/inventory')
    assert response.status_code == 200
    assert response.json == []


# Test adding a new inventory item
def test_put_inventory(client):
    data = {'quantity': 10}
    response = client.put('/inventory/1', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert response.json == {'product_id': 1, 'quantity': 10}
    assert inventory == {1: {'product_id': 1, 'quantity': 10}}


# Test getting the inventory list with one item
def test_get_inventory(client):
    response = client.get('/inventory')
    assert response.status_code == 200
    assert response.json == [{'product_id': 1, 'quantity': 10}]


# Test getting a specific inventory item
def test_get_inventory_item(client):
    response = client.get('/inventory/1')
    assert response.status_code == 200
    assert response.json == {'product_id': 1, 'quantity': 10}


# Test getting an inventory item that does not exist
def test_get_inventory_item_not_found(client):
    response = client.get('/inventory/2')
    assert response.status_code == 404
    assert response.json == {'message': 'Inventory not found'}


# Test updating inventory with a missing quantity value
def test_put_inventory_missing_quantity(client):
    response = client.put('/inventory/1', data=json.dumps({}), content_type='application/json')
    assert response.status_code == 400
    assert response.json == {'message': 'Missing quantity'}


# Test updating an existing inventory item
def test_put_inventory_update(client):
    data = {'quantity': 20}
    response = client.put('/inventory/1', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert response.json == {'product_id': 1, 'quantity': 20}
    assert inventory == {1: {'product_id': 1, 'quantity': 20}}
