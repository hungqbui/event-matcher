from flask import current_app, jsonify
from sqlalchemy import text
class VolunteerService:
	@staticmethod
	def get_volunteer_history_user(id):
		engine = current_app.config["ENGINE"]
		with engine.connect() as conn:
			user_id = id
			result = conn.execute(text("""
				SELECT name, event_name as eventName, time_label as date,
						location, description,
						CASE 
							WHEN urgency = 'low' THEN 'Registered'
							WHEN urgency = 'medium' THEN 'Attended'
							WHEN urgency = 'high' THEN 'Cancelled'
							ELSE 'No-Show'
						END as status
				FROM volunteer_history
				WHERE volunteer_id = :volunteer_id
				ORDER BY created_at DESC
			"""), {"volunteer_id": user_id}).mappings().all()
   
		return jsonify([dict(row) for row in result])
