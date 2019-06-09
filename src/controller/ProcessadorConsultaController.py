import http
from flask import Blueprint, abort, jsonify, request

processadorconsulta_controller = Blueprint('processadorconsulta_controller', __name__, template_folder='templates')

@processadorconsulta_controller.route('/processadorconsulta')
def consultar():
    try:
        return 'processador_consulta'
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)
