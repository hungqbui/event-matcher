"""
Comprehensive tests for NotificationService with database implementation
Run: pytest tests/new_tests/test_notification_service_db.py -v
"""

import pytest
from sqlalchemy import text
from services.notificationService import NotificationService
from flask import json


class TestGetNotifications:
    """Test fetching notifications"""
    
    def test_get_all_notifications_success(self, app, test_user):
        """Test user can fetch their notifications"""
        with app.app_context():
            engine = app.config['ENGINE']
            
            # Create test notification
            with engine.begin() as conn:
                conn.execute(
                    text(
                    """INSERT INTO notifications (id, user_id, message, type, is_read, created_at)
                    VALUES (9991, :user_id, 'Test notification', 'info', FALSE, NOW())"""),
                    {"user_id": test_user['id']}
                )
            
            response, status = NotificationService.get_notifications(test_user['id'])
            
            assert status == 200
            notifications = response.get_json()
            assert isinstance(notifications, list)
            assert len(notifications) >= 1
            assert any(n['message'] == 'Test notification' for n in notifications)
    
    def test_get_unread_notifications(self, app, test_user):
        """Test fetching only unread notifications"""
        with app.app_context():
            engine = app.config['ENGINE']
            
            # Create test notifications
            with engine.begin() as conn:
                conn.execute(
                    text("""INSERT INTO notifications (id, user_id, message, type, is_read, created_at)
                         VALUES (9992, :user_id, 'Unread notification', 'warning', FALSE, NOW())"""),
                    {"user_id": test_user['id']}
                )
                conn.execute(
                    text("""INSERT INTO notifications (id, user_id, message, type, is_read, created_at)
                         VALUES (9993, :user_id, 'Read notification', 'info', TRUE, NOW())"""),
                    {"user_id": test_user['id']}
                )

            response, status = NotificationService.get_notifications(test_user['id'], unread_only=True)
            
            assert status == 200
            notifications = response.get_json()
            assert all(not n['is_read'] for n in notifications)
    
    def test_get_notifications_empty_list(self, app, test_user):
        """Test fetching notifications returns empty list when none exist"""
        with app.app_context():
            response, status = NotificationService.get_notifications(test_user['id'])
            
            assert status == 200
            notifications = response.get_json()
            assert isinstance(notifications, list)
            assert len(notifications) == 0
    
    def test_get_notifications_invalid_user(self, app):
        """Test fetching notifications for invalid user"""
        with app.app_context():
            response, status = NotificationService.get_notifications(99999)
            
            assert status == 200  # Still returns 200 with empty list
            notifications = response.get_json()
            assert isinstance(notifications, list)
            assert len(notifications) == 0


class TestCreateNotification:
    """Test creating notifications"""
    
    def test_create_notification_success(self, app, test_user):
        """Test creating a notification"""
        with app.app_context():
            data = {
                'user_id': test_user['id'],
                'message': 'New test notification',
                'type': 'success'
            }
            
            response, status = NotificationService.create_notification(data)
            
            assert status == 201
            notification = response.get_json()
            assert notification['message'] == 'New test notification'
            assert notification['type'] == 'success'
            assert notification['is_read'] == False
    
    def test_create_notification_missing_required_fields(self, app):
        """Test create notification fails with missing fields"""
        with app.app_context():
            data = {
                'message': 'Missing user_id'
                # Missing user_id and type
            }
            
            response, status = NotificationService.create_notification(data)
            
            assert status == 400
            json_data = response.get_json()
            assert "missing" in json_data['message'].lower() or "required" in json_data['message'].lower()
    
    def test_create_notification_default_type(self, app, test_user):
        """Test notification creation with default type"""
        with app.app_context():
            data = {
                'user_id': test_user['id'],
                'message': 'Default type notification'
                # Not specifying type
            }
            
            response, status = NotificationService.create_notification(data)
            
            assert status == 201
            notification = response.get_json()
            assert 'type' in notification
            assert notification['type'] == 'info'
    
    def test_create_notification_all_types(self, app, test_user):
        """Test creating notifications with different types"""
        with app.app_context():
            types = ['info', 'success', 'warning', 'error']
            
            for notif_type in types:
                data = {
                    'user_id': test_user['id'],
                    'message': f'Test {notif_type} notification',
                    'type': notif_type
                }
                
                response, status = NotificationService.create_notification(data)
                
                assert status == 201
                notification = response.get_json()
                assert notification['type'] == notif_type


