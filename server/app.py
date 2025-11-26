
from flask import Flask
from flask_cors import CORS
import os
from sqlalchemy import create_engine
from urllib.parse import quote_plus

try:
    from dotenv import load_dotenv
    load_dotenv()
except Exception:
    pass

def make_engine_from_env():
    host = os.getenv("DB_HOST", "127.0.0.1")
    port = os.getenv("DB_PORT", "3306")
    name = os.getenv("DB_NAME", "eventmatcher")
    user = os.getenv("DB_USER", "root")
    pw   = quote_plus(os.getenv("DB_PASS", "admin"))  


    url = f"mysql+pymysql://{user}:{pw}@{host}:{port}/{name}?charset=utf8mb4"

    return create_engine(url, pool_pre_ping=True, future=True)

app = Flask(__name__)
CORS(app, resources={r"/api/*": {"origins": "*"}})
app.config["ENGINE"] = make_engine_from_env()

from .routes.auth import bp as auth_bp
from .routes.manager import bp as manager_bp
from .routes.notification import bp as notifications_bp
from .routes.profile import profile_bp
from .routes.volunteer_history import history_bp
from .routes.volunteer_matching import bp as matching_bp
from .routes.volunteer_user import bp as volunteer_user_bp
from .routes.task import task_bp
from .routes.report import report_bp


app.register_blueprint(auth_bp,          url_prefix="/api")
app.register_blueprint(notifications_bp, url_prefix="/api")
app.register_blueprint(profile_bp,       url_prefix="/api")
app.register_blueprint(matching_bp,      url_prefix="/api")
app.register_blueprint(history_bp,       url_prefix="/api")
app.register_blueprint(manager_bp,       url_prefix="/api/manager")
app.register_blueprint(volunteer_user_bp,url_prefix="/api/volunteer_user")
app.register_blueprint(task_bp,          url_prefix="/api/tasks")
app.register_blueprint(report_bp, url_prefix="/api")

@app.get("/ping")
def ping():
    return "pong", 200

if __name__ == "__main__":
    print("Flask running on http://127.0.0.1:5000")
    app.run(host="127.0.0.1", port=5000, debug=True)
