import pytest
from flask import json
from shipping_service import app, shipping_providers


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# Test getting a list of shipping providers
def test_shipping_providers_list(client):
    response = client.get('/shipping/providers')
    assert response.status_code == 200
    assert response.json == list(shipping_providers.keys())


# Test calculating shipping cost with missing parameters
def test_shipping_calculate_missing_parameters(client):
    data = {'provider': 'FedEx'}
    response = client.post('/shipping/calculate', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    assert response.json == {'message': 'Missing provider or weight'}


# Test calculating shipping cost with an invalid provider
def test_shipping_calculate_invalid_provider(client):
    data = {'provider': 'InvalidProvider', 'weight': 5}
    response = client.post('/shipping/calculate', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    assert response.json == {'message': 'Invalid provider'}


# Test calculating shipping cost with a valid provider and weight
def test_shipping_calculate(client):
    data = {'provider': 'FedEx', 'weight': 5}
    response = client.post('/shipping/calculate', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert response.json == {'provider': 'FedEx',
                             'cost': shipping_providers['FedEx']['base_rate'] + 5 * shipping_providers['FedEx'][
                                 'rate_per_kg']}
