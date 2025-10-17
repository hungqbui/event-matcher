import pytest
from services.volunteerMatchingService import (
    ValidationHelper,
    MatchingHelper,
    VolunteerService,
    EventService,
    MatchService,
    VOLUNTEERS,
    EVENTS,
    MATCHES,

)


@pytest.fixture(autouse=True)
def reset_data():
    """Reset all data stores before each test"""
    VOLUNTEERS.clear()
    EVENTS.clear()
    MATCHES.clear()

    yield


class TestValidationHelper:
    """Test validation utilities"""
    
    def test_valid_email_correct(self):
        assert ValidationHelper.valid_email('test@example.com') == True
        assert ValidationHelper.valid_email('user.name@domain.co.uk') == True
    
    def test_valid_email_incorrect(self):
        assert ValidationHelper.valid_email('invalid') == False
        assert ValidationHelper.valid_email('no@domain') == False
        assert ValidationHelper.valid_email('@domain.com') == False
    
    def test_valid_phone_correct(self):
        assert ValidationHelper.valid_phone('123-456-7890') == True
        assert ValidationHelper.valid_phone('(123) 456-7890') == True
        assert ValidationHelper.valid_phone('1234567890') == True
    
    def test_valid_phone_incorrect(self):
        assert ValidationHelper.valid_phone('123') == False
        assert ValidationHelper.valid_phone('abc-def-ghij') == False
    
    def test_valid_date_correct(self):
        # Update to match actual format: MM/DD/YYYY
        assert ValidationHelper.valid_date('12/31/2024') == True
        assert ValidationHelper.valid_date('01/01/2025') == True
    
    def test_valid_date_incorrect(self):
        # Update expectations based on actual validation
        assert ValidationHelper.valid_date('12-31-2024') == False
        assert ValidationHelper.valid_date('13/01/2024') == False
        assert ValidationHelper.valid_date('invalid') == False


class TestMatchingHelper:
    """Test matching algorithms"""
    
    def test_calculate_score_perfect_match(self):
        vol = {
            'skills': ['Python', 'JavaScript', 'Teaching'],
            'availability': ['Monday', 'Wednesday']
        }
        event = {
            'requirements': ['Python', 'JavaScript'],
            'date': 'Monday'
        }
        score = MatchingHelper.calculate_score(vol, event)
        # Score is based on percentage match
        assert score > 0
    
    def test_calculate_score_partial_match(self):
        vol = {
            'skills': ['Python'],
            'availability': ['Monday']
        }
        event = {
            'requirements': ['Python', 'JavaScript'],
            'date': 'Tuesday'
        }
        score = MatchingHelper.calculate_score(vol, event)
        assert score > 0  # Has some skill match
    
    def test_calculate_score_no_match(self):
        vol = {
            'skills': ['Java'],
            'availability': ['Monday']
        }
        event = {
            'requirements': ['Python'],
            'date': 'Tuesday'
        }
        score = MatchingHelper.calculate_score(vol, event)
        assert score == 0
    
    def test_count_volunteers_no_matches(self):
        count = MatchingHelper.count_volunteers(1)
        assert count == 0
    
    def test_count_volunteers_with_matches(self):
        MATCHES.append({'id': 1, 'event_id': 1, 'volunteer_id': 1})
        MATCHES.append({'id': 2, 'event_id': 1, 'volunteer_id': 2})
        MATCHES.append({'id': 3, 'event_id': 2, 'volunteer_id': 3})
        
        assert MatchingHelper.count_volunteers(1) == 2
        assert MatchingHelper.count_volunteers(2) == 1
        assert MatchingHelper.count_volunteers(3) == 0
    
    def test_is_matched_true(self):
        MATCHES.append({'id': 1, 'event_id': 1, 'volunteer_id': 1})
        assert MatchingHelper.is_matched(1, 1) == True
    
    def test_is_matched_false(self):
        MATCHES.append({'id': 1, 'event_id': 1, 'volunteer_id': 1})
        assert MatchingHelper.is_matched(1, 2) == False
        assert MatchingHelper.is_matched(2, 1) == False


