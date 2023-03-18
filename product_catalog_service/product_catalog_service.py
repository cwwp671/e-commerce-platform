from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory product and category storage
products = {}
categories = {}
product_id_counter = 1
category_id_counter = 1


# Route for handling product list retrieval and creation
@app.route('/products', methods=['GET', 'POST'])
def products_list():
    global product_id_counter

    # If it's a GET request, return the list of all products
    if request.method == 'GET':
        return jsonify(list(products.values()))

    # If it's a POST request, create a new product with the given details
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        category_id = data.get('category_id')

        # Check if all required fields are provided
        if not name or not description or not category_id:
            return jsonify({'message': 'Missing name, description or category_id'}), 400

        # Check if the provided category_id is valid
        if category_id not in categories:
            return jsonify({'message': 'Invalid category_id'}), 400

        # Create the new product and store it in the products dictionary
        product_id = product_id_counter
        product = {
            'id': product_id,
            'name': name,
            'description': description,
            'category_id': category_id
        }
        products[product_id] = product
        product_id_counter += 1

        return jsonify(product), 201


# Route for handling individual product retrieval, updates, and deletion
@app.route('/products/<int:product_id>', methods=['GET', 'PUT', 'DELETE'])
def product_details(product_id):
    product = products.get(product_id)
    if not product:
        return jsonify({'message': 'Product not found'}), 404

    # If it's a GET request, return the product details
    if request.method == 'GET':
        return jsonify(product)

    # If it's a PUT request, update the product details
    if request.method == 'PUT':
        data = request.get_json()
        name = data.get('name')
        description = data.get('description')
        category_id = data.get('category_id')

        # Check if any updates are provided
        if not name and not description and not category_id:
            return jsonify({'message': 'No updates provided'}), 400

        # Check if the provided category_id is valid
        if category_id and category_id not in categories:
            return jsonify({'message': 'Invalid category_id'}), 400

        # Update the product with the new details
        if name:
            product['name'] = name
        if description:
            product['description'] = description
        if category_id:
            product['category_id'] = category_id

        return jsonify(product)

    # If it's a DELETE request, delete the product
    if request.method == 'DELETE':
        del products[product_id]
        return jsonify({'message': 'Product deleted'})


# Route for handling category list retrieval and creation
@app.route('/categories', methods=['GET', 'POST'])
def categories_list():
    global category_id_counter

    # If it's a GET request, return the list of all categories
    if request.method == 'GET':
        return jsonify(list(categories.values()))

    # If it's a POST request, create a new category with the given name
    if request.method == 'POST':
        data = request.get_json()
        name = data.get('name')

        # Check if the name is provided
        if not name:
            return jsonify({'message': 'Missing name'}), 400

        # Create the new category and store it in the categories dictionary
        category_id = category_id_counter
        category = {
            'id': category_id,
            'name': name
        }
        categories[category_id] = category
        category_id_counter += 1

        return jsonify(category), 201


# Start the Flask application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
