from sqlalchemy import create_engine, text
from ..db.db import get_db_connection

class VolunteerService:
    @staticmethod
    def get_volunteer_history_user():
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        user_id = 1  # TODO: from auth

        try:
            cursor.execute("""
                SELECT v.id as volunteer_id
                FROM volunteers v
                WHERE v.user_id = %s
            """, (user_id,))
            vol = cursor.fetchone()
            if not vol:
                return []

            volunteer_id = vol['volunteer_id']

            cursor.execute("""
                SELECT name, event_name as eventName, time_label as date,
                       location, description,
                       CASE 
                         WHEN urgency = 'low' THEN 'Registered'
                         WHEN urgency = 'medium' THEN 'Attended'
                         WHEN urgency = 'high' THEN 'Cancelled'
                         ELSE 'No-Show'
                       END as status
                FROM volunteer_history
                WHERE volunteer_id = %s
                ORDER BY created_at DESC
            """, (volunteer_id,))
            return cursor.fetchall()
        finally:
            cursor.close()