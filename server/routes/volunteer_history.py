from flask import Blueprint, request, jsonify, current_app
from sqlalchemy import text
from ..services.volunteerService import VolunteerService

history_bp = Blueprint('history', __name__)

@history_bp.route('/volunteer-history', methods=['GET'])
def get_volunteer_history():
    id = request.args.get('user_id')
    
    return VolunteerService.get_volunteer_history_user(id)

@history_bp.route('/admin/volunteer-attendance', methods=['GET'])
def get_admin_volunteer_attendance():
    """Get all volunteers who attended events owned by this admin"""
    admin_user_id = request.args.get('admin_user_id')
    
    if not admin_user_id:
        return jsonify({'error': 'admin_user_id is required'}), 400
    
    engine = current_app.config["ENGINE"]
    with engine.connect() as conn:
        # Get admin_id from user_id
        admin_result = conn.execute(text("""
            SELECT id FROM admins WHERE user_id = :user_id
        """), {"user_id": admin_user_id}).mappings().first()
        
        if not admin_result:
            return jsonify({'error': 'Admin not found'}), 404
        
        # Get all volunteers who attended this admin's events
        result = conn.execute(text("""
            SELECT DISTINCT
                u.id as user_id,
                u.name,
                e.id as event_id,
                e.name as eventName,
                e.date,
                e.location,
                e.description,
                v.id as volunteer_id
            FROM matches m
            JOIN events e ON m.event_id = e.id
            JOIN volunteers v ON m.volunteer_id = v.id
            JOIN users u ON v.user_id = u.id
            WHERE e.ownerid = :admin_user_id
                AND m.status = 'confirmed'
            ORDER BY e.date DESC, u.name ASC
        """), {"admin_user_id": admin_user_id}).mappings().all()
        
    return jsonify([dict(row) for row in result]), 200

@history_bp.route('/volunteer-tasks/<int:volunteer_id>/<int:event_id>', methods=['GET'])
def get_volunteer_tasks(volunteer_id, event_id):
    """Get all tasks claimed by a volunteer for a specific event"""
    
    engine = current_app.config["ENGINE"]
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT id, name, score, completed, volunteer_id, event_id
            FROM history_tasks
            WHERE volunteer_id = :volunteer_id
                AND event_id = :event_id
        """), {"volunteer_id": volunteer_id, "event_id": event_id}).mappings().all()
        
    return jsonify([dict(row) for row in result]), 200

@history_bp.route('/task/<int:task_id>/rate', methods=['POST'])
def rate_task(task_id):
    """Rate a task and mark it as completed"""
    data = request.get_json()
    
    rating_percent = data.get('rating_percent')  # 0-100
    
    if rating_percent is None or rating_percent < 0 or rating_percent > 100:
        return jsonify({'error': 'rating_percent must be between 0 and 100'}), 400
    
    engine = current_app.config["ENGINE"]
    with engine.begin() as conn:
        # Get task details
        task = conn.execute(text("""
            SELECT score FROM history_tasks WHERE id = :task_id
        """), {"task_id": task_id}).mappings().first()
        
        if not task:
            return jsonify({'error': 'Task not found'}), 404
        
        # Calculate actual score based on rating
        original_score = task['score']
        actual_score = int((original_score * rating_percent) / 100)
        
        # Update task as completed with the rated score
        conn.execute(text("""
            UPDATE history_tasks
            SET completed = 1, score = :actual_score
            WHERE id = :task_id
        """), {"task_id": task_id, "actual_score": actual_score})
        
    return jsonify({
        'message': 'Task rated successfully',
        'original_score': original_score,
        'rating_percent': rating_percent,
        'actual_score': actual_score
    }), 200

@history_bp.route('/volunteer-total-points', methods=['GET'])
def get_volunteer_total_points():
    """Get total points for a volunteer across all completed tasks"""
    user_id = request.args.get('user_id')
    
    if not user_id:
        return jsonify({'error': 'user_id is required'}), 400
    
    engine = current_app.config["ENGINE"]
    with engine.connect() as conn:
        # Get volunteer_id from user_id
        volunteer_result = conn.execute(text("""
            SELECT id FROM volunteers WHERE user_id = :user_id
        """), {"user_id": user_id}).mappings().first()
        
        if not volunteer_result:
            return jsonify({'total_points': 0}), 200
        
        volunteer_id = volunteer_result['id']
        
        # Sum all scores from completed tasks for this volunteer
        result = conn.execute(text("""
            SELECT COALESCE(SUM(score), 0) as total_points
            FROM history_tasks
            WHERE volunteer_id = :volunteer_id
                AND completed = 1
        """), {"volunteer_id": volunteer_id}).mappings().first()
        
    return jsonify({'total_points': result['total_points']}), 200

@history_bp.route('/leaderboard', methods=['GET'])
def get_leaderboard():
    """Get top 10 volunteers by total points"""
    
    engine = current_app.config["ENGINE"]
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT 
                u.name,
                v.id as volunteer_id,
                COALESCE(SUM(ht.score), 0) as total_points
            FROM volunteers v
            JOIN users u ON v.user_id = u.id
            LEFT JOIN history_tasks ht ON ht.volunteer_id = v.id AND ht.completed = 1
            GROUP BY v.id, u.name
            ORDER BY total_points DESC
            LIMIT 10
        """)).mappings().all()
        
    return jsonify([dict(row) for row in result]), 200