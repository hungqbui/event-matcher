from flask import Blueprint, request
from ..services.volunteerService import VolunteerService

bp = Blueprint('volunteer', __name__)

@bp.route('/history', methods=['POST'])
def get_volunteer_history():
    """Get volunteer history for the user"""
    user_id = request.get_json().get('userId')
    
    return VolunteerService.get_volunteer_history_user(id=user_id)