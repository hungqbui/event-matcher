from flask import Blueprint, request, jsonify
from functools import wraps
from ..services.managerService import ManagerEventService, MOCK_EVENTS
from ..middleware.auth import admin_required


bp = Blueprint('manager', __name__)

@bp.route('/events', methods=['GET'])
@admin_required
def fetch_events():
    return ManagerEventService.fetch_events()

@bp.route('/events', methods=['POST'])
@admin_required
def create_event():
    """Create a new event"""
    data = request.get_json()
    return ManagerEventService.create_event(data)

@bp.route('/events/<event_id>', methods=['PUT'])
@admin_required
def update_event(event_id):
    """Update an existing event"""
   
    data = request.get_json()

    return ManagerEventService.update_event(event_id, data)


@bp.route('/events/<event_id>', methods=['DELETE'])
@admin_required
def delete_event(event_id):
    """Delete an event"""
    if event_id not in MOCK_EVENTS:
        return jsonify({'message': 'Event not found'}), 404

    return ManagerEventService.delete_event(event_id)