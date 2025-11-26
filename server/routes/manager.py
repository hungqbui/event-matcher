from flask import Blueprint, request, jsonify
from ..services.managerService import ManagerEventService


bp = Blueprint('manager', __name__)

@bp.route('/listevents', methods=['POST'])
def fetch_events():
    return ManagerEventService.fetch_events()

@bp.route('/events', methods=['POST'])
def create_event():
    """Create a new event"""
    data = request.get_json()
    return ManagerEventService.create_event(data)

@bp.route('/events/<event_id>', methods=['POST'])
def update_event(event_id):
    """Update an existing event"""
   
    data = request.get_json()

    return ManagerEventService.update_event(event_id, data)


@bp.route('/events/<event_id>', methods=['DELETE'])
def delete_event(event_id):

    return ManagerEventService.delete_event(event_id)