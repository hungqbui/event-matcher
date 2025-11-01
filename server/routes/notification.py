from flask import Blueprint, request
from ..services.notificationService import NotificationService

bp = Blueprint('notifications', __name__)


@bp.route('/notifications', methods=['GET'])
def get_notifications():
    """Get all notifications for the user"""
    # Check if we want unread only
    user_id = request.args.get('user_id')  # for now passed in query string
    print("hit")
    if not user_id:
        return {'success': False, 'error': 'Missing user_id'}, 400

    unread_only = request.args.get('unread', '').lower() == 'true'

    if unread_only:
        return NotificationService.get_unread_notifications(user_id)
    return NotificationService.get_all_notifications(user_id)


@bp.route('/notifications/<notification_id>', methods=['GET'])
def get_notification(notification_id):
    """Get a specific notification"""
    return NotificationService.get_notification_by_id(notification_id)


@bp.route('/notifications/count', methods=['GET'])
def get_notification_count():
    """Get notification counts"""
    user_id = request.args.get('user_id')
    if not user_id:
        return {'success': False, 'error': 'Missing user_id'}, 400
    return NotificationService.get_notification_count(user_id)


@bp.route('/notifications/<notification_id>/read', methods=['PUT'])
def mark_as_read(notification_id):
    """Mark a specific notification as read"""
    return NotificationService.mark_as_read(notification_id)


@bp.route('/notifications/read-all', methods=['PUT'])
def mark_all_as_read():
    """Mark all notifications as read"""
    user_id = request.args.get('user_id')
    if not user_id:
        return {'success': False, 'error': 'Missing user_id'}, 400
    return NotificationService.mark_all_as_read(user_id)


@bp.route('/notifications/<notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    """Delete a specific notification"""
    return NotificationService.delete_notification(notification_id)


@bp.route('/notifications/read', methods=['DELETE'])
def delete_all_read():
    """Delete all read notifications"""
    user_id = request.args.get('user_id')
    if not user_id:
        return {'success': False, 'error': 'Missing user_id'}, 400
    return NotificationService.delete_all_read_notifications(user_id)


@bp.route('/notifications', methods=['POST'])
def create_notification():
    """Create a new notification"""
    data = request.get_json()
    if not data or 'user_id' not in data or 'message' not in data:
        return {'success': False, 'error': 'Missing user_id or message'}, 400
    return NotificationService.create_notification(data)