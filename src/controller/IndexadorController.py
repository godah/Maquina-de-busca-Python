
import http
from flask import Blueprint, abort, jsonify, request

from src.model.models import Documento
from src.service.IndexadorService import IndexadorService

indexador_controller = Blueprint('indexador_controller', __name__, template_folder='templates')

iis = IndexadorService()

@indexador_controller.route('/indexador/indice', methods=["POST"])
def criaindice():
    try:
        confirmacao = iis.limpaCriaIndice();
        if confirmacao:
            return 'o índice invertido foi criado com sucesso'
        else:
            raise Exception('o índice invertido não pode ser criado')
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)
        
@indexador_controller.route('/indexador/documento')
def getdocumento():
    try:
        documento = Documento()
        documento = iis.getDocumentos()
        if documento is not None:
            return jsonify(documento.documentoToJson())
    except:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)