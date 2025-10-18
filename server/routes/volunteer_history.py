from flask import Blueprint, jsonify
from services.volunteerService import VolunteerService

history_bp = Blueprint('history', __name__)

@history_bp.route('/volunteer-history', methods=['GET'])  # Note: /volunteer-history under /api prefix
def get_volunteer_history():
    return VolunteerService.get_volunteer_history_user()