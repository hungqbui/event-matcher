from flask import jsonify, current_app
from datetime import datetime
from sqlalchemy import text
import re

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
        engine = current_app.config["ENGINE"]
        
        with engine.connect() as conn:
            result = conn.execute(text("SELECT COUNT(*) FROM matches WHERE event_id = :event_id"), {"event_id": event_id})
            (count,) = result.mappings().first().values()
        return count
    
    @staticmethod
    def is_matched(vol_id, event_id):
        """Check if volunteer is already matched to event"""
        engine = current_app.config["ENGINE"]
        with engine.connect() as conn:
            result = conn.execute(
                text("SELECT COUNT(*) FROM matches WHERE volunteer_id = :vol_id AND event_id = :event_id"),
                {"vol_id": vol_id, "event_id": event_id}
            )
        (exists,) = result.mappings().first().values()
        return exists > 0


class VolunteerService:
    """Service for managing volunteers"""
    
    @staticmethod
    def get_all():
        """Get all volunteers"""
        engine = current_app.config["ENGINE"]
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM volunteers"))
            volunteers = result.mappings().all()
        return jsonify(volunteers), 200
    
    @staticmethod
    def get_by_id(vol_id):
        """Get volunteer by ID"""
        engine = current_app.config["ENGINE"]
        with engine.connect() as conn:
            result = conn.execute(text("SELECT * FROM volunteers WHERE id = :vol_id"), {"vol_id": vol_id})
            volunteer = result.mappings().first()
        if not volunteer:
            return jsonify({'error': 'Not found'}), 404
        return jsonify(volunteer), 200
    
    @staticmethod
    def create(data):
        """Create a new volunteer"""
        
        # Validate required fields
        if not data.get('name') or not data.get('email') or not data.get('availability'):
            return jsonify({'error': 'Name, email, and availability required'}), 400
        if not ValidationHelper.valid_email(data['email']):
            return jsonify({'error': 'Invalid email'}), 400

        engine = current_app.config["ENGINE"]
        try:
            with engine.connect() as conn:
                result = conn.execute(
                    text("INSERT INTO volunteers (name, email, phone, availability) VALUES (:name, :email, :phone, :availability)"),
                    {
                        "name": data['name'],
                        "email": data['email'].lower(),
                        "phone": data.get('phone', ''),
                        "availability": data['availability']
                    }
                )
                conn.commit()
                new_id = result.lastrowid
        except Exception as e:
            conn.rollback()
            return jsonify({'error': str(e)}), 400

        return jsonify({'id': new_id, **data}), 201
    
    @staticmethod
    def delete(vol_id):
        """Delete a volunteer"""
        engine = current_app.config["ENGINE"]
        with engine.connect() as conn:
            result = conn.execute(text("DELETE FROM volunteers WHERE id = :vol_id"), {"vol_id": vol_id})
            conn.commit()
        return jsonify({'message': 'Deleted'}), 200


class EventService:
    """Service for managing events"""
    
    @staticmethod
    def get_all():
        """Get all events with volunteer counts"""
        engine = current_app.config["ENGINE"]
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT e.*, 
                       COUNT(m.id) AS current_volunteers
                FROM events e
                LEFT JOIN matches m ON e.id = m.event_id
                GROUP BY e.id
            """))
        events = result.mappings().all()
        return jsonify(events), 200
    
    @staticmethod
    def get_by_id(event_id):
        """Get event by ID"""
        engine = current_app.config["ENGINE"]
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT e.*, COUNT(m.id) AS current_volunteers
                FROM events e
                LEFT JOIN matches m ON e.id = m.event_id
            WHERE e.id = :event_id
            GROUP BY e.id
        """), {"event_id": event_id})
        event = result.mappings().first()
        if not event:
            return jsonify({'error': 'Not found'}), 404
        return jsonify(event), 200

