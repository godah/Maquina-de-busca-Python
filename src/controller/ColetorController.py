import http
from flask import Blueprint, abort, jsonify, request
from src.service.ColetorService import ColetorService

coletor_controller = Blueprint('coletor_controller', __name__, template_folder='templates')
service = ColetorService()


@coletor_controller.route('/coletor')
def iniciar():
    try:
        service.executar()
        return http.HTTPStatus.OK
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)
