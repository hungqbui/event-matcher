from flask import Blueprint, request
from ..services.volunteerService import VolunteerService

bp = Blueprint('volunteer', __name__)

@bp.route('/history', methods=['GET'])
def get_volunteer_history():
    """Get volunteer history for the user"""
    return VolunteerService.get_volunteer_history()