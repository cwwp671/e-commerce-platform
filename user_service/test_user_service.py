import pytest
from flask import json
from user_service import app, users, find_user


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client


# Test registering a new user
def test_register(client):
    data = {'username': 'testuser', 'password': 'testpassword'}
    response = client.post('/register', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 201
    assert response.json == {'message': 'User registered'}


# Test registering a user with an existing username
def test_register_existing_user(client):
    data = {'username': 'testuser', 'password': 'testpassword'}
    response = client.post('/register', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 400
    assert response.json == {'message': 'User already exists'}


# Test logging in with an invalid username
def test_login_invalid_username(client):
    data = {'username': 'invaliduser', 'password': 'testpassword'}
    response = client.post('/login', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 401
    assert response.json == {'message': 'Invalid username or password'}


# Test logging in with a valid username and password
def test_login(client):
    data = {'username': 'testuser', 'password': 'testpassword'}
    response = client.post('/login', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert response.json == {'message': 'User logged in'}


# Test getting a user's profile
def test_get_profile(client):
    data = {'username': 'testuser'}
    response = client.get('/profile', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert response.json == users['testuser']['profile']


# Test updating a user's profile
def test_update_profile(client):
    data = {'username': 'testuser', 'profile': {'name': 'Test User', 'email': 'test@example.com'}}
    response = client.put('/profile', data=json.dumps(data), content_type='application/json')
    assert response.status_code == 200
    assert response.json == {'message': 'User profile updated'}
