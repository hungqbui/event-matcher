"""
Comprehensive tests for VolunteerService with database implementation
Run: pytest tests/new_tests/test_volunteer_service_db.py -v
"""

import pytest
from services.volunteerService import VolunteerService
from flask import json
from sqlalchemy import text

class TestGetVolunteerHistory:
    """Test fetching volunteer history"""
    
    def test_get_volunteer_history_success(self, app, test_volunteer, test_admin):
        """Test volunteer can fetch their history"""
        with app.app_context():
            engine = app.config['ENGINE']
            
            # Create events first
            with engine.begin() as conn:
                conn.execute(text("""
                    INSERT INTO events (id, ownerid, name, description, date, location, max_volunteers, urgency, time_label)
                    VALUES (9991, :admin_id, 'Food Drive', 'Distribute food to community', '2024-12-20', 'Community Center', 10, 'medium', 'Sat, Dec 20 · 9:00 AM')
                """), {"admin_id": test_admin['id']})
                
                conn.execute(text("""
                    INSERT INTO events (id, ownerid, name, description, date, location, max_volunteers, urgency, time_label)
                    VALUES (9992, :admin_id, 'Tree Planting', 'Plant trees in city park', '2024-12-15', 'City Park', 15, 'low', 'Sun, Dec 15 · 10:00 AM')
                """), {"admin_id": test_admin['id']})
                
                # Create matches
                conn.execute(text("""
                    INSERT INTO matches (volunteer_id, event_id, status) 
                    VALUES (:volunteer_id, 9991, 'confirmed')
                """), {"volunteer_id": test_volunteer['volunteer_id']})
                
                conn.execute(text("""
                    INSERT INTO matches (volunteer_id, event_id, status) 
                    VALUES (:volunteer_id, 9992, 'pending')
                """), {"volunteer_id": test_volunteer['volunteer_id']})
                
                # Create history records
                conn.execute(text("""
                    INSERT INTO volunteer_history (volunteer_id, event_id, created_at) 
                    VALUES (:volunteer_id, 9991, NOW())
                """), {"volunteer_id": test_volunteer['volunteer_id']})
                
                conn.execute(text("""
                    INSERT INTO volunteer_history (volunteer_id, event_id, created_at) 
                    VALUES (:volunteer_id, 9992, NOW())
                """), {"volunteer_id": test_volunteer['volunteer_id']})
            
            response = VolunteerService.get_volunteer_history_user(test_volunteer['volunteer_id'])
            
            assert response.status_code == 200
            history = response.get_json()
            assert isinstance(history, list)
            assert len(history) >= 2
            
            # Check first record (most recent due to ORDER BY created_at DESC)
            assert 'eventName' in history[0]
            assert 'date' in history[0]
            assert 'status' in history[0]
    
    def test_get_volunteer_history_empty(self, app, test_volunteer):
        """Test fetching history returns empty list when none exists"""
        with app.app_context():
            response = VolunteerService.get_volunteer_history_user(test_volunteer['volunteer_id'])
            
            assert response.status_code == 200
            history = response.get_json()
            assert isinstance(history, list)
            assert len(history) == 0
    
    def test_get_volunteer_history_status_mapping(self, app, test_volunteer, test_admin):
        """Test status mapping based on match status"""
        with app.app_context():
            engine = app.config['ENGINE']
            
            # Create events and matches with different statuses
            with engine.begin() as conn:
                # Event with pending match
                conn.execute(text("""
                    INSERT INTO events (id, ownerid, name, description, date, location, max_volunteers, urgency, time_label)
                    VALUES (9993, :admin_id, 'Pending Event', 'Test', '2024-12-20', 'Location', 10, 'low', 'Dec 20')
                """), {"admin_id": test_admin['id']})
                
                conn.execute(text("""
                    INSERT INTO matches (volunteer_id, event_id, status) 
                    VALUES (:volunteer_id, 9993, 'pending')
                """), {"volunteer_id": test_volunteer['volunteer_id']})
                
                conn.execute(text("""
                    INSERT INTO volunteer_history (volunteer_id, event_id, created_at) 
                    VALUES (:volunteer_id, 9993, NOW())
                """), {"volunteer_id": test_volunteer['volunteer_id']})
                
                # Event with confirmed match
                conn.execute(text("""
                    INSERT INTO events (id, ownerid, name, description, date, location, max_volunteers, urgency, time_label)
                    VALUES (9994, :admin_id, 'Confirmed Event', 'Test', '2024-12-21', 'Location', 10, 'medium', 'Dec 21')
                """), {"admin_id": test_admin['id']})
                
                conn.execute(text("""
                    INSERT INTO matches (volunteer_id, event_id, status) 
                    VALUES (:volunteer_id, 9994, 'confirmed')
                """), {"volunteer_id": test_volunteer['volunteer_id']})
                
                conn.execute(text("""
                    INSERT INTO volunteer_history (volunteer_id, event_id, created_at) 
                    VALUES (:volunteer_id, 9994, NOW())
                """), {"volunteer_id": test_volunteer['volunteer_id']})
                
                # Event with cancelled match
                conn.execute(text("""
                    INSERT INTO events (id, ownerid, name, description, date, location, max_volunteers, urgency, time_label)
                    VALUES (9995, :admin_id, 'Cancelled Event', 'Test', '2024-12-22', 'Location', 10, 'high', 'Dec 22')
                """), {"admin_id": test_admin['id']})
                
                conn.execute(text("""
                    INSERT INTO matches (volunteer_id, event_id, status) 
                    VALUES (:volunteer_id, 9995, 'cancelled')
                """), {"volunteer_id": test_volunteer['volunteer_id']})
                
                conn.execute(text("""
                    INSERT INTO volunteer_history (volunteer_id, event_id, created_at) 
                    VALUES (:volunteer_id, 9995, NOW())
                """), {"volunteer_id": test_volunteer['volunteer_id']})
            
            response = VolunteerService.get_volunteer_history_user(test_volunteer['volunteer_id'])
            history = response.get_json()
            
            # Find each record and check status mapping
            pending_record = next((h for h in history if h['eventName'] == 'Pending Event'), None)
            confirmed_record = next((h for h in history if h['eventName'] == 'Confirmed Event'), None)
            cancelled_record = next((h for h in history if h['eventName'] == 'Cancelled Event'), None)
            
            assert pending_record is not None
            assert pending_record['status'] == 'Registered'
            
            assert confirmed_record is not None
            assert confirmed_record['status'] == 'Attended'
            
            assert cancelled_record is not None
            assert cancelled_record['status'] == 'Cancelled'
    
    def test_get_volunteer_history_ordered_by_date(self, app, test_volunteer, test_admin):
        """Test history is ordered by created_at DESC (most recent first)"""
        with app.app_context():
            engine = app.config['ENGINE']
            
            # Create events and history with different dates
            with engine.begin() as conn:
                # Oldest event
                conn.execute(text("""
                    INSERT INTO events (id, ownerid, name, description, date, location, max_volunteers, urgency, time_label)
                    VALUES (9996, :admin_id, 'Oldest Event', 'Test', '2024-12-01', 'Location', 10, 'low', 'Dec 1')
                """), {"admin_id": test_admin['id']})
                
                conn.execute(text("""
                    INSERT INTO volunteer_history (volunteer_id, event_id, created_at)
                    VALUES (:volunteer_id, 9996, '2024-12-01 10:00:00')
                """), {"volunteer_id": test_volunteer['volunteer_id']})
                
                # Middle event
                conn.execute(text("""
                    INSERT INTO events (id, ownerid, name, description, date, location, max_volunteers, urgency, time_label)
                    VALUES (9997, :admin_id, 'Middle Event', 'Test', '2024-12-15', 'Location', 10, 'low', 'Dec 15')
                """), {"admin_id": test_admin['id']})
                
                conn.execute(text("""
                    INSERT INTO volunteer_history (volunteer_id, event_id, created_at)
                    VALUES (:volunteer_id, 9997, '2024-12-15 10:00:00')
                """), {"volunteer_id": test_volunteer['volunteer_id']})
                
                # Newest event
                conn.execute(text("""
                    INSERT INTO events (id, ownerid, name, description, date, location, max_volunteers, urgency, time_label)
                    VALUES (9998, :admin_id, 'Newest Event', 'Test', '2024-12-25', 'Location', 10, 'low', 'Dec 25')
                """), {"admin_id": test_admin['id']})
                
                conn.execute(text("""
                    INSERT INTO volunteer_history (volunteer_id, event_id, created_at)
                    VALUES (:volunteer_id, 9998, '2024-12-25 10:00:00')
                """), {"volunteer_id": test_volunteer['volunteer_id']})
            
            response = VolunteerService.get_volunteer_history_user(test_volunteer['volunteer_id'])
            history = response.get_json()
            
            # First record should be newest
            assert history[0]['eventName'] == 'Newest Event'
            # Last record should be oldest
            assert history[-1]['eventName'] == 'Oldest Event'
    
    def test_get_volunteer_history_field_mapping(self, app, test_volunteer, test_admin):
        """Test correct field name mapping (event.name -> eventName, time_label -> date)"""
        with app.app_context():
            engine = app.config['ENGINE']
            
            with engine.begin() as conn:
                conn.execute(text("""
                    INSERT INTO events (id, ownerid, name, description, date, location, max_volunteers, urgency, time_label)
                    VALUES (9999, :admin_id, 'Test Event', 'Test Description', '2024-12-20', 'Test Location', 10, 'medium', '2024-12-20 15:30:00')
                """), {"admin_id": test_admin['id']})
                
                conn.execute(text("""
                    INSERT INTO matches (volunteer_id, event_id, status) 
                    VALUES (:volunteer_id, 9999, 'confirmed')
                """), {"volunteer_id": test_volunteer['volunteer_id']})
                
                conn.execute(text("""
                    INSERT INTO volunteer_history (volunteer_id, event_id, created_at) 
                    VALUES (:volunteer_id, 9999, NOW())
                """), {"volunteer_id": test_volunteer['volunteer_id']})
            
            response = VolunteerService.get_volunteer_history_user(test_volunteer['volunteer_id'])
            history = response.get_json()
            
            assert len(history) >= 1
            record = history[0]
            
            # Check field names are correctly mapped
            assert 'eventName' in record
            assert 'date' in record
            assert 'location' in record
            assert 'description' in record
            assert 'status' in record
            
            # Check values
            assert record['eventName'] == 'Test Event'
            assert record['date'] == '2024-12-20 15:30:00'
            assert record['location'] == 'Test Location'
            assert record['description'] == 'Test Description'
            assert record['status'] == 'Attended'  # confirmed match -> Attended
    
    def test_get_volunteer_history_other_volunteer_not_included(self, app, test_volunteer, test_admin, test_user2):
        """Test that only the specified volunteer's history is returned"""
        with app.app_context():
            engine = app.config['ENGINE']
            
            # Create another volunteer
            with engine.begin() as conn:
                conn.execute(text("""
                    INSERT INTO volunteers (id, user_id, phone, availability)
                    VALUES (8888, :user_id, '555-9999', 'weekdays')
                """), {"user_id": test_user2['id']})
                
                # Create events
                conn.execute(text("""
                    INSERT INTO events (id, ownerid, name, description, date, location, max_volunteers, urgency, time_label)
                    VALUES (10001, :admin_id, 'Johns Event', 'Test', '2024-12-20', 'Location', 10, 'low', 'Dec 20')
                """), {"admin_id": test_admin['id']})
                
                conn.execute(text("""
                    INSERT INTO events (id, ownerid, name, description, date, location, max_volunteers, urgency, time_label)
                    VALUES (10002, :admin_id, 'Janes Event', 'Test', '2024-12-20', 'Location', 10, 'low', 'Dec 20')
                """), {"admin_id": test_admin['id']})
                
                # Create history for test volunteer
                conn.execute(text("""
                    INSERT INTO volunteer_history (volunteer_id, event_id, created_at) 
                    VALUES (:volunteer_id, 10001, NOW())
                """), {"volunteer_id": test_volunteer['volunteer_id']})
                
                # Create history for another volunteer
                conn.execute(text("""
                    INSERT INTO volunteer_history (volunteer_id, event_id, created_at) 
                    VALUES (8888, 10002, NOW())
                """))
            
            response = VolunteerService.get_volunteer_history_user(test_volunteer['volunteer_id'])
            history = response.get_json()
            
            # Should only contain test volunteer's history
            assert all(h['eventName'] == 'Johns Event' for h in history)
            assert not any(h['eventName'] == 'Janes Event' for h in history)
    
    def test_get_volunteer_history_multiple_events_same_volunteer(self, app, test_volunteer, test_admin):
        """Test volunteer with multiple event participations"""
        with app.app_context():
            engine = app.config['ENGINE']
            
            # Create multiple events and history records
            with engine.begin() as conn:
                for i in range(5):
                    event_id = 10003 + i
                    conn.execute(text("""
                        INSERT INTO events (id, ownerid, name, description, date, location, max_volunteers, urgency, time_label)
                        VALUES (:event_id, :admin_id, :event_name, 'Test', '2024-12-20', 'Location', 10, 'low', 'Dec 20')
                    """), {
                        "event_id": event_id,
                        "admin_id": test_admin['id'],
                        "event_name": f'Event {i+1}'
                    })
                    
                    conn.execute(text("""
                        INSERT INTO volunteer_history (volunteer_id, event_id, created_at) 
                        VALUES (:volunteer_id, :event_id, NOW())
                    """), {
                        "volunteer_id": test_volunteer['volunteer_id'],
                        "event_id": event_id
                    })
            
            response = VolunteerService.get_volunteer_history_user(test_volunteer['volunteer_id'])
            history = response.get_json()
            
            assert len(history) >= 5
            assert all(isinstance(record, dict) for record in history)
            assert all('eventName' in record for record in history)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
