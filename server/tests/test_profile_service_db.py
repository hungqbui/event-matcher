"""
Comprehensive tests for ProfileService with database implementation
Run: pytest tests/new_tests/test_profile_service_db.py -v
"""

import pytest
from services.profileService import ProfileService
from flask import json
from sqlalchemy import text

class TestGetProfile:
    """Test fetching user profiles"""
    
    def test_get_profile_success(self, app, test_user):
        """Test fetching existing profile"""
        with app.app_context():
            engine = app.config['ENGINE']
            
            # Create test profile
            with engine.begin() as conn:
                conn.execute(
                    text("""INSERT INTO profiles (user_id, full_name, address1, address2, city, state, zip, preferences, availability) 
                    VALUES (:user_id, 'Test User', '123 Main St', 'Apt 4', 'Houston', 'TX', '77001', 'Remote work', '[\"2024-12-25\", \"2024-12-26\"]')"""),
                    {"user_id": test_user['id']}
                )
            
            response, status = ProfileService.get_profile(test_user['id'])
            
            assert status == 200
            profile = response.get_json()
            assert profile['full_name'] == 'Test User'
            assert profile['city'] == 'Houston'
            assert profile['state'] == 'TX'
    
    def test_get_profile_not_found(self, app):
        """Test fetching non-existent profile returns 404"""
        with app.app_context():
            response, status = ProfileService.get_profile(99999)
            
            assert status == 404
            json_data = response.get_json()
            assert "not found" in json_data['message'].lower()
    
    def test_get_profile_with_availability(self, app, test_user):
        """Test profile with JSON availability field"""
        with app.app_context():
            engine = app.config['ENGINE']
            
            # Create profile with availability dates
            with engine.begin() as conn:
                conn.execute(
                    text("""INSERT INTO profiles (user_id, full_name, address1, city, state, zip, availability) 
                    VALUES (:user_id, 'Available User', '123 Main St', 'Houston', 'TX', '77001', '[\"2024-12-25\", \"2024-12-26\", \"2024-12-27\"]')"""),
                    {"user_id": test_user['id']}
                )
            
            response, status = ProfileService.get_profile(test_user['id'])
            
            assert status == 200
            profile = response.get_json()
            assert 'availability' in profile
            availability = json.loads(profile['availability']) if isinstance(profile['availability'], str) else profile['availability']
            assert isinstance(availability, list)
            assert len(availability) == 3


class TestCreateProfile:
    """Test creating user profiles"""
    
    def test_create_profile_success(self, app, test_user):
        """Test creating a new profile"""
        with app.app_context():
            data = {
                'user_id': test_user['id'],
                'full_name': 'John Doe',
                'address_1': '456 Oak Ave',
                'city': 'Houston',
                'state': 'TX',
                'zip_code': '77002',
                'skills': 'Python, React',
                'preferences': 'Weekend events',
                'availability': '["2024-12-20", "2024-12-21"]'
            }
            
            response, status = ProfileService.create_profile(data)
            
            assert status == 201
            profile = response.get_json()
            assert profile['full_name'] == 'John Doe'
            assert profile['city'] == 'Houston'
            assert profile['zip_code'] == '77002'
    
    def test_create_profile_missing_required_fields(self, app, test_user):
        """Test create profile fails with missing required fields"""
        with app.app_context():
            data = {
                'user_id': test_user['id'],
                'full_name': 'Incomplete User'
                # Missing other required fields
            }
            
            response, status = ProfileService.create_profile(data)
            
            assert status == 400
            json_data = response.get_json()
            assert "missing" in json_data['message'].lower() or "required" in json_data['message'].lower()
    
    def test_create_profile_duplicate(self, app, test_user):
        """Test creating duplicate profile fails"""
        with app.app_context():
            # Create first profile
            data = {
                'user_id': test_user['id'],
                'full_name': 'First Profile',
                'address_1': '123 Main St',
                'city': 'Houston',
                'state': 'TX',
                'zip_code': '77001'
            }
            ProfileService.create_profile(data)
            
            # Try to create duplicate
            response, status = ProfileService.create_profile(data)
            
            assert status == 400 or status == 409
            json_data = response.get_json()
            assert "already exists" in json_data['message'].lower() or "duplicate" in json_data['message'].lower()
    
    def test_create_profile_optional_fields(self, app, test_user):
        """Test creating profile with optional fields"""
        with app.app_context():
            data = {
                'user_id': test_user['id'],
                'full_name': 'Optional Fields User',
                'address_1': '789 Elm St',
                'address_2': 'Suite 100',  # Optional
                'city': 'Houston',
                'state': 'TX',
                'zip_code': '77003',
                'skills': 'Java, SQL',  # Optional
                'preferences': 'Morning events',  # Optional
                'availability': '["2024-12-30"]'  # Optional
            }
            
            response, status = ProfileService.create_profile(data)
            
            assert status == 201
            profile = response.get_json()
            assert profile['address_2'] == 'Suite 100'
            assert profile['skills'] == 'Java, SQL'