class MatchService:
    """Service for managing volunteer-event matches"""
    
    @staticmethod
    def find_best_match(vol_id):
        """Find best matching event for a volunteer"""
        engine = current_app.config["ENGINE"]
        with engine.connect() as conn:

            # 1️⃣ Get volunteer info
            result = conn.execute(text("SELECT * FROM volunteers WHERE id = :vol_id"), {"vol_id": vol_id})
            volunteer = result.mappings().first()
            if not volunteer:
                return jsonify({'error': 'Volunteer not found'}), 404

            # 2️⃣ Get volunteer’s skills
            result = conn.execute(text("""
                SELECT s.name FROM skills s
                JOIN volunteer_skills vs ON vs.skill_id = s.id
                WHERE vs.volunteer_id = :vol_id
            """), {"vol_id": vol_id})
            volunteer_skills = [row['name'].lower() for row in result.mappings().all()]

            # 3️⃣ Get events with required skills and open slots
            result = conn.execute(text("""
                SELECT e.*, GROUP_CONCAT(s.name) AS required_skills, COUNT(m.id) AS current_volunteers
                FROM events e
                LEFT JOIN event_requirements er ON e.id = er.event_id
                LEFT JOIN skills s ON er.skill_id = s.id
                LEFT JOIN matches m ON e.id = m.event_id
                GROUP BY e.id
                HAVING current_volunteers < e.max_volunteers
            """))
            events = result.mappings().all()

        best_event = None
        best_score = 0

        for evt in events:
            event_skills = [s.lower() for s in evt['required_skills'].split(',')] if evt['required_skills'] else []
            score = MatchingHelper.calculate_score(volunteer_skills, event_skills)
            if volunteer['availability'].lower() in (evt.get('time_label') or '').lower():
                score += 10  # bonus for availability match
            if score > best_score:
                best_score = score
                best_event = evt

        if not best_event:
            return jsonify({'message': 'No matches found'}), 404

        best_event['match_score'] = best_score
        return jsonify({'event': best_event, 'score': best_score}), 200
    
    @staticmethod
    def create_match(vol_id, event_id):
        """Create a match between volunteer and event"""
        
        engine = current_app.config["ENGINE"]
        with engine.connect() as conn:
            # check existing match
            result = conn.execute(text("""
                SELECT * FROM matches WHERE volunteer_id = :vol_id AND event_id = :event_id
            """), {"vol_id": vol_id, "event_id": event_id})
            if result.mappings().first():
                return jsonify({'error': 'Already matched'}), 400

            # event capacity
            result = conn.execute(text("""
                SELECT COUNT(m.id) AS count, e.max_volunteers
                FROM events e
                LEFT JOIN matches m ON e.id = m.event_id
                WHERE e.id = :event_id
                GROUP BY e.id
            """), {"event_id": event_id})
            row = result.mappings().first()
            if row and row['count'] >= row['max_volunteers']:
                return jsonify({'error': 'Event full'}), 400

            # insert match
            conn.execute(text("""
                INSERT INTO matches (volunteer_id, event_id, status, matched_at)
                VALUES (:vol_id, :event_id, 'confirmed', NOW())
            """), {"vol_id": vol_id, "event_id": event_id})
            conn.commit()

            result = conn.execute(text("SELECT * FROM matches WHERE id = LAST_INSERT_ID()"))
            new_match = result.mappings().first()

        return jsonify(new_match), 201
    
    @staticmethod
    def get_all():
        """Get all matches"""
        
        engine = current_app.config["ENGINE"]
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT m.*, v.name AS volunteer_name, e.name AS event_name
                FROM matches m
                JOIN volunteers v ON m.volunteer_id = v.id
                JOIN events e ON m.event_id = e.id
            """))
        matches = result.mappings().all()
        return jsonify(matches), 200

    @staticmethod
    def get_by_volunteer(vol_id):
        """Get all matches for a volunteer"""
        engine = current_app.config["ENGINE"]
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT m.*, v.name AS volunteer_name, e.name AS event_name
                FROM matches m
                JOIN volunteers v ON m.volunteer_id = v.id
                JOIN events e ON m.event_id = e.id
                WHERE m.volunteer_id = :vol_id
        """), {"vol_id": vol_id})
        matches = result.mappings().all()
        return jsonify(matches), 200

    @staticmethod
    def get_by_event(event_id):
        """Get all matches for an event"""
        engine = current_app.config["ENGINE"]
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT m.*, v.name AS volunteer_name, e.name AS event_name
                FROM matches m
                JOIN volunteers v ON m.volunteer_id = v.id
                JOIN events e ON m.event_id = e.id
                WHERE m.event_id = :event_id
            """), {"event_id": event_id})
        matches = result.mappings().all()
        return jsonify(matches), 200

    @staticmethod
    def delete(match_id):
        """Delete a match"""
        engine = current_app.config["ENGINE"]
        with engine.connect() as conn:
            result = conn.execute(text("SELECT id FROM matches WHERE id = :match_id"), {"match_id": match_id})
            if not result.mappings().first():
                return jsonify({'error': 'Not found'}), 404

            conn.execute(text("DELETE FROM matches WHERE id = :match_id"), {"match_id": match_id})
            conn.commit()
        return jsonify({'message': 'Deleted'}), 200


    @staticmethod
    def update_status(match_id, status):
        """Update match status"""
        if status not in ['pending', 'confirmed', 'cancelled']:
            return jsonify({'error': 'Invalid status'}), 400
        engine = current_app.config["ENGINE"]
        with engine.connect() as conn:
            conn.execute(text("UPDATE matches SET status = :status WHERE id = :match_id"), {"status": status, "match_id": match_id})
            conn.commit()
        return jsonify({'message': 'Status updated'}), 200
