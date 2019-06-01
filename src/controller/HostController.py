import http
from flask import Blueprint, abort, jsonify, request
from src.model.models import Host
from src.service.HostService import HostService

host_controller = Blueprint('host_controller', __name__, template_folder='templates')
service = HostService()

@host_controller.route('/host')
def list():
    try:
        objs = service.listAll()
        list = []
        for obj in objs:
            list.append(obj.hostToJson())
        return jsonify(list)
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@host_controller.route('/host/<id>')
def findById(id):
    try:
        obj = service.findById(id)
        return jsonify(obj.hostToJson())
    except:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@host_controller.route('/host', methods=["POST"])
def post():
    if request.get_json() is None:
        abort(http.HTTPStatus.PRECONDITION_REQUIRED)
    try:
        body = request.get_json()
        obj = Host()
        obj.dictToHost(body)
        service.save(obj)
        return jsonify(obj.hostToJson())
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@host_controller.route('/host', methods=["PUT"])
def put():
    if request.get_json() is None:
        abort(http.HTTPStatus.PRECONDITION_REQUIRED)
    try:
        body = request.get_json()
        obj = Host()
        obj.dictToHost(body)
        obj = service.update(obj)
        return jsonify(obj.hostToJson())
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@host_controller.route('/host/<id>', methods=["DELETE"])
def delete(id):
    if id == None:
        abort(http.HTTPStatus.PRECONDITION_REQUIRED)
    try:
        obj = service.findById(id)
        service.remove(obj)
        return obj
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)