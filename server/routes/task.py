from flask import Blueprint, request, jsonify
from server.services.taskService import TaskService

task_bp = Blueprint('task', __name__)

@task_bp.route('/event/<int:event_id>', methods=['GET'])
def get_event_tasks(event_id):
    """Get all tasks for a specific event"""
    return TaskService.get_tasks_by_event(event_id)

@task_bp.route('/event/<int:event_id>/unassigned', methods=['GET'])
def get_unassigned_tasks(event_id):
    """Get all unassigned tasks for a specific event"""
    return TaskService.get_unassigned_tasks_by_event(event_id)

@task_bp.route('/', methods=['POST'])
def create_task():
    """Create a new task"""
    data = request.get_json()
    return TaskService.create_task(data)

@task_bp.route('/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    """Update an existing task"""
    data = request.get_json()
    return TaskService.update_task(task_id, data)

@task_bp.route('/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    """Delete a task"""
    return TaskService.delete_task(task_id)

@task_bp.route('/<int:task_id>/assign', methods=['POST'])
def assign_task(task_id):
    """Assign a task to a volunteer"""
    data = request.get_json()
    
    if 'volunteer_id' not in data:
        return jsonify({'success': False, 'message': 'volunteer_id is required'}), 400
    
    return TaskService.assign_task(task_id, data['volunteer_id'])
