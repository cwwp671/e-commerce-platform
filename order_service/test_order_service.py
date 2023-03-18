import pytest
from flask import json
from order_service import app, orders


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# Test getting an empty list of orders
def test_get_empty_orders(client):
    response = client.get('/orders')
    assert response.status_code == 200
    assert response.json == []


# Test creating a new order
def test_create_order(client):
    data = {'user_id': 1, 'items': [{'product_id': 1, 'quantity': 2}]}
    response = client.post('/orders', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 201
    assert response.json == {'id': 1, 'user_id': 1, 'items': [{'product_id': 1, 'quantity': 2}], 'status': 'created'}
    assert orders == {1: {'id': 1, 'user_id': 1, 'items': [{'product_id': 1, 'quantity': 2}], 'status': 'created'}}


# Test getting the list of orders with one order
def test_get_orders(client):
    response = client.get('/orders')
    assert response.status_code == 200
    assert response.json == [{'id': 1, 'user_id': 1, 'items': [{'product_id': 1, 'quantity': 2}], 'status': 'created'}]


# Test getting a specific order
def test_get_order(client):
    response = client.get('/orders/1')
    assert response.status_code == 200
    assert response.json == {'id': 1, 'user_id': 1, 'items': [{'product_id': 1, 'quantity': 2}], 'status': 'created'}


# Test getting a non-existent order
def test_get_order_not_found(client):
    response = client.get('/orders/2')
    assert response.status_code == 404
    assert response.json == {'message': 'Order not found'}


# Test updating an order
def test_update_order(client):
    data = {'status': 'shipped'}
    response = client.put('/orders/1', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert response.json == {'id': 1, 'user_id': 1, 'items': [{'product_id': 1, 'quantity': 2}], 'status': 'shipped'}


# Test deleting an order
def test_delete_order(client):
    response = client.delete('/orders/1')
    assert response.status_code == 200
    assert response.json == {'message': 'Order deleted'}


# Test processing a payment for an order
def test_payment(client):
    global order_id_counter

    # Create a new order for testing
    data = {'user_id': 1, 'items': [{'product_id': 1, 'quantity': 2}]}
    response = client.post('/orders', data=json.dumps(data), content_type='application/json')

    # Get the order_id from the response
    order_id = response.get_json().get('id')

    payment_data = {'order_id': order_id, 'payment_info': {'card_number': '1234567890123456', 'expiry': '12/25', 'cvc': '123'}}
    response = client.post('/payment', data=json.dumps(payment_data), content_type='application/json')
    assert response.status_code == 200

