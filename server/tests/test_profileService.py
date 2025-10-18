import pytest
from services.profileService import ProfileService, current_profile


@pytest.fixture(autouse=True)
def reset_profile():
    """Reset profile to default state before each test"""
    current_profile.clear()
    current_profile.update({
        "fullName": "John Doe",
        "address1": "123 Main St",
        "address2": "",
        "city": "Houston",
        "state": "TX",
        "zip": "77001",
        "skills": ["Tree Planting", "Food Drives"],
        "preferences": "Prefer outdoor activities",
        "availability": ["2025-10-01", "2025-10-15"]
    })
    yield


class TestProfileService:
    """Test profile service operations"""
    
    def test_get_current_profile_success(self):
        """Test getting current profile returns correct data"""
        response, status = ProfileService.get_current_profile()
        
        assert status == 200
        assert response.json['fullName'] == 'John Doe'
        assert response.json['address1'] == '123 Main St'
        assert response.json['city'] == 'Houston'
        assert response.json['state'] == 'TX'
        assert response.json['zip'] == '77001'
        assert 'Tree Planting' in response.json['skills']
        assert 'Food Drives' in response.json['skills']
        assert response.json['preferences'] == 'Prefer outdoor activities'
        assert len(response.json['availability']) == 2
    
    def test_get_current_profile_returns_all_fields(self):
        """Test that profile contains all expected fields"""
        response, status = ProfileService.get_current_profile()
        
        assert status == 200
        profile_data = response.json
        
        # Check all required fields exist
        assert 'fullName' in profile_data
        assert 'address1' in profile_data
        assert 'address2' in profile_data
        assert 'city' in profile_data
        assert 'state' in profile_data
        assert 'zip' in profile_data
        assert 'skills' in profile_data
        assert 'preferences' in profile_data
        assert 'availability' in profile_data
    
    def test_update_profile_success_all_fields(self):
        """Test updating profile with all fields"""
        updated_data = {
            "fullName": "Jane Smith",
            "address1": "456 Oak Ave",
            "address2": "Apt 5B",
            "city": "Austin",
            "state": "TX",
            "zip": "78701",
            "skills": ["Community Organizing", "Youth Mentoring"],
            "preferences": "Weekends only",
            "availability": ["2025-11-01", "2025-11-15"]
        }
        
        response, status = ProfileService.update_profile(updated_data)
        
        assert status == 200
        assert 'message' in response.json
        assert response.json['message'] == 'Profile updated successfully'
        assert response.json['profile']['fullName'] == 'Jane Smith'
        assert response.json['profile']['address1'] == '456 Oak Ave'
        assert response.json['profile']['address2'] == 'Apt 5B'
        assert response.json['profile']['city'] == 'Austin'
        assert response.json['profile']['zip'] == '78701'
        assert 'Community Organizing' in response.json['profile']['skills']
        assert response.json['profile']['preferences'] == 'Weekends only'
    
    def test_update_profile_success_partial_fields(self):
        """Test updating only some fields keeps others intact"""
        partial_data = {
            "fullName": "John Updated",
            "address1": "123 Main St",  # Keep same
            "city": "Dallas",
            "state": "TX",
            "zip": "75201"
        }
        
        response, status = ProfileService.update_profile(partial_data)
        
        assert status == 200
        assert response.json['profile']['fullName'] == 'John Updated'
        assert response.json['profile']['city'] == 'Dallas'
        assert response.json['profile']['zip'] == '75201'
        # Original skills should still be there
        assert 'Tree Planting' in response.json['profile']['skills']
    
    def test_update_profile_missing_full_name(self):
        """Test that missing fullName returns error"""
        invalid_data = {
            "address1": "456 Oak Ave",
            "city": "Austin",
            "state": "TX",
            "zip": "78701"
        }
        
        response, status = ProfileService.update_profile(invalid_data)
        
        assert status == 400
        assert 'error' in response.json
        assert 'fullName' in response.json['error']
        assert 'Missing required field' in response.json['error']
    
    def test_update_profile_missing_address1(self):
        """Test that missing address1 returns error"""
        invalid_data = {
            "fullName": "Jane Smith",
            "city": "Austin",
            "state": "TX",
            "zip": "78701"
        }
        
        response, status = ProfileService.update_profile(invalid_data)
        
        assert status == 400
        assert 'error' in response.json
        assert 'address1' in response.json['error']
    
    def test_update_profile_missing_city(self):
        """Test that missing city returns error"""
        invalid_data = {
            "fullName": "Jane Smith",
            "address1": "456 Oak Ave",
            "state": "TX",
            "zip": "78701"
        }
        
        response, status = ProfileService.update_profile(invalid_data)
        
        assert status == 400
        assert 'error' in response.json
        assert 'city' in response.json['error']
    
    def test_update_profile_missing_state(self):
        """Test that missing state returns error"""
        invalid_data = {
            "fullName": "Jane Smith",
            "address1": "456 Oak Ave",
            "city": "Austin",
            "zip": "78701"
        }
        
        response, status = ProfileService.update_profile(invalid_data)
        
        assert status == 400
        assert 'error' in response.json
        assert 'state' in response.json['error']
    
    def test_update_profile_missing_zip(self):
        """Test that missing zip returns error"""
        invalid_data = {
            "fullName": "Jane Smith",
            "address1": "456 Oak Ave",
            "city": "Austin",
            "state": "TX"
        }
        
        response, status = ProfileService.update_profile(invalid_data)
        
        assert status == 400
        assert 'error' in response.json
        assert 'zip' in response.json['error']
    
    def test_update_profile_empty_full_name(self):
        """Test that empty fullName returns error"""
        invalid_data = {
            "fullName": "",
            "address1": "456 Oak Ave",
            "city": "Austin",
            "state": "TX",
            "zip": "78701"
        }
        
        response, status = ProfileService.update_profile(invalid_data)
        
        assert status == 400
        assert 'error' in response.json
        assert 'fullName' in response.json['error']
    
    def test_update_profile_empty_address1(self):
        """Test that empty address1 returns error"""
        invalid_data = {
            "fullName": "Jane Smith",
            "address1": "",
            "city": "Austin",
            "state": "TX",
            "zip": "78701"
        }
        
        response, status = ProfileService.update_profile(invalid_data)
        
        assert status == 400
        assert 'error' in response.json
        assert 'address1' in response.json['error']
    
    def test_update_profile_with_new_skills(self):
        """Test updating skills array"""
        updated_data = {
            "fullName": "John Doe",
            "address1": "123 Main St",
            "city": "Houston",
            "state": "TX",
            "zip": "77001",
            "skills": ["Teaching", "Coaching", "Event Planning"]
        }
        
        response, status = ProfileService.update_profile(updated_data)
        
        assert status == 200
        assert len(response.json['profile']['skills']) == 3
        assert 'Teaching' in response.json['profile']['skills']
        assert 'Coaching' in response.json['profile']['skills']
        assert 'Event Planning' in response.json['profile']['skills']
        # Old skills should be replaced
        assert 'Tree Planting' not in response.json['profile']['skills']
    
    def test_update_profile_with_empty_address2(self):
        """Test that address2 can be empty (it's optional)"""
        updated_data = {
            "fullName": "Jane Smith",
            "address1": "456 Oak Ave",
            "address2": "",
            "city": "Austin",
            "state": "TX",
            "zip": "78701"
        }
        
        response, status = ProfileService.update_profile(updated_data)
        
        assert status == 200
        assert response.json['profile']['address2'] == ""
    
    def test_update_profile_with_preferences(self):
        """Test updating preferences text"""
        updated_data = {
            "fullName": "John Doe",
            "address1": "123 Main St",
            "city": "Houston",
            "state": "TX",
            "zip": "77001",
            "preferences": "Prefer indoor activities and administrative tasks"
        }
        
        response, status = ProfileService.update_profile(updated_data)
        
        assert status == 200
        assert response.json['profile']['preferences'] == "Prefer indoor activities and administrative tasks"
    
    def test_update_profile_with_availability(self):
        """Test updating availability dates"""
        updated_data = {
            "fullName": "John Doe",
            "address1": "123 Main St",
            "city": "Houston",
            "state": "TX",
            "zip": "77001",
            "availability": ["2025-12-01", "2025-12-15", "2025-12-25"]
        }
        
        response, status = ProfileService.update_profile(updated_data)
        
        assert status == 200
        assert len(response.json['profile']['availability']) == 3
        assert "2025-12-01" in response.json['profile']['availability']
        assert "2025-12-15" in response.json['profile']['availability']
        assert "2025-12-25" in response.json['profile']['availability']
    
    def test_update_profile_persists_changes(self):
        """Test that profile changes persist across calls"""
        updated_data = {
            "fullName": "Updated Name",
            "address1": "New Address",
            "city": "New City",
            "state": "CA",
            "zip": "90001"
        }
        
        # Update profile
        ProfileService.update_profile(updated_data)
        
        # Get profile again
        response, status = ProfileService.get_current_profile()
        
        assert status == 200
        assert response.json['fullName'] == 'Updated Name'
        assert response.json['address1'] == 'New Address'
        assert response.json['city'] == 'New City'
        assert response.json['state'] == 'CA'
        assert response.json['zip'] == '90001'
    
    def test_update_profile_with_whitespace_fields(self):
        """Test that fields with only whitespace are currently accepted (note: could be enhanced to reject)"""
        data_with_whitespace = {
            "fullName": "   ",
            "address1": "456 Oak Ave",
            "city": "Austin",
            "state": "TX",
            "zip": "78701"
        }
        
        response, status = ProfileService.update_profile(data_with_whitespace)
        
        # TODO: Current implementation accepts whitespace-only strings
        # This could be enhanced in the future to validate and reject them
        assert status == 200
        assert response.json['profile']['fullName'] == "   "
    
    def test_update_profile_all_required_fields_present(self):
        """Test successful update when all required fields are present"""
        valid_data = {
            "fullName": "Test User",
            "address1": "789 Elm St",
            "city": "San Antonio",
            "state": "TX",
            "zip": "78201"
        }
        
        response, status = ProfileService.update_profile(valid_data)
        
        assert status == 200
        assert 'Profile updated successfully' in response.json['message']
        assert response.json['profile']['fullName'] == 'Test User'
    
    def test_get_profile_structure(self):
        """Test that profile has correct data types"""
        response, status = ProfileService.get_current_profile()
        
        assert status == 200
        profile = response.json
        
        assert isinstance(profile['fullName'], str)
        assert isinstance(profile['address1'], str)
        assert isinstance(profile['address2'], str)
        assert isinstance(profile['city'], str)
        assert isinstance(profile['state'], str)
        assert isinstance(profile['zip'], str)
        assert isinstance(profile['skills'], list)
        assert isinstance(profile['preferences'], str)
        assert isinstance(profile['availability'], list)
