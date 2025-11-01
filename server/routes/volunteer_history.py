from flask import Blueprint
from ..services.volunteerService import VolunteerService

history_bp = Blueprint('history', __name__)

@history_bp.route('/volunteer-history', methods=['GET'])
def get_volunteer_history():
    return VolunteerService.get_volunteer_history_user()