# auth_microservice.py
from flask import Flask, request, jsonify

app = Flask(__name__)
users = []

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

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
