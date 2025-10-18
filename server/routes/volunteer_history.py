from flask import Blueprint, jsonify

history_bp = Blueprint('history', __name__)

volunteer_records = [
    {
        "name": "John Doe",
        "eventName": "Food Drive",
        "date": "2025-09-20",
        "location": "Houston Community Center",
        "description": "Helped distribute meals.",
        "status": "Attended"
    },
    {
        "name": "Jane Smith",
        "eventName": "Beach Cleanup",
        "date": "2025-08-15",
        "location": "Galveston Beach",
        "description": "Collected trash along shoreline.",
        "status": "No-Show"
    }
]

@history_bp.route('/volunteer-history', methods=['GET'])  # Note: /volunteer-history under /api prefix
def get_volunteer_history():
    return jsonify(volunteer_records)