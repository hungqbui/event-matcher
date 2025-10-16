from flask import Blueprint, request, jsonify
from datetime import datetime
import re

bp = Blueprint('volunteer_matching', __name__)

# Store data in memory
volunteers = [
    {'id': 1, 'name': 'John Doe', 'email': 'john@example.com', 'phone': '555-0101', 
     'skills': ['tree planting', 'gardening'], 'availability': 'weekends'},
    {'id': 2, 'name': 'Jane Smith', 'email': 'jane@example.com', 'phone': '555-0102',
     'skills': ['disaster relief', 'first aid'], 'availability': 'weekdays'},
    {'id': 3, 'name': 'Joe Doe', 'email': 'joe@example.com', 'phone': '555-0103',
     'skills': ['youth mentors', 'teaching'], 'availability': 'evenings'},
    {'id': 4, 'name': 'Jim Doe', 'email': 'jim@example.com', 'phone': '555-0104',
     'skills': ['food drives', 'organizing'], 'availability': 'flexible'}
]

events = [
    {'id': 1, 'name': 'Food Bank Distribution', 'description': 'Help distribute food to families in need',
     'requirements': ['food drives', 'organizing'], 'date': '10/15/2025', 'location': 'Community Center', 'max_volunteers': 10},
    {'id': 2, 'name': 'Community Garden Build', 'description': 'Build a new community garden space',
     'requirements': ['tree planting', 'gardening'], 'date': '10/20/2025', 'location': 'Central Park', 'max_volunteers': 8},
    {'id': 3, 'name': 'Hurricane Relief Effort', 'description': 'Assist families affected by recent hurricane',
     'requirements': ['disaster relief', 'first aid'], 'date': '10/25/2025', 'location': 'Relief Center', 'max_volunteers': 15},
    {'id': 4, 'name': 'Youth Mentorship Program', 'description': 'Mentor young people in the community',
     'requirements': ['youth mentors', 'teaching'], 'date': '10/30/2025', 'location': 'Youth Center', 'max_volunteers': 12}
]

matches = []

next_vol_id = 5
next_event_id = 5
next_match_id = 1


def valid_email(email):
    return re.match(r'^[\w\.-]+@[\w\.-]+\.\w+$', email) is not None


def valid_phone(phone):
    if not phone:
        return True
    digits = ''.join(c for c in phone if c.isdigit())
    return len(digits) >= 10


def valid_date(date_str):
    try:
        datetime.strptime(date_str, '%m/%d/%Y')
        return True
    except:
        return False


def calculate_score(volunteer, event):
    vol_skills = set(s.lower() for s in volunteer['skills'])
    event_reqs = set(r.lower() for r in event['requirements'])
    if not event_reqs:
        return 0
    matching = vol_skills & event_reqs
    return round((len(matching) / len(event_reqs)) * 100, 2)


def count_volunteers(event_id):
    return sum(1 for m in matches if m['event_id'] == event_id)


def is_matched(vol_id, event_id):
    return any(m['volunteer_id'] == vol_id and m['event_id'] == event_id for m in matches)


# Get all volunteers
@bp.route('/volunteers', methods=['GET'])
def list_volunteers():
    return jsonify(volunteers)


# Get one volunteer
@bp.route('/volunteers/<int:id>', methods=['GET'])
def get_volunteer(id):
    vol = next((v for v in volunteers if v['id'] == id), None)
    if not vol:
        return jsonify({'error': 'Not found'}), 404
    return jsonify(vol)


# Create volunteer
@bp.route('/volunteers', methods=['POST'])
def add_volunteer():
    global next_vol_id
    data = request.json
    
    if not data.get('name'):
        return jsonify({'error': 'Name required'}), 400
    if not data.get('email'):
        return jsonify({'error': 'Email required'}), 400
    if not valid_email(data['email']):
        return jsonify({'error': 'Invalid email'}), 400
    if not data.get('skills'):
        return jsonify({'error': 'Skills required'}), 400
    if not data.get('availability'):
        return jsonify({'error': 'Availability required'}), 400
    
    if any(v['email'].lower() == data['email'].lower() for v in volunteers):
        return jsonify({'error': 'Email exists'}), 400
    
    new_vol = {
        'id': next_vol_id,
        'name': data['name'],
        'email': data['email'].lower(),
        'phone': data.get('phone', ''),
        'skills': data['skills'],
        'availability': data['availability']
    }
    
    volunteers.append(new_vol)
    next_vol_id += 1
    return jsonify(new_vol), 201


# Update volunteer
@bp.route('/volunteers/<int:id>', methods=['PUT'])
def edit_volunteer(id):
    vol = next((v for v in volunteers if v['id'] == id), None)
    if not vol:
        return jsonify({'error': 'Not found'}), 404
    
    data = request.json
    
    if 'email' in data:
        if not valid_email(data['email']):
            return jsonify({'error': 'Invalid email'}), 400
        if any(v['id'] != id and v['email'].lower() == data['email'].lower() for v in volunteers):
            return jsonify({'error': 'Email exists'}), 400
        vol['email'] = data['email'].lower()
    
    if 'name' in data:
        vol['name'] = data['name']
    if 'phone' in data:
        vol['phone'] = data['phone']
    if 'skills' in data:
        vol['skills'] = data['skills']
    if 'availability' in data:
        vol['availability'] = data['availability']
    
    return jsonify(vol)


# Delete volunteer
@bp.route('/volunteers/<int:id>', methods=['DELETE'])
def remove_volunteer(id):
    global volunteers, matches
    vol = next((v for v in volunteers if v['id'] == id), None)
    if not vol:
        return jsonify({'error': 'Not found'}), 404
    
    volunteers = [v for v in volunteers if v['id'] != id]
    matches = [m for m in matches if m['volunteer_id'] != id]
    return jsonify({'message': 'Deleted'})


