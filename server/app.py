from flask import render_template, Flask, jsonify
from flask_cors import CORS
import jwt
from functools import wraps
from flask import request

# Import blueprints

app = Flask(__name__)
CORS(app)

# Import manager related routes
from routes.manager import bp as manager_bp
app.register_blueprint(manager_bp, url_prefix='/api/manager')

# Import volunteer matching routes
from routes.volunteer_matching import bp as volunteer_bp
app.register_blueprint(volunteer_bp, url_prefix='/api')

# Import notification routes
from routes.notification import bp as notification_bp
app.register_blueprint(notification_bp, url_prefix='/api')

# Import usersided volunteer routes
from routes.volunteer_user import bp as volunteer_user_bp
app.register_blueprint(volunteer_user_bp, url_prefix='/api/volunteer_user')

#import profile routes
from routes.profile import profile_bp
app.register_blueprint(profile_bp, url_prefix='/api')

#import volunteer history routes
from routes.volunteer_history import history_bp
app.register_blueprint(history_bp, url_prefix='/api')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)