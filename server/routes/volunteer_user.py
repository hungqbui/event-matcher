from flask import Blueprint, request
from ..services.volunteerService import VolunteerService

bp = Blueprint('volunteer', __name__)

@bp.route('/history', methods=['POST'])
def get_volunteer_history():
    """Get volunteer history for the user"""
    user_id = request.get_json().get('userId')
    
    return VolunteerService.get_volunteer_history_user(id=user_id)

@bp.route('/events/upcoming', methods=['GET'])
def get_upcoming_events():
    """Get all upcoming events with skill matching for the current user"""
    user_id = request.args.get('user_id')
    if not user_id:
        return VolunteerService.get_upcoming_events_public()
    return VolunteerService.get_upcoming_events_with_skills(user_id)