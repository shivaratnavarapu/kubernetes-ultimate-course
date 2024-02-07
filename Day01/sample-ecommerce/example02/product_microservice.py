# product_microservice.py
from flask import Flask, request, jsonify

app = Flask(__name__)
products = []

@app.route('/add_product', methods=['POST'])
def add_product():
    data = request.get_json()
    products.append(data)
    return jsonify({'message': 'Product added successfully'})

@app.route('/get_products', methods=['GET'])
def get_products():
    return jsonify({'products': products})

if __name__ == '__main__':
    app.run(port=5001)

