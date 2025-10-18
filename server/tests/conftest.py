import pytest
from flask import Flask


@pytest.fixture(scope='function', autouse=True)
def app_context():
    """Provide Flask application context for all tests"""
    app = Flask(__name__)
    with app.app_context():
        yield app
