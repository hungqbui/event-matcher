"""
JWT Authentication Middleware
Provides decorators for protecting routes with JWT tokens.
"""

from functools import wraps
from flask import request, jsonify, current_app
import jwt
from datetime import datetime, timedelta


def generate_token(user_data):
    """
    Generate a JWT token for a user.
    
    Args:
        user_data: dict with keys: id, email, name, role (optional)
    
    Returns:
        str: JWT token
    """
    expiration = datetime.utcnow() + timedelta(
        hours=current_app.config.get("JWT_EXPIRATION_HOURS", 24)
    )
    
    payload = {
        "user_id": user_data.get("id"),
        "email": user_data.get("email"),
        "name": user_data.get("name"),
        "role": user_data.get("role", "volunteer"),
        "exp": expiration,
        "iat": datetime.utcnow()
    }
    
    token = jwt.encode(
        payload,
        current_app.config["SECRET_KEY"],
        algorithm="HS256"
    )
    
    return token


def decode_token(token):
    """
    Decode and verify a JWT token.
    
    Args:
        token: JWT token string
    
    Returns:
        dict: Decoded payload or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            current_app.config["SECRET_KEY"],
            algorithms=["HS256"]
        )
        return payload
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def jwt_required(f):
    """
    Decorator to protect routes that require authentication.
    Adds 'current_user' to the request context.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Check Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({"message": "Authentication token is missing"}), 401
        
        # Decode token
        payload = decode_token(token)
        if not payload:
            return jsonify({"message": "Invalid or expired token"}), 401
        
        # Add user info to request context
        request.current_user = payload
        
        return f(*args, **kwargs)
    
    return decorated_function


def admin_required(f):
    """
    Decorator to protect routes that require admin privileges.
    Must be used with @jwt_required or after it.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Check Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        
        if not token:
            return jsonify({"message": "Authentication token is missing"}), 401
        
        # Decode token
        payload = decode_token(token)
        if not payload:
            return jsonify({"message": "Invalid or expired token"}), 401
        
        # Check if user is admin
        if payload.get("role") != "admin":
            return jsonify({"message": "Admin privileges required"}), 403
        
        # Add user info to request context
        request.current_user = payload
        
        return f(*args, **kwargs)
    
    return decorated_function


def optional_jwt(f):
    """
    Decorator that adds user info if token is present but doesn't require it.
    Useful for routes that behave differently for authenticated users.
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Check Authorization header
        auth_header = request.headers.get("Authorization")
        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
        
        if token:
            payload = decode_token(token)
            if payload:
                request.current_user = payload
            else:
                request.current_user = None
        else:
            request.current_user = None
        
        return f(*args, **kwargs)
    
    return decorated_function
