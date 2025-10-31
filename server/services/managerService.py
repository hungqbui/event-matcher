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

from sqlalchemy import text
from flask import jsonify, current_app

engine = current_app.config["ENGINE"]

conn = engine.connect()

class ManagerEventService:
    
    @staticmethod
    def fetch_events(status=None):
        
        events = conn.execute("SELECT * FROM events").mappings().all()

        if status:
            filtered_events = {k: v for k, v in events.items() if v['urgency'] == status}
            return jsonify(list(filtered_events.values()))
        return jsonify(list(events.values()))

    @staticmethod
    def create_event(data):
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
        
        try:
            conn.execute(text("""
                INSERT INTO events (id, img, name, time, description, location, urgency, desiredSkills)
                VALUES (:id, :img, :name, :time, :description, :location, :urgency, :desiredSkills)
            """), new_event)
        except Exception as e:
            return jsonify({'message': 'Error creating event', 'error': str(e)}), 500
            
        return jsonify(new_event), 201
    
    @staticmethod
    def update_event(event_id, data):
        if event_id not in MOCK_EVENTS:
            return jsonify({'message': 'Event not found'}), 404
        event = conn.execute(text("SELECT * FROM events WHERE id = :id"), {'id': event_id}).mappings().first()
        if not event:
            return jsonify({'message': 'Event not found'}), 404
        if event['ownerid'] != :

        try:
            event = conn.execute(text("""
                UPDATE events
                SET img = :img,
                    name = :name,
                    time = :time,
                    description = :description,
                    location = :location,
                    urgency = :urgency,
                    desiredSkills = :desiredSkills
                WHERE id = :id
            """), {
                'id': event_id,
                'img': data.get('img', MOCK_EVENTS[event_id]['img']),
                'name': data.get('name', MOCK_EVENTS[event_id]['name']),
                'time': data.get('time', MOCK_EVENTS[event_id]['time']),
                'description': data.get('description', MOCK_EVENTS[event_id]['description']),
                'location': data.get('location', MOCK_EVENTS[event_id]['location']),
                'urgency': data.get('urgency', MOCK_EVENTS[event_id]['urgency']),
                'desiredSkills': data.get('desiredSkills', MOCK_EVENTS[event_id]['desiredSkills'])
            })

        except Exception as e:
            return jsonify({'message': 'Error updating event', 'error': str(e)}), 500


        return jsonify(event)
    
    @staticmethod
    def delete_event(event_id):
        if event_id not in MOCK_EVENTS:
            return jsonify({'message': 'Event not found'}), 404
        
        del MOCK_EVENTS[event_id]
        return jsonify({'message': 'Event deleted successfully'})