class TestVolunteerService:
    """Test volunteer CRUD operations"""
    
    def test_get_all_empty(self):
            response, status = VolunteerService.get_all()
            assert status == 200
            assert response.json == []
    
    def test_get_all_with_data(self):
            VOLUNTEERS.append({'id': 1, 'name': 'John'})
            VOLUNTEERS.append({'id': 2, 'name': 'Jane'})
            
            response, status = VolunteerService.get_all()
            assert status == 200
            assert len(response.json) == 2
    
    def test_get_by_id_success(self):
            VOLUNTEERS.append({'id': 1, 'name': 'John'})
            
            response, status = VolunteerService.get_by_id(1)
            assert status == 200
            assert response.json['name'] == 'John'
    
    def test_get_by_id_not_found(self):
            response, status = VolunteerService.get_by_id(999)
            assert status == 404
            assert 'error' in response.json
    
    def test_create_success(self):
            data = {
                'name': 'John Doe',
                'email': 'john@example.com',
                'phone': '123-456-7890',
                'skills': ['Python', 'Teaching'],
                'availability': ['Monday', 'Wednesday']
            }
            print(VOLUNTEERS)
            response, status = VolunteerService.create(data)
            print(VOLUNTEERS)

            assert status == 201
            assert response.json['id'] == 1
            assert response.json['name'] == 'John Doe'
            assert response.json['email'] == 'john@example.com'
            assert len(VOLUNTEERS) == 1
    
    def test_create_missing_name(self):
            data = {'email': 'john@example.com', 'skills': ['Python'], 'availability': ['Monday']}
            response, status = VolunteerService.create(data)
            assert status == 400
            assert 'Name required' in response.json['error']
    
    def test_create_missing_email(self):
            data = {'name': 'John', 'skills': ['Python'], 'availability': ['Monday']}
            response, status = VolunteerService.create(data)
            assert status == 400
            assert 'Email required' in response.json['error']
    
    def test_create_invalid_email(self):
            data = {
                'name': 'John',
                'email': 'invalid-email',
                'skills': ['Python'],
                'availability': ['Monday']
            }
            response, status = VolunteerService.create(data)
            assert status == 400
            assert 'Invalid email' in response.json['error']
    
    def test_create_missing_skills(self):
            data = {'name': 'John', 'email': 'john@example.com', 'availability': ['Monday']}
            response, status = VolunteerService.create(data)
            assert status == 400
            assert 'Skills required' in response.json['error']
    
    def test_create_missing_availability(self):
            data = {'name': 'John', 'email': 'john@example.com', 'skills': ['Python']}
            response, status = VolunteerService.create(data)
            assert status == 400
            assert 'Availability required' in response.json['error']
    
    def test_create_duplicate_email(self):
            data = {
                'name': 'John',
                'email': 'john@example.com',
                'skills': ['Python'],
                'availability': ['Monday']
            }
            VolunteerService.create(data)
            
            response, status = VolunteerService.create(data)
            assert status == 400
            assert 'Email exists' in response.json['error']
    
    def test_create_email_case_insensitive(self):
            data = {
                'name': 'John',
                'email': 'JOHN@EXAMPLE.COM',
                'skills': ['Python'],
                'availability': ['Monday']
            }
            response, status = VolunteerService.create(data)
            assert status == 201
            assert response.json['email'] == 'john@example.com'
    
    def test_update_success(self):
            VOLUNTEERS.append({
                'id': 1,
                'name': 'John',
                'email': 'john@example.com',
                'phone': '123-456-7890',
                'skills': ['Python'],
                'availability': ['Monday']
            })
            
            update_data = {'name': 'John Updated', 'skills': ['Python', 'JavaScript']}
            temp = VolunteerService.update(1, update_data)
            # print(temp)
            response , status = temp

            assert status == 200
            assert response.json['name'] == 'John Updated'
            assert 'JavaScript' in response.json['skills']
    
    def test_update_not_found(self):
            response, status = VolunteerService.update(999, {'name': 'Test'})
            assert status == 404
    
    def test_update_invalid_email(self):
            VOLUNTEERS.append({
                'id': 1,
                'name': 'John',
                'email': 'john@example.com',
                'phone': '',
                'skills': ['Python'],
                'availability': ['Monday']
            })
            
            response, status = VolunteerService.update(1, {'email': 'invalid'})
            assert status == 400
            assert 'Invalid email' in response.json['error']
    
    def test_update_duplicate_email(self):
            VOLUNTEERS.append({
                'id': 1,
                'name': 'John',
                'email': 'john@example.com',
                'phone': '',
                'skills': ['Python'],
                'availability': ['Monday']
            })
            VOLUNTEERS.append({
                'id': 2,
                'name': 'Jane',
                'email': 'jane@example.com',
                'phone': '',
                'skills': ['Python'],
                'availability': ['Monday']
            })
            
            response, status = VolunteerService.update(1, {'email': 'jane@example.com'})
            assert status == 400
            assert 'Email exists' in response.json['error']
    
    def test_delete_success(self):
            VOLUNTEERS.append({'id': 1, 'name': 'John'})
            MATCHES.append({'id': 1, 'volunteer_id': 1, 'event_id': 1})
            
            response, status = VolunteerService.delete(1)
            assert status == 200
            assert 'Deleted' in response.json['message']
            assert len(VOLUNTEERS) == 0
            assert len(MATCHES) == 0
    
    def test_delete_not_found(self):
            response, status = VolunteerService.delete(999)
            assert status == 404


