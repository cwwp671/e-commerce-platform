import pytest
from flask import json
from recommendation_service import app, user_preferences, products


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# Test getting user preferences for a non-existent user
def test_get_preferences_not_found(client):
    response = client.get('/preferences', query_string={'user_id': 1})
    assert response.status_code == 400


# Test updating user preferences
def test_update_preferences(client):
    data = {'user_id': 1, 'preferences': {'categories': ['Electronics', 'Books']}}
    response = client.post('/preferences', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert response.json == {'message': 'User preferences updated'}
    assert user_preferences == {1: {'categories': ['Electronics', 'Books']}}


# Test getting user preferences for an existing user
def test_get_preferences(client):
    response = client.get('/preferences', data=json.dumps({'user_id': 1}), content_type='application/json')
    assert response.status_code == 200
    assert response.json == {'categories': ['Electronics', 'Books']}


# Test getting recommendations without user preferences
def test_get_recommendations_no_preferences(client):
    response = client.get('/recommendations/2')
    assert response.status_code == 404
    assert response.json == {'message': 'User preferences not found'}


# Test getting recommendations for a user with preferences
def test_get_recommendations(client):
    response = client.get('/recommendations/1')
    assert response.status_code == 200
    assert len(response.json) <= 5
    assert all([product['category'] in ['Electronics', 'Books'] for product in response.json])
