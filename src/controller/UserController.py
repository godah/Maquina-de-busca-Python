import http
from flask import Blueprint, abort, jsonify, request
from src.model.models import Users
from src.service.UserService import UserService

user_controller = Blueprint('user_controller', __name__, template_folder='templates')
userService = UserService()

@user_controller.route('/user')
def list():
    try:
        users = userService.listAll()
        list = []
        for u in users:
            list.append(u.userToJson())
        return jsonify(list)
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@user_controller.route('/user/<id>')
def findById(id):
    try:
        u = userService.findById(id)
        return jsonify(u.userToJson())
    except:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@user_controller.route('/user', methods=["POST"])
def post():
    if request.get_json() is None:
        abort(http.HTTPStatus.PRECONDITION_REQUIRED)
    try:
        body = request.get_json()
        print(body.get('username'))
        u = Users()
        u.dictToUser(body)
        userService.save(u)
        return jsonify(u.userToJson())
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@user_controller.route('/user', methods=["PUT"])
def put():
    if request.get_json() is None:
        abort(http.HTTPStatus.PRECONDITION_REQUIRED)
    try:
        body = request.get_json()
        print(body.get('username'))
        u = Users()
        u.dictToUser(body)
        u = userService.update(u)
        return jsonify(u.userToJson())
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@user_controller.route('/user/<id>', methods=["DELETE"])
def delete(id):
    if id == None:
        abort(http.HTTPStatus.PRECONDITION_REQUIRED)
    try:
        u = userService.findById(id)
        userService.remove(u)
        return u
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)