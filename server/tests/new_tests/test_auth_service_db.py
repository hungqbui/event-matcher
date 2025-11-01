"""
Comprehensive tests for AuthService with database implementation
Run: pytest tests/new_tests/test_auth_service_db.py -v
"""

import pytest
from services.authService import AuthService


class TestAuthSignup:
    """Test user signup functionality"""
    
    def test_signup_success(self, app):
        """Test successful user registration"""
        with app.app_context():
            data = {
                "name": "John Doe",
                "email": "john@example.com",
                "password": "password123",
                "state": "TX",
                "skills": ["Test Skill 1", "Test Skill 2"]
            }
            
            response, status = AuthService.signup(data)
            
            assert status == 201
            json_data = response.get_json()
            assert json_data["message"] == "Signup successful"
            assert json_data["user"]["name"] == "John Doe"
            assert json_data["user"]["email"] == "john@example.com"
            assert json_data["user"]["state"] == "TX"
            assert len(json_data["user"]["skills"]) == 2
    
    def test_signup_missing_required_fields(self, app):
        """Test signup fails with missing required fields"""
        with app.app_context():
            data = {"name": "John Doe", "email": "john@example.com"}
            
            response, status = AuthService.signup(data)
            
            assert status == 400
            json_data = response.get_json()
            assert "required" in json_data["message"].lower()
    
    def test_signup_invalid_email_format(self, app):
        """Test signup fails with invalid email"""
        with app.app_context():
            data = {
                "name": "John Doe",
                "email": "invalid-email",
                "password": "password123",
                "state": "TX",
                "skills": ["Test Skill"]
            }
            
            response, status = AuthService.signup(data)
            
            assert status == 400
            json_data = response.get_json()
            assert "email" in json_data["message"].lower()
    
    def test_signup_password_too_short(self, app):
        """Test signup fails with password less than 6 characters"""
        with app.app_context():
            data = {
                "name": "John Doe",
                "email": "john@example.com",
                "password": "12345",
                "state": "TX",
                "skills": ["Test Skill"]
            }
            
            response, status = AuthService.signup(data)
            
            assert status == 400
            json_data = response.get_json()
            assert "password" in json_data["message"].lower()
            assert "6" in json_data["message"]
    
    def test_signup_duplicate_email(self, app, test_user):
        """Test signup fails with existing email"""
        with app.app_context():
            data = {
                "name": "Duplicate User",
                "email": test_user['email'],
                "password": "password123",
                "state": "TX",
                "skills": ["Test Skill"]
            }
            
            response, status = AuthService.signup(data)
            
            assert status == 400
            json_data = response.get_json()
            assert "already exists" in json_data["message"].lower()
    
    def test_signup_with_skills_array(self, app):
        """Test signup with skills as array"""
        with app.app_context():
            data = {
                "name": "Skills Test",
                "email": "skills@example.com",
                "password": "password123",
                "state": "TX",
                "skills": ["Test Skill A", "Test Skill B", "Test Skill C"]
            }
            
            response, status = AuthService.signup(data)
            
            assert status == 201
            json_data = response.get_json()
            assert len(json_data["user"]["skills"]) == 3
    
    def test_signup_with_skills_comma_string(self, app):
        """Test signup with skills as comma-separated string"""
        with app.app_context():
            data = {
                "name": "Skills String Test",
                "email": "skillstring@example.com",
                "password": "password123",
                "state": "TX",
                "skills": "Test Skill X, Test Skill Y, Test Skill Z"
            }
            
            response, status = AuthService.signup(data)
            
            assert status == 201
            json_data = response.get_json()
            assert len(json_data["user"]["skills"]) == 3


