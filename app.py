from flask import Flask, jsonify, request
import uuid
from datetime import datetime

app = Flask(__name__)

users = {}
categories = {}
records = {}

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

@app.route('/category', methods=['GET'])
def get_categories():
    return jsonify(list(categories.values()))

@app.route('/category', methods=['POST'])
def create_category():
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({"error": "Name is required"}), 400
    
    cat_id = generate_id()
    new_cat = {"id": cat_id, "name": data['name']}
    categories[cat_id] = new_cat
    return jsonify(new_cat), 201

@app.route('/category', methods=['DELETE'])
def delete_category():
    data = request.get_json(silent=True)
    cat_id = data.get('id') if data else request.args.get('id')
    
    if not cat_id:
        return jsonify({"error": "Category ID is required"}), 400
        
    if cat_id in categories:
        del categories[cat_id]
        return jsonify({"message": "Category deleted"}), 200
    return jsonify({"error": "Category not found"}), 404

@app.route('/record', methods=['POST'])
def create_record():
    data = request.get_json()
    required_fields = ['user_id', 'category_id', 'amount']
    if not data or not all(field in data for field in required_fields):
        return jsonify({"error": "Missing fields: user_id, category_id, amount"}), 400
    
    if data['user_id'] not in users:
        return jsonify({"error": "User does not exist"}), 404
    if data['category_id'] not in categories:
        return jsonify({"error": "Category does not exist"}), 404

    rec_id = generate_id()
    new_record = {
        "id": rec_id,
        "user_id": data['user_id'],
        "category_id": data['category_id'],
        "timestamp": datetime.now().isoformat(),
        "amount": float(data['amount'])
    }
    records[rec_id] = new_record
    return jsonify(new_record), 201

@app.route('/record/<record_id>', methods=['GET'])
def get_record(record_id):
    record = records.get(record_id)
    if record:
        return jsonify(record)
    return jsonify({"error": "Record not found"}), 404

@app.route('/record/<record_id>', methods=['DELETE'])
def delete_record(record_id):
    if record_id in records:
        del records[record_id]
        return jsonify({"message": "Record deleted"}), 200
    return jsonify({"error": "Record not found"}), 404

@app.route('/record', methods=['GET'])
def get_records_filtered():
    user_id = request.args.get('user_id')
    category_id = request.args.get('category_id')

    if not user_id and not category_id:
        return jsonify({"error": "Filter parameters (user_id, category_id) are required"}), 400

    filtered = list(records.values())

    if user_id:
        filtered = [r for r in filtered if r['user_id'] == user_id]
    
    if category_id:
        filtered = [r for r in filtered if r['category_id'] == category_id]

    return jsonify(filtered)

@app.route('/')
def home():
    return jsonify({"status": "running", "message": "Expense Tracker API"})

if __name__ == '__main__':
    app.run(debug=True, port=5000)