class TestMarkAsRead:
    """Test marking notifications as read"""
    
    def test_mark_notification_as_read_success(self, app, test_user):
        """Test marking a notification as read"""
        with app.app_context():
            engine = app.config['ENGINE']
            
            # Create unread notification
            with engine.begin() as conn:
                conn.execute(text("""
                    INSERT INTO notifications (id, user_id, message, type, is_read, created_at) 
                    VALUES (9994, :user_id, 'Unread notification', 'info', FALSE, NOW())
                """), {"user_id": test_user['id']})

            response, status = NotificationService.mark_as_read(9994, test_user['id'])
            
            assert status == 200
            json_data = response.get_json()
            assert "marked as read" in json_data['message'].lower()
    
    def test_mark_notification_not_found(self, app, test_user):
        """Test marking non-existent notification"""
        with app.app_context():
            response, status = NotificationService.mark_as_read(99999, test_user['id'])
            
            assert status == 404
            json_data = response.get_json()
            assert "not found" in json_data['message'].lower()
    
    def test_mark_notification_unauthorized(self, app, test_user, test_user2):
        """Test user cannot mark another user's notification"""
        with app.app_context():
            engine = app.config['ENGINE']
            
            # Create notification for different user
            with engine.begin() as conn:
                conn.execute(
                    text("""INSERT INTO notifications (id, user_id, message, type, is_read, created_at) 
                    VALUES (9995, :other_user_id, 'Other user notification', 'info', FALSE, NOW())"""),
                    {"other_user_id": test_user2['id']}
                )
            
            response, status = NotificationService.mark_as_read(9995, test_user['id'])
            
            assert status == 403
            json_data = response.get_json()
            assert "unauthorized" in json_data['message'].lower()


class TestDeleteNotification:
    """Test deleting notifications"""
    
    def test_delete_notification_success(self, app, test_user):
        """Test user can delete their notification"""
        with app.app_context():
            engine = app.config['ENGINE']
            
            # Create notification
            with engine.begin() as conn:
                conn.execute(
                    text("""INSERT INTO notifications (id, user_id, message, type, is_read, created_at) 
                    VALUES (9996, :user_id, 'To be deleted', 'info', FALSE, NOW())"""),
                    {"user_id": test_user['id']}
                )
            
            response, status = NotificationService.delete_notification(9996, test_user['id'])
            
            assert status == 200
            json_data = response.get_json()
            assert "deleted" in json_data['message'].lower()
    
    def test_delete_notification_not_found(self, app, test_user):
        """Test deleting non-existent notification"""
        with app.app_context():
            response, status = NotificationService.delete_notification(99999, test_user['id'])
            
            assert status == 404
            json_data = response.get_json()
            assert "not found" in json_data['message'].lower()
    
    def test_delete_notification_unauthorized(self, app, test_user, test_user2):
        """Test user cannot delete another user's notification"""
        with app.app_context():
            engine = app.config['ENGINE']
            
            # Create notification for different user
            with engine.begin() as conn:
                conn.execute(
                    text("""INSERT INTO notifications (id, user_id, message, type, is_read, created_at) 
                    VALUES (9997, :other_user_id, 'Other user notification', 'info', FALSE, NOW())"""),
                    {"other_user_id": test_user2['id']}
                )
            
            response, status = NotificationService.delete_notification(9997, test_user['id'])
            
            assert status == 403
            json_data = response.get_json()
            assert "unauthorized" in json_data['message'].lower()


class TestBulkOperations:
    """Test bulk notification operations"""
    
    def test_mark_all_as_read(self, app, test_user):
        """Test marking all notifications as read"""
        with app.app_context():
            engine = app.config['ENGINE']
            
            # Create multiple unread notifications
            with engine.begin() as conn:
                conn.execute(
                    text("""INSERT INTO notifications (user_id, message, type, is_read, created_at) 
                    VALUES (:user_id, 'Notification 1', 'info', FALSE, NOW()), 
                           (:user_id, 'Notification 2', 'info', FALSE, NOW())"""),
                    {"user_id": test_user['id']}
                )
            
            response, status = NotificationService.mark_all_as_read(test_user['id'])
            
            assert status == 200
            json_data = response.get_json()
            assert "notifications marked as read" in json_data['message'].lower()
    
    def test_delete_all_read_notifications(self, app, test_user):
        """Test deleting all read notifications"""
        with app.app_context():
            engine = app.config['ENGINE']
            
            # Create read and unread notifications
            with engine.begin() as conn:
                conn.execute(
                    text("""INSERT INTO notifications (user_id, message, type, is_read, created_at) 
                    VALUES (:user_id, 'Read notification', 'info', TRUE, NOW()), 
                           (:user_id, 'Unread notification', 'info', FALSE, NOW())"""),
                    {"user_id": test_user['id']}
                )

            
            response, status = NotificationService.delete_all_read(test_user['id'])
            
            assert status == 200
            json_data = response.get_json()
            assert "deleted" in json_data['message'].lower()
            
            # Verify unread notification still exists
            response, status = NotificationService.get_notifications(test_user['id'])
            notifications = response.get_json()
            assert len(notifications) >= 1
            assert all(not n['is_read'] for n in notifications)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
