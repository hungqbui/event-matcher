# server/routes/auth.py
from flask import Blueprint, jsonify, request
from ..services.authService import AuthService

bp = Blueprint("auth", __name__)  # app registers with url_prefix="/api"


@bp.route("/signup", methods=["POST"])
def signup():
    """
    Body: { name, email, password, state, skills[] }
    Creates user (hashed password) and links skills.
    """
    data = request.get_json(silent=True) or {}

    return AuthService.signup(data)

@bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    return AuthService.login(data) 

@bp.route("/check-email", methods=["GET"])
def check_email():
    return AuthService.check_email()


@bp.route("/skills", methods=["GET"])
def list_skills():
    return AuthService.list_skills()
