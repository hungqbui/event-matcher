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

@bp.route("/admin/user/<int:user_id>", methods=["GET"])
def get_admin_user_id(user_id):
    """Get admin's user_id from admin table by looking up the user_id"""
    from flask import current_app
    from sqlalchemy import text
    
    engine = current_app.config["ENGINE"]
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT user_id FROM admins WHERE user_id = :user_id
        """), {"user_id": user_id}).mappings().first()
        
        if not result:
            return jsonify({'error': 'Admin not found', 'user_id': user_id}), 404
        
        return jsonify({'user_id': result['user_id']}), 200
