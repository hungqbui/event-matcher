from flask import jsonify
from datetime import datetime
import re

# Mock data storage
VOLUNTEERS = [
    {'id': 1, 'name': 'John Doe', 'email': 'john@example.com', 'phone': '555-0101', 
     'skills': ['tree planting', 'gardening'], 'availability': 'weekends'},
    {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com', 'phone': '555-0102',
     'skills': ['disaster relief', 'first aid'], 'availability': 'weekdays'},
    {'id': 3, 'name': 'Joe Doe', 'email': 'joe@example.com', 'phone': '555-0103',
     'skills': ['youth mentors', 'teaching'], 'availability': 'evenings'},
    {'id': 4, 'name': 'Jim Doe', 'email': 'jim@example.com', 'phone': '555-0104',
     'skills': ['food drives', 'organizing'], 'availability': 'flexible'}
]

EVENTS = [
    {'id': 1, 'name': 'Food Bank Distribution', 'description': 'Help distribute food to families in need',
     'requirements': ['food drives', 'organizing'], 'date': '10/15/2025', 'location': 'Community Center', 'max_volunteers': 10},
    {'id': 2, 'name': 'Community Garden Build', 'description': 'Build a new community garden space',
     'requirements': ['tree planting', 'gardening'], 'date': '10/20/2025', 'location': 'Central Park', 'max_volunteers': 8},
    {'id': 3, 'name': 'Hurricane Relief Effort', 'description': 'Assist families affected by recent hurricane',
     'requirements': ['disaster relief', 'first aid'], 'date': '10/25/2025', 'location': 'Relief Center', 'max_volunteers': 15},
    {'id': 4, 'name': 'Youth Mentorship Program', 'description': 'Mentor young people in the community',
     'requirements': ['youth mentors', 'teaching'], 'date': '10/30/2025', 'location': 'Youth Center', 'max_volunteers': 12}
]

MATCHES = []



class ValidationHelper:
    """Helper class for validation functions"""
    
    @staticmethod
    def valid_email(email):
        """Validate email format"""
        return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is not None
    
    @staticmethod
    def valid_phone(phone):
        """Validate phone number (optional, at least 10 digits if provided)"""
        if not phone:
            return True
        digits = ''.join(c for c in phone if c.isdigit())
        return len(digits) >= 10
    
    @staticmethod
    def valid_date(date_str):
        """Validate date format MM/DD/YYYY"""
        try:
            datetime.strptime(date_str, '%m/%d/%Y')
            return True
        except:
            return False


class MatchingHelper:
    """Helper class for matching logic"""
    
    @staticmethod
    def calculate_score(volunteer, event):
        """Calculate match score between volunteer skills and event requirements"""
        vol_skills = set(s.lower() for s in volunteer['skills'])
        event_reqs = set(r.lower() for r in event['requirements'])
        if not event_reqs:
            return 0
        matching = vol_skills & event_reqs
        return round((len(matching) / len(event_reqs)) * 100, 2)
    
    @staticmethod
    def count_volunteers(event_id):
        """Count volunteers matched to an event"""
        return sum(1 for m in MATCHES if m['event_id'] == event_id)
    
    @staticmethod
    def is_matched(vol_id, event_id):
        """Check if volunteer is already matched to event"""
        return any(m['volunteer_id'] == vol_id and m['event_id'] == event_id for m in MATCHES)


