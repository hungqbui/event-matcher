from flask import render_template, Flask
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

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
    app.run(debug=True, port=5000)

