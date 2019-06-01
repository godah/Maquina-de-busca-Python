import http
from flask import Blueprint, abort, jsonify, request
from src.model.models import Link
from src.service.LinkService import LinkService

link_controller = Blueprint('link_controller', __name__, template_folder='templates')
service = LinkService()

@link_controller.route('/link')
def list():
    try:
        objs = service.listAll()
        list = []
        for obj in objs:
            list.append(obj.linkToJson())
        return jsonify(list)
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@link_controller.route('/link/<id>')
def findById(id):
    try:
        obj = service.findById(id)
        return jsonify(obj.linkToJson())
    except:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@link_controller.route('/link', methods=["POST"])
def post():
    if request.get_json() is None:
        abort(http.HTTPStatus.PRECONDITION_REQUIRED)
    try:
        body = request.get_json()
        obj = Link()
        obj.dictToLink(body)
        service.save(obj)
        return jsonify(obj.linkToJson())
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@link_controller.route('/link', methods=["PUT"])
def put():
    if request.get_json() is None:
        abort(http.HTTPStatus.PRECONDITION_REQUIRED)
    try:
        body = request.get_json()
        obj = Link()
        obj.dictToLink(body)
        obj = service.update(obj)
        return jsonify(obj.linkToJson())
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@link_controller.route('/link/<id>', methods=["DELETE"])
def delete(id):
    if id == None:
        abort(http.HTTPStatus.PRECONDITION_REQUIRED)
    try:
        obj = service.findById(id)
        service.remove(obj)
        return obj
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)