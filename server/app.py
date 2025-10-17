from flask import render_template, Flask, jsonify
from flask_cors import CORS
import jwt
from functools import wraps
from flask import request

# Import blueprints
from routes.manager import bp as manager_bp

app = Flask(__name__)
CORS(app)

# Register blueprints
app.register_blueprint(manager_bp, url_prefix='/api/manager')

# Register blueprints
app.register_blueprint(manager_bp, url_prefix='/api/manager')

# Import volunteer matching routes
from routes.volunteer_matching import bp as volunteer_bp
app.register_blueprint(volunteer_bp, url_prefix='/api')

# Import notification routes
from routes.notification import bp as notification_bp
app.register_blueprint(notification_bp, url_prefix='/api')

@app.route('/')
def index():
    return render_template('index.html')
