from flask import jsonify, current_app, request
from sqlalchemy import text
import json
import re
import hashlib

users = [{"email": "test@example.com", "password": "1234", "name": "Test User"}]
EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

def _normalize_skills(skills):
    """Accept list | comma string | JSON string; return clean list[str]."""
    if not skills:
        return []
    if isinstance(skills, list):
        return [str(s).strip() for s in skills if str(s).strip()]
    if isinstance(skills, str):
        # try JSON first
        try:
            arr = json.loads(skills)
            if isinstance(arr, list):
                return [str(s).strip() for s in arr if str(s).strip()]
        except Exception:
            pass
        # fallback: comma-separated
        return [s.strip() for s in skills.split(",") if s.strip()]
    return []

def _email_exists(conn, email: str) -> bool:
    row = conn.execute(
        text("SELECT id FROM users WHERE email=:email LIMIT 1"),
        {"email": email}
    ).first()
    return row is not None

def _ensure_skill_ids(conn, skills):
    """Upsert skills by name and return {name: id}."""
    if not skills:
        return {}
    # INSERT .. ON DUPLICATE to set LAST_INSERT_ID to existing id
    upsert = text("""
        INSERT INTO skills (name) VALUES (:name)
        ON DUPLICATE KEY UPDATE id = LAST_INSERT_ID(id)
    """)
    for s in skills:
        conn.execute(upsert, {"name": s})

    # fetch ids
    rows = conn.execute(
        text("SELECT id, name FROM skills WHERE name IN :names"),
        {"names": tuple(skills)}
    ).mappings().all()

    return {r["name"]: r["id"] for r in rows}

class AuthService:
    @staticmethod
    def signup(data):
        required = ["name", "email", "password", "state", "skills"]
        missing = [k for k in required if not data.get(k)]
        if missing:
            return jsonify({"message": f"{', '.join(missing)} is required"}), 400

        email = str(data["email"]).strip().lower()
        if not EMAIL_RE.match(email):
            return jsonify({"message": "Invalid email format"}), 400

        password = str(data["password"])
        if len(password) < 6:
            return jsonify({"message": "Password must be at least 6 characters long"}), 400

        name = str(data["name"]).strip()
        state = str(data.get("state") or "").strip()[:2].upper()
        skills = _normalize_skills(data.get("skills"))

        engine = current_app.config["ENGINE"]
        with engine.begin() as conn:
            # duplicate email?
            if _email_exists(conn, email):
                return jsonify({"message": "Email already exists"}), 400

            # insert user
            pwd_hash = hashlib.sha256(password.encode()).hexdigest()
            conn.execute(
                text("""
                    INSERT INTO users (name, email, password_hash, state)
                    VALUES (:name, :email, :hash, :state)
                """),
                {"name": name, "email": email, "hash": pwd_hash, "state": state or None}
            )
            user_id = conn.execute(text("SELECT LAST_INSERT_ID()")).scalar()

            # upsert skills and link
            if skills:
                name_to_id = _ensure_skill_ids(conn, skills)
                for s in skills:
                    sid = name_to_id.get(s)
                    if sid:
                        conn.execute(
                            text("INSERT IGNORE INTO user_skills (user_id, skill_id) VALUES (:u, :s)"),
                            {"u": user_id, "s": sid}
                        )


        return jsonify({
            "message": "Signup successful",
            "user": {"id": user_id, "name": name, "email": email, "state": state, "skills": skills}
        }), 201
    
    @staticmethod
    def login(data):
        """
        Body: { email, password }
        Verifies password hash and returns basic profile.
        """
        email = str(data.get("email") or "").strip().lower()
        pw    = str(data.get("password") or "")

        if not email or not pw:
            return jsonify({"message": "Email and password are required"}), 400

        engine = current_app.config["ENGINE"]
        with engine.connect() as conn:
            row = conn.execute(text("""
                SELECT id, name, email, password_hash, state
                FROM users
                WHERE email = :email
                LIMIT 1
            """), {"email": email}).mappings().first()

            print(row)
    
            ad = conn.execute(text("""
                SELECT * FROM admins, users WHERE users.email = :email AND admins.user_id = users.id LIMIT 1
            """), {"email": email}).mappings().first()
            
            vl = conn.execute(text("""
                SELECT * FROM volunteers, users WHERE users.email = :email AND users.id = volunteers.user_id LIMIT 1
            """), {"email": email}).mappings().first()

        # Verify password using SHA-256
        pw_hash = hashlib.sha256(pw.encode()).hexdigest()
        if not row or row["password_hash"] != pw_hash:
            return jsonify({"message": "Invalid credentials"}), 401

        print({
            "message": "Login successful",
            "user": {
                "id": row["id"],
                "name": row["name"],
                "email": row["email"],
                "state": row["state"],
                "role": "admin" if ad else "volunteer" if vl else "none"
            }
        })

        return jsonify({
            "message": "Login successful",
            "user": {
                "id": row["id"],
                "name": row["name"],
                "email": row["email"],
                "state": row["state"],
                "role": "admin" if ad else "volunteer" if vl else "none"
            }
        }), 200
        
    @staticmethod
    def check_email():
        """Check if email is already taken."""
        """
        Query: ?email=
        Returns { available: bool }
        """
        email = (request.args.get("email") or "").strip().lower()
        if not EMAIL_RE.match(email):
            return jsonify({"available": False, "message": "Invalid email"}), 400

        engine = current_app.config["ENGINE"]
        with engine.connect() as conn:
            taken = _email_exists(conn, email)

        return jsonify({"available": not taken}), 200
    
    @staticmethod
    def list_skills():
        """Return all skills as a list of strings."""
        """
        Returns all skills as an array of strings.
        Useful for populating the signup multiselect.
        """
        engine = current_app.config["ENGINE"]
        with engine.connect() as conn:
            rows = conn.execute(text("SELECT name FROM skills ORDER BY name ASC")).all()
        return jsonify([r[0] for r in rows]), 200