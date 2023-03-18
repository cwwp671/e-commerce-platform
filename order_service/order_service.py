from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory order storage
orders = {}
order_id_counter = 1


# Route for handling the retrieval and creation of orders
@app.route('/orders', methods=['GET', 'POST'])
def orders_list():
    global order_id_counter

    # If it's a GET request, return the list of all orders
    if request.method == 'GET':
        return jsonify(list(orders.values()))

    # If it's a POST request, create a new order
    if request.method == 'POST':
        data = request.get_json()
        user_id = data.get('user_id')
        items = data.get('items')

        # Check if user_id and items are present in the request data
        if not user_id or not items:
            return jsonify({'message': 'Missing user_id or items'}), 400

        # TODO: validate the items and user_id

        # Create a new order and add it to the in-memory storage
        order_id = order_id_counter
        order = {
            'id': order_id,
            'user_id': user_id,
            'items': items,
            'status': 'created'
        }
        orders[order_id] = order
        order_id_counter += 1

        return jsonify(order), 201


# Route for handling the retrieval, update, and deletion of a specific order
@app.route('/orders/<int:order_id>', methods=['GET', 'PUT', 'DELETE'])
def order_details(order_id):
    order = orders.get(order_id)

    # Check if the order exists
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    # If it's a GET request, return the order details
    if request.method == 'GET':
        return jsonify(order)

    # If it's a PUT request, update the order status
    if request.method == 'PUT':
        data = request.get_json()
        status = data.get('status')

        # Check if the status is present in the request data
        if not status:
            return jsonify({'message': 'Missing status'}), 400

        # Update the order status
        order['status'] = status
        return jsonify(order)

    # If it's a DELETE request, remove the order from in-memory storage
    if request.method == 'DELETE':
        del orders[order_id]
        return jsonify({'message': 'Order deleted'})


# Route for handling the payment processing for an order
@app.route('/payment', methods=['POST'])
def payment():
    data = request.get_json()
    order_id = data.get('order_id')
    payment_info = data.get('payment_info')

    # Check if order_id and payment_info are present in the request data
    if not order_id or not payment_info:
        return jsonify({'message': 'Missing order_id or payment_info'}), 400

    order = orders.get(order_id)

    # Check if the order exists
    if not order:
        return jsonify({'message': 'Order not found'}), 404

    # TODO: process the payment using a payment provider

    # Update the order status to 'paid'
    order['status'] = 'paid'
    return jsonify({'message': 'Payment processed'})


# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
