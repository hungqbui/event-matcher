from flask import Blueprint

bp = Blueprint('example', __name__)


# This means /example/hello
@bp.route('/hello', methods=['GET'])
def hello():
    return "Hello, World!"
