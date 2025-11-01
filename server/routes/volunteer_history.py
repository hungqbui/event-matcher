from flask import Blueprint, request
from ..services.volunteerService import VolunteerService

history_bp = Blueprint('history', __name__)

@history_bp.route('/volunteer-history', methods=['GET'])
def get_volunteer_history():
    id = request.args.get('user_id')
    
    return VolunteerService.get_volunteer_history_user(id)