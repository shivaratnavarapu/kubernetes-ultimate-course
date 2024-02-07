# ui.py
from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register_user():
    username = request.form['username']
    password = request.form['password']
    
    data = {'username': username, 'password': password}
    response = requests.post('http://backend-auth:5000/register', json=data)
    return response.json()['message']

@app.route('/authenticate', methods=['POST'])
def authenticate_user():
    username = request.form['username']
    password = request.form['password']

    data = {'username': username, 'password': password}
    response = requests.post('http://backend-auth:5000/authenticate', json=data)
    return response.json()['message']

@app.route('/add_product', methods=['POST'])
def add_product():
    name = request.form['name']
    price = request.form['price']

    data = {'name': name, 'price': price}
    response = requests.post('http://backend-catalog:5001/add_product', json=data)
    return response.json()['message']

@app.route('/get_products')
def get_products():
    response = requests.get('http://backend-catalog:5001/get_products')
    products = response.json().get('products', [])
    return render_template('products.html', products=products)

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=80)