class VolunteerService:
    """Service for managing volunteers"""
    
    @staticmethod
    def get_all():
        """Get all volunteers"""
        return jsonify(VOLUNTEERS), 200
    
    @staticmethod
    def get_by_id(vol_id):
        """Get volunteer by ID"""
        vol = next((v for v in VOLUNTEERS if v['id'] == vol_id), None)
        if not vol:
            return jsonify({'error': 'Not found'}), 404
        return jsonify(vol), 200
    
    @staticmethod
    def create(data):
        """Create a new volunteer"""
        
        # Validate required fields
        if not data.get('name'):
            return jsonify({'error': 'Name required'}), 400
        if not data.get('email'):
            return jsonify({'error': 'Email required'}), 400
        if not ValidationHelper.valid_email(data['email']):
            return jsonify({'error': 'Invalid email'}), 400
        if not data.get('skills'):
            return jsonify({'error': 'Skills required'}), 400
        if not data.get('availability'):
            return jsonify({'error': 'Availability required'}), 400
        
        # Check for duplicate email
        if any(v['email'].lower() == data['email'].lower() for v in VOLUNTEERS):
            return jsonify({'error': 'Email exists'}), 400
        
        # Create new volunteer
        new_vol = {
            'id': len(VOLUNTEERS) + 1,
            'name': data['name'],
            'email': data['email'].lower(),
            'phone': data.get('phone', ''),
            'skills': data['skills'],
            'availability': data['availability']
        }
        
        VOLUNTEERS.append(new_vol)
        return jsonify(new_vol), 201
    
    @staticmethod
    def update(vol_id, data):
        """Update a volunteer"""
        vol = next((v for v in VOLUNTEERS if v['id'] == vol_id), None)
        if not vol:
            return jsonify({'error': 'Not found'}), 404
        
        # Validate email if provided
        if 'email' in data:
            if not ValidationHelper.valid_email(data['email']):
                return jsonify({'error': 'Invalid email'}), 400
            if any(v['id'] != vol_id and v['email'].lower() == data['email'].lower() for v in VOLUNTEERS):
                return jsonify({'error': 'Email exists'}), 400
            vol['email'] = data['email'].lower()
        
        # Update other fields
        if 'name' in data:
            vol['name'] = data['name']
        if 'phone' in data:
            vol['phone'] = data['phone']
        if 'skills' in data:
            vol['skills'] = data['skills']
        if 'availability' in data:
            vol['availability'] = data['availability']
        
        return jsonify(vol), 200
    
    @staticmethod
    def delete(vol_id):
        """Delete a volunteer"""
        global VOLUNTEERS, MATCHES
        vol = next((v for v in VOLUNTEERS if v['id'] == vol_id), None)
        if not vol:
            return jsonify({'error': 'Not found'}), 404
        
        VOLUNTEERS[:] = [v for v in VOLUNTEERS if v['id'] != vol_id]
        MATCHES[:] = [m for m in MATCHES if m['volunteer_id'] != vol_id]
        return jsonify({'message': 'Deleted'}), 200


class EventService:
    """Service for managing events"""
    
    @staticmethod
    def get_all():
        """Get all events with volunteer counts"""
        result = []
        for evt in EVENTS:
            e = evt.copy()
            e['current_volunteers'] = MatchingHelper.count_volunteers(evt['id'])
            result.append(e)
        return jsonify(result), 200
    
    @staticmethod
    def get_by_id(event_id):
        """Get event by ID"""
        evt = next((e for e in EVENTS if e['id'] == event_id), None)
        if not evt:
            return jsonify({'error': 'Not found'}), 404
        
        result = evt.copy()
        result['current_volunteers'] = MatchingHelper.count_volunteers(event_id)
        return jsonify(result), 200
    
    @staticmethod
    def create(data):
        """Create a new event"""
        
        # Validate required fields
        if not data.get('name'):
            return jsonify({'error': 'Name required'}), 400
        if not data.get('requirements'):
            return jsonify({'error': 'Requirements required'}), 400
        if not data.get('date'):
            return jsonify({'error': 'Date required'}), 400
        if not ValidationHelper.valid_date(data['date']):
            return jsonify({'error': 'Invalid date'}), 400
        
        # Create new event
        new_event = {
            'id': len(EVENTS) + 1,
            'name': data['name'],
            'description': data.get('description', ''),
            'requirements': data['requirements'],
            'date': data['date'],
            'location': data.get('location', ''),
            'max_volunteers': data.get('max_volunteers', 10)
        }
        
        EVENTS.append(new_event)
        return jsonify(new_event), 201
    
    @staticmethod
    def update(event_id, data):
        """Update an event"""
        evt = next((e for e in EVENTS if e['id'] == event_id), None)
        if not evt:
            return jsonify({'error': 'Not found'}), 404
        
        # Validate date if provided
        if 'date' in data and not ValidationHelper.valid_date(data['date']):
            return jsonify({'error': 'Invalid date'}), 400
        
        # Update fields
        if 'name' in data:
            evt['name'] = data['name']
        if 'description' in data:
            evt['description'] = data['description']
        if 'requirements' in data:
            evt['requirements'] = data['requirements']
        if 'date' in data:
            evt['date'] = data['date']
        if 'location' in data:
            evt['location'] = data['location']
        if 'max_volunteers' in data:
            evt['max_volunteers'] = data['max_volunteers']
        
        return jsonify(evt), 200
    
    @staticmethod
    def delete(event_id):
        """Delete an event"""
        global EVENTS, MATCHES
        evt = next((e for e in EVENTS if e['id'] == event_id), None)
        if not evt:
            return jsonify({'error': 'Not found'}), 404
        
        EVENTS[:] = [e for e in EVENTS if e['id'] != event_id]
        MATCHES[:] = [m for m in MATCHES if m['event_id'] != event_id]
        return jsonify({'message': 'Deleted'}), 200


