import http
from flask import Blueprint, abort, jsonify, request

login_controller = Blueprint('login_controller', __name__, template_folder='templates')

@login_controller.route('/login')
def login():
    try:
        return 'login'
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)
