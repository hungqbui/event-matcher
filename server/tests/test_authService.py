import pytest
import sys
import os
from flask import Flask
from sqlalchemy import create_engine, text

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from services.authService import AuthService


@pytest.fixture
def app():
    """Create and configure a test Flask app."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    # Update with your test database credentials
    app.config['ENGINE'] = create_engine('mysql+pymysql://root:@localhost/eventmatcher_test')
    
    with app.app_context():
        # Clean up test data before tests
        engine = app.config['ENGINE']
        with engine.begin() as conn:
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            conn.execute(text("TRUNCATE TABLE user_skills"))
            conn.execute(text("TRUNCATE TABLE volunteer_skills"))
            conn.execute(text("TRUNCATE TABLE volunteers"))
            conn.execute(text("TRUNCATE TABLE admins"))
            conn.execute(text("TRUNCATE TABLE users"))
            conn.execute(text("DELETE FROM skills WHERE name LIKE 'Test%'"))
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
    
    yield app
    
    # Cleanup after tests
    with app.app_context():
        engine = app.config['ENGINE']
        with engine.begin() as conn:
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            conn.execute(text("TRUNCATE TABLE user_skills"))
            conn.execute(text("TRUNCATE TABLE volunteer_skills"))
            conn.execute(text("TRUNCATE TABLE volunteers"))
            conn.execute(text("TRUNCATE TABLE admins"))
            conn.execute(text("TRUNCATE TABLE users"))
            conn.execute(text("DELETE FROM skills WHERE name LIKE 'Test%'"))
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))


class TestAuthServiceSignup:
    """Test signup functionality"""
    
    def test_signup_success(self):
        """Test successful user signup with all required fields"""
        signup_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
            "state": "TX",
            "skills": ["Python", "JavaScript"]
        }
        
        response, status = AuthService.signup(signup_data)
        
        assert status == 201
        assert response.json['message'] == 'Signup successful'
        assert response.json['user']['name'] == 'John Doe'
        assert response.json['user']['email'] == 'john@example.com'
        assert len(users) == 2  # Original test user + new user
    
    def test_signup_missing_name(self):
        """Test signup fails when name is missing"""
        signup_data = {
            "email": "john@example.com",
            "password": "password123",
            "state": "TX",
            "skills": ["Python"]
        }
        
        response, status = AuthService.signup(signup_data)
        
        assert status == 400
        assert 'name' in response.json['message'].lower()
        assert 'required' in response.json['message'].lower()
    
    def test_signup_missing_email(self):
        """Test signup fails when email is missing"""
        signup_data = {
            "name": "John Doe",
            "password": "password123",
            "state": "TX",
            "skills": ["Python"]
        }
        
        response, status = AuthService.signup(signup_data)
        
        assert status == 400
        assert 'email' in response.json['message'].lower()
        assert 'required' in response.json['message'].lower()
    
    def test_signup_missing_password(self):
        """Test signup fails when password is missing"""
        signup_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "state": "TX",
            "skills": ["Python"]
        }
        
        response, status = AuthService.signup(signup_data)
        
        assert status == 400
        assert 'password' in response.json['message'].lower()
        assert 'required' in response.json['message'].lower()
    
    def test_signup_missing_state(self):
        """Test signup fails when state is missing"""
        signup_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
            "skills": ["Python"]
        }
        
        response, status = AuthService.signup(signup_data)
        
        assert status == 400
        assert 'state' in response.json['message'].lower()
        assert 'required' in response.json['message'].lower()
    
    def test_signup_missing_skills(self):
        """Test signup fails when skills are missing"""
        signup_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
            "state": "TX"
        }
        
        response, status = AuthService.signup(signup_data)
        
        assert status == 400
        assert 'skills' in response.json['message'].lower()
        assert 'required' in response.json['message'].lower()
    
    def test_signup_empty_name(self):
        """Test signup fails when name is empty string"""
        signup_data = {
            "name": "",
            "email": "john@example.com",
            "password": "password123",
            "state": "TX",
            "skills": ["Python"]
        }
        
        response, status = AuthService.signup(signup_data)
        
        assert status == 400
        assert 'name' in response.json['message'].lower()
    
    def test_signup_empty_email(self):
        """Test signup fails when email is empty string"""
        signup_data = {
            "name": "John Doe",
            "email": "",
            "password": "password123",
            "state": "TX",
            "skills": ["Python"]
        }
        
        response, status = AuthService.signup(signup_data)
        
        assert status == 400
        assert 'email' in response.json['message'].lower()
    
    def test_signup_empty_skills_list(self):
        """Test signup fails when skills list is empty"""
        signup_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "password123",
            "state": "TX",
            "skills": []
        }
        
        response, status = AuthService.signup(signup_data)
        
        assert status == 400
        assert 'skills' in response.json['message'].lower()
    
    def test_signup_invalid_email_format_no_at(self):
        """Test signup fails with invalid email format (no @)"""
        signup_data = {
            "name": "John Doe",
            "email": "johnexample.com",
            "password": "password123",
            "state": "TX",
            "skills": ["Python"]
        }
        
        response, status = AuthService.signup(signup_data)
        
        assert status == 400
        assert 'email' in response.json['message'].lower()
        assert 'invalid' in response.json['message'].lower()
    
    def test_signup_invalid_email_format_no_domain(self):
        """Test signup fails with invalid email format (no domain)"""
        signup_data = {
            "name": "John Doe",
            "email": "john@",
            "password": "password123",
            "state": "TX",
            "skills": ["Python"]
        }
        
        response, status = AuthService.signup(signup_data)
        
        assert status == 400
        assert 'email' in response.json['message'].lower()
        assert 'invalid' in response.json['message'].lower()
    
    def test_signup_invalid_email_format_no_tld(self):
        """Test signup fails with invalid email format (no top-level domain)"""
        signup_data = {
            "name": "John Doe",
            "email": "john@example",
            "password": "password123",
            "state": "TX",
            "skills": ["Python"]
        }
        
        response, status = AuthService.signup(signup_data)
        
        assert status == 400
        assert 'email' in response.json['message'].lower()
        assert 'invalid' in response.json['message'].lower()
    
    def test_signup_password_too_short(self):
        """Test signup fails when password is less than 6 characters"""
        signup_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "12345",  # Only 5 characters
            "state": "TX",
            "skills": ["Python"]
        }
        
        response, status = AuthService.signup(signup_data)
        
        assert status == 400
        assert 'password' in response.json['message'].lower()
        assert '6' in response.json['message']
    
    def test_signup_password_exactly_6_characters(self):
        """Test signup succeeds when password is exactly 6 characters"""
        signup_data = {
            "name": "John Doe",
            "email": "john@example.com",
            "password": "123456",  # Exactly 6 characters
            "state": "TX",
            "skills": ["Python"]
        }
        
        response, status = AuthService.signup(signup_data)
        
        assert status == 201
        assert response.json['message'] == 'Signup successful'
    
    def test_signup_duplicate_email(self):
        """Test signup fails when email already exists"""
        signup_data = {
            "name": "Duplicate User",
            "email": "test@example.com",  # Already exists in fixture
            "password": "password123",
            "state": "TX",
            "skills": ["Python"]
        }
        
        response, status = AuthService.signup(signup_data)
        
        assert status == 400
        assert 'email' in response.json['message'].lower()
        assert 'exists' in response.json['message'].lower()
    
    def test_signup_duplicate_email_case_sensitive(self):
        """Test that email duplication check is case-sensitive (current behavior)"""
        signup_data = {
            "name": "John Doe",
            "email": "TEST@EXAMPLE.COM",  # Different case
            "password": "password123",
            "state": "TX",
            "skills": ["Python"]
        }
        
        response, status = AuthService.signup(signup_data)
        
        # Current implementation is case-sensitive, so this should succeed
        assert status == 201
    
    def test_signup_user_added_to_list(self):
        """Test that new user is actually added to users list"""
        initial_count = len(users)
        
        signup_data = {
            "name": "New User",
            "email": "new@example.com",
            "password": "password123",
            "state": "CA",
            "skills": ["Java", "Python"]
        }
        
        AuthService.signup(signup_data)
        
        assert len(users) == initial_count + 1
        assert any(u['email'] == 'new@example.com' for u in users)
    
    def test_signup_preserves_all_user_data(self):
        """Test that all user data is preserved in the users list"""
        signup_data = {
            "name": "Complete User",
            "email": "complete@example.com",
            "password": "password123",
            "state": "NY",
            "skills": ["React", "Node.js"],
            "phone": "123-456-7890",  # Extra field
            "city": "New York"  # Extra field
        }
        
        response, status = AuthService.signup(signup_data)
        
        assert status == 201
        # Check that extra fields are preserved
        new_user = next(u for u in users if u['email'] == 'complete@example.com')
        assert new_user['phone'] == "123-456-7890"
        assert new_user['city'] == "New York"


class TestAuthServiceLogin:
    """Test login functionality"""
    
    def test_login_success(self):
        """Test successful login with correct credentials"""
        login_data = {
            "email": "test@example.com",
            "password": "1234"
        }
        
        response, status = AuthService.login(login_data)
        
        assert status == 200
        assert response.json['message'] == 'Login successful'
        assert response.json['name'] == 'Test User'
    
    def test_login_wrong_password(self):
        """Test login fails with incorrect password"""
        login_data = {
            "email": "test@example.com",
            "password": "wrongpassword"
        }
        
        response, status = AuthService.login(login_data)
        
        assert status == 401
        assert 'invalid' in response.json['message'].lower()
        assert 'credentials' in response.json['message'].lower()
    
    def test_login_nonexistent_email(self):
        """Test login fails with non-existent email"""
        login_data = {
            "email": "nonexistent@example.com",
            "password": "password123"
        }
        
        response, status = AuthService.login(login_data)
        
        assert status == 401
        assert 'invalid' in response.json['message'].lower()
        assert 'credentials' in response.json['message'].lower()
    
    def test_login_missing_email(self):
        """Test login fails when email is missing"""
        login_data = {
            "password": "1234"
        }
        
        response, status = AuthService.login(login_data)
        
        assert status == 400
        assert 'email' in response.json['message'].lower()
        assert 'required' in response.json['message'].lower()
    
    def test_login_missing_password(self):
        """Test login fails when password is missing"""
        login_data = {
            "email": "test@example.com"
        }
        
        response, status = AuthService.login(login_data)
        
        assert status == 400
        assert 'password' in response.json['message'].lower()
        assert 'required' in response.json['message'].lower()
    
    def test_login_empty_email(self):
        """Test login fails when email is empty string"""
        login_data = {
            "email": "",
            "password": "1234"
        }
        
        response, status = AuthService.login(login_data)
        
        assert status == 400
        assert 'email' in response.json['message'].lower()
        assert 'required' in response.json['message'].lower()
    
    def test_login_empty_password(self):
        """Test login fails when password is empty string"""
        login_data = {
            "email": "test@example.com",
            "password": ""
        }
        
        response, status = AuthService.login(login_data)
        
        assert status == 400
        assert 'password' in response.json['message'].lower()
        assert 'required' in response.json['message'].lower()
    
    def test_login_both_fields_missing(self):
        """Test login fails when both email and password are missing"""
        login_data = {}
        
        response, status = AuthService.login(login_data)
        
        assert status == 400
        assert 'email' in response.json['message'].lower()
        assert 'password' in response.json['message'].lower()
        assert 'required' in response.json['message'].lower()
    
    def test_login_case_sensitive_email(self):
        """Test that email matching is case-sensitive (current behavior)"""
        login_data = {
            "email": "TEST@EXAMPLE.COM",  # Different case
            "password": "1234"
        }
        
        response, status = AuthService.login(login_data)
        
        # Current implementation is case-sensitive, so this should fail
        assert status == 401
    
    def test_login_after_signup(self):
        """Test that user can login after signing up"""
        # First signup
        signup_data = {
            "name": "New User",
            "email": "newuser@example.com",
            "password": "password123",
            "state": "TX",
            "skills": ["Python"]
        }
        AuthService.signup(signup_data)
        
        # Then login
        login_data = {
            "email": "newuser@example.com",
            "password": "password123"
        }
        response, status = AuthService.login(login_data)
        
        assert status == 200
        assert response.json['message'] == 'Login successful'
        assert response.json['name'] == 'New User'
    
    def test_login_returns_correct_user_name(self):
        """Test that login returns the correct user's name"""
        # Add another user
        users.append({
            "email": "another@example.com",
            "password": "password456",
            "name": "Another User"
        })
        
        login_data = {
            "email": "another@example.com",
            "password": "password456"
        }
        
        response, status = AuthService.login(login_data)
        
        assert status == 200
        assert response.json['name'] == 'Another User'
        assert response.json['name'] != 'Test User'
