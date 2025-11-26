from flask import Blueprint, request
from ..services.profileService import ProfileService

profile_bp = Blueprint('profile', __name__)

@profile_bp.route('/profile', methods=['GET'])
def get_profile():
    id = request.args.get('user_id')
    return ProfileService.get_current_profile(id)

@profile_bp.route('/profile', methods=['POST'])
def update_profile():
    from flask import request
    data = request.json
    return ProfileService.update_profile_legacy(data)
