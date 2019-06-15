import http
from flask import Blueprint, abort, jsonify, request
from flask_login import login_required

from src.model.models import User
from src.service.UserService import UserService

user_controller = Blueprint('user_controller', __name__, template_folder='templates')
service = UserService()

@user_controller.route('/usuario', methods=["PUT"])
@login_required
def put():
    if request.get_json() is None:
        abort(http.HTTPStatus.BAD_REQUEST)
    try:
        body = request.get_json()
        obj = User()
        obj.dictToUser(body)
        obj = service.update(obj)
        return jsonify(obj.userToJson())
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@user_controller.route('/usuario/remove/<id>', methods=["DELETE"])
@login_required
def removerusuario(id):
    if id is None:
        abort(http.HTTPStatus.PRECONDITION_FAILED)
    try:
        obj = service.findById(id)
        if(obj.id is None):
            raise ModuleNotFoundError('Não encontrado')
        service.remove(obj)
        return jsonify(obj.userToJson())
    except ModuleNotFoundError:
        abort((http.HTTPStatus.NO_CONTENT))
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)


@user_controller.route('/usuario/remove', methods=["DELETE"])
@login_required
def removeruser():
    if request.get_json() is None:
        abort(http.HTTPStatus.BAD_REQUEST)
    try:
        body = request.get_json()
        obj = User()
        obj.dictToUser(body)
        obj = service.findById(obj.id)
        if(obj.id is None):
            raise ModuleNotFoundError('Não encontrado')
        service.remove(obj)
        return jsonify(obj.userToJson())
    except ModuleNotFoundError:
        abort((http.HTTPStatus.NO_CONTENT))
    except Exception:
        abort(http.HTTPStatus.BAD_REQUEST)

@user_controller.route('/usuario/administrador')
@login_required
def listaradmin():
    try:
        objs = service.listaradmin()
        return jsonify(objs)
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@user_controller.route('/usuario/administrador/<ident>')
@login_required
def listaradminid(ident):
    try:
        ident = int(ident)
    except ValueError:
        abort(http.HTTPStatus.BAD_REQUEST)

    try:
        objs = service.listaradminid(ident)
        return jsonify(objs)
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@user_controller.route('/usuario')
@login_required
def listarusuarios():
    try:
        objs = service.listarusuarios()
        return jsonify(objs)
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)


@user_controller.route('/usuario/<ident>')
@login_required
def listarusuarioid(ident):
    try:
        ident = int(ident)
    except ValueError:
        abort(http.HTTPStatus.BAD_REQUEST)

    try:
        objs = service.listarusuarioid(ident)
        return jsonify(objs)
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@user_controller.route('/usuario/administrador', methods=["POST"])
@login_required
def inseriradmin():
    if request.get_json() is None:
        abort(http.HTTPStatus.BAD_REQUEST)
    try:
        body = request.get_json()
        obj = User()
        obj.dictToUser(body)
        service.save(obj)
        return jsonify(obj.userToJson())
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@user_controller.route('/usuario', methods=["POST"])
@login_required
def inserirusuario():
    if request.get_json() is None:
        abort(http.HTTPStatus.BAD_REQUEST)
    try:
        body = request.get_json()
        obj = User()
        obj.dictToUser(body)
        service.inserirusuario(obj)
        if(obj.id is None):
            raise Exception('Não autorizado')
        return jsonify(obj.userToJson())
    except Exception:
        abort(http.HTTPStatus.BAD_REQUEST)

@user_controller.route('/usuario/encontrar/<username>')
@login_required
def encontrarusuario(username):
    try:
        if(username is ''):
            raise Exception('entrada não é válida')
        obj = service.findByUsername(username)
        if(obj is None):
            raise ModuleNotFoundError('não encontrado.')
        return jsonify(obj)
    except ModuleNotFoundError:
        abort(http.HTTPStatus.BAD_REQUEST)
    except Exception:
        abort(http.HTTPStatus.BAD_REQUEST)

@user_controller.route('/usuario/ordemAlfabetica')
@login_required
def listaremordemalfabetica():
    try:
        users = service.listAll()
        usorted = sorted(users, key=lambda u: u.username)
        retjson = []
        for u in usorted:
            #TODO filtrar users para não usuario logado não admin
            retjson.append(u.userToJson())
        return jsonify(retjson)
    except Exception:
        abort(http.HTTPStatus.BAD_REQUEST)