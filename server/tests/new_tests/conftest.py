# Test Configuration and Fixtures
# Run: pytest tests/new_tests/ -v

import pytest
from flask import Flask
from sqlalchemy import create_engine, text
import sys
import os
from urllib.parse import quote_plus

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))


@pytest.fixture(scope='session')
def test_engine():
    """Create a test database engine."""
    # Use environment variables or defaults matching app.py
    host = os.getenv("DB_HOST", "127.0.0.1")
    port = os.getenv("DB_PORT", "3306")
    user = os.getenv("DB_USER", "dev_user")
    pw = quote_plus(os.getenv("DB_PASS", "Team15"))
    test_db_name = os.getenv("TEST_DB_NAME", "eventmatcher_test")
    
    url = f"mysql+pymysql://{user}:{pw}@{host}:{port}/{test_db_name}?charset=utf8mb4"
    engine = create_engine(url)
    return engine


@pytest.fixture(scope='function')
def app(test_engine):
    """Create and configure a test Flask app for each test."""
    app = Flask(__name__)
    app.config['TESTING'] = True
    app.config['ENGINE'] = test_engine
    
    with app.app_context():
        # Clean up test data before each test
        with test_engine.begin() as conn:
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            conn.execute(text("TRUNCATE TABLE history_tasks"))
            conn.execute(text("TRUNCATE TABLE volunteer_history"))
            conn.execute(text("TRUNCATE TABLE matches"))
            conn.execute(text("TRUNCATE TABLE event_requirements"))
            conn.execute(text("TRUNCATE TABLE volunteer_skills"))
            conn.execute(text("TRUNCATE TABLE user_skills"))
            conn.execute(text("TRUNCATE TABLE notifications"))
            conn.execute(text("TRUNCATE TABLE profiles"))
            conn.execute(text("TRUNCATE TABLE events"))
            conn.execute(text("TRUNCATE TABLE volunteers"))
            conn.execute(text("TRUNCATE TABLE admins"))
            conn.execute(text("DELETE FROM skills WHERE name LIKE 'Test%'"))
            conn.execute(text("TRUNCATE TABLE users"))
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))
    
    yield app
    
    # Cleanup after each test
    with app.app_context():
        with test_engine.begin() as conn:
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 0"))
            conn.execute(text("TRUNCATE TABLE history_tasks"))
            conn.execute(text("TRUNCATE TABLE volunteer_history"))
            conn.execute(text("TRUNCATE TABLE matches"))
            conn.execute(text("TRUNCATE TABLE event_requirements"))
            conn.execute(text("TRUNCATE TABLE volunteer_skills"))
            conn.execute(text("TRUNCATE TABLE user_skills"))
            conn.execute(text("TRUNCATE TABLE notifications"))
            conn.execute(text("TRUNCATE TABLE profiles"))
            conn.execute(text("TRUNCATE TABLE events"))
            conn.execute(text("TRUNCATE TABLE volunteers"))
            conn.execute(text("TRUNCATE TABLE admins"))
            conn.execute(text("DELETE FROM skills WHERE name LIKE 'Test%'"))
            conn.execute(text("TRUNCATE TABLE users"))
            conn.execute(text("SET FOREIGN_KEY_CHECKS = 1"))


@pytest.fixture
def client(app):
    """Create a test client."""
    return app.test_client()


@pytest.fixture
def test_user(app):
    """Create a test user in the database."""
    with app.app_context():
        engine = app.config['ENGINE']
        with engine.begin() as conn:
            # Insert test user with SHA-256 hash of "password123"
            conn.execute(text("""
                INSERT INTO users (id, name, email, password_hash, state, created_at)
                VALUES (:id, :name, :email, :hash, :state, NOW())
            """), {
                'id': 999,
                'name': 'Test User',
                'email': 'testuser@example.com',
                'hash': 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f',
                'state': 'TX'
            })
        return {
            'id': 999,
            'name': 'Test User',
            'email': 'testuser@example.com',
            'password': 'password123',
            'state': 'TX'
        }


@pytest.fixture
def test_admin(app, test_user):
    """Create a test admin user."""
    with app.app_context():
        engine = app.config['ENGINE']
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO admins (id, user_id, phone, created_at)
                VALUES (:id, :user_id, :phone, NOW())
            """), {
                'id': 999,
                'user_id': test_user['id'],
                'phone': '555-0100'
            })
        return {**test_user, 'admin_id': 999, 'role': 'admin'}


@pytest.fixture
def test_user2(app):
    """Create a second test user (not an admin)."""
    with app.app_context():
        engine = app.config['ENGINE']
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO users (id, name, email, password_hash, state, created_at)
                VALUES (:id, :name, :email, :hash, :state, NOW())
            """), {
                'id': 998,
                'name': 'Test User 2',
                'email': 'testuser2@example.com',
                'hash': 'ef92b778bafe771e89245b89ecbc08a44a4e166c06659911881f383d4473e94f',
                'state': 'CA'
            })
        return {
            'id': 998,
            'name': 'Test User 2',
            'email': 'testuser2@example.com',
            'password': 'password123',
            'state': 'CA'
        }


@pytest.fixture
def test_volunteer(app, test_user):
    """Create a test volunteer."""
    with app.app_context():
        engine = app.config['ENGINE']
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO volunteers (id, user_id, phone, availability, created_at)
                VALUES (:id, :user_id, :phone, :availability, NOW())
            """), {
                'id': 999,
                'user_id': test_user['id'],
                'phone': '555-0101',
                'availability': 'weekends'
            })
        return {
            **test_user, 
            'volunteer_id': 999, 
            'user_id': test_user['id'],  # Add user_id for test compatibility
            'role': 'volunteer'
        }


@pytest.fixture
def test_event(app, test_admin):
    """Create a test event."""
    with app.app_context():
        engine = app.config['ENGINE']
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO events (id, ownerid, name, description, date, location, 
                                  max_volunteers, urgency, img, time_label, created_at)
                VALUES (:id, :ownerid, :name, :desc, :date, :loc, :max, :urgency, 
                       :img, :time_label, NOW())
            """), {
                'id': 999,
                'ownerid': test_admin['id'],
                'name': 'Test Event',
                'desc': 'Test Description',
                'date': '2024-12-31',
                'loc': 'Test Location',
                'max': 20,
                'urgency': 'medium',
                'img': '/test.jpg',
                'time_label': 'Dec 31 · 9:00 AM - 5:00 PM'
            })
        return {
            'id': 999,
            'ownerid': test_admin['id'],
            'name': 'Test Event',
            'description': 'Test Description',
            'date': '2024-12-31',
            'location': 'Test Location',
            'max_volunteers': 20,
            'urgency': 'medium'
        }


@pytest.fixture
def test_skills(app):
    """Create test skills in the database."""
    with app.app_context():
        engine = app.config['ENGINE']
        with engine.begin() as conn:
            conn.execute(text("""
                INSERT INTO skills (id, name) VALUES
                (9991, 'Test Skill 1'),
                (9992, 'Test Skill 2'),
                (9993, 'Test Skill 3')
            """))
        return [
            {'id': 9991, 'name': 'Test Skill 1'},
            {'id': 9992, 'name': 'Test Skill 2'},
            {'id': 9993, 'name': 'Test Skill 3'}
        ]
