from sqlalchemy import text
from flask import jsonify, current_app, request
import json

class ProfileService:
    @staticmethod
    def get_profile(user_id):
        """Get a user's profile by user_id"""
        engine = current_app.config["ENGINE"]
        
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
            """), {"user_id": user_id}).mappings().first()

        if not result:
            return jsonify({'message': 'Profile not found'}), 404

        profile = dict(result)

        # Rename DB columns to match API format
        profile['address_1'] = profile.pop('address1')
        profile['address_2'] = profile.pop('address2')
        profile['zip_code'] = profile.pop('zip')
        
        # Parse skills
        if profile.get('skill_names'):
            profile['skills'] = profile['skill_names'].split(',')
        else:
            profile['skills'] = []
        
        # Remove skill_names from response
        profile.pop('skill_names', None)

        # Parse availability if it's a string
        if profile.get('availability'):
            if isinstance(profile['availability'], str):
                profile['availability'] = json.loads(profile['availability'])
        else:
            profile['availability'] = []

        return jsonify(profile), 200

    @staticmethod
    def get_current_profile(id):
        """Legacy method for compatibility"""
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
    def create_profile(data):
        """Create a new profile"""
        # Validate required fields (accept both API format and DB format)
        user_id = data.get('user_id')
        full_name = data.get('full_name')
        address_1 = data.get('address_1') or data.get('address1')
        address_2 = data.get('address_2') or data.get('address2', '')
        city = data.get('city')
        state = data.get('state')
        zip_code = data.get('zip_code') or data.get('zip')
        
        # Validate required fields
        if not user_id or not full_name or not address_1 or not city or not state or not zip_code:
            return jsonify({'message': 'Missing required fields'}), 400
        
        # Validate zip code format (5 digits or 5-4 format)
        import re
        if not re.match(r'^\d{5}(-\d{4})?$', zip_code):
            return jsonify({'message': 'Invalid zip code format'}), 400
        
        # Validate state code (2 uppercase letters)
        if not re.match(r'^[A-Z]{2}$', state):
            return jsonify({'message': 'Invalid state code'}), 400
        
        # Validate full_name not empty
        if not full_name.strip():
            return jsonify({'message': 'Full name cannot be empty'}), 400

        engine = current_app.config["ENGINE"]
        
        with engine.connect() as conn:
            # Check if profile already exists
            existing = conn.execute(text("SELECT user_id FROM profiles WHERE user_id = :user_id"), 
                                   {"user_id": user_id}).mappings().first()
            if existing:
                return jsonify({'message': 'Profile already exists for this user'}), 409

            # Insert new profile using actual DB column names
            conn.execute(text("""
                INSERT INTO profiles (user_id, full_name, address1, address2, city, state, zip, 
                                    preferences, availability)
                VALUES (:user_id, :full_name, :address1, :address2, :city, :state, :zip,
                       :preferences, :availability)
            """), {
                "user_id": user_id,
                "full_name": full_name,
                "address1": address_1,
                "address2": address_2,
                "city": city,
                "state": state,
                "zip": zip_code,
                "preferences": data.get('preferences', ''),
                "availability": json.dumps(data.get('availability', []))
            })
            conn.commit()

            # Fetch and return the created profile with API format
            result = conn.execute(text("SELECT * FROM profiles WHERE user_id = :user_id"), 
                                {"user_id": user_id}).mappings().first()
            
            profile = dict(result)
            profile['address_1'] = profile.pop('address1')
            profile['address_2'] = profile.pop('address2')
            profile['zip_code'] = profile.pop('zip')
            profile['skills'] = data.get('skills', '')

        return jsonify(profile), 201

    @staticmethod
    def update_profile(user_id, data):
        """Update an existing profile"""
        engine = current_app.config["ENGINE"]
        
        with engine.connect() as conn:
            # Check if profile exists
            existing = conn.execute(text("SELECT * FROM profiles WHERE user_id = :user_id"), 
                                   {"user_id": user_id}).mappings().first()
            if not existing:
                return jsonify({'message': 'Profile not found'}), 404

            # Build update query with only provided fields
            update_fields = []
            params = {"user_id": user_id}
            
            # Map API fields to DB fields
            field_mapping = {
                'full_name': 'full_name',
                'address_1': 'address1',
                'address_2': 'address2',
                'city': 'city',
                'state': 'state',
                'zip_code': 'zip',
                'preferences': 'preferences',
                'availability': 'availability'
            }
            
            for json_field, db_field in field_mapping.items():
                if json_field in data:
                    value = data[json_field]
                    # Convert availability to JSON string if needed
                    if json_field == 'availability' and isinstance(value, (list, dict)):
                        value = json.dumps(value)
                    update_fields.append(f"{db_field} = :{db_field}")
                    params[db_field] = value
            
            if update_fields:
                query = f"UPDATE profiles SET {', '.join(update_fields)} WHERE user_id = :user_id"
                conn.execute(text(query), params)
                conn.commit()

            # Fetch and return updated profile with API format
            result = conn.execute(text("SELECT * FROM profiles WHERE user_id = :user_id"), 
                                {"user_id": user_id}).mappings().first()
            
            profile = dict(result)
            profile['address_1'] = profile.pop('address1')
            profile['address_2'] = profile.pop('address2')
            profile['zip_code'] = profile.pop('zip')
            profile['skills'] = data.get('skills', '')

        return jsonify(profile), 200

    @staticmethod
    def delete_profile(user_id):
        """Delete a profile"""
        engine = current_app.config["ENGINE"]
        
        with engine.connect() as conn:
            # Check if profile exists
            existing = conn.execute(text("SELECT user_id FROM profiles WHERE user_id = :user_id"), 
                                   {"user_id": user_id}).mappings().first()
            if not existing:
                return jsonify({'message': 'Profile not found'}), 404

            # Delete the profile
            conn.execute(text("DELETE FROM profiles WHERE user_id = :user_id"), {"user_id": user_id})
            conn.commit()

        return jsonify({'message': 'Profile deleted successfully'}), 200

    @staticmethod
    def update_profile_legacy(data):
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