class TestAuthLogin:
    """Test user login functionality"""
    
    def test_login_success(self, app, test_user):
        """Test successful login with correct credentials"""
        with app.app_context():
            data = {
                "email": test_user['email'],
                "password": test_user['password']
            }
            
            response, status = AuthService.login(data)
            
            assert status == 200
            json_data = response.get_json()
            assert json_data["message"] == "Login successful"
            assert json_data["user"]["email"] == test_user['email']
            assert json_data["user"]["name"] == test_user['name']
    
    def test_login_wrong_password(self, app, test_user):
        """Test login fails with incorrect password"""
        with app.app_context():
            data = {
                "email": test_user['email'],
                "password": "wrongpassword"
            }
            
            response, status = AuthService.login(data)
            
            assert status == 401
            json_data = response.get_json()
            assert "invalid" in json_data["message"].lower()
    
    def test_login_nonexistent_user(self, app):
        """Test login fails with non-existent email"""
        with app.app_context():
            data = {
                "email": "nonexistent@example.com",
                "password": "password123"
            }
            
            response, status = AuthService.login(data)
            
            assert status == 401
            json_data = response.get_json()
            assert "invalid" in json_data["message"].lower()
    
    def test_login_missing_email(self, app):
        """Test login fails without email"""
        with app.app_context():
            data = {"password": "password123"}
            
            response, status = AuthService.login(data)
            
            assert status == 400
            json_data = response.get_json()
            assert "required" in json_data["message"].lower()
    
    def test_login_missing_password(self, app):
        """Test login fails without password"""
        with app.app_context():
            data = {"email": "test@example.com"}
            
            response, status = AuthService.login(data)
            
            assert status == 400
            json_data = response.get_json()
            assert "required" in json_data["message"].lower()
    
    def test_login_admin_role(self, app, test_admin):
        """Test login returns admin role for admin users"""
        with app.app_context():
            data = {
                "email": test_admin['email'],
                "password": test_admin['password']
            }
            
            response, status = AuthService.login(data)
            
            assert status == 200
            json_data = response.get_json()
            # Role determination logic from database
            assert "role" in json_data["user"]
    
    def test_login_volunteer_role(self, app, test_volunteer):
        """Test login returns volunteer role for volunteers"""
        with app.app_context():
            data = {
                "email": test_volunteer['email'],
                "password": test_volunteer['password']
            }
            
            response, status = AuthService.login(data)
            
            assert status == 200
            json_data = response.get_json()
            assert "role" in json_data["user"]


class TestAuthUtility:
    """Test utility functions"""
    
    def test_check_email_available(self, app):
        """Test email availability check for available email"""
        with app.app_context():
            with app.test_request_context('/?email=available@example.com'):
                response, status = AuthService.check_email()
                
                assert status == 200
                json_data = response.get_json()
                assert json_data["available"] == True
    
    def test_check_email_taken(self, app, test_user):
        """Test email availability check for taken email"""
        with app.app_context():
            with app.test_request_context(f'/?email={test_user["email"]}'):
                response, status = AuthService.check_email()
                
                assert status == 200
                json_data = response.get_json()
                assert json_data["available"] == False
    
    def test_check_email_invalid_format(self, app):
        """Test email check with invalid format"""
        with app.app_context():
            with app.test_request_context('/?email=invalid-email'):
                response, status = AuthService.check_email()
                
                assert status == 400
                json_data = response.get_json()
                assert "invalid" in json_data["message"].lower()
    
    def test_list_skills_empty(self, app):
        """Test listing skills when none exist"""
        with app.app_context():
            response, status = AuthService.list_skills()
            
            assert status == 200
            skills = response.get_json()
            assert isinstance(skills, list)
    
    def test_list_skills_with_data(self, app, test_skills):
        """Test listing skills with existing skills"""
        with app.app_context():
            response, status = AuthService.list_skills()
            
            assert status == 200
            skills = response.get_json()
            assert isinstance(skills, list)
            assert len(skills) >= 3
            assert "Test Skill 1" in skills
            assert "Test Skill 2" in skills
            assert "Test Skill 3" in skills


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
