# Mock data storage for notifications
MOCK_NOTIFICATIONS = {
    '1': {
        'id': 1,
        'message': 'New event assignment: Community Food Drive',
        'type': 'info',
        'read': False,
        'timestamp': '2025-10-15T10:00:00Z'
    },
    '2': {
        'id': 2,
        'message': 'Event update: Beach cleanup location changed',
        'type': 'warning',
        'read': False,
        'timestamp': '2025-10-16T14:30:00Z'
    },
    '3': {
        'id': 3,
        'message': 'Reminder: Community Garden Build tomorrow',
        'type': 'info',
        'read': True,
        'timestamp': '2025-10-17T09:15:00Z'
    }
}

from flask import jsonify
from datetime import datetime


class NotificationService:
    """Service for managing notifications"""
    
    @staticmethod
    def get_all_notifications(user_id=None):
        """Get all notifications, optionally filtered by user"""
        # In a real app, you'd filter by user_id
        return jsonify(list(MOCK_NOTIFICATIONS.values()))
    
    @staticmethod
    def get_unread_notifications(user_id=None):
        """Get only unread notifications"""
        unread = [n for n in MOCK_NOTIFICATIONS.values() if not n['read']]
        return jsonify(unread)
    
    @staticmethod
    def get_notification_by_id(notification_id):
        """Get a specific notification by ID"""
        if notification_id not in MOCK_NOTIFICATIONS:
            return jsonify({'success': False, 'error': 'Notification not found'}), 404
        
        return jsonify({
            'success': True,
            'notification': MOCK_NOTIFICATIONS[notification_id]
        })
    
    @staticmethod
    def mark_as_read(notification_id):
        """Mark a notification as read"""
        if notification_id not in MOCK_NOTIFICATIONS:
            return jsonify({'success': False, 'error': 'Notification not found'}), 404
        
        MOCK_NOTIFICATIONS[notification_id]['read'] = True
        return jsonify({
            'success': True,
            'notification': MOCK_NOTIFICATIONS[notification_id]
        })
    
    @staticmethod
    def mark_all_as_read(user_id=None):
        """Mark all notifications as read"""
        # In a real app, you'd filter by user_id
        for notification in MOCK_NOTIFICATIONS.values():
            notification['read'] = True
        
        return jsonify({'success': True, 'message': 'All notifications marked as read'})
    
    @staticmethod
    def create_notification(data):
        """Create a new notification"""
        # Validate required fields
        required_fields = ['message']
        for field in required_fields:
            if field not in data:
                return jsonify({
                    'success': False,
                    'error': f'Missing required field: {field}'
                }), 400
        
        # Generate new notification ID
        notification_id = max([int(k) for k in MOCK_NOTIFICATIONS.keys()]) + 1 if MOCK_NOTIFICATIONS else 1
        
        # Create new notification
        new_notification = {
            'id': notification_id,
            'message': data['message'],
            'type': data.get('type', 'info'),  # info, success, warning, error
            'read': False,
            'timestamp': datetime.utcnow().isoformat() + 'Z'
        }
        
        MOCK_NOTIFICATIONS[str(notification_id)] = new_notification
        return jsonify({
            'success': True,
            'notification': new_notification
        }), 201
    
    @staticmethod
    def delete_notification(notification_id):
        """Delete a notification"""
        if notification_id not in MOCK_NOTIFICATIONS:
            return jsonify({'success': False, 'error': 'Notification not found'}), 404
        
        del MOCK_NOTIFICATIONS[notification_id]
        return jsonify({'success': True, 'message': 'Notification deleted successfully'})
    
    @staticmethod
    def delete_all_read_notifications(user_id=None):
        """Delete all read notifications"""
        # In a real app, you'd filter by user_id
        keys_to_delete = [k for k, v in MOCK_NOTIFICATIONS.items() if v['read']]
        
        for key in keys_to_delete:
            del MOCK_NOTIFICATIONS[key]
        
        return jsonify({
            'success': True,
            'message': f'{len(keys_to_delete)} notifications deleted'
        })
    
    @staticmethod
    def get_notification_count(user_id=None):
        """Get notification counts"""
        total = len(MOCK_NOTIFICATIONS)
        unread = len([n for n in MOCK_NOTIFICATIONS.values() if not n['read']])
        
        return jsonify({
            'total': total,
            'unread': unread,
            'read': total - unread
        })
