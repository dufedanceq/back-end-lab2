from flask import Flask, jsonify, request
import uuid

app = Flask(__name__)

users = {}

def generate_id():
    return str(uuid.uuid4())

@app.route('/users', methods=['GET'])
def get_all_users():
    return jsonify(list(users.values()))

@app.route('/user', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400
    
    user_id = generate_id()
    new_user = {"id": user_id, "name": data['name']}
    users[user_id] = new_user
    return jsonify(new_user), 201

@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):
    user = users.get(user_id)
    if user:
        return jsonify(user)
    return jsonify({"error": "User not found"}), 404

@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id in users:
        del users[user_id]
        return jsonify({"message": "User deleted"}), 200
    return jsonify({"error": "User not found"}), 404

@app.route('/')
def home():
    return jsonify({"status": "running", "message": "Expense Tracker API"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)