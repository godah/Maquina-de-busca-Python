import http
from flask import Blueprint, abort, jsonify, request
from src.model.models import Users
from src.service.UserService import UserService

user_controller = Blueprint('user_controller', __name__, template_folder='templates')
service = UserService()

@user_controller.route('/user')
def list():
    try:
        objs = service.listAll()
        list = []
        for obj in objs:
            list.append(obj.userToJson())
        return jsonify(list)
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@user_controller.route('/user/<id>')
def findById(id):
    try:
        obj = service.findById(id)
        return jsonify(obj.userToJson())
    except:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@user_controller.route('/user', methods=["POST"])
def post():
    if request.get_json() is None:
        abort(http.HTTPStatus.PRECONDITION_REQUIRED)
    try:
        body = request.get_json()
        obj = Users()
        obj.dictToUser(body)
        service.save(obj)
        return jsonify(obj.userToJson())
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@user_controller.route('/user', methods=["PUT"])
def put():
    if request.get_json() is None:
        abort(http.HTTPStatus.PRECONDITION_REQUIRED)
    try:
        body = request.get_json()
        obj = Users()
        obj.dictToUser(body)
        obj = service.update(obj)
        return jsonify(obj.userToJson())
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@user_controller.route('/user/<id>', methods=["DELETE"])
def delete(id):
    if id == None:
        abort(http.HTTPStatus.PRECONDITION_REQUIRED)
    try:
        obj = service.findById(id)
        service.remove(obj)
        return obj
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)