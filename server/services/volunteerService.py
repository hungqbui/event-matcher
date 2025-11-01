from flask import current_app, jsonify
from sqlalchemy import text
class VolunteerService:
	@staticmethod
	def get_volunteer_history_user(id):
		engine = current_app.config["ENGINE"]
		with engine.connect() as conn:
			user_id = id
			result = conn.execute(text("""
				SELECT e.name as eventName, e.time_label as date,
						e.location, e.description,
						CASE 
							WHEN m.status = 'pending' THEN 'Registered'
							WHEN m.status = 'confirmed' THEN 'Attended'
							WHEN m.status = 'cancelled' THEN 'Cancelled'
							ELSE 'Registered'
						END as status
				FROM volunteer_history vh
				JOIN events e ON vh.event_id = e.id
				LEFT JOIN matches m ON vh.volunteer_id = m.volunteer_id AND vh.event_id = m.event_id
				WHERE vh.volunteer_id = :volunteer_id
				ORDER BY vh.created_at DESC
			"""), {"volunteer_id": user_id}).mappings().all()
   
		return jsonify([dict(row) for row in result])
