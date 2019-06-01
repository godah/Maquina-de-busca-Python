import http
from flask import Blueprint, abort, jsonify, request
from src.model.models import IndiceInvertido
from src.service.IndiceInvertidoService import IndiceInvertidoService

indiceinvertido_controller = Blueprint('indiceinvertido_controller', __name__, template_folder='templates')
service = IndiceInvertidoService()

@indiceinvertido_controller.route('/indiceInvertido')
def list():
    try:
        objs = service.listAll()
        list = []
        for obj in objs:
            list.append(obj.indiceInvertidoToJson())
        return jsonify(list)
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@indiceinvertido_controller.route('/indiceInvertido/<id>')
def findById(id):
    try:
        obj = service.findById(id)
        return jsonify(obj.indiceInvertidoToJson())
    except:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@indiceinvertido_controller.route('/indiceInvertido', methods=["POST"])
def post():
    if request.get_json() is None:
        abort(http.HTTPStatus.PRECONDITION_REQUIRED)
    try:
        body = request.get_json()
        obj = IndiceInvertido()
        obj.dictToIndiceInvertido(body)
        service.save(obj)
        return jsonify(obj.indiceInvertidoToJson())
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@indiceinvertido_controller.route('/indiceInvertido', methods=["PUT"])
def put():
    if request.get_json() is None:
        abort(http.HTTPStatus.PRECONDITION_REQUIRED)
    try:
        body = request.get_json()
        obj = IndiceInvertido()
        obj.dictToIndiceInvertido(body)
        obj = service.update(obj)
        return jsonify(obj.indiceInvertidoToJson())
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@indiceinvertido_controller.route('/indiceInvertido/<id>', methods=["DELETE"])
def delete(id):
    if id == None:
        abort(http.HTTPStatus.PRECONDITION_REQUIRED)
    try:
        obj = service.findById(id)
        service.remove(obj)
        return obj
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)