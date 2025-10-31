from flask import Blueprint, jsonify, request
import re
from ..services.profileService import ProfileService
from ..middleware.auth import jwt_required

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/profile', methods=['GET'])  # Note: /profile under /api prefix
@jwt_required
def get_profile():
    # Can access request.current_user for the authenticated user
    return ProfileService.get_current_profile()

@profile_bp.route('/profile', methods=['POST'])
@jwt_required
def update_profile():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    return ProfileService.update_profile(data)
    # ... (rest of validation code from earlier)