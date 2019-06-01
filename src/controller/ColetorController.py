import http
from flask import Blueprint, abort, jsonify, request

coletor_controller = Blueprint('coletor_controller', __name__, template_folder='templates')

@coletor_controller.route('/coletor')
def coletor():
    try:
        return 'coletor'
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)
