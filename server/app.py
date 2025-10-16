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

# Define a route for the home page
@app.route('/')
def index():
    """Home page route."""
    return render_template('index.html')

@app.errorhandler(404)
def not_found(error):
    return jsonify({'message': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    return jsonify({'message': 'Internal server error'}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)