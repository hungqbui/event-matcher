"""
Comprehensive tests for ManagerService with database implementation
Run: pytest tests/new_tests/test_manager_service_db.py -v
"""

import pytest
from services.managerService import ManagerEventService
from flask import json


class TestManagerFetchEvents:
    """Test fetching events for managers"""
    
    def test_fetch_events_success(self, app, test_admin, test_event):
        """Test admin can fetch their own events"""
        with app.app_context():
            with app.test_request_context(json={'userId': test_admin['id']}):
                response, status = ManagerEventService.fetch_events()
                
                assert status == 200
                events = response.get_json()
                assert isinstance(events, list)
                assert len(events) >= 1
                assert any(e['id'] == test_event['id'] for e in events)
    
    def test_fetch_events_unauthorized(self, app, test_user):
        """Test non-admin cannot fetch events"""
        with app.app_context():
            with app.test_request_context(json={'userId': test_user['id']}):
                response, status = ManagerEventService.fetch_events()
                
                assert status == 403
                json_data = response.get_json()
                assert "unauthorized" in json_data['message'].lower()
    
    def test_fetch_events_no_user_id(self, app):
        """Test fetch events fails without user ID"""
        with app.app_context():
            with app.test_request_context(json={}):
                response, status = ManagerEventService.fetch_events()
                
                assert status == 400
                json_data = response.get_json()
                assert "user" in json_data['message'].lower()
    
    def test_fetch_events_filter_by_urgency(self, app, test_admin, test_event):
        """Test filtering events by urgency status"""
        with app.app_context():
            with app.test_request_context(json={'userId': test_admin['id']}):
                response, status = ManagerEventService.fetch_events(status='medium')
                
                assert status == 200
                events = response.get_json()
                assert isinstance(events, list)
                if len(events) > 0:
                    assert all(e['urgency'] == 'medium' for e in events)


class TestManagerCreateEvent:
    """Test creating events"""
    
    def test_create_event_success(self, app, test_admin):
        """Test admin can create an event"""
        with app.app_context():
            data = {
                'userId': test_admin['id'],
                'name': 'New Test Event',
                'time': '2024-12-25',
                'description': 'Christmas event',
                'location': 'Community Center',
                'urgency': 'high',
                'img': '/test-image.jpg'
            }
            
            response, status = ManagerEventService.create_event(data)
            
            assert status == 201
            event = response.get_json()
            assert event['name'] == 'New Test Event'
            assert event['description'] == 'Christmas event'
    
    def test_create_event_missing_required_fields(self, app, test_admin):
        """Test create event fails with missing required fields"""
        with app.app_context():
            data = {
                'userId': test_admin['id'],
                'name': 'Incomplete Event'
                # Missing time, description, location
            }
            
            response, status = ManagerEventService.create_event(data)
            
            assert status == 400
            json_data = response.get_json()
            assert "missing" in json_data['message'].lower()
    
    def test_create_event_unauthorized(self, app, test_user):
        """Test non-admin cannot create events"""
        with app.app_context():
            data = {
                'userId': test_user['id'],
                'name': 'Unauthorized Event',
                'time': '2024-12-25',
                'description': 'Should fail',
                'location': 'Nowhere'
            }
            
            response, status = ManagerEventService.create_event(data)
            
            assert status == 403
            json_data = response.get_json()
            assert "unauthorized" in json_data['message'].lower()
    
    def test_create_event_default_urgency(self, app, test_admin):
        """Test event creation uses default urgency when not provided"""
        with app.app_context():
            data = {
                'userId': test_admin['id'],
                'name': 'Default Urgency Event',
                'time': '2024-12-25',
                'description': 'Test default',
                'location': 'Test Location'
            }
            
            response, status = ManagerEventService.create_event(data)
            
            assert status == 201
            event = response.get_json()
            assert 'urgency' in event
            assert event['urgency'] == 'low'


class TestManagerUpdateEvent:
    """Test updating events"""
    
    def test_update_event_success(self, app, test_admin, test_event):
        """Test admin can update their own event"""
        with app.app_context():
            data = {
                'userId': test_admin['id'],
                'name': 'Updated Event Name',
                'date': '2025-01-01',
                'description': 'Updated description',
                'location': 'Updated Location',
                'urgency': 'high'
            }
            
            response, status = ManagerEventService.update_event(test_event['id'], data)
            
            assert status == 200
            event = response.get_json()
            assert event['name'] == 'Updated Event Name'
            assert event['urgency'] == 'high'
    
    def test_update_event_not_found(self, app, test_admin):
        """Test updating non-existent event returns 404"""
        with app.app_context():
            data = {
                'userId': test_admin['id'],
                'name': 'Updated Name'
            }
            
            response, status = ManagerEventService.update_event(99999, data)
            
            assert status == 404
            json_data = response.get_json()
            assert "not found" in json_data['message'].lower()
    
    def test_update_event_unauthorized(self, app, test_user2, test_event):
        """Test non-owner cannot update event"""
        with app.app_context():
            data = {
                'userId': test_user2['id'],
                'name': 'Unauthorized Update'
            }
            
            response, status = ManagerEventService.update_event(test_event['id'], data)
            
            assert status == 403
            json_data = response.get_json()
            assert "unauthorized" in json_data['message'].lower()
    
    def test_update_event_partial_fields(self, app, test_admin, test_event):
        """Test updating only some fields preserves others"""
        with app.app_context():
            data = {
                'userId': test_admin['id'],
                'name': 'Only Name Updated'
                # Not updating other fields
            }
            
            response, status = ManagerEventService.update_event(test_event['id'], data)
            
            assert status == 200
            event = response.get_json()
            assert event['name'] == 'Only Name Updated'
            # Other fields should remain unchanged
            assert event['location'] == test_event['location']


class TestManagerDeleteEvent:
    """Test deleting events"""
    
    def test_delete_event_success(self, app, test_admin, test_event):
        """Test admin can delete their own event"""
        with app.app_context():
            with app.test_request_context(json={'userId': test_admin['id']}):
                response, status = ManagerEventService.delete_event(test_event['id'])
                
                assert status == 200
                json_data = response.get_json()
                assert "deleted" in json_data['message'].lower()
    
    def test_delete_event_not_found(self, app, test_admin):
        """Test deleting non-existent event returns 404"""
        with app.app_context():
            with app.test_request_context(json={'userId': test_admin['id']}):
                response, status = ManagerEventService.delete_event(99999)
                
                assert status == 404
                json_data = response.get_json()
                assert "not found" in json_data['message'].lower()
    
    def test_delete_event_unauthorized(self, app, test_user2, test_event):
        """Test non-owner cannot delete event"""
        with app.app_context():
            with app.test_request_context(json={'userId': test_user2['id']}):
                response, status = ManagerEventService.delete_event(test_event['id'])
                
                assert status == 403
                json_data = response.get_json()
                assert "unauthorized" in json_data['message'].lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
