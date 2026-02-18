from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage
users = {}
user_id_counter = 1


# GET all users
@app.route('/users', methods=['GET'])
def get_users():
    return jsonify(users), 200


# GET single user
@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    if user_id in users:
        return jsonify(users[user_id]), 200
    return jsonify({"error": "User not found"}), 404


# POST - create user
@app.route('/users', methods=['POST'])
def create_user():
    global user_id_counter
    data = request.json

    if not data or "name" not in data or "email" not in data:
        return jsonify({"error": "Invalid data"}), 400

    users[user_id_counter] = {
        "id": user_id_counter,
        "name": data["name"],
        "email": data["email"]
    }

    user_id_counter += 1
    return jsonify({"message": "User created"}), 201


# PUT - update user
@app.route('/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    data = request.json
    users[user_id]["name"] = data.get("name", users[user_id]["name"])
    users[user_id]["email"] = data.get("email", users[user_id]["email"])

    return jsonify({"message": "User updated"}), 200


# DELETE user
@app.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    del users[user_id]
    return jsonify({"message": "User deleted"}), 200


if __name__ == '__main__':
    app.run(debug=True)
