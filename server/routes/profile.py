from flask import Blueprint
from ..services.profileService import ProfileService

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET'])
def get_profile():
    return ProfileService.get_current_profile()

@profile_bp.route('/profile', methods=['POST'])
def update_profile():
    from flask import request
    data = request.json
    return ProfileService.update_profile(data)