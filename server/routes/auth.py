from flask import Blueprint, jsonify, request
import re
from services.authService import AuthService

bp = Blueprint('auth', __name__)

@bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    return AuthService.signup(data)

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    return AuthService.login(data) 
