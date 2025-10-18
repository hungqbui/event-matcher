from flask import Blueprint, jsonify, request
import re

bp = Blueprint('auth', __name__)

users = [{"email": "test@example.com", "password": "1234", "name": "Test User"}]

@bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    # Basic field presence validation
    required_fields = ["name", "email", "password", "state", "skills"]
    for field in required_fields:
        if field not in data or not data[field]:
            return jsonify({"message": f"{field} is required"}), 400

    # Email format check
    if not re.match(r"[^@]+@[^@]+\.[^@]+", data["email"]):
        return jsonify({"message": "Invalid email format"}), 400

    # Password length check
    if len(data["password"]) < 6:
        return jsonify({"message": "Password must be at least 6 characters long"}), 400

    # Duplicate email check
    for user in users:
        if user["email"] == data["email"]:
            return jsonify({"message": "Email already exists"}), 400

    new_user = data
    users.append(new_user)

    return jsonify({"message": "Signup successful", "user": new_user}), 201


@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    # Required field validation
    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400

    for user in users:
        if user["email"] == email and user["password"] == password:
            return jsonify({"message": "Login successful", "name": user["name"]}), 200

    return jsonify({"message": "Invalid credentials"}), 401
