from sqlalchemy import text
from flask import jsonify, current_app
from datetime import datetime

class TaskService:
    """Service for managing event tasks"""
    
    @staticmethod
    def get_tasks_by_event(event_id):
        """Get all tasks for a specific event"""
        engine = current_app.config["ENGINE"]
        
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id, history_id, name, completed, volunteer_id, event_id, score
                FROM history_tasks
                WHERE event_id = :event_id
                ORDER BY id ASC
            """), {"event_id": event_id}).mappings().all()
            
        return jsonify([dict(row) for row in result]), 200
    
    @staticmethod
    def create_task(data):
        """Create a new task for an event"""
        required_fields = ['event_id', 'name', 'score']
        for field in required_fields:
            if field not in data:
                return jsonify({'success': False, 'message': f'Missing field: {field}'}), 400
        
        # Validate score is a number
        try:
            score = int(data['score'])
            if score < 0:
                return jsonify({'success': False, 'message': 'Score must be non-negative'}), 400
        except (ValueError, TypeError):
            return jsonify({'success': False, 'message': 'Score must be a valid number'}), 400
        
        engine = current_app.config["ENGINE"]
        
        with engine.connect() as conn:
            # Check if event exists
            event = conn.execute(text("SELECT id FROM events WHERE id = :event_id"), 
                               {"event_id": data['event_id']}).first()
            if not event:
                return jsonify({'success': False, 'message': 'Event not found'}), 404
            
            result = conn.execute(text("""
                INSERT INTO history_tasks (event_id, name, score, completed)
                VALUES (:event_id, :name, :score, FALSE)
            """), {
                "event_id": data['event_id'],
                "name": data['name'],
                "score": score
            })
            conn.commit()
            task_id = result.lastrowid
            
        return jsonify({
            'success': True,
            'message': 'Task created successfully',
            'task_id': task_id
        }), 201
    
    @staticmethod
    def update_task(task_id, data):
        """Update an existing task"""
        engine = current_app.config["ENGINE"]
        
        with engine.connect() as conn:
            # Check if task exists
            task = conn.execute(text("SELECT id FROM history_tasks WHERE id = :task_id"), 
                              {"task_id": task_id}).first()
            if not task:
                return jsonify({'success': False, 'message': 'Task not found'}), 404
            
            # Build update query dynamically based on provided fields
            update_fields = []
            params = {"task_id": task_id}
            
            if 'name' in data:
                update_fields.append("name = :name")
                params['name'] = data['name']
            
            if 'score' in data:
                try:
                    score = int(data['score'])
                    if score < 0:
                        return jsonify({'success': False, 'message': 'Score must be non-negative'}), 400
                    update_fields.append("score = :score")
                    params['score'] = score
                except (ValueError, TypeError):
                    return jsonify({'success': False, 'message': 'Score must be a valid number'}), 400
            
            if 'completed' in data:
                update_fields.append("completed = :completed")
                params['completed'] = bool(data['completed'])
            
            if not update_fields:
                return jsonify({'success': False, 'message': 'No fields to update'}), 400
            
            query = f"UPDATE history_tasks SET {', '.join(update_fields)} WHERE id = :task_id"
            conn.execute(text(query), params)
            conn.commit()
            
        return jsonify({'success': True, 'message': 'Task updated successfully'}), 200
    
    @staticmethod
    def delete_task(task_id):
        """Delete a task"""
        engine = current_app.config["ENGINE"]
        
        with engine.connect() as conn:
            result = conn.execute(text("DELETE FROM history_tasks WHERE id = :task_id"), 
                                {"task_id": task_id})
            conn.commit()
            
            if result.rowcount == 0:
                return jsonify({'success': False, 'message': 'Task not found'}), 404
            
        return jsonify({'success': True, 'message': 'Task deleted successfully'}), 200
    
    @staticmethod
    def assign_task(task_id, volunteer_id):
        """Assign a task to a volunteer"""
        engine = current_app.config["ENGINE"]
        
        with engine.connect() as conn:
            # Check if task exists and is not already assigned
            task = conn.execute(text("""
                SELECT id, volunteer_id, event_id, name
                FROM history_tasks 
                WHERE id = :task_id
            """), {"task_id": task_id}).mappings().first()
            
            if not task:
                return jsonify({'success': False, 'message': 'Task not found'}), 404
            
            if task['volunteer_id'] is not None:
                return jsonify({'success': False, 'message': 'Task already assigned'}), 400
            
            # Check if volunteer exists
            volunteer = conn.execute(text("SELECT id, user_id FROM volunteers WHERE id = :volunteer_id"), 
                                   {"volunteer_id": volunteer_id}).mappings().first()
            if not volunteer:
                return jsonify({'success': False, 'message': 'Volunteer not found'}), 404
            
            # Assign the task
            conn.execute(text("""
                UPDATE history_tasks 
                SET volunteer_id = :volunteer_id
                WHERE id = :task_id
            """), {
                "task_id": task_id,
                "volunteer_id": volunteer_id
            })
            conn.commit()
            
            # Get event owner (admin) to send notification
            event = conn.execute(text("""
                SELECT ownerid FROM events WHERE id = :event_id
            """), {"event_id": task['event_id']}).mappings().first()
            
            if event and event['ownerid']:
                # Get volunteer name
                user = conn.execute(text("""
                    SELECT name FROM users WHERE id = :user_id
                """), {"user_id": volunteer['user_id']}).mappings().first()
                
                volunteer_name = user['name'] if user else 'A volunteer'
                
                # Create notification for admin
                conn.execute(text("""
                    INSERT INTO notifications (user_id, type, message)
                    VALUES (:user_id, :type, :message)
                """), {
                    "user_id": event['ownerid'],
                    "type": "info",
                    "message": f"{volunteer_name} has claimed the task '{task['name']}' for your event."
                })
                conn.commit()
        
        return jsonify({
            'success': True,
            'message': 'Task assigned successfully'
        }), 200
    
    @staticmethod
    def get_unassigned_tasks_by_event(event_id):
        """Get all unassigned tasks for a specific event"""
        engine = current_app.config["ENGINE"]
        
        with engine.connect() as conn:
            result = conn.execute(text("""
                SELECT id, name, score, completed
                FROM history_tasks
                WHERE event_id = :event_id AND volunteer_id IS NULL
                ORDER BY id ASC
            """), {"event_id": event_id}).mappings().all()
            
        return jsonify([dict(row) for row in result]), 200
