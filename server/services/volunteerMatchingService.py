from flask import jsonify
from datetime import datetime
import re
from ..db.db import get_db_connection

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
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM matches WHERE event_id = %s", (event_id,))
        (count,) = cursor.fetchone()  # fetchone() returns a tuple like (3,)
        cursor.close()
        conn.close()
        return count
    
    @staticmethod
    def is_matched(vol_id, event_id):
        """Check if volunteer is already matched to event"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT COUNT(*) FROM matches WHERE volunteer_id = %s AND event_id = %s",
            (vol_id, event_id)
        )
        (exists,) = cursor.fetchone()
        cursor.close()
        conn.close()
        return exists > 0


class VolunteerService:
    """Service for managing volunteers"""
    
    @staticmethod
    def get_all():
        """Get all volunteers"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM volunteers")
        volunteers = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(volunteers), 200
    
    @staticmethod
    def get_by_id(vol_id):
        """Get volunteer by ID"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM volunteers WHERE id = %s", (vol_id,))
        volunteer = cursor.fetchone()
        cursor.close()
        conn.close()
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

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO volunteers (name, email, phone, availability) VALUES (%s, %s, %s, %s)",
                (data['name'], data['email'].lower(), data.get('phone', ''), data['availability'])
            )
            conn.commit()
            new_id = cursor.lastrowid
        except Exception as e:
            conn.rollback()
            return jsonify({'error': str(e)}), 400
        finally:
            cursor.close()
            conn.close()

        return jsonify({'id': new_id, **data}), 201
    
    @staticmethod
    def delete(vol_id):
        """Delete a volunteer"""
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM volunteers WHERE id = %s", (vol_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Deleted'}), 200


class EventService:
    """Service for managing events"""
    
    @staticmethod
    def get_all():
        """Get all events with volunteer counts"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT e.*, 
                   COUNT(m.id) AS current_volunteers
            FROM events e
            LEFT JOIN matches m ON e.id = m.event_id
            GROUP BY e.id
        """)
        events = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(events), 200
    
    @staticmethod
    def get_by_id(event_id):
        """Get event by ID"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT e.*, COUNT(m.id) AS current_volunteers
            FROM events e
            LEFT JOIN matches m ON e.id = m.event_id
            WHERE e.id = %s
            GROUP BY e.id
        """, (event_id,))
        event = cursor.fetchone()
        cursor.close()
        conn.close()
        if not event:
            return jsonify({'error': 'Not found'}), 404
        return jsonify(event), 200

class MatchService:
    """Service for managing volunteer-event matches"""
    
    @staticmethod
    def find_best_match(vol_id):
        """Find best matching event for a volunteer"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # 1️⃣ Get volunteer info
        cursor.execute("SELECT * FROM volunteers WHERE id = %s", (vol_id,))
        volunteer = cursor.fetchone()
        if not volunteer:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Volunteer not found'}), 404

        # 2️⃣ Get volunteer’s skills
        cursor.execute("""
            SELECT s.name FROM skills s
            JOIN volunteer_skills vs ON vs.skill_id = s.id
            WHERE vs.volunteer_id = %s
        """, (vol_id,))
        volunteer_skills = [row['name'].lower() for row in cursor.fetchall()]

        # 3️⃣ Get events with required skills and open slots
        cursor.execute("""
            SELECT e.*, GROUP_CONCAT(s.name) AS required_skills, COUNT(m.id) AS current_volunteers
            FROM events e
            LEFT JOIN event_requirements er ON e.id = er.event_id
            LEFT JOIN skills s ON er.skill_id = s.id
            LEFT JOIN matches m ON e.id = m.event_id
            GROUP BY e.id
            HAVING current_volunteers < e.max_volunteers
        """)
        events = cursor.fetchall()

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

        cursor.close()
        conn.close()

        if not best_event:
            return jsonify({'message': 'No matches found'}), 404

        best_event['match_score'] = best_score
        return jsonify({'event': best_event, 'score': best_score}), 200
    
    @staticmethod
    def create_match(vol_id, event_id):
        """Create a match between volunteer and event"""
        
        # Validate IDs
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        # check existing match
        cursor.execute("""
            SELECT * FROM matches WHERE volunteer_id = %s AND event_id = %s
        """, (vol_id, event_id))
        if cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'error': 'Already matched'}), 400

        # event capacity
        cursor.execute("""
            SELECT COUNT(m.id) AS count, e.max_volunteers
            FROM events e
            LEFT JOIN matches m ON e.id = m.event_id
            WHERE e.id = %s
            GROUP BY e.id
        """, (event_id,))
        row = cursor.fetchone()
        if row and row['count'] >= row['max_volunteers']:
            cursor.close()
            conn.close()
            return jsonify({'error': 'Event full'}), 400

        # insert match
        cursor.execute("""
            INSERT INTO matches (volunteer_id, event_id, status, matched_at)
            VALUES (%s, %s, 'confirmed', NOW())
        """, (vol_id, event_id))
        conn.commit()

        cursor.execute("SELECT * FROM matches WHERE id = LAST_INSERT_ID()")
        new_match = cursor.fetchone()

        cursor.close()
        conn.close()
        return jsonify(new_match), 201
    
    @staticmethod
    def get_all():
        """Get all matches"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT m.*, v.name AS volunteer_name, e.name AS event_name
            FROM matches m
            JOIN volunteers v ON m.volunteer_id = v.id
            JOIN events e ON m.event_id = e.id
        """)
        matches = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(matches), 200

    @staticmethod
    def get_by_volunteer(vol_id):
        """Get all matches for a volunteer"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT m.*, v.name AS volunteer_name, e.name AS event_name
            FROM matches m
            JOIN volunteers v ON m.volunteer_id = v.id
            JOIN events e ON m.event_id = e.id
            WHERE m.volunteer_id = %s
        """, (vol_id,))
        matches = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(matches), 200

    @staticmethod
    def get_by_event(event_id):
        """Get all matches for an event"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("""
            SELECT m.*, v.name AS volunteer_name, e.name AS event_name
            FROM matches m
            JOIN volunteers v ON m.volunteer_id = v.id
            JOIN events e ON m.event_id = e.id
            WHERE m.event_id = %s
        """, (event_id,))
        matches = cursor.fetchall()
        cursor.close()
        conn.close()
        return jsonify(matches), 200

    @staticmethod
    def delete(match_id):
        """Delete a match"""
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute("SELECT id FROM matches WHERE id = %s", (match_id,))
        if not cursor.fetchone():
            cursor.close()
            conn.close()
            return jsonify({'error': 'Not found'}), 404

        cursor.execute("DELETE FROM matches WHERE id = %s", (match_id,))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Deleted'}), 200

    @staticmethod
    def update_status(match_id, status):
        """Update match status"""
        if status not in ['pending', 'confirmed', 'cancelled']:
            return jsonify({'error': 'Invalid status'}), 400
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("UPDATE matches SET status = %s WHERE id = %s", (status, match_id))
        conn.commit()
        cursor.close()
        conn.close()
        return jsonify({'message': 'Status updated'}), 200
