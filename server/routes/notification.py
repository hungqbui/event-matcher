from flask import Blueprint, request
from services.notificationService import NotificationService

bp = Blueprint('notifications', __name__)


@bp.route('/notifications', methods=['GET'])
def get_notifications():
    """Get all notifications for the user"""
    # Check if we want unread only
    unread_only = request.args.get('unread', '').lower() == 'true'
    
    if unread_only:
        return NotificationService.get_unread_notifications()
    return NotificationService.get_all_notifications()


@bp.route('/notifications/<notification_id>', methods=['GET'])
def get_notification(notification_id):
    """Get a specific notification"""
    return NotificationService.get_notification_by_id(notification_id)


@bp.route('/notifications/count', methods=['GET'])
def get_notification_count():
    """Get notification counts"""
    return NotificationService.get_notification_count()


@bp.route('/notifications/<notification_id>/read', methods=['PUT'])
def mark_as_read(notification_id):
    """Mark a specific notification as read"""
    return NotificationService.mark_as_read(notification_id)


@bp.route('/notifications/read-all', methods=['PUT'])
def mark_all_as_read():
    """Mark all notifications as read"""
    return NotificationService.mark_all_as_read()


@bp.route('/notifications/<notification_id>', methods=['DELETE'])
def delete_notification(notification_id):
    """Delete a specific notification"""
    return NotificationService.delete_notification(notification_id)


@bp.route('/notifications/read', methods=['DELETE'])
def delete_all_read():
    """Delete all read notifications"""
    return NotificationService.delete_all_read_notifications()


@bp.route('/notifications', methods=['POST'])
def create_notification():
    """Create a new notification"""
    data = request.get_json()
    return NotificationService.create_notification(data)