from flask import current_app, jsonify
from sqlalchemy import text
from datetime import datetime

class VolunteerService:
	@staticmethod
	def get_volunteer_history_user(id):
		engine = current_app.config["ENGINE"]
		with engine.connect() as conn:
			user_id = id
			
			# First, get volunteer_id from user_id
			volunteer_result = conn.execute(text("""
				SELECT id FROM volunteers WHERE user_id = :user_id
			"""), {"user_id": user_id}).mappings().first()
			
			if not volunteer_result:
				return jsonify([])
			
			volunteer_id = volunteer_result['id']
			
			# Get all events the user joined from matches table
			result = conn.execute(text("""
				SELECT e.id, e.name as event_name, e.date, e.time_label,
						e.location, e.description, e.urgency, e.img,
						m.volunteer_id, e.id as event_id,
						m.status,
						CASE 
							WHEN m.status = 'pending' THEN 'Registered'
							WHEN m.status = 'confirmed' THEN 'Confirmed'
							WHEN m.status = 'cancelled' THEN 'Cancelled'
							ELSE 'Registered'
						END as status_display,
						0 as score
				FROM matches m
				JOIN events e ON m.event_id = e.id
				WHERE m.volunteer_id = :volunteer_id
				ORDER BY e.date DESC
			"""), {"volunteer_id": volunteer_id}).mappings().all()
   
		return jsonify([dict(row) for row in result])

	@staticmethod
	def get_upcoming_events_public():
		"""Get all upcoming events without skill matching"""
		engine = current_app.config["ENGINE"]
		with engine.connect() as conn:
			result = conn.execute(text("""
				SELECT e.*,
					   GROUP_CONCAT(DISTINCT s.name) as required_skills,
					   COUNT(DISTINCT m.id) as current_volunteers
				FROM events e
				LEFT JOIN event_requirements er ON e.id = er.event_id
				LEFT JOIN skills s ON er.skill_id = s.id
				LEFT JOIN matches m ON e.id = m.event_id
				GROUP BY e.id
				ORDER BY e.date DESC, e.urgency DESC
			""")).mappings().all()
		
		events_list = []
		for event in result:
			event_dict = dict(event)
			event_dict['required_skills'] = event_dict['required_skills'].split(',') if event_dict['required_skills'] else []
			event_dict['skill_match_count'] = 0
			event_dict['is_skill_match'] = False
			events_list.append(event_dict)
		
		return jsonify(events_list), 200

	@staticmethod
	def get_upcoming_events_with_skills(user_id):
		"""Get all upcoming events with skill matching for the user"""
		engine = current_app.config["ENGINE"]
		with engine.connect() as conn:
			# Get user's skills
			user_skills_result = conn.execute(text("""
				SELECT s.name
				FROM user_skills us
				JOIN skills s ON us.skill_id = s.id
				WHERE us.user_id = :user_id
			"""), {"user_id": user_id}).mappings().all()
			
			user_skills = set(row['name'].lower() for row in user_skills_result)
			
			# Get volunteer_id for the user
			volunteer_result = conn.execute(text("""
				SELECT id FROM volunteers WHERE user_id = :user_id
			"""), {"user_id": user_id}).mappings().first()
			
			volunteer_id = volunteer_result['id'] if volunteer_result else None
			
			# Get all upcoming events with required skills and registration status
			result = conn.execute(text("""
				SELECT e.*,
					   GROUP_CONCAT(DISTINCT s.name) as required_skills,
					   COUNT(DISTINCT m.id) as current_volunteers,
					   MAX(CASE WHEN m2.volunteer_id = :volunteer_id THEN 1 ELSE 0 END) as is_registered
				FROM events e
				LEFT JOIN event_requirements er ON e.id = er.event_id
				LEFT JOIN skills s ON er.skill_id = s.id
				LEFT JOIN matches m ON e.id = m.event_id
				LEFT JOIN matches m2 ON e.id = m2.event_id
				GROUP BY e.id
				ORDER BY e.date DESC, e.urgency DESC
			"""), {"volunteer_id": volunteer_id}).mappings().all()
		
		events_list = []
		for event in result:
			event_dict = dict(event)
			required_skills = event_dict['required_skills'].split(',') if event_dict['required_skills'] else []
			event_dict['required_skills'] = required_skills
			
			# Calculate skill matching
			required_skills_lower = set(s.lower() for s in required_skills)
			matching_skills = user_skills & required_skills_lower
			
			event_dict['skill_match_count'] = len(matching_skills)
			event_dict['matching_skills'] = list(matching_skills)
			event_dict['is_skill_match'] = len(matching_skills) > 0
			event_dict['is_registered'] = bool(event_dict['is_registered'])
			
			events_list.append(event_dict)
		
		# Sort by skill match count (descending), then by date
		events_list.sort(key=lambda x: (-x['skill_match_count'], x['date']))
		
		return jsonify(events_list), 200
