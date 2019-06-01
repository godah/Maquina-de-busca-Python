import http
from flask import Blueprint, abort, jsonify, request
from src.model.models import Documento
from src.service.DocumentoService import DocumentoService

documento_controller = Blueprint('documento_controller', __name__, template_folder='templates')
service = DocumentoService()

@documento_controller.route('/documento')
def list():
    try:
        objs = service.listAll()
        list = []
        for obj in objs:
            list.append(obj.documentoToJson())
        return jsonify(list)
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@documento_controller.route('/documento/<id>')
def findById(id):
    try:
        obj = service.findById(id)
        return jsonify(obj.documentoToJson())
    except:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@documento_controller.route('/documento', methods=["POST"])
def post():
    if request.get_json() is None:
        abort(http.HTTPStatus.PRECONDITION_REQUIRED)
    try:
        body = request.get_json()
        obj = Documento()
        obj.dictToDocumento(body)
        service.save(obj)
        return jsonify(obj.documentoToJson())
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@documento_controller.route('/documento', methods=["PUT"])
def put():
    if request.get_json() is None:
        abort(http.HTTPStatus.PRECONDITION_REQUIRED)
    try:
        body = request.get_json()
        obj = Documento()
        obj.dictToDocumento(body)
        obj = service.update(obj)
        return jsonify(obj.documentoToJson())
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@documento_controller.route('/documento/<id>', methods=["DELETE"])
def delete(id):
    if id == None:
        abort(http.HTTPStatus.PRECONDITION_REQUIRED)
    try:
        obj = service.findById(id)
        service.remove(obj)
        return obj
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)