import http
from flask import Blueprint, abort, jsonify, request

indexador_controller = Blueprint('indexador_controller', __name__, template_folder='templates')

@indexador_controller.route('/indexador')
def indexar():
    try:
        return 'indexador'
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)
