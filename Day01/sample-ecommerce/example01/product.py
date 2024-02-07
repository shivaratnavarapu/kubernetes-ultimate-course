# combined_microservices.py
from flask import Flask, request, jsonify

app = Flask(__name__)
users = []
products = []

# Authentication Endpoints
@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    users.append(data)
    return jsonify({'message': 'User registered successfully'})

@app.route('/authenticate', methods=['POST'])
def authenticate_user():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    for user in users:
        if user['username'] == username and user['password'] == password:
            return jsonify({'message': 'Authentication successful'})
    
    return jsonify({'message': 'Authentication failed'})

# Product Catalog Endpoints
@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.get_json()
    products.append(data)
    return jsonify({'message': 'Product added successfully'})

@app.route('/get_products', methods=['GET'])
def get_products():
    return jsonify({'products': products})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)  # Run on port 5002

