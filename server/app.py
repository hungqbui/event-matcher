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

# Import usersided volunteer routes
from routes.volunteer_user import bp as volunteer_user_bp
app.register_blueprint(volunteer_user_bp, url_prefix='/api/volunteer_user')

# Import volunteer matching routes
from routes.volunteer_matching import bp as volunteer_bp
app.register_blueprint(volunteer_bp, url_prefix='/api')

# Import notification routes
from routes.notification import bp as notification_bp
app.register_blueprint(notification_bp, url_prefix='/api')

from routes.auth import bp as auth_bp
app.register_blueprint(auth_bp, url_prefix='/api')

#@app.route('/')
#def index():
 #   return render_template('index.html')

if __name__ == '__main__':
    print("Flask running on http://localhost:5000")
    app.run(host="0.0.0.0", debug=True, port=5000)

