from flask import Blueprint, request, jsonify
from functools import wraps
import jwt
from datetime import datetime, timedelta
import uuid

bp = Blueprint('manager', __name__)

# Mock data storage
MOCK_EVENTS = {
    '1': {
        'id': 1,
        'img': '/src/assets/Volunteer_home.jpg',
        'name': 'Community Food Drive',
        'time': 'Sat, Oct 5 · 9:00 AM - 12:00 PM',
        'description': 'Join us to collect and distribute food to local families in need. Volunteers will help sort donations and assemble boxes for distribution.',
        'location': 'Houston Food Bank, 535 Portwall St, Houston, TX 77029',
        'urgency': 'low',
        'desiredSkills': ['organization', 'communication', 'physical stamina']
    },
    '2': {
        'id': 2,
        'img': '/src/assets/TreePlant.jpg',
        'name': 'Neighborhood Tree Planting',
        'time': 'Sun, Oct 13 · 10:00 AM - 2:00 PM',
        'description': 'Help us plant trees around the park to improve air quality and provide shade. Gloves and tools will be provided.',
        'location': 'Memorial Park, 6501 Memorial Dr, Houston, TX 77007',
        'urgency': 'low',
        'desiredSkills': ['physical labor', 'gardening', 'teamwork']
    },
    '3': {
        'id': 3,
        'img': '/src/assets/VCleanupHome.webp',
        'name': 'Coastal Cleanup',
        'time': 'Sat, Nov 2 · 8:00 AM - 11:00 AM',
        'description': 'A morning of beach cleanup to remove litter and protect marine life. All ages welcome; bring reusable water bottle.',
        'location': 'Galveston Beach, 2501 Seawall Blvd, Galveston, TX 77550',
        'urgency': 'low',
        'desiredSkills': ['environmental awareness', 'teamwork', 'physical stamina']
    }
}

def admin_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        auth_header = request.headers.get('Authorization')
        
        print(request)

        if not auth_header:
            return jsonify({'message': 'Token is missing'}), 401
        
        try:
            # if not auth_header.startswith('Bearer '):
            #     raise jwt.InvalidTokenError('Invalid token format')
            
            # token = auth_header.split('Bearer ')[1]
            # decoded = jwt.decode(token, Config.JWT_SECRET_KEY, algorithms=['HS256'])
            
            return f(*args, **kwargs)
            
        except jwt.ExpiredSignatureError:
            return jsonify({'message': 'Token has expired'}), 401
        except jwt.InvalidTokenError:
            return jsonify({'message': 'Invalid token'}), 401
            
    return decorated

@bp.route('/events', methods=['GET'])
@admin_required
def fetch_events():
    """Get all events"""
    status = request.args.get('status')
    if status:
        filtered_events = {k: v for k, v in MOCK_EVENTS.items() if v['status'] == status}
        return jsonify(list(filtered_events.values()))
    return jsonify(list(MOCK_EVENTS.values()))

@bp.route('/events', methods=['POST'])
@admin_required
def create_event():
    """Create a new event"""
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name', 'time', 'description', 'location']
    for field in required_fields:
        if field not in data:
            return jsonify({'message': f'Missing required field: {field}'}), 400
    
    # Generate new event ID
    event_id = max([int(k) for k in MOCK_EVENTS.keys()]) + 1 if MOCK_EVENTS else 1
    
    # Create new event
    new_event = {
        'id': event_id,  # Convert first 8 chars of UUID to integer
        'img': data.get('img', '/src/assets/Volunteer_home.jpg'),  # Default image if none provided
        'name': data['name'],
        'time': data['time'],
        'description': data['description'],
        'location': data['location'],
        'urgency': data.get('urgency', 'low'),
        'desiredSkills': data.get('desiredSkills', [])
    }
    
    MOCK_EVENTS[str(event_id)] = new_event
    return jsonify(new_event), 201

@bp.route('/events/<event_id>', methods=['PUT'])
@admin_required
def update_event(event_id):
    """Update an existing event"""
    print(MOCK_EVENTS)
    if event_id not in MOCK_EVENTS:
        return jsonify({'message': 'Event not found'}), 404
        
    data = request.get_json()
    event = MOCK_EVENTS[event_id]
    

    # Update fields
    field_mapping = {
        'name': 'name',
        'img': 'img',
        'time': 'time',
        'description': 'description',
        'location': 'location',
        'urgency': 'urgency',
        'desiredSkills': 'desiredSkills'
    }
    
    for client_field, db_field in field_mapping.items():
        if client_field in data:
            event[db_field] = data[client_field]
    
    return jsonify(event)

@bp.route('/events/<event_id>', methods=['DELETE'])
@admin_required
def delete_event(event_id):
    """Delete an event"""
    if event_id not in MOCK_EVENTS:
        return jsonify({'message': 'Event not found'}), 404
        
    del MOCK_EVENTS[event_id]
    return jsonify({'message': 'Event deleted successfully'})