class TestEventService:
    """Test event CRUD operations"""
    
    def test_get_all_empty(self):
        response, status = EventService.get_all()
        assert status == 200
        assert response.json == []
    
    def test_get_all_with_volunteer_count(self):
        EVENTS.append({
            'id': 1,
            'name': 'Event 1',
            'description': 'Test',
            'requirements': ['Python'],
            'date': '12/31/2024',
            'location': 'City',
            'max_volunteers': 10
        })
        MATCHES.append({'id': 1, 'event_id': 1, 'volunteer_id': 1})
        MATCHES.append({'id': 2, 'event_id': 1, 'volunteer_id': 2})
        
        response, status = EventService.get_all()
        assert status == 200
        assert response.json[0]['current_volunteers'] == 2
    
    def test_get_by_id_success(self):
        EVENTS.append({
            'id': 1,
            'name': 'Event 1',
            'description': 'Test',
            'requirements': ['Python'],
            'date': '12/31/2024',
            'location': 'City',
            'max_volunteers': 10
        })
        
        response, status = EventService.get_by_id(1)
        assert status == 200
        assert response.json['name'] == 'Event 1'
        assert response.json['current_volunteers'] == 0
    
    def test_get_by_id_not_found(self):
        response, status = EventService.get_by_id(999)
        assert status == 404
    
    def test_create_success(self):
        data = {
            'name': 'Beach Cleanup',
            'description': 'Clean the beach',
            'requirements': ['Physical fitness'],
            'date': '12/31/2024',
            'location': 'Beach',
            'max_volunteers': 20
        }
        
        response, status = EventService.create(data)
        assert status == 201
        assert response.json['id'] == 1
        assert response.json['name'] == 'Beach Cleanup'
        assert response.json['max_volunteers'] == 20
        assert len(EVENTS) == 1
    
    def test_create_missing_name(self):
        data = {
            'requirements': ['Python'],
            'date': '12/31/2024'
        }
        response, status = EventService.create(data)
        assert status == 400
        assert 'Name required' in response.json['error']
    
    def test_create_missing_requirements(self):
        data = {
            'name': 'Event',
            'date': '12/31/2024'
        }
        response, status = EventService.create(data)
        assert status == 400
        assert 'Requirements required' in response.json['error']
    
    def test_create_missing_date(self):
        data = {
            'name': 'Event',
            'requirements': ['Python']
        }
        response, status = EventService.create(data)
        assert status == 400
        assert 'Date required' in response.json['error']
    
    def test_create_invalid_date(self):
        data = {
            'name': 'Event',
            'requirements': ['Python'],
            'date': 'invalid-date'
        }
        response, status = EventService.create(data)
        assert status == 400
        assert 'Invalid date' in response.json['error']
    
    def test_create_default_max_volunteers(self):
        data = {
            'name': 'Event',
            'requirements': ['Python'],
            'date': '12/31/2025'
        }
        response, status = EventService.create(data)
        print(response.json)
        assert status == 201
        assert response.json['max_volunteers'] == 10
    
    def test_update_success(self):
        EVENTS.append({
            'id': 1,
            'name': 'Original',
            'description': 'Test',
            'requirements': ['Python'],
            'date': '12/31/2024',
            'location': 'City',
            'max_volunteers': 10
        })
        
        update_data = {'name': 'Updated', 'max_volunteers': 20}
        response, status = EventService.update(1, update_data)
        
        assert status == 200
        assert response.json['name'] == 'Updated'
        assert response.json['max_volunteers'] == 20
    
    def test_update_not_found(self):
        response, status = EventService.update(999, {'name': 'Test'})
        assert status == 404
    
    def test_update_invalid_date(self):
        EVENTS.append({
            'id': 1,
            'name': 'Event',
            'description': 'Test',
            'requirements': ['Python'],
            'date': '12/31/2024',
            'location': 'City',
            'max_volunteers': 10
        })
        
        response, status = EventService.update(1, {'date': 'invalid'})
        assert status == 400
        assert 'Invalid date' in response.json['error']
    
    def test_delete_success(self):
        EVENTS.append({'id': 1, 'name': 'Event'})
        MATCHES.append({'id': 1, 'event_id': 1, 'volunteer_id': 1})
        
        response, status = EventService.delete(1)
        assert status == 200
        assert 'Deleted' in response.json['message']
        assert len(EVENTS) == 0
        assert len(MATCHES) == 0
    
    def test_delete_not_found(self):
        response, status = EventService.delete(999)
        assert status == 404


