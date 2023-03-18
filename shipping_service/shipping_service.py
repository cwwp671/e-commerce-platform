from flask import Flask, jsonify, request

app = Flask(__name__)

# In-memory shipping provider storage
shipping_providers = {
    'FedEx': {'base_rate': 5.0, 'rate_per_kg': 1.0},
    'UPS': {'base_rate': 4.5, 'rate_per_kg': 1.5},
    'DHL': {'base_rate': 6.0, 'rate_per_kg': 0.8},
}


# Endpoint to get a list of available shipping providers
@app.route('/shipping/providers', methods=['GET'])
def shipping_providers_list():
    return jsonify(list(shipping_providers.keys()))


# Endpoint to calculate shipping costs based on provider and package weight
@app.route('/shipping/calculate', methods=['POST'])
def shipping_calculate():
    data = request.get_json()
    provider_name = data.get('provider')
    weight = data.get('weight')

    # Check if provider name and weight are provided
    if not provider_name or weight is None:
        return jsonify({'message': 'Missing provider or weight'}), 400

    # Get shipping provider information
    provider = shipping_providers.get(provider_name)
    if not provider:
        return jsonify({'message': 'Invalid provider'}), 400

    # Calculate shipping cost based on provider rates and package weight
    cost = provider['base_rate'] + weight * provider['rate_per_kg']
    return jsonify({'provider': provider_name, 'cost': cost})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005)