# Get all events
@bp.route('/events', methods=['GET'])
def list_events():
    result = []
    for evt in events:
        e = evt.copy()
        e['current_volunteers'] = count_volunteers(evt['id'])
        result.append(e)
    return jsonify(result)


# Get one event
@bp.route('/events/<int:id>', methods=['GET'])
def get_event(id):
    evt = next((e for e in events if e['id'] == id), None)
    if not evt:
        return jsonify({'error': 'Not found'}), 404
    
    result = evt.copy()
    result['current_volunteers'] = count_volunteers(id)
    return jsonify(result)


# Create event
@bp.route('/events', methods=['POST'])
def add_event():
    global next_event_id
    data = request.json
    
    if not data.get('name'):
        return jsonify({'error': 'Name required'}), 400
    if not data.get('requirements'):
        return jsonify({'error': 'Requirements required'}), 400
    if not data.get('date'):
        return jsonify({'error': 'Date required'}), 400
    if not valid_date(data['date']):
        return jsonify({'error': 'Invalid date'}), 400
    
    new_event = {
        'id': next_event_id,
        'name': data['name'],
        'description': data.get('description', ''),
        'requirements': data['requirements'],
        'date': data['date'],
        'location': data.get('location', ''),
        'max_volunteers': data.get('max_volunteers', 10)
    }
    
    events.append(new_event)
    next_event_id += 1
    return jsonify(new_event), 201


# Update event
@bp.route('/events/<int:id>', methods=['PUT'])
def edit_event(id):
    evt = next((e for e in events if e['id'] == id), None)
    if not evt:
        return jsonify({'error': 'Not found'}), 404
    
    data = request.json
    
    if 'date' in data and not valid_date(data['date']):
        return jsonify({'error': 'Invalid date'}), 400
    
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
    
    return jsonify(evt)


# Delete event
@bp.route('/events/<int:id>', methods=['DELETE'])
def remove_event(id):
    global events, matches
    evt = next((e for e in events if e['id'] == id), None)
    if not evt:
        return jsonify({'error': 'Not found'}), 404
    
    events = [e for e in events if e['id'] != id]
    matches = [m for m in matches if m['event_id'] != id]
    return jsonify({'message': 'Deleted'})


# Find best match for volunteer
@bp.route('/match/find', methods=['POST'])
def find_match():
    data = request.json
    vol_id = data.get('volunteer_id')
    
    if not vol_id:
        return jsonify({'error': 'Volunteer ID required'}), 400
    
    vol = next((v for v in volunteers if v['id'] == vol_id), None)
    if not vol:
        return jsonify({'error': 'Volunteer not found'}), 404
    
    best = None
    best_score = 0
    
    for evt in events:
        if is_matched(vol_id, evt['id']):
            continue
        if count_volunteers(evt['id']) >= evt['max_volunteers']:
            continue
        
        score = calculate_score(vol, evt)
        if score > best_score:
            best_score = score
            best = evt
    
    if not best:
        return jsonify({'message': 'No matches'}), 404
    
    result = best.copy()
    result['current_volunteers'] = count_volunteers(best['id'])
    return jsonify({'event': result})


# Create a match
@bp.route('/match', methods=['POST'])
def make_match():
    global next_match_id
    data = request.json
    
    vol_id = data.get('volunteer_id')
    event_id = data.get('event_id')
    
    if not vol_id or not event_id:
        return jsonify({'error': 'IDs required'}), 400
    
    vol = next((v for v in volunteers if v['id'] == vol_id), None)
    evt = next((e for e in events if e['id'] == event_id), None)
    
    if not vol:
        return jsonify({'error': 'Volunteer not found'}), 404
    if not evt:
        return jsonify({'error': 'Event not found'}), 404
    
    if is_matched(vol_id, event_id):
        return jsonify({'error': 'Already matched'}), 400
    
    if count_volunteers(event_id) >= evt['max_volunteers']:
        return jsonify({'error': 'Event full'}), 400
    
    new_match = {
        'id': next_match_id,
        'volunteer_id': vol_id,
        'volunteer_name': vol['name'],
        'event_id': event_id,
        'event_name': evt['name'],
        'status': 'confirmed',
        'matched_at': datetime.now().isoformat()
    }
    
    matches.append(new_match)
    next_match_id += 1
    return jsonify(new_match), 201


# Get all matches
@bp.route('/matches', methods=['GET'])
def list_matches():
    return jsonify(matches)


# Get volunteer's matches
@bp.route('/matches/volunteer/<int:id>', methods=['GET'])
def volunteer_matches(id):
    result = [m for m in matches if m['volunteer_id'] == id]
    return jsonify(result)


# Get event's matches
@bp.route('/matches/event/<int:id>', methods=['GET'])
def event_matches(id):
    result = [m for m in matches if m['event_id'] == id]
    return jsonify(result)


# Delete match
@bp.route('/matches/<int:id>', methods=['DELETE'])
def remove_match(id):
    global matches
    match = next((m for m in matches if m['id'] == id), None)
    if not match:
        return jsonify({'error': 'Not found'}), 404
    
    matches = [m for m in matches if m['id'] != id]
    return jsonify({'message': 'Deleted'})


# Update match status
@bp.route('/matches/<int:id>/status', methods=['PUT'])
def change_status(id):
    match = next((m for m in matches if m['id'] == id), None)
    if not match:
        return jsonify({'error': 'Not found'}), 404
    
    data = request.json
    status = data.get('status')
    
    if not status:
        return jsonify({'error': 'Status required'}), 400
    if status not in ['pending', 'confirmed', 'cancelled']:
        return jsonify({'error': 'Invalid status'}), 400
    
    match['status'] = status
    return jsonify(match)