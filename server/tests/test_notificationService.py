import unittest
import sys
import os
from flask import json

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import app
from services.notificationService import NotificationService, MOCK_NOTIFICATIONS


class TestNotificationService(unittest.TestCase):
    """Unit tests for NotificationService"""
    
    def setUp(self):
        """Set up test data before each test"""
        # Create Flask app context
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Save original state
        self.original_notifications = MOCK_NOTIFICATIONS.copy()
        
        # Clear and reset to known state
        MOCK_NOTIFICATIONS.clear()
        MOCK_NOTIFICATIONS.update({
            '1': {
                'id': 1,
                'message': 'Test notification 1',
                'type': 'info',
                'read': False,
                'timestamp': '2025-10-15T10:00:00Z'
            },
            '2': {
                'id': 2,
                'message': 'Test notification 2',
                'type': 'warning',
                'read': False,
                'timestamp': '2025-10-16T14:30:00Z'
            },
            '3': {
                'id': 3,
                'message': 'Test notification 3',
                'type': 'info',
                'read': True,
                'timestamp': '2025-10-17T09:15:00Z'
            }
        })

    def tearDown(self):
        """Restore original state after each test"""
        MOCK_NOTIFICATIONS.clear()
        MOCK_NOTIFICATIONS.update(self.original_notifications)
        # Pop Flask app context
        self.app_context.pop()

    # ========== Get All Notifications Tests ==========
    
    def test_get_all_notifications(self):
        """Test fetching all notifications"""
        response = NotificationService.get_all_notifications()
        data = json.loads(response.data)
        
        self.assertEqual(len(data), 3)
        self.assertIsInstance(data, list)

    def test_get_all_notifications_structure(self):
        """Test notification structure"""
        response = NotificationService.get_all_notifications()
        data = json.loads(response.data)
        
        notification = data[0]
        self.assertIn('id', notification)
        self.assertIn('message', notification)
        self.assertIn('type', notification)
        self.assertIn('read', notification)
        self.assertIn('timestamp', notification)

    # ========== Get Unread Notifications Tests ==========
    
    def test_get_unread_notifications(self):
        """Test fetching only unread notifications"""
        response = NotificationService.get_unread_notifications()
        data = json.loads(response.data)
        
        self.assertEqual(len(data), 2)
        for notification in data:
            self.assertFalse(notification['read'])

    def test_get_unread_notifications_when_all_read(self):
        """Test fetching unread when all are read"""
        # Mark all as read
        for notification in MOCK_NOTIFICATIONS.values():
            notification['read'] = True
        
        response = NotificationService.get_unread_notifications()
        data = json.loads(response.data)
        
        self.assertEqual(len(data), 0)

    # ========== Get Notification By ID Tests ==========
    
    def test_get_notification_by_id_success(self):
        """Test getting a specific notification"""
        result = NotificationService.get_notification_by_id('1')
        if isinstance(result, tuple):
            response, status_code = result
        else:
            response = result
            status_code = 200
        
        data = json.loads(response.data)
        
        self.assertTrue(data['success'])
        self.assertEqual(data['notification']['id'], 1)
        self.assertEqual(data['notification']['message'], 'Test notification 1')

    def test_get_notification_by_id_not_found(self):
        """Test getting a non-existent notification"""
        response, status_code = NotificationService.get_notification_by_id('999')
        data = json.loads(response.data)
        
        self.assertEqual(status_code, 404)
        self.assertFalse(data['success'])
        self.assertIn('not found', data['error'].lower())

    # ========== Mark As Read Tests ==========
    
    def test_mark_as_read_success(self):
        """Test marking a notification as read"""
        # Verify it's unread first
        self.assertFalse(MOCK_NOTIFICATIONS['1']['read'])
        
        result = NotificationService.mark_as_read('1')
        if isinstance(result, tuple):
            response, status_code = result
        else:
            response = result
            status_code = 200
            
        data = json.loads(response.data)
        
        self.assertTrue(data['success'])
        self.assertTrue(data['notification']['read'])
        self.assertTrue(MOCK_NOTIFICATIONS['1']['read'])

    def test_mark_as_read_already_read(self):
        """Test marking an already read notification"""
        # Mark as read first
        MOCK_NOTIFICATIONS['1']['read'] = True
        
        result = NotificationService.mark_as_read('1')
        if isinstance(result, tuple):
            response, status_code = result
        else:
            response = result
            status_code = 200
            
        data = json.loads(response.data)
        
        self.assertTrue(data['success'])
        self.assertTrue(data['notification']['read'])

    def test_mark_as_read_not_found(self):
        """Test marking a non-existent notification as read"""
        response, status_code = NotificationService.mark_as_read('999')
        data = json.loads(response.data)
        
        self.assertEqual(status_code, 404)
        self.assertFalse(data['success'])

    # ========== Mark All As Read Tests ==========
    
    def test_mark_all_as_read(self):
        """Test marking all notifications as read"""
        # Verify some are unread
        self.assertFalse(MOCK_NOTIFICATIONS['1']['read'])
        self.assertFalse(MOCK_NOTIFICATIONS['2']['read'])
        
        response = NotificationService.mark_all_as_read()
        data = json.loads(response.data)
        
        self.assertTrue(data['success'])
        
        # Verify all are now read
        for notification in MOCK_NOTIFICATIONS.values():
            self.assertTrue(notification['read'])

    def test_mark_all_as_read_when_already_read(self):
        """Test marking all as read when all are already read"""
        # Mark all as read first
        for notification in MOCK_NOTIFICATIONS.values():
            notification['read'] = True
        
        response = NotificationService.mark_all_as_read()
        data = json.loads(response.data)
        
        self.assertTrue(data['success'])

    # ========== Create Notification Tests ==========
    
    def test_create_notification_with_all_fields(self):
        """Test creating a notification with all fields"""
        notification_data = {
            'message': 'New test notification',
            'type': 'success'
        }
        
        response, status_code = NotificationService.create_notification(notification_data)
        data = json.loads(response.data)
        
        self.assertEqual(status_code, 201)
        self.assertTrue(data['success'])
        self.assertEqual(data['notification']['message'], 'New test notification')
        self.assertEqual(data['notification']['type'], 'success')
        self.assertFalse(data['notification']['read'])
        self.assertIn('timestamp', data['notification'])
        
        # Verify it was added to storage
        self.assertEqual(len(MOCK_NOTIFICATIONS), 4)

    def test_create_notification_with_minimum_fields(self):
        """Test creating a notification with only required fields"""
        notification_data = {
            'message': 'Minimal notification'
        }
        
        response, status_code = NotificationService.create_notification(notification_data)
        data = json.loads(response.data)
        
        self.assertEqual(status_code, 201)
        self.assertTrue(data['success'])
        self.assertEqual(data['notification']['message'], 'Minimal notification')
        self.assertEqual(data['notification']['type'], 'info')  # Default value
        self.assertFalse(data['notification']['read'])

    def test_create_notification_missing_message(self):
        """Test creating a notification without required message"""
        notification_data = {
            'type': 'info'
        }
        
        response, status_code = NotificationService.create_notification(notification_data)
        data = json.loads(response.data)
        
        self.assertEqual(status_code, 400)
        self.assertFalse(data['success'])
        self.assertIn('message', data['error'].lower())

    def test_create_notification_generates_unique_id(self):
        """Test that created notifications get unique IDs"""
        notification_data1 = {'message': 'Notification 1'}
        notification_data2 = {'message': 'Notification 2'}
        
        response1, _ = NotificationService.create_notification(notification_data1)
        data1 = json.loads(response1.data)
        
        response2, _ = NotificationService.create_notification(notification_data2)
        data2 = json.loads(response2.data)
        
        self.assertNotEqual(data1['notification']['id'], data2['notification']['id'])
        self.assertEqual(data2['notification']['id'], data1['notification']['id'] + 1)

    # ========== Delete Notification Tests ==========
    
    def test_delete_notification_success(self):
        """Test successfully deleting a notification"""
        # Verify it exists
        self.assertIn('1', MOCK_NOTIFICATIONS)
        
        result = NotificationService.delete_notification('1')
        if isinstance(result, tuple):
            response, status_code = result
        else:
            response = result
            status_code = 200
            
        data = json.loads(response.data)
        
        self.assertEqual(status_code, 200)
        self.assertTrue(data['success'])
        
        # Verify it was deleted
        self.assertNotIn('1', MOCK_NOTIFICATIONS)
        self.assertEqual(len(MOCK_NOTIFICATIONS), 2)

    def test_delete_notification_not_found(self):
        """Test deleting a non-existent notification"""
        response, status_code = NotificationService.delete_notification('999')
        data = json.loads(response.data)
        
        self.assertEqual(status_code, 404)
        self.assertFalse(data['success'])
        
        # Verify nothing was deleted
        self.assertEqual(len(MOCK_NOTIFICATIONS), 3)

    # ========== Delete All Read Notifications Tests ==========
    
    def test_delete_all_read_notifications(self):
        """Test deleting all read notifications"""
        # One notification is already read
        self.assertTrue(MOCK_NOTIFICATIONS['3']['read'])
        
        result = NotificationService.delete_all_read_notifications()
        if isinstance(result, tuple):
            response, status_code = result
        else:
            response = result
            
        data = json.loads(response.data)
        
        self.assertTrue(data['success'])
        self.assertIn('1 notifications deleted', data['message'])
        
        # Verify only unread remain
        self.assertEqual(len(MOCK_NOTIFICATIONS), 2)
        self.assertNotIn('3', MOCK_NOTIFICATIONS)

    def test_delete_all_read_when_none_read(self):
        """Test deleting read notifications when none are read"""
        # Mark all as unread
        for notification in MOCK_NOTIFICATIONS.values():
            notification['read'] = False
        
        result = NotificationService.delete_all_read_notifications()
        if isinstance(result, tuple):
            response, status_code = result
        else:
            response = result
            
        data = json.loads(response.data)
        
        self.assertTrue(data['success'])
        self.assertIn('0 notifications deleted', data['message'])
        self.assertEqual(len(MOCK_NOTIFICATIONS), 3)

    def test_delete_all_read_when_all_read(self):
        """Test deleting all notifications when all are read"""
        # Mark all as read
        for notification in MOCK_NOTIFICATIONS.values():
            notification['read'] = True
        
        result = NotificationService.delete_all_read_notifications()
        if isinstance(result, tuple):
            response, status_code = result
        else:
            response = result
            
        data = json.loads(response.data)
        
        self.assertTrue(data['success'])
        self.assertIn('3 notifications deleted', data['message'])
        self.assertEqual(len(MOCK_NOTIFICATIONS), 0)

    # ========== Get Notification Count Tests ==========
    
    def test_get_notification_count(self):
        """Test getting notification counts"""
        response = NotificationService.get_notification_count()
        data = json.loads(response.data)
        
        self.assertEqual(data['total'], 3)
        self.assertEqual(data['unread'], 2)
        self.assertEqual(data['read'], 1)

    def test_get_notification_count_after_changes(self):
        """Test counts after marking notifications as read"""
        # Mark one as read
        MOCK_NOTIFICATIONS['1']['read'] = True
        
        response = NotificationService.get_notification_count()
        data = json.loads(response.data)
        
        self.assertEqual(data['total'], 3)
        self.assertEqual(data['unread'], 1)
        self.assertEqual(data['read'], 2)

    def test_get_notification_count_empty(self):
        """Test counts when no notifications exist"""
        MOCK_NOTIFICATIONS.clear()
        
        response = NotificationService.get_notification_count()
        data = json.loads(response.data)
        
        self.assertEqual(data['total'], 0)
        self.assertEqual(data['unread'], 0)
        self.assertEqual(data['read'], 0)

    # ========== Integration Tests ==========
    
    def test_create_mark_read_delete_workflow(self):
        """Test a complete workflow: create, mark as read, delete"""
        # Create
        notification_data = {'message': 'Workflow test'}
        response, _ = NotificationService.create_notification(notification_data)
        created_id = str(json.loads(response.data)['notification']['id'])
        
        # Mark as read
        result = NotificationService.mark_as_read(created_id)
        if isinstance(result, tuple):
            response, _ = result
        else:
            response = result
        data = json.loads(response.data)
        self.assertTrue(data['notification']['read'])
        
        # Delete
        NotificationService.delete_notification(created_id)
        self.assertNotIn(created_id, MOCK_NOTIFICATIONS)


if __name__ == '__main__':
    unittest.main()
