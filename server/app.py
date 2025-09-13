from flask import render_template, Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Define a route for the home page
@app.route('/')
def index():
    """Home page route."""
    return render_template('index.html')
