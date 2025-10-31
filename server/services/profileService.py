from sqlalchemy import create_engine, text
import json
from ..db.db import get_db_connection

class ProfileService:
    @staticmethod
    def get_current_profile():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        try:
            # Replace 1 with actual user_id from auth later
            user_id = 1

            cursor.execute("""
                SELECT p.*, u.email, u.name,
                       GROUP_CONCAT(s.name) as skill_names
                FROM profiles p
                JOIN users u ON p.user_id = u.id
                LEFT JOIN user_skills us ON us.user_id = u.id
                LEFT JOIN skills s ON s.id = us.skill_id
                WHERE p.user_id = %s
                GROUP BY p.user_id
            """, (user_id,))
            profile = cursor.fetchone()

            if not profile:
                return {"fullName": "", "address1": "", "address2": "", "city": "", "state": "", "zip": "", "skills": [], "preferences": "", "availability": []}

            # Parse skills
            if profile['skill_names']:
                profile['skills'] = profile['skill_names'].split(',')
            else:
                profile['skills'] = []

            # Parse availability
            if profile['availability']:
                profile['availability'] = json.loads(profile['availability'])
            else:
                profile['availability'] = []

            return {
                "fullName": profile['full_name'],
                "address1": profile['address1'],
                "address2": profile['address2'] or "",
                "city": profile['city'],
                "state": profile['state'],
                "zip": profile['zip'],
                "skills": profile['skills'],
                "preferences": profile['preferences'] or "",
                "availability": profile['availability']
            }
        finally:
            cursor.close()

    @staticmethod
    def update_profile(data):
        conn = get_db_connection()
        cursor = conn.cursor()
        user_id = 1  # TODO: get from JWT/session

        try:
            # Validate required
            required = ['fullName', 'address1', 'city', 'state', 'zip']
            for field in required:
                if not data.get(field):
                    return {"error": f"{field} is required"}, 400

            if len(data['state']) != 2:
                return {"error": "State must be 2 letters"}, 400

            # Upsert profile
            cursor.execute("""
                INSERT INTO profiles (user_id, full_name, address1, address2, city, state, zip, preferences, availability)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON DUPLICATE KEY UPDATE
                full_name=VALUES(full_name), address1=VALUES(address1), address2=VALUES(address2),
                city=VALUES(city), state=VALUES(state), zip=VALUES(zip),
                preferences=VALUES(preferences), availability=VALUES(availability)
            """, (
                user_id,
                data['fullName'],
                data['address1'],
                data.get('address2'),
                data['city'],
                data['state'],
                data['zip'],
                data.get('preferences'),
                json.dumps(data.get('availability', []))
            ))

            # Sync skills
            cursor.execute("DELETE FROM user_skills WHERE user_id = %s", (user_id,))
            for skill in data.get('skills', []):
                cursor.execute("INSERT IGNORE INTO skills (name) VALUES (%s)", (skill,))
                cursor.execute("SELECT id FROM skills WHERE name = %s", (skill,))
                skill_id = cursor.fetchone()[0]
                cursor.execute("INSERT IGNORE INTO user_skills (user_id, skill_id) VALUES (%s, %s)", (user_id, skill_id))

            conn.commit()
            return {"message": "Profile saved!"}, 200
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}, 500
        finally:
            cursor.close()