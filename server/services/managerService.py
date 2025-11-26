from sqlalchemy import text
from flask import jsonify, current_app, request

class ManagerEventService:
    
    @staticmethod
    def fetch_events(status=None):
        engine = current_app.config["ENGINE"]
        
        body = request.get_json()
        user_id = body.get('userId')

        if not user_id:
            return jsonify({'message': 'User is not sign in'}), 400

        with engine.connect() as conn:
            user = conn.execute(text("SELECT * FROM admins WHERE user_id = :id"), {'id': user_id}).mappings().first()
            if not user:
                return jsonify({'message': 'Unauthorized'}), 403

            events = conn.execute(text("SELECT * FROM events WHERE ownerid = :user_id"), {'user_id': user_id}).mappings().all()

            # Convert RowMapping objects to dictionaries
            events_list = [dict(event) for event in events]

            if status:
                filtered_events = [event for event in events_list if event['urgency'] == status]
                return jsonify(filtered_events), 200
            
            return jsonify(events_list), 200

    @staticmethod
    def create_event(data):
        # Validate required fields
        required_fields = ['name', 'time', 'description', 'location']
        for field in required_fields:
            if field not in data:
                return jsonify({'message': f'Missing required field: {field}'}), 400
        
        engine = current_app.config["ENGINE"]
        userid = data.get('userId')
        
        with engine.connect() as conn:
            user = conn.execute(text("SELECT * FROM admins WHERE user_id = :user_id"), {'user_id': userid}).mappings().first()
            
            if not user:
                return jsonify({'message': 'Unauthorized'}), 403
            
            # Create new event
            new_event = {
                'ownerid': user['user_id'],
                'img': data.get('img', '/src/assets/Volunteer_home.jpg'),  # Default image if none provided
                'name': data['name'],
                'time_label': data['time'],
                'date': data.get('date', '2024-12-31'),  # Default date
                'description': data['description'],
                'location': data['location'],
                'max_volunteers': data.get('max_volunteers', 10),
                'urgency': data.get('urgency', 'low')
            }
            
            try:
                result = conn.execute(text("""
                    INSERT INTO events (ownerid, img, name, time_label, date, description, location, max_volunteers, urgency)
                    VALUES (:ownerid, :img, :name, :time_label, :date, :description, :location, :max_volunteers, :urgency)
                """), new_event)
                conn.commit()
                new_event['id'] = result.lastrowid
            except Exception as e:
                return jsonify({'message': 'Error creating event', 'error': str(e)}), 500
                
        return jsonify(new_event), 201
    
    @staticmethod
    def update_event(event_id, data):
        engine = current_app.config["ENGINE"]
        
        with engine.connect() as conn:
            event = conn.execute(text("SELECT * FROM events WHERE id = :id"), {'id': event_id}).mappings().first()
            if not event:
                return jsonify({'message': 'Event not found'}), 404

            # Check if user is the event owner
            userid = data.get('userId')
            if str(event['ownerid']) != str(userid):
                return jsonify({'message': 'Unauthorized'}), 403

            try:
                conn.execute(text("""
                    UPDATE events
                    SET img = :img,
                        name = :name,
                        date = :time,
                        description = :description,
                        location = :location,
                        urgency = :urgency
                    WHERE id = :id
                """), {
                    'id': int(event_id),
                    'img': data.get('img', event['img']),
                    'name': data.get('name', event['name']),
                    'time': data.get('time', event['date']),
                    'description': data.get('description', event['description']),
                    'location': data.get('location', event['location']),
                    'urgency': data.get('urgency', event['urgency']),
                })
                conn.commit()
                
                # Fetch updated event
                updated_event = conn.execute(text("SELECT * FROM events WHERE id = :id"), {'id': event_id}).mappings().first()

            except Exception as e:
                print(e)
                return jsonify({'message': 'Error updating event', 'error': str(e)}), 500

        return jsonify(dict(updated_event)), 200
    
    @staticmethod
    def delete_event(event_id):
        engine = current_app.config["ENGINE"]
        
        with engine.connect() as conn:
            event = conn.execute(text("SELECT * FROM events WHERE id = :id"), {'id': event_id}).mappings().first()
            if not event:
                return jsonify({'message': 'Event not found'}), 404
            
            body = request.get_json()
            userid = body.get('userId')

            # Check if user is the event owner
            if str(event['ownerid']) != str(userid):
                return jsonify({'message': 'Unauthorized'}), 403
            
            conn.execute(text("DELETE FROM events WHERE id = :id"), {'id': event_id})
            conn.commit()
        
        return jsonify({'message': 'Event deleted successfully'}), 200