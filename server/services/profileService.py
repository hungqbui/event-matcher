
current_profile = {
    "fullName": "John Doe",
    "address1": "123 Main St",
    "address2": "",
    "city": "Houston",
    "state": "TX",
    "zip": "77001",
    "skills": ["Tree Planting", "Food Drives"],
    "preferences": "Prefer outdoor activities",
    "availability": ["2025-10-01", "2025-10-15"]
}

from flask import jsonify
class ProfileService:
    @staticmethod
    def get_current_profile():
        return jsonify(current_profile), 200

    @staticmethod
    def update_profile(data):
        # Basic validation
        required_fields = ["fullName", "address1", "city", "state", "zip"]
        for field in required_fields:
            if field not in data or not data[field]:
                return jsonify({"error": f"Missing required field: {field}"}), 400
        
        # Update the current profile
        current_profile.update(data)
        return jsonify({"message": "Profile updated successfully", "profile": current_profile}), 200