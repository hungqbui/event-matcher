# server/routes/auth.py
from flask import Blueprint, jsonify, request, current_app
from sqlalchemy import text
from werkzeug.security import generate_password_hash, check_password_hash
import re, json

bp = Blueprint("auth", __name__)  # app registers with url_prefix="/api"

EMAIL_RE = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")

# ---------- helpers ----------

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

# ---------- routes ----------

@bp.route("/signup", methods=["POST"])
def signup():
    """
    Body: { name, email, password, state, skills[] }
    Creates user (hashed password) and links skills.
    """
    data = request.get_json(silent=True) or {}

    # presence checks
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
        pwd_hash = generate_password_hash(password)
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


@bp.route("/login", methods=["POST"])
def login():
    """
    Body: { email, password }
    Verifies password hash and returns basic profile.
    """
    data = request.get_json(silent=True) or {}
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

    if not row or not check_password_hash(row["password_hash"], pw):
        return jsonify({"message": "Invalid credentials"}), 401

    return jsonify({
        "message": "Login successful",
        "id": row["id"],
        "name": row["name"],
        "email": row["email"],
        "state": row["state"],
    }), 200


@bp.route("/check-email", methods=["GET"])
def check_email():
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


@bp.route("/skills", methods=["GET"])
def list_skills():
    """
    Returns all skills as an array of strings.
    Useful for populating the signup multiselect.
    """
    engine = current_app.config["ENGINE"]
    with engine.connect() as conn:
        rows = conn.execute(text("SELECT name FROM skills ORDER BY name ASC")).all()
    return jsonify([r[0] for r in rows]), 200