class TestMatchService:
    """Test matching operations"""
    
    def test_find_best_match_volunteer_not_found(self):
        response, status = MatchService.find_best_match(999)
        assert status == 404
        assert 'Volunteer not found' in response.json['error']
    
    def test_find_best_match_no_events(self):
        VOLUNTEERS.append({
            'id': 1,
            'name': 'John',
            'skills': ['Python'],
            'availability': ['Monday']
        })
        
        response, status = MatchService.find_best_match(1)
        assert status == 404
        assert 'No matches' in response.json['message']
    
    def test_find_best_match_already_matched(self):
        VOLUNTEERS.append({
            'id': 1,
            'name': 'John',
            'skills': ['Python'],
            'availability': ['Monday']
        })
        EVENTS.append({
            'id': 1,
            'name': 'Event',
            'requirements': ['Python'],
            'date': 'Monday',
            'max_volunteers': 10
        })
        MATCHES.append({'id': 1, 'volunteer_id': 1, 'event_id': 1})
        
        response, status = MatchService.find_best_match(1)
        assert status == 404
    
    def test_find_best_match_event_full(self):
        VOLUNTEERS.append({
            'id': 1,
            'name': 'John',
            'skills': ['Python'],
            'availability': ['Monday']
        })
        EVENTS.append({
            'id': 1,
            'name': 'Event',
            'requirements': ['Python'],
            'date': 'Monday',
            'max_volunteers': 1
        })
        MATCHES.append({'id': 1, 'volunteer_id': 2, 'event_id': 1})
        
        response, status = MatchService.find_best_match(1)
        assert status == 404
    
    def test_find_best_match_success(self):
        VOLUNTEERS.append({
            'id': 1,
            'name': 'John',
            'skills': ['Python', 'JavaScript'],
            'availability': ['Monday', 'Wednesday']
        })
        EVENTS.append({
            'id': 1,
            'name': 'Event 1',
            'requirements': ['Python'],
            'date': 'Tuesday',
            'max_volunteers': 10
        })
        EVENTS.append({
            'id': 2,
            'name': 'Event 2',
            'requirements': ['Python', 'JavaScript'],
            'date': 'Monday',
            'max_volunteers': 10
        })
        
        response, status = MatchService.find_best_match(1)

        assert status == 200
        assert response.json['event']['id'] == 1  # Better match
        assert response.json['event']['current_volunteers'] == 0
    
    def test_create_match_missing_ids(self):
        response, status = MatchService.create_match(None, None)
        assert status == 400
        assert 'required' in response.json['error'].lower()
    
    def test_create_match_volunteer_not_found(self):
        response, status = MatchService.create_match(999, 1)
        assert status == 404
        assert 'Volunteer not found' in response.json['error']
    
    def test_create_match_event_not_found(self):
        VOLUNTEERS.append({'id': 1, 'name': 'John'})
        response, status = MatchService.create_match(1, 999)
        assert status == 404
        assert 'Event not found' in response.json['error']
    
    def test_create_match_already_matched(self):
        VOLUNTEERS.append({'id': 1, 'name': 'John'})
        EVENTS.append({'id': 1, 'name': 'Event', 'max_volunteers': 10})
        MATCHES.append({'id': 1, 'volunteer_id': 1, 'event_id': 1})
        
        response, status = MatchService.create_match(1, 1)
        assert status == 400
        assert 'Already matched' in response.json['error']
    
    def test_create_match_event_full(self):
        VOLUNTEERS.append({'id': 1, 'name': 'John'})
        EVENTS.append({'id': 1, 'name': 'Event', 'max_volunteers': 1})
        MATCHES.append({'id': 1, 'volunteer_id': 2, 'event_id': 1})
        
        response, status = MatchService.create_match(1, 1)
        assert status == 400
        assert 'Event full' in response.json['error']
    
    def test_create_match_success(self):
        VOLUNTEERS.append({'id': 1, 'name': 'John Doe'})
        EVENTS.append({'id': 1, 'name': 'Beach Cleanup', 'max_volunteers': 10})
        
        response, status = MatchService.create_match(1, 1)
        assert status == 201
        assert response.json['volunteer_id'] == 1
        assert response.json['event_id'] == 1
        assert response.json['volunteer_name'] == 'John Doe'
        assert response.json['event_name'] == 'Beach Cleanup'
        assert response.json['status'] == 'confirmed'
        assert 'matched_at' in response.json
        assert len(MATCHES) == 1
    
    def test_get_all_matches_empty(self):
        response, status = MatchService.get_all()
        assert status == 200
        assert response.json == []
    
    def test_get_all_matches_with_data(self):
        MATCHES.append({'id': 1, 'volunteer_id': 1, 'event_id': 1})
        MATCHES.append({'id': 2, 'volunteer_id': 2, 'event_id': 2})
        
        response, status = MatchService.get_all()
        assert status == 200
        assert len(response.json) == 2
    
    def test_get_by_volunteer(self):
        MATCHES.append({'id': 1, 'volunteer_id': 1, 'event_id': 1})
        MATCHES.append({'id': 2, 'volunteer_id': 1, 'event_id': 2})
        MATCHES.append({'id': 3, 'volunteer_id': 2, 'event_id': 3})
        
        response, status = MatchService.get_by_volunteer(1)
        assert status == 200
        assert len(response.json) == 2
        assert all(m['volunteer_id'] == 1 for m in response.json)
    
    def test_get_by_event(self):
        MATCHES.append({'id': 1, 'volunteer_id': 1, 'event_id': 1})
        MATCHES.append({'id': 2, 'volunteer_id': 2, 'event_id': 1})
        MATCHES.append({'id': 3, 'volunteer_id': 3, 'event_id': 2})
        
        response, status = MatchService.get_by_event(1)
        assert status == 200
        assert len(response.json) == 2
        assert all(m['event_id'] == 1 for m in response.json)
    
    def test_delete_match_not_found(self):
        response, status = MatchService.delete(999)
        assert status == 404
    
    def test_delete_match_success(self):
        MATCHES.append({'id': 1, 'volunteer_id': 1, 'event_id': 1})
        
        response, status = MatchService.delete(1)
        assert status == 200
        assert 'Deleted' in response.json['message']
        assert len(MATCHES) == 0
    
    def test_update_status_not_found(self):
        response, status = MatchService.update_status(999, 'confirmed')
        assert status == 404
    
    def test_update_status_missing(self):
        MATCHES.append({'id': 1, 'volunteer_id': 1, 'event_id': 1, 'status': 'pending'})
        response, status = MatchService.update_status(1, None)
        assert status == 400
        assert 'Status required' in response.json['error']
    
    def test_update_status_invalid(self):
        MATCHES.append({'id': 1, 'volunteer_id': 1, 'event_id': 1, 'status': 'pending'})
        response, status = MatchService.update_status(1, 'invalid_status')
        assert status == 400
        assert 'Invalid status' in response.json['error']
    
    def test_update_status_success(self):
        MATCHES.append({'id': 1, 'volunteer_id': 1, 'event_id': 1, 'status': 'pending'})
        
        response, status = MatchService.update_status(1, 'confirmed')
        assert status == 200
        assert response.json['status'] == 'confirmed'
        
        response, status = MatchService.update_status(1, 'cancelled')
        assert status == 200
        assert response.json['status'] == 'cancelled'
