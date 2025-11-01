from sqlalchemy import text
from flask import jsonify, current_app
from datetime import datetime

class NotificationService:
    """Service for managing notifications"""
    
    @staticmethod
    def get_notifications(user_id=None, unread_only=False):
        """Get notifications, optionally filtered by user and read status"""
        engine = current_app.config["ENGINE"]
        
        with engine.connect() as conn:
            if unread_only:
                result = conn.execute(text("""
                    SELECT id, user_id, type, message, is_read, created_at 
                    FROM notifications
                    WHERE user_id = :user_id AND is_read = FALSE
                    ORDER BY created_at DESC
                """), {"user_id": user_id}).mappings().all()
            else:
                result = conn.execute(text("""
                    SELECT id, user_id, type, message, is_read, created_at 
                    FROM notifications
                    WHERE user_id = :user_id
                    ORDER BY created_at DESC
                """), {"user_id": user_id}).mappings().all()
        return jsonify([dict(row) for row in result]), 200
    
    @staticmethod
    def get_all_notifications(user_id=None):
        """Get all notifications, optionally filtered by user"""
        return NotificationService.get_notifications(user_id, unread_only=False)

    
    @staticmethod
    def get_unread_notifications(user_id=None):
        """Get only unread notifications"""
        return NotificationService.get_notifications(user_id, unread_only=True)
    
    @staticmethod
    def get_notification_by_id(notification_id):
        """Get a specific notification by ID"""
        engine = current_app.config["ENGINE"]
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM notifications WHERE id = :notification_id"), {"notification_id": notification_id}).mappings().first()
        
            if not result:
                return jsonify({'success': False, 'message': 'Notification not found'}), 404
            return jsonify({'success': True, 'notification': dict(result)}), 200
    
    @staticmethod
    def mark_as_read(notification_id, user_id=None):
        """Mark a notification as read"""
        engine = current_app.config["ENGINE"]
        with engine.connect() as conn:
            # Check if notification exists and belongs to user if user_id provided
            if user_id is not None:
                # First check if notification exists at all
                exists = conn.execute(text("SELECT id, user_id FROM notifications WHERE id = :id"), 
                                    {"id": notification_id}).mappings().first()
                if not exists:
                    return jsonify({'success': False, 'message': 'Notification not found'}), 404
                # Then check if it belongs to the user
                if exists['user_id'] != user_id:
                    return jsonify({'success': False, 'message': 'Unauthorized'}), 403
            
            result = conn.execute(text("UPDATE notifications SET is_read = TRUE WHERE id = :notification_id"), {"notification_id": notification_id})
            conn.commit()
            affected = result.rowcount
            
        if affected == 0:
            return jsonify({'success': False, 'message': 'Notification not found'}), 404
        return jsonify({'success': True, 'message': 'Notification marked as read'}), 200
    
    @staticmethod
    def mark_all_as_read(user_id=None):
        """Mark all notifications as read"""
        engine = current_app.config["ENGINE"]
        with engine.connect() as conn:
            result = conn.execute(text("UPDATE notifications SET is_read = TRUE WHERE user_id = :user_id"), {"user_id": user_id})
            conn.commit()
            affected = result.rowcount
        return jsonify({'success': True, 'message': f'{affected} notifications marked as read'}), 200
    
    @staticmethod
    def create_notification(data):
        """Create a new notification"""
        # Validate required fields
        required_fields = ['user_id', 'message']
        for f in required_fields:
            if f not in data:
                return jsonify({'message': f'Missing field: {f}'}), 400

        engine = current_app.config["ENGINE"]
        with engine.connect() as conn:
            notification_type = data.get('type', 'info')
            result = conn.execute(text("""
                INSERT INTO notifications (user_id, type, message)
                VALUES (:user_id, :type, :message)
            """), {"user_id": data['user_id'], "type": notification_type, "message": data['message']})
            conn.commit()
            new_id = result.lastrowid
        return jsonify({
            'id': new_id, 
            'type': notification_type, 
            'message': data['message'],
            'user_id': data['user_id'],
            'is_read': False
        }), 201
    
    @staticmethod
    def delete_notification(notification_id, user_id=None):
        """Delete a notification"""
        engine = current_app.config["ENGINE"]
        with engine.connect() as conn:
            # Check if notification belongs to user if user_id provided
            if user_id is not None:
                # First check if notification exists at all
                exists = conn.execute(text("SELECT id, user_id FROM notifications WHERE id = :id"), 
                                    {"id": notification_id}).mappings().first()
                if not exists:
                    return jsonify({'success': False, 'message': 'Notification not found'}), 404
                # Then check if it belongs to the user
                if exists['user_id'] != user_id:
                    return jsonify({'success': False, 'message': 'Unauthorized'}), 403
            
            result = conn.execute(text("DELETE FROM notifications WHERE id = :notification_id"), {"notification_id": notification_id})
            conn.commit()
            affected = result.rowcount
        if affected == 0:
            return jsonify({'success': False, 'message': 'Notification not found'}), 404
        return jsonify({'success': True, 'message': 'Notification deleted'}), 200
    
    @staticmethod
    def delete_all_read_notifications(user_id=None):
        """Delete all read notifications"""
        engine = current_app.config["ENGINE"]
        with engine.connect() as conn:
            result = conn.execute(text("DELETE FROM notifications WHERE user_id = :user_id AND is_read = TRUE"), {"user_id": user_id})
            conn.commit()
            deleted = result.rowcount
        return jsonify({'success': True, 'message': f'{deleted} notifications deleted'}), 200
    
    @staticmethod
    def delete_all_read(user_id=None):
        """Alias for delete_all_read_notifications"""
        return NotificationService.delete_all_read_notifications(user_id)
    
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
            counts = dict(result.mappings().first())
        counts['read'] = counts['total'] - counts['unread']
        return jsonify(counts), 200