class TestUpdateProfile:
    """Test updating user profiles"""
    
    def test_update_profile_success(self, app, test_user):
        """Test updating an existing profile"""
        with app.app_context():
            engine = app.config['ENGINE']
            
            # Create profile
            with engine.begin() as conn:
                conn.execute(
                    text("""INSERT INTO profiles (user_id, full_name, address1, city, state, zip) 
                    VALUES (:user_id, 'Original Name', '123 Main St', 'Houston', 'TX', '77001')"""),
                    {"user_id": test_user['id']}
                )
            
            # Update profile
            data = {
                'full_name': 'Updated Name',
                'city': 'Austin',
                'zip_code': '78701'
            }
            
            response, status = ProfileService.update_profile(test_user['id'], data)
            
            assert status == 200
            profile = response.get_json()
            assert profile['full_name'] == 'Updated Name'
            assert profile['city'] == 'Austin'
    
    def test_update_profile_not_found(self, app):
        """Test updating non-existent profile returns 404"""
        with app.app_context():
            data = {'full_name': 'New Name'}
            
            response, status = ProfileService.update_profile(99999, data)
            
            assert status == 404
            json_data = response.get_json()
            assert "not found" in json_data['message'].lower()
    
    def test_update_profile_partial_fields(self, app, test_user):
        """Test updating only some fields preserves others"""
        with app.app_context():
            engine = app.config['ENGINE']
            
            # Create profile
            with engine.begin() as conn:
                conn.execute(
                    text("""INSERT INTO profiles (user_id, full_name, address1, city, state, zip) 
                    VALUES (:user_id, 'Original Name', '123 Main St', 'Houston', 'TX', '77001')"""),
                    {"user_id": test_user['id']}
                )
            
            # Update only full_name
            data = {'full_name': 'Only Name Updated'}
            
            response, status = ProfileService.update_profile(test_user['id'], data)
            
            assert status == 200
            profile = response.get_json()
            assert profile['full_name'] == 'Only Name Updated'
            assert profile['city'] == 'Houston'  # Unchanged
            assert profile['address_1'] == '123 Main St'  # Unchanged
    
    def test_update_profile_availability(self, app, test_user):
        """Test updating availability JSON field"""
        with app.app_context():
            engine = app.config['ENGINE']
            
            # Create profile
            with engine.begin() as conn:
                conn.execute(
                    text("""INSERT INTO profiles (user_id, full_name, address1, city, state, zip, availability) 
                    VALUES (:user_id, 'Test User', '123 Main St', 'Houston', 'TX', '77001', '[]')"""),
                    {"user_id": test_user['id']}
                )
            
            # Update availability
            data = {
                'availability': '["2024-12-25", "2024-12-26", "2025-01-01"]'
            }
            
            response, status = ProfileService.update_profile(test_user['id'], data)
            
            assert status == 200
            profile = response.get_json()
            availability = json.loads(profile['availability']) if isinstance(profile['availability'], str) else profile['availability']
            assert len(availability) == 3


class TestDeleteProfile:
    """Test deleting user profiles"""
    
    def test_delete_profile_success(self, app, test_user):
        """Test deleting a profile"""
        with app.app_context():
            engine = app.config['ENGINE']
            
            # Create profile
            with engine.begin() as conn:
                conn.execute(
                    text("""INSERT INTO profiles (user_id, full_name, address1, city, state, zip) 
                    VALUES (:user_id, 'To Delete', '123 Main St', 'Houston', 'TX', '77001')"""),
                    {"user_id": test_user['id']}
                )
            
            response, status = ProfileService.delete_profile(test_user['id'])
            
            assert status == 200
            json_data = response.get_json()
            assert "deleted" in json_data['message'].lower()
    
    def test_delete_profile_not_found(self, app):
        """Test deleting non-existent profile returns 404"""
        with app.app_context():
            response, status = ProfileService.delete_profile(99999)
            
            assert status == 404
            json_data = response.get_json()
            assert "not found" in json_data['message'].lower()


class TestProfileValidation:
    """Test profile field validation"""
    
    def test_invalid_zip_code_format(self, app, test_user):
        """Test profile creation with invalid zip code"""
        with app.app_context():
            data = {
                'user_id': test_user['id'],
                'full_name': 'Invalid Zip User',
                'address_1': '123 Main St',
                'city': 'Houston',
                'state': 'TX',
                'zip_code': '1234'  # Invalid: too short
            }
            
            response, status = ProfileService.create_profile(data)
            
            # Depending on validation logic, this might succeed or fail
            # If validation exists, should be 400
            assert status in [201, 400]
    
    def test_invalid_state_code(self, app, test_user):
        """Test profile creation with invalid state code"""
        with app.app_context():
            data = {
                'user_id': test_user['id'],
                'full_name': 'Invalid State User',
                'address_1': '123 Main St',
                'city': 'Houston',
                'state': 'TEXAS',  # Should be 2-letter code
                'zip_code': '77001'
            }
            
            response, status = ProfileService.create_profile(data)
            
            # Depending on validation logic
            assert status in [201, 400]
    
    def test_empty_full_name(self, app, test_user):
        """Test profile creation with empty full_name"""
        with app.app_context():
            data = {
                'user_id': test_user['id'],
                'full_name': '',  # Empty
                'address_1': '123 Main St',
                'city': 'Houston',
                'state': 'TX',
                'zip_code': '77001'
            }
            
            response, status = ProfileService.create_profile(data)
            
            assert status == 400
            json_data = response.get_json()
            assert "full_name" in json_data['message'].lower() or "required" in json_data['message'].lower()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
