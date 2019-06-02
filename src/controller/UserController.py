import http
from flask import Blueprint, abort, jsonify, request, json, app
from src.model.models import Users
from src.service.UserService import UserService

user_controller = Blueprint('user_controller', __name__, template_folder='templates')
service = UserService()

@user_controller.route('/usuario', methods=["PUT"])
def put():
    if request.get_json() is None:
        abort(http.HTTPStatus.BAD_REQUEST)
    try:
        body = request.get_json()
        obj = Users()
        obj.dictToUser(body)
        obj = service.update(obj)
        return jsonify(obj.userToJson())
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@user_controller.route('/usuario/remove/<id>', methods=["DELETE"])
def delete(id):
    if id == None:
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
def deleteobj():
    if request.get_json() is None:
        abort(http.HTTPStatus.BAD_REQUEST)
    try:
        body = request.get_json()
        obj = Users()
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
def listaradmin():
    try:
        objs = service.listaradmin()
        return jsonify(objs)
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@user_controller.route('/usuario/administrador/<ident>')
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
def listarusuarios():
    try:
        objs = service.listarusuarios()
        return jsonify(objs)
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)


@user_controller.route('/usuario/<ident>')
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
        
@user_controller.route('/usuario/administrador', methods=['POST'])
def inseriradmin():
    if request.get_json() is None:
        abort(http.HTTPStatus.BAD_REQUEST)
    try:
        body = request.get_json()
        obj = Users()
        obj.dictToUser(body)
        service.save(obj)
        return jsonify(obj.userToJson())
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@user_controller.route('/usuario/administrador', methods=["POST"])
def inserir():
    if request.get_json() is None:
        abort(http.HTTPStatus.BAD_REQUEST)
    try:
        body = request.get_json()
        obj = Users()
        obj.dictToUser(body)
        service.save(obj)
        return jsonify(obj.userToJson())
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@user_controller.route('/usuario', methods=["POST"])
def inserirusuario():
    if request.get_json() is None:
        abort(http.HTTPStatus.BAD_REQUEST)
    try:
        body = request.get_json()
        obj = Users()
        obj.dictToUser(body)
        service.inserirusuario(obj)
        if(obj.id is None):
            raise Exception('Não autorizado')
        return jsonify(obj.userToJson())
    except Exception:
        abort(http.HTTPStatus.BAD_REQUEST)

@user_controller.route('/usuario/encontrar/<username>')
def encontrarpornome(username):
    try:
        if(username is ''):
            raise Exception('entrada não é válida')
        obj = service.findByUsername(username)
        if(obj is None):
            raise ModuleNotFoundError('não encontrado.')
        return jsonify(obj)
    except ModuleNotFoundError:
        abort(http.HTTPStatus.NO_CONTENT)
    except Exception:
        abort(http.HTTPStatus.BAD_REQUEST)

@user_controller.route('/usuario/ordemAlfabetica')
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