import http
from flask import Blueprint, abort, jsonify, request
from src.model.models import Host
from src.service.HostService import HostService

host_controller = Blueprint('host_controller', __name__, template_folder='templates')
service = HostService()

@host_controller.route('/host/')
def list():
    try:
        objs = service.listAll()
        if(objs is None):
            raise ModuleNotFoundError('Hosts não encontrados')
        list = []
        for obj in objs:
            list.append(obj.hostToJson())
        return jsonify(list)
    except ModuleNotFoundError:
        abort(http.HTTPStatus.BAD_REQUEST)
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@host_controller.route('/host/<id>')
def findById(id):
    try:
        obj = service.findById(id)
        if(obj is None):
            raise ModuleNotFoundError('no content')
        return jsonify(obj.hostToJson())
    except ModuleNotFoundError:
        abort(http.HTTPStatus.BAD_REQUEST)
    except:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@host_controller.route('/host/encontrar/<url>')
def encontrardocumento(url):
    try:
        if(url is ''):
            raise Exception('entrada não é válida')
        obj = service.findByUrl(url)
        if(obj is None):
            raise ModuleNotFoundError('não encontrado.')
        return jsonify(obj.hostToJson())
    except ModuleNotFoundError:
        abort(http.HTTPStatus.BAD_REQUEST)
    except Exception:
        abort(http.HTTPStatus.BAD_REQUEST)

@host_controller.route('/host/<id>', methods=["DELETE"])
def removerdocid(id):
    if id is None:
        abort(http.HTTPStatus.PRECONDITION_REQUIRED)
    try:
        obj = service.findById(id)
        if (obj is None):
            raise ModuleNotFoundError('no content')
        service.remove(obj)
        return obj
    except ModuleNotFoundError:
        abort(http.HTTPStatus.BAD_REQUEST)
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@host_controller.route('/documento/remove', methods=["DELETE"])
def removerdoc():
    if request.get_json() is None:
        abort(http.HTTPStatus.PRECONDITION_REQUIRED)
    try:
        body = request.get_json()
        obj = Host()
        obj.dictToHost(body)
        obj = service.findById(obj.id)
        if(obj.id is None):
            raise ModuleNotFoundError('Não encontrado')
        service.remove(obj)
        return jsonify(obj.documentoToJson())
    except ModuleNotFoundError:
        abort(http.HTTPStatus.BAD_REQUEST)
    except Exception:
        abort(http.HTTPStatus.BAD_REQUEST)

@host_controller.route('/host/ordemAlfabetica')
def listEmOrdemAlfabetica():
    try:
        objs = service.listarEmOrdemAlfabetica()
        if(objs is None):
            raise ModuleNotFoundError('Hosts não encontrados')
        list = []
        for obj in objs:
            list.append(obj.hostToJson())
        return jsonify(list)
    except ModuleNotFoundError:
        abort(http.HTTPStatus.BAD_REQUEST)
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)