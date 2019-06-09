import http
from flask import Blueprint, abort, jsonify, request
from src.model.models import Documento
from src.service.DocumentoService import DocumentoService

documento_controller = Blueprint('documento_controller', __name__, template_folder='templates')
service = DocumentoService()

@documento_controller.route('/documento')
def listardocumento():
    try:
        objs = service.listAll()
        list = []
        for obj in objs:
            list.append(obj.documentoToJson())
        return jsonify(list)
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@documento_controller.route('/documento/<id>')
def listardocumentoid(id):
    try:
        obj = service.findById(id)
        if(obj is None):
            raise ModuleNotFoundError('Nao encontrado')
        return jsonify(obj.documentoToJson())
    except ModuleNotFoundError:
        abort(http.HTTPStatus.BAD_REQUEST)
    except:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@documento_controller.route('/documento/<id>', methods=["DELETE"])
def removerdocid(id):
    if id is None:
        abort(http.HTTPStatus.PRECONDITION_REQUIRED)
    try:
        obj = service.findById(id)
        service.remove(obj)
        return obj
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@documento_controller.route('/documento/remove', methods=["DELETE"])
def removerdoc():
    if request.get_json() is None:
        abort(http.HTTPStatus.PRECONDITION_REQUIRED)
    try:
        body = request.get_json()
        obj = Documento()
        obj.dictToDocumento(body)
        obj = service.findById(obj.id)
        if(obj.id is None):
            raise ModuleNotFoundError('Não encontrado')
        service.remove(obj)
        return jsonify(obj.documentoToJson())
    except ModuleNotFoundError:
        abort(http.HTTPStatus.BAD_REQUEST)
    except Exception:
        abort(http.HTTPStatus.BAD_REQUEST)

@documento_controller.route('/documento/encontrar/<url>')
def encontrardocumento(url):
    try:
        if(url is ''):
            raise Exception('entrada não é válida')
        obj = service.findByUrl(url)
        if(obj is None):
            raise ModuleNotFoundError('não encontrado.')
        return jsonify(obj.documentoToJson())
    except ModuleNotFoundError:
        abort(http.HTTPStatus.BAD_REQUEST)
    except Exception:
        abort(http.HTTPStatus.BAD_REQUEST)
