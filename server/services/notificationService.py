from flask import jsonify
from datetime import datetime
from ..db.db import get_db_connection

class NotificationService:
    """Service for managing notifications"""
    
    @staticmethod
    def get_all_notifications(user_id=None):
        """Get all notifications, optionally filtered by user"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, user_id, type, message, is_read, created_at 
            FROM notifications
            WHERE user_id = %s
            ORDER BY created_at DESC
        """, (user_id,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result), 200
    
    @staticmethod
    def get_unread_notifications(user_id=None):
        """Get only unread notifications"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT id, user_id, type, message, is_read, created_at 
            FROM notifications
            WHERE user_id = %s AND is_read = FALSE
            ORDER BY created_at DESC
        """, (user_id,))
        result = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(result)
    
    @staticmethod
    def get_notification_by_id(notification_id):
        """Get a specific notification by ID"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM notifications WHERE id = %s", (notification_id,))
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        if not row:
            return jsonify({'success': False, 'error': 'Notification not found'}), 404
        return jsonify({'success': True, 'notification': row})
    
    @staticmethod
    def mark_as_read(notification_id):
        """Mark a notification as read"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE notifications SET is_read = TRUE WHERE id = %s", (notification_id,))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        if affected == 0:
            return jsonify({'success': False, 'error': 'Notification not found'}), 404
        return jsonify({'success': True, 'message': 'Notification marked as read'})
    
    @staticmethod
    def mark_all_as_read(user_id=None):
        """Mark all notifications as read"""
        # In a real app, you'd filter by user_id
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE notifications SET is_read = TRUE WHERE user_id = %s", (user_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'message': 'All notifications marked as read'})
    
    @staticmethod
    def create_notification(data):
        """Create a new notification"""
        # Validate required fields
        required_fields = ['user_id', 'message']
        for f in required_fields:
            if f not in data:
                return jsonify({'success': False, 'error': f'Missing field: {f}'}), 400

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO notifications (user_id, type, message)
            VALUES (%s, %s, %s)
        """, (data['user_id'], data.get('type', 'info'), data['message']))
        conn.commit()
        new_id = cursor.lastrowid
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'id': new_id}), 201
    
    @staticmethod
    def delete_notification(notification_id):
        """Delete a notification"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notifications WHERE id = %s", (notification_id,))
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        if affected == 0:
            return jsonify({'success': False, 'error': 'Notification not found'}), 404
        return jsonify({'success': True, 'message': 'Notification deleted'})
    
    @staticmethod
    def delete_all_read_notifications(user_id=None):
        """Delete all read notifications"""
        # In a real app, you'd filter by user_id
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM notifications WHERE user_id = %s AND is_read = TRUE", (user_id,))
        conn.commit()
        deleted = cursor.rowcount
        cursor.close()
        conn.close()
        return jsonify({'success': True, 'message': f'{deleted} notifications deleted'})
    
    @staticmethod
    def get_notification_count(user_id=None):
        """Get notification counts"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT 
                COUNT(*) AS total,
                SUM(CASE WHEN is_read = FALSE THEN 1 ELSE 0 END) AS unread
            FROM notifications
            WHERE user_id = %s
        """, (user_id,))
        counts = cursor.fetchone()
        cursor.close()
        conn.close()
        counts['read'] = counts['total'] - counts['unread']
        return jsonify(counts)
