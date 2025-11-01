from sqlalchemy import text
from flask import jsonify, current_app
from datetime import datetime

class NotificationService:
    """Service for managing notifications"""
    
    @staticmethod
    def get_all_notifications(user_id=None):
        """Get all notifications, optionally filtered by user"""
        engine = current_app.config["ENGINE"]
        
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id, user_id, type, message, is_read, created_at 
                FROM notifications
                WHERE user_id = :user_id
            """), {"user_id": user_id}).mappings().all()
        return jsonify(list(result)), 200

    
    @staticmethod
    def get_unread_notifications(user_id=None):
        """Get only unread notifications"""

        engine = current_app.config["ENGINE"]
        with engine.connect() as conn:

            result = conn.execute(text("""
                SELECT id, user_id, type, message, is_read, created_at 
                FROM notifications
                WHERE user_id = :user_id AND is_read = FALSE
                ORDER BY created_at DESC
            """), {"user_id": user_id}).mappings().all()
        return jsonify(list(result)), 200
    
    @staticmethod
    def get_notification_by_id(notification_id):
        """Get a specific notification by ID"""

        engine = current_app.config["ENGINE"]
        with engine.connect() as conn:

            result = conn.execute(text("SELECT * FROM notifications WHERE id = :notification_id"), {"notification_id": notification_id}).mappings().first()
        
            if not result:
                return jsonify({'success': False, 'error': 'Notification not found'}), 404
            return jsonify({'success': True, 'notification': result})
    
    @staticmethod
    def mark_as_read(notification_id):
        """Mark a notification as read"""
        engine = current_app.config["ENGINE"]
        with engine.connect() as conn:
            result = conn.execute(text("UPDATE notifications SET is_read = TRUE WHERE id = :notification_id"), {"notification_id": notification_id})
            affected = result.rowcount
        if affected == 0:
            return jsonify({'success': False, 'error': 'Notification not found'}), 404
        return jsonify({'success': True, 'message': 'Notification marked as read'})
    
    @staticmethod
    def mark_all_as_read(user_id=None):
        """Mark all notifications as read"""
        # In a real app, you'd filter by user_id
        engine = current_app.config["ENGINE"]
        with engine.connect() as conn:
            result = conn.execute("UPDATE notifications SET is_read = TRUE WHERE user_id = :user_id", {"user_id": user_id})
            affected = result.rowcount
        if affected == 0:
            return jsonify({'success': False, 'error': 'No notifications found'}), 404
        return jsonify({'success': True, 'message': 'All notifications marked as read'})
    
    @staticmethod
    def create_notification(data):
        """Create a new notification"""
        # Validate required fields
        required_fields = ['user_id', 'message']
        for f in required_fields:
            if f not in data:
                return jsonify({'success': False, 'error': f'Missing field: {f}'}), 400

        engine = current_app.config["ENGINE"]
        with engine.connect() as conn:
            result = conn.execute(text("""
                INSERT INTO notifications (user_id, type, message)
                VALUES (:user_id, :type, :message)
            """), {"user_id": data['user_id'], "type": data.get('type', 'info'), "message": data['message']})
            conn.commit()
            new_id = result.lastrowid
        return jsonify({'success': True, 'id': new_id}), 201
    
    @staticmethod
    def delete_notification(notification_id):
        """Delete a notification"""
        engine = current_app.config["ENGINE"]
        with engine.connect() as conn:
            result = conn.execute(text("DELETE FROM notifications WHERE id = :notification_id"), {"notification_id": notification_id})
            conn.commit()
            affected = result.rowcount
        if affected == 0:
            return jsonify({'success': False, 'error': 'Notification not found'}), 404
        return jsonify({'success': True, 'message': 'Notification deleted'})
    
    @staticmethod
    def delete_all_read_notifications(user_id=None):
        """Delete all read notifications"""
        # In a real app, you'd filter by user_id
        engine = current_app.config["ENGINE"]
        with engine.connect() as conn:
            result = conn.execute(text("DELETE FROM notifications WHERE user_id = :user_id AND is_read = TRUE"), {"user_id": user_id})
            conn.commit()
            deleted = result.rowcount
        return jsonify({'success': True, 'message': f'{deleted} notifications deleted'})
    
    @staticmethod
    def get_notification_count(user_id=None):
        """Get notification counts"""
        engine = current_app.config["ENGINE"]
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT 
                    COUNT(*) AS total,
                    SUM(CASE WHEN is_read = FALSE THEN 1 ELSE 0 END) AS unread
            FROM notifications
            WHERE user_id = :user_id
        """), {"user_id": user_id})
        counts = result.mappings().first()
        conn.close()
        counts['read'] = counts['total'] - counts['unread']
        return jsonify(counts)
