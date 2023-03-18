from flask import Flask, jsonify, request
import random

app = Flask(__name__)

# In-memory user preferences and product storage
user_preferences = {}
products = {
    1: {'id': 1, 'name': 'Product A', 'category': 'Electronics'},
    2: {'id': 2, 'name': 'Product B', 'category': 'Electronics'},
    3: {'id': 3, 'name': 'Product C', 'category': 'Books'},
    4: {'id': 4, 'name': 'Product D', 'category': 'Books'},
}


# Endpoint to get or update user preferences
@app.route('/preferences', methods=['GET', 'POST'])
def preferences():
    data = request.get_json()
    user_id = data.get('user_id')

    # Check if user_id is provided
    if not user_id:
        return jsonify({'message': 'Missing user_id'}), 400

    # Get user preferences
    if request.method == 'GET':
        preferences = user_preferences.get(user_id, {})
        return jsonify(preferences)

    # Update user preferences
    if request.method == 'POST':
        preferences = data.get('preferences')
        if not preferences:
            return jsonify({'message': 'Missing preferences'}), 400

        user_preferences[user_id] = preferences
        return jsonify({'message': 'User preferences updated'})


# Endpoint to get product recommendations based on user preferences
@app.route('/recommendations/<int:user_id>', methods=['GET'])
def recommendations(user_id):
    preferences = user_preferences.get(user_id)

    # Check if user preferences are available
    if not preferences:
        return jsonify({'message': 'User preferences not found'}), 404

    recommended_products = []

    # Add products to the recommendation list if they match the user's preferred categories
    for product in products.values():
        if product['category'] in preferences['categories']:
            recommended_products.append(product)

    # Shuffle and limit recommendations to 5 items
    random.shuffle(recommended_products)
    recommended_products = recommended_products[:5]

    return jsonify(recommended_products)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)
