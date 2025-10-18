from flask import Blueprint, request, jsonify
from services.volunteerMatchingService import VolunteerService, EventService, MatchService

bp = Blueprint('volunteer_matching', __name__)


# ========== Volunteer Routes ==========

@bp.route('/volunteers', methods=['GET'])
def list_volunteers():
    """Get all volunteers"""
    return VolunteerService.get_all()


@bp.route('/volunteers/<int:id>', methods=['GET'])
def get_volunteer(id):
    """Get volunteer by ID"""
    return VolunteerService.get_by_id(id)


@bp.route('/volunteers', methods=['POST'])
def add_volunteer():
    """Create a new volunteer"""
    data = request.json
    return VolunteerService.create(data)


@bp.route('/volunteers/<int:id>', methods=['PUT'])
def edit_volunteer(id):
    """Update a volunteer"""
    data = request.json
    return VolunteerService.update(id, data)


@bp.route('/volunteers/<int:id>', methods=['DELETE'])
def remove_volunteer(id):
    """Delete a volunteer"""
    return VolunteerService.delete(id)


# ========== Event Routes ==========

@bp.route('/events', methods=['GET'])
def list_events():
    """Get all events"""
    return EventService.get_all()


@bp.route('/events/<int:id>', methods=['GET'])
def get_event(id):
    """Get event by ID"""
    return EventService.get_by_id(id)


@bp.route('/events', methods=['POST'])
def add_event():
    """Create a new event"""
    data = request.json
    return EventService.create(data)


@bp.route('/events/<int:id>', methods=['PUT'])
def edit_event(id):
    """Update an event"""
    data = request.json
    return EventService.update(id, data)


@bp.route('/events/<int:id>', methods=['DELETE'])
def remove_event(id):
    """Delete an event"""
    return EventService.delete(id)


# ========== Match Routes ==========

@bp.route('/match/find', methods=['POST'])
def find_match():
    """Find best matching event for a volunteer"""
    data = request.json
    vol_id = data.get('volunteer_id')
    
    if not vol_id:
        return jsonify({'error': 'Volunteer ID required'}), 400
    
    return MatchService.find_best_match(vol_id)


@bp.route('/match', methods=['POST'])
def make_match():
    """Create a match between volunteer and event"""
    data = request.json
    vol_id = data.get('volunteer_id')
    event_id = data.get('event_id')
    
    return MatchService.create_match(vol_id, event_id)


@bp.route('/matches', methods=['GET'])
def list_matches():
    """Get all matches"""
    return MatchService.get_all()


@bp.route('/matches/volunteer/<int:id>', methods=['GET'])
def volunteer_matches(id):
    """Get matches for a specific volunteer"""
    return MatchService.get_by_volunteer(id)


@bp.route('/matches/event/<int:id>', methods=['GET'])
def event_matches(id):
    """Get matches for a specific event"""
    return MatchService.get_by_event(id)


@bp.route('/matches/<int:id>', methods=['DELETE'])
def remove_match(id):
    """Delete a match"""
    return MatchService.delete(id)


@bp.route('/matches/<int:id>/status', methods=['PUT'])
def change_status(id):
    """Update match status"""
    data = request.json
    status = data.get('status')
    return MatchService.update_status(id, status)