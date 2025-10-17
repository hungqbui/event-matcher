import unittest
from flask import json

from app import app
from services.managerService import ManagerEventService, MOCK_EVENTS


class TestManagerEventService(unittest.TestCase):
    def setUp(self):
        """Set up test data before each test"""
        # Create Flask app context
        self.app = app
        self.app_context = self.app.app_context()
        self.app_context.push()
        
        # Save original state
        self.original_events = MOCK_EVENTS.copy()
        
        # Clear and reset to known state
        MOCK_EVENTS.clear()
        MOCK_EVENTS.update({
            '1': {
                'id': 1,
                'img': '/src/assets/Volunteer_home.jpg',
                'name': 'Community Food Drive',
                'time': 'Sat, Oct 5 · 9:00 AM - 12:00 PM',
                'description': 'Join us to collect and distribute food to local families in need.',
                'location': 'Houston Food Bank',
                'urgency': 'low',
                'desiredSkills': ['organization', 'communication']
            },
            '2': {
                'id': 2,
                'img': '/src/assets/TreePlant.jpg',
                'name': 'Neighborhood Tree Planting',
                'time': 'Sun, Oct 13 · 10:00 AM - 2:00 PM',
                'description': 'Help us plant trees around the park.',
                'location': 'Memorial Park',
                'urgency': 'high',
                'desiredSkills': ['physical labor', 'gardening']
            }
        })

    def tearDown(self):
        """Restore original state after each test"""
        MOCK_EVENTS.clear()
        MOCK_EVENTS.update(self.original_events)
        # Pop Flask app context
        self.app_context.pop()

    def test_fetch_all_events(self):
        """Test fetching all events without filters"""
        response = ManagerEventService.fetch_events()
        data = json.loads(response.data)
        
        self.assertEqual(len(data), 2)
        self.assertEqual(data[0]['name'], 'Community Food Drive')
        self.assertEqual(data[1]['name'], 'Neighborhood Tree Planting')

    def test_fetch_events_with_status_filter(self):
        """Test fetching events filtered by urgency status"""
        # Filter by 'low' urgency
        response = ManagerEventService.fetch_events(status='low')
        data = json.loads(response.data)
        
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Community Food Drive')
        self.assertEqual(data[0]['urgency'], 'low')

        # Filter by 'high' urgency
        response = ManagerEventService.fetch_events(status='high')
        data = json.loads(response.data)
        
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]['name'], 'Neighborhood Tree Planting')
        self.assertEqual(data[0]['urgency'], 'high')

    def test_fetch_events_with_no_matches(self):
        """Test filtering events with status that doesn't match any events"""
        response = ManagerEventService.fetch_events(status='urgent')
        data = json.loads(response.data)
        
        self.assertEqual(len(data), 0)

    def test_create_event_with_all_fields(self):
        """Test creating an event with all required and optional fields"""
        event_data = {
            'name': 'New Volunteer Event',
            'time': 'Mon, Oct 21 · 1:00 PM - 4:00 PM',
            'description': 'A new exciting volunteer opportunity',
            'location': 'Community Center',
            'img': '/src/assets/custom.jpg',
            'urgency': 'medium',
            'desiredSkills': ['teamwork', 'leadership']
        }
        
        response, status_code = ManagerEventService.create_event(event_data)
        data = json.loads(response.data)
        
        self.assertEqual(status_code, 201)
        self.assertEqual(data['name'], 'New Volunteer Event')
        self.assertEqual(data['time'], 'Mon, Oct 21 · 1:00 PM - 4:00 PM')
        self.assertEqual(data['description'], 'A new exciting volunteer opportunity')
        self.assertEqual(data['location'], 'Community Center')
        self.assertEqual(data['img'], '/src/assets/custom.jpg')
        self.assertEqual(data['urgency'], 'medium')
        self.assertEqual(data['desiredSkills'], ['teamwork', 'leadership'])
        self.assertIsInstance(data['id'], int)
        
        # Verify event was added to MOCK_EVENTS
        self.assertEqual(len(MOCK_EVENTS), 3)

    def test_create_event_with_minimum_fields(self):
        """Test creating an event with only required fields"""
        event_data = {
            'name': 'Minimal Event',
            'time': 'Tue, Oct 22 · 2:00 PM - 5:00 PM',
            'description': 'Minimal description',
            'location': 'Some Location'
        }
        
        response, status_code = ManagerEventService.create_event(event_data)
        data = json.loads(response.data)
        
        self.assertEqual(status_code, 201)
        self.assertEqual(data['name'], 'Minimal Event')
        self.assertEqual(data['img'], '/src/assets/Volunteer_home.jpg')  # Default value
        self.assertEqual(data['urgency'], 'low')  # Default value
        self.assertEqual(data['desiredSkills'], [])  # Default value

    def test_create_event_missing_name(self):
        """Test creating event without required 'name' field"""
        event_data = {
            'time': 'Wed, Oct 23 · 3:00 PM - 6:00 PM',
            'description': 'Description without name',
            'location': 'Location'
        }
        
        response, status_code = ManagerEventService.create_event(event_data)
        data = json.loads(response.data)
        
        self.assertEqual(status_code, 400)
        self.assertIn('Missing required field: name', data['message'])

    def test_create_event_missing_time(self):
        """Test creating event without required 'time' field"""
        event_data = {
            'name': 'Event Name',
            'description': 'Description',
            'location': 'Location'
        }
        
        response, status_code = ManagerEventService.create_event(event_data)
        data = json.loads(response.data)
        
        self.assertEqual(status_code, 400)
        self.assertIn('Missing required field: time', data['message'])

    def test_create_event_missing_description(self):
        """Test creating event without required 'description' field"""
        event_data = {
            'name': 'Event Name',
            'time': 'Thu, Oct 24 · 4:00 PM - 7:00 PM',
            'location': 'Location'
        }
        
        response, status_code = ManagerEventService.create_event(event_data)
        data = json.loads(response.data)
        
        self.assertEqual(status_code, 400)
        self.assertIn('Missing required field: description', data['message'])

    def test_create_event_missing_location(self):
        """Test creating event without required 'location' field"""
        event_data = {
            'name': 'Event Name',
            'time': 'Fri, Oct 25 · 5:00 PM - 8:00 PM',
            'description': 'Description'
        }
        
        response, status_code = ManagerEventService.create_event(event_data)
        data = json.loads(response.data)
        
        self.assertEqual(status_code, 400)
        self.assertIn('Missing required field: location', data['message'])

    def test_create_event_generates_unique_id(self):
        """Test that created events get unique IDs"""
        event_data = {
            'name': 'Event One',
            'time': 'Sat, Oct 26 · 9:00 AM - 12:00 PM',
            'description': 'First event',
            'location': 'Location One'
        }
        
        response1, _ = ManagerEventService.create_event(event_data)
        data1 = json.loads(response1.data)
        
        event_data['name'] = 'Event Two'
        response2, _ = ManagerEventService.create_event(event_data)
        data2 = json.loads(response2.data)
        
        self.assertNotEqual(data1['id'], data2['id'])
        self.assertEqual(data2['id'], data1['id'] + 1)

    def test_update_event_success(self):
        """Test successfully updating an existing event"""
        update_data = {
            'name': 'Updated Food Drive',
            'urgency': 'high',
            'desiredSkills': ['organization', 'communication', 'logistics']
        }
        
        response = ManagerEventService.update_event('1', update_data)
        data = json.loads(response.data)
        
        self.assertEqual(data['name'], 'Updated Food Drive')
        self.assertEqual(data['urgency'], 'high')
        self.assertEqual(len(data['desiredSkills']), 3)
        # Original fields should remain unchanged
        self.assertEqual(data['time'], 'Sat, Oct 5 · 9:00 AM - 12:00 PM')
        self.assertEqual(data['location'], 'Houston Food Bank')

    def test_update_event_all_fields(self):
        """Test updating all fields of an event"""
        update_data = {
            'name': 'Completely Updated Event',
            'img': '/src/assets/new.jpg',
            'time': 'Sun, Oct 27 · 10:00 AM - 1:00 PM',
            'description': 'Brand new description',
            'location': 'New Location',
            'urgency': 'urgent',
            'desiredSkills': ['new', 'skills']
        }
        
        response = ManagerEventService.update_event('1', update_data)
        data = json.loads(response.data)
        
        self.assertEqual(data['name'], 'Completely Updated Event')
        self.assertEqual(data['img'], '/src/assets/new.jpg')
        self.assertEqual(data['time'], 'Sun, Oct 27 · 10:00 AM - 1:00 PM')
        self.assertEqual(data['description'], 'Brand new description')
        self.assertEqual(data['location'], 'New Location')
        self.assertEqual(data['urgency'], 'urgent')
        self.assertEqual(data['desiredSkills'], ['new', 'skills'])

    def test_update_event_partial_fields(self):
        """Test updating only some fields of an event"""
        update_data = {
            'description': 'Updated description only'
        }
        
        response = ManagerEventService.update_event('1', update_data)
        data = json.loads(response.data)
        
        self.assertEqual(data['description'], 'Updated description only')
        # Other fields should remain unchanged
        self.assertEqual(data['name'], 'Community Food Drive')
        self.assertEqual(data['urgency'], 'low')

    def test_update_nonexistent_event(self):
        """Test updating an event that doesn't exist"""
        update_data = {
            'name': 'Should Not Work'
        }
        
        response, status_code = ManagerEventService.update_event('999', update_data)
        data = json.loads(response.data)
        
        self.assertEqual(status_code, 404)
        self.assertEqual(data['message'], 'Event not found')

    def test_delete_event_success(self):
        """Test successfully deleting an existing event"""
        # Verify event exists
        self.assertIn('1', MOCK_EVENTS)
        
        result = ManagerEventService.delete_event('1')
        # When successful, returns only Response, not tuple
        if isinstance(result, tuple):
            response, status_code = result
        else:
            response = result
            status_code = 200
            
        data = json.loads(response.data)
        
        self.assertEqual(status_code, 200)
        self.assertEqual(data['message'], 'Event deleted successfully')
        
        # Verify event was deleted
        self.assertNotIn('1', MOCK_EVENTS)
        self.assertEqual(len(MOCK_EVENTS), 1)

    def test_delete_nonexistent_event(self):
        """Test deleting an event that doesn't exist"""
        response, status_code = ManagerEventService.delete_event('999')
        data = json.loads(response.data)
        
        self.assertEqual(status_code, 404)
        self.assertEqual(data['message'], 'Event not found')
        
        # Verify no events were deleted
        self.assertEqual(len(MOCK_EVENTS), 2)

    def test_delete_all_events(self):
        """Test deleting all events one by one"""
        result1 = ManagerEventService.delete_event('1')
        self.assertEqual(len(MOCK_EVENTS), 1)
        
        result2 = ManagerEventService.delete_event('2')
        self.assertEqual(len(MOCK_EVENTS), 0)

    def test_create_after_delete(self):
        """Test creating an event after deleting one"""
        # Delete an event
        ManagerEventService.delete_event('1')
        
        # Create a new event
        event_data = {
            'name': 'Post-Delete Event',
            'time': 'Mon, Oct 28 · 11:00 AM - 2:00 PM',
            'description': 'Created after deletion',
            'location': 'Test Location'
        }
        
        response, status_code = ManagerEventService.create_event(event_data)
        data = json.loads(response.data)
        
        self.assertEqual(status_code, 201)
        self.assertEqual(data['name'], 'Post-Delete Event')
        # ID should be 3 (next after highest existing ID of 2)
        self.assertEqual(data['id'], 3)


if __name__ == '__main__':
    unittest.main()
