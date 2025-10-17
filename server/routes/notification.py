from flask import Blueprint, jsonify, request

bp = Blueprint('notifications', __name__)

# In-memory storage for demo purposes
# In production, you'd use a proper database
notifications_db = [
    {
        "id": 1,
        "message": "New event assignment: Community Food Drive",
        "read": False
    },
    {
        "id": 2,
        "message": "Event update: Beach cleanup location changed",
        "read": False
    },
    {
        "id": 3,
        "message": "Reminder: Community Garden Build tomorrow",
        "read": True
    }
]

next_id = 4  # Track next available ID


@bp.route('/notifications', methods=['GET'])
def get_notifications():
    """Get all notifications for the user"""
    return jsonify(notifications_db)


@bp.route('/notifications/<int:notification_id>/read', methods=['PUT'])
def mark_as_read(notification_id):
    """Mark a specific notification as read"""
    for notification in notifications_db:
        if notification['id'] == notification_id:
            notification['read'] = True
            return jsonify({"success": True, "notification": notification})
    
    return jsonify({"success": False, "error": "Notification not found"}), 404


@bp.route('/notifications/<int:notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    """Delete a specific notification"""
    global notifications_db
    
    initial_length = len(notifications_db)
    notifications_db = [n for n in notifications_db if n['id'] != notification_id]
    
    if len(notifications_db) < initial_length:
        return jsonify({"success": True})
    
    return jsonify({"success": False, "error": "Notification not found"}), 404


@bp.route('/notifications', methods=['POST'])
def create_notification():
    """Create a new notification"""
    global next_id
    
    data = request.get_json()
    
    if not data or 'message' not in data:
        return jsonify({"success": False, "error": "Message is required"}), 400
    
    new_notification = {
        "id": next_id,
        "message": data['message'],
        "read": False
    }
    
    notifications_db.append(new_notification)
    next_id += 1
    
    return jsonify({"success": True, "notification": new_notification}), 201