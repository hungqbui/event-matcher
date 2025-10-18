from flask import Blueprint, jsonify, request
import re

profile_bp = Blueprint('profile', __name__)

current_profile = {
    "fullName": "John Doe",
    "address1": "123 Main St",
    "address2": "",
    "city": "Houston",
    "state": "TX",
    "zip": "77001",
    "skills": ["Tree Planting", "Food Drives"],
    "preferences": "Prefer outdoor activities",
    "availability": ["2025-10-01", "2025-10-15"]
}

@profile_bp.route('/profile', methods=['GET'])  # Note: /profile under /api prefix
def get_profile():
    return jsonify(current_profile)

@profile_bp.route('/profile', methods=['POST'])
def update_profile():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    # ... (rest of validation code from earlier)