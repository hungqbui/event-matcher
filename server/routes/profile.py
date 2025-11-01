from flask import Blueprint, jsonify, request
import re
from ..services.profileService import ProfileService

profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/profile', methods=['GET'])
def get_profile():
    return ProfileService.get_current_profile()

@profile_bp.route('/profile', methods=['POST'])
def update_profile():
    data = request.json
    if not data:
        return jsonify({"error": "No data provided"}), 400
    
    return ProfileService.update_profile(data)
