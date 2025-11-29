from flask import Blueprint, request, jsonify, current_app
from sqlalchemy import text
from ..services.volunteerMatchingService import VolunteerService, EventService, MatchService

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
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid or missing JSON body'}), 400
    return VolunteerService.create(data)


@bp.route('/volunteers/<int:id>', methods=['PUT'])
def edit_volunteer(id):
    """Update a volunteer"""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid or missing JSON body'}), 400
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
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid or missing JSON body'}), 400
    return EventService.create(data)


@bp.route('/events/<int:id>', methods=['PUT'])
def edit_event(id):
    """Update an event"""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid or missing JSON body'}), 400
    return EventService.update(id, data)


@bp.route('/events/<int:id>', methods=['DELETE'])
def remove_event(id):
    """Delete an event"""
    return EventService.delete(id)


# ========== Match Routes ==========

@bp.route('/match/find', methods=['POST'])
def find_match():
    """Find best matching event for a volunteer"""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid or missing JSON body'}), 400

    vol_id = data.get('volunteer_id')
    admin_id = data.get('admin_id')
    if not vol_id:
        return jsonify({'error': 'Volunteer ID required'}), 400

    return MatchService.find_best_match(vol_id, admin_id)


@bp.route('/match', methods=['POST'])
def make_match():
    """Create a match between volunteer and event"""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid or missing JSON body'}), 400

    vol_id = data.get('volunteer_id')
    event_id = data.get('event_id')

    if not vol_id or not event_id:
        return jsonify({'error': 'volunteer_id and event_id are required'}), 400

    return MatchService.create_match(vol_id, event_id)


@bp.route('/register-event', methods=['POST'])
def register_for_event():
    """Register a user for an event (creates match using user_id)"""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid or missing JSON body'}), 400

    user_id = data.get('user_id')
    event_id = data.get('event_id')

    if not user_id or not event_id:
        return jsonify({'error': 'user_id and event_id are required'}), 400

    # Get volunteer_id from user_id
    engine = current_app.config["ENGINE"]
    with engine.connect() as conn:
        result = conn.execute(text("SELECT id FROM volunteers WHERE user_id = :user_id"), {"user_id": user_id})
        volunteer = result.mappings().first()
        
        if not volunteer:
            return jsonify({'error': 'Volunteer profile not found for this user'}), 404
        
        volunteer_id = volunteer['id']
        
        # Get event details and owner
        event_result = conn.execute(text("""
            SELECT e.name as event_name, e.ownerid, u.name as volunteer_name
            FROM events e, users u
            WHERE e.id = :event_id AND u.id = :user_id
        """), {"event_id": event_id, "user_id": user_id})
        event_data = event_result.mappings().first()
        
        if event_data:
            # Create notification for event owner
            conn.execute(text("""
                INSERT INTO notifications (user_id, type, message, is_read, created_at)
                VALUES (:owner_id, 'info', :message, 0, NOW())
            """), {
                "owner_id": event_data['ownerid'],
                "message": f"{event_data['volunteer_name']} has registered for your event '{event_data['event_name']}'"
            })
            conn.commit()

    # Create the match
    return MatchService.create_match(volunteer_id, event_id, status='confirmed')


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
    # Get match details before deleting for notification
    engine = current_app.config["ENGINE"]
    with engine.connect() as conn:
        match_result = conn.execute(text("""
            SELECT m.volunteer_id, m.event_id, e.name as event_name, e.ownerid, u.name as volunteer_name
            FROM matches m
            JOIN events e ON m.event_id = e.id
            JOIN volunteers v ON m.volunteer_id = v.id
            JOIN users u ON v.user_id = u.id
            WHERE m.id = :match_id
        """), {"match_id": id})
        match_data = match_result.mappings().first()
        
        if match_data:
            # Create notification for event owner about unregistration
            conn.execute(text("""
                INSERT INTO notifications (user_id, type, message, is_read, created_at)
                VALUES (:owner_id, 'warning', :message, 0, NOW())
            """), {
                "owner_id": match_data['ownerid'],
                "message": f"{match_data['volunteer_name']} has unregistered from your event '{match_data['event_name']}'"
            })
            conn.commit()
    
    return MatchService.delete(id)


@bp.route('/matches/<int:id>/status', methods=['PUT'])
def change_status(id):
    """Update match status"""
    data = request.get_json(silent=True)
    if not data:
        return jsonify({'error': 'Invalid or missing JSON body'}), 400

    status = data.get('status')
    if not status:
        return jsonify({'error': 'Status required'}), 400

    return MatchService.update_status(id, status)