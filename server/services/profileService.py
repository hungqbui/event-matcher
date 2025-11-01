from sqlalchemy import text
from flask import jsonify, current_app, request
import json

class ProfileService:
    @staticmethod
    def get_current_profile(id):

        engine = current_app.config["ENGINE"]
        user_id = id
        
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT p.*, u.email, u.name,
                        GROUP_CONCAT(s.name) as skill_names
                FROM profiles p
                JOIN users u ON p.user_id = u.id
                LEFT JOIN user_skills us ON us.user_id = u.id
                LEFT JOIN skills s ON s.id = us.skill_id
                WHERE p.user_id = :user_id
                GROUP BY p.user_id
                LIMIT 1
            """), {"user_id": user_id})

        profile = result.mappings().first()

        if not profile:
            return {"fullName": "", "address1": "", "address2": "", "city": "", "state": "", "zip": "", "skills": [], "preferences": "", "availability": []}

        profile = dict(profile)

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
    @staticmethod
    def update_profile(data):
        user_id = data.get('userId')

        try:
            # Validate required
            required = ['fullName', 'address1', 'city', 'state', 'zip']
            for field in required:
                if not data.get(field):
                    return {"error": f"{field} is required"}, 400

            if len(data['state']) != 2:
                return {"error": "State must be 2 letters"}, 400

            engine = current_app.config["ENGINE"]
            
            with engine.connect() as conn:
                conn.execute(text("""
                    INSERT INTO profiles (user_id, full_name, address1, address2, city, state, zip, preferences, availability)
                    VALUES (:user_id, :full_name, :address1, :address2, :city, :state, :zip, :preferences, :availability)
                    ON DUPLICATE KEY UPDATE
                    full_name=VALUES(full_name), address1=VALUES(address1), address2=VALUES(address2),
                    city=VALUES(city), state=VALUES(state), zip=VALUES(zip),
                    preferences=VALUES(preferences), availability=VALUES(availability)
                """), {
                    "user_id": user_id,
                    "full_name": data['fullName'],
                    "address1": data['address1'],
                    "address2": data.get('address2'),
                    "city": data['city'],
                    "state": data['state'],
                    "zip": data['zip'],
                    "preferences": data.get('preferences'),
                    "availability": json.dumps(data.get('availability', []))
                })

            # Sync skills
                conn.execute(text("DELETE FROM user_skills WHERE user_id = :user_id"), {"user_id": user_id})
                for skill in data.get('skills', []):
                    conn.execute(text("INSERT IGNORE INTO skills (name) VALUES (:name)"), {"name": skill})
                    conn.execute(text("SELECT id FROM skills WHERE name = :name"), {"name": skill})
                    skill_id = conn.fetchone()[0]
                    conn.execute(text("INSERT IGNORE INTO user_skills (user_id, skill_id) VALUES (:user_id, :skill_id)"), {"user_id": user_id, "skill_id": skill_id})

                conn.commit()
            return {"message": "Profile saved!"}, 200
        except Exception as e:
            conn.rollback()
            return {"error": str(e)}, 500