class MatchService:
    """Service for managing volunteer-event matches"""
    
    @staticmethod
    def find_best_match(vol_id):
        """Find best matching event for a volunteer"""
        vol = next((v for v in VOLUNTEERS if v['id'] == vol_id), None)
        if not vol:
            return jsonify({'error': 'Volunteer not found'}), 404
        
        best = None
        best_score = 0
        
        for evt in EVENTS:
            if MatchingHelper.is_matched(vol_id, evt['id']):
                continue
            if MatchingHelper.count_volunteers(evt['id']) >= evt['max_volunteers']:
                continue
            
            score = MatchingHelper.calculate_score(vol, evt)
            if score > best_score:
                best_score = score
                best = evt
        
        if not best:
            return jsonify({'message': 'No matches'}), 404
        
        result = best.copy()
        result['current_volunteers'] = MatchingHelper.count_volunteers(best['id'])
        result['match_score'] = best_score
        return jsonify({'event': result, 'score': best_score}), 200
    
    @staticmethod
    def create_match(vol_id, event_id):
        """Create a match between volunteer and event"""
        
        # Validate IDs
        if not vol_id or not event_id:
            return jsonify({'error': 'IDs required'}), 400
        
        vol = next((v for v in VOLUNTEERS if v['id'] == vol_id), None)
        evt = next((e for e in EVENTS if e['id'] == event_id), None)
        
        if not vol:
            return jsonify({'error': 'Volunteer not found'}), 404
        if not evt:
            return jsonify({'error': 'Event not found'}), 404
        
        # Check if already matched
        if MatchingHelper.is_matched(vol_id, event_id):
            return jsonify({'error': 'Already matched'}), 400
        
        # Check if event is full
        if MatchingHelper.count_volunteers(event_id) >= evt['max_volunteers']:
            return jsonify({'error': 'Event full'}), 400
        
        # Create match
        new_match = {
            'id': len(MATCHES) + 1,
            'volunteer_id': vol_id,
            'volunteer_name': vol['name'],
            'event_id': event_id,
            'event_name': evt['name'],
            'status': 'confirmed',
            'matched_at': datetime.now().isoformat()
        }
        
        MATCHES.append(new_match)
        return jsonify(new_match), 201
    
    @staticmethod
    def get_all():
        """Get all matches"""
        return jsonify(MATCHES) , 200
    
    @staticmethod
    def get_by_volunteer(vol_id):
        """Get all matches for a volunteer"""
        result = [m for m in MATCHES if m['volunteer_id'] == vol_id]
        return jsonify(result), 200
    
    @staticmethod
    def get_by_event(event_id):
        """Get all matches for an event"""
        result = [m for m in MATCHES if m['event_id'] == event_id]
        return jsonify(result), 200
    
    @staticmethod
    def delete(match_id):
        """Delete a match"""
        global MATCHES
        match = next((m for m in MATCHES if m['id'] == match_id), None)
        if not match:
            return jsonify({'error': 'Not found'}), 404
        
        MATCHES[:] = [m for m in MATCHES if m['id'] != match_id]
        return jsonify({'message': 'Deleted'}), 200
    
    @staticmethod
    def update_status(match_id, status):
        """Update match status"""
        match = next((m for m in MATCHES if m['id'] == match_id), None)
        if not match:
            return jsonify({'error': 'Not found'}), 404
        
        if not status:
            return jsonify({'error': 'Status required'}), 400
        if status not in ['pending', 'confirmed', 'cancelled']:
            return jsonify({'error': 'Invalid status'}), 400
        
        match['status'] = status
        return jsonify(match), 200
