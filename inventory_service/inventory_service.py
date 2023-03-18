from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory inventory storage
inventory = {}
inventory_id_counter = 1


# Route for getting the list of all inventory items
@app.route('/inventory', methods=['GET'])
def inventory_list():
    return jsonify(list(inventory.values()))


# Route for handling the retrieval and updating of a specific product's inventory
@app.route('/inventory/<int:product_id>', methods=['GET', 'PUT'])
def product_inventory(product_id):
    inv = inventory.get(product_id)

    # If it's a GET request, return the inventory details for the specified product_id
    if request.method == 'GET':
        if not inv:
            return jsonify({'message': 'Inventory not found'}), 404
        return jsonify(inv)

    # If it's a PUT request, update the inventory for the specified product_id
    if request.method == 'PUT':
        data = request.get_json()
        quantity = data.get('quantity')

        # Check if the quantity is present in the request data
        if quantity is None:
            return jsonify({'message': 'Missing quantity'}), 400

        # If the inventory for the product_id doesn't exist, create a new entry
        if not inv:
            inv = {
                'product_id': product_id,
                'quantity': quantity
            }
            inventory[product_id] = inv
        else:
            # If the inventory for the product_id exists, update the quantity
            inv['quantity'] = quantity

        return jsonify(inv)


# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003)
