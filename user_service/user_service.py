from flask import Flask, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# In-memory user storage
users = {}


# Helper function to find a user by username
def find_user(username):
    return users.get(username)


# Endpoint to register a new user
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # Check if both username and password are provided
    if not username or not password:
        return jsonify({'message': 'Missing username or password'}), 400

    # Check if the user already exists
    if find_user(username):
        return jsonify({'message': 'User already exists'}), 400

    # Hash the password and store the new user
    hashed_password = generate_password_hash(password)
    users[username] = {
        'username': username,
        'password': hashed_password,
        'profile': {}
    }

    return jsonify({'message': 'User registered'}), 201


# Endpoint to log in a user
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = find_user(username)
    if not user:
        return jsonify({'message': 'Invalid username or password'}), 401

    # Check if the password matches the stored hash
    if not check_password_hash(user['password'], password):
        return jsonify({'message': 'Invalid username or password'}), 401

    # Return a success message (in a real-world scenario, you would return an authentication token)
    return jsonify({'message': 'User logged in'})


# Endpoint to get or update a user's profile
@app.route('/profile', methods=['GET', 'PUT'])
def profile():
    data = request.get_json()
    username = data.get('username')

    user = find_user(username)
    if not user:
        return jsonify({'message': 'User not found'}), 404

    # Return the user's profile
    if request.method == 'GET':
        return jsonify(user['profile'])

    # Update the user's profile
    if request.method == 'PUT':
        new_profile_data = data.get('profile')
        if not new_profile_data:
            return jsonify({'message': 'Missing profile data'}), 400

        user['profile'].update(new_profile_data)
        return jsonify({'message': 'User profile updated'})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
