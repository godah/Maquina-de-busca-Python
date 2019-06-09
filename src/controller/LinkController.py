import http
from flask import Blueprint, abort, jsonify, request
from src.model.models import Link
from src.service.LinkService import LinkService

link_controller = Blueprint('link_controller', __name__, template_folder='templates')
service = LinkService()

@link_controller.route('/link/')
def listarlink():
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
        if (obj is None):
            raise ModuleNotFoundError('não encontrado.')
        return jsonify(obj.linkToJson())
    except ModuleNotFoundError:
        abort(http.HTTPStatus.NO_CONTENT)
    except:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@link_controller.route('/link/', methods=["POST"])
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

@link_controller.route('/link/', methods=["PUT"])
def atualizaLink():
    if request.get_json() is None:
        abort(http.HTTPStatus.PRECONDITION_REQUIRED)
    try:
        body = request.get_json()
        obj = Link()
        obj.dictToLink(body)
        obj = service.findById(obj.id)
        if(obj is None):
            raise ModuleNotFoundError('não encontrado.')
        obj = service.update(obj)
        return jsonify(obj.linkToJson())
    except ModuleNotFoundError:
        abort(http.HTTPStatus.NO_CONTENT)
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@link_controller.route('/link/atualizaUltimaColetaSementes', methods=["PUT"])
def atualizaUltimaColetaSementes():
    if request.get_json() is None:
        abort(http.HTTPStatus.PRECONDITION_REQUIRED)
    try:
        body = request.get_json()
        objn = Link()
        obj = Link()
        objn.dictToLink(body)
        obj = service.findById(obj.id)
        if(obj is None):
            raise ModuleNotFoundError('não encontrado.')
        obj.ultimaColeta = objn.ultimaColeta
        obj = service.update(obj)
        return jsonify(obj.linkToJson())
    except ModuleNotFoundError:
        abort(http.HTTPStatus.NO_CONTENT)
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@link_controller.route('/link/<id>', methods=["DELETE"])
def removerlinkid(id):
    if id is None:
        abort(http.HTTPStatus.PRECONDITION_REQUIRED)
    try:
        obj = service.findById(id)
        service.remove(obj)
        return obj
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@link_controller.route('/link', methods=["DELETE"])
def removerdoc():
    if request.get_json() is None:
        abort(http.HTTPStatus.PRECONDITION_REQUIRED)
    try:
        body = request.get_json()
        obj = Link()
        obj.dictToLink(body)
        obj = service.findById(obj.id)
        if(obj.id is None):
            raise ModuleNotFoundError('Não encontrado')
        service.remove(obj)
        return jsonify(obj.linkToJson())
    except ModuleNotFoundError:
        abort(http.HTTPStatus.BAD_REQUEST)
    except Exception:
        abort(http.HTTPStatus.BAD_REQUEST)


@link_controller.route('/link/encontrar/<url>')
def encontrardocumento(url):
    try:
        if(url is ''):
            raise Exception('entrada não é válida')
        obj = service.findByUrl(url)
        if(obj is None):
            raise ModuleNotFoundError('não encontrado.')
        return jsonify(obj.linkToJson())
    except ModuleNotFoundError:
        abort(http.HTTPStatus.BAD_REQUEST)
    except Exception:
        abort(http.HTTPStatus.BAD_REQUEST)

@link_controller.route('/link/ordemAlfabetica')
def listEmOrdemAlfabetica():
    try:
        objs = service.listarEmOrdemAlfabetica()
        if(objs is None):
            raise ModuleNotFoundError('Links não encontrados')
        list = []
        for obj in objs:
            list.append(obj.linkToJson())
        return jsonify(list)
    except ModuleNotFoundError:
        abort(http.HTTPStatus.BAD_REQUEST)
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)


@link_controller.route('/link/sementes')
def listarSementes():
    try:
        objs = service.obterLinksNaoColetados()
        if(objs is None):
            raise ModuleNotFoundError('não encontrado.')
        list = []
        for obj in objs:
            list.append(obj.linkToJson())
        return jsonify(list)
    except ModuleNotFoundError:
        abort(http.HTTPStatus.BAD_REQUEST)
    except Exception:
        abort(http.HTTPStatus.BAD_REQUEST)

@link_controller.route('/link/pagina')
def listarPagina():
    try:
        paginator = service.listarPagina()
        list = []
        while paginator.has_next:
            page = paginator.next()
            objs = page.items
            for obj in objs:
                print(obj.url)
                list.append(obj.linkToJson())
        return jsonify(list)
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@link_controller.route('/link/pagina/<pageFlag>')
def listarPaginaPorPageFlag(pageFlag):
    if (int(id) is None):
        abort(http.HTTPStatus.PRECONDITION_REQUIRED)
    try:
        paginator = service.buscarPagina(pageFlag)
        list = []
        while paginator.has_next:
            page = paginator.next()
            objs = page.items
            for obj in objs:
                print(obj.url)
                list.append(obj.linkToJson())
        return jsonify(list)
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@link_controller.route('/link/intervalo/<id1>/<id2>')
def encontrarLinkPorIntervalo(id1, id2):
    try:
        if (int(id1) is None or int(id2) is None):
            abort(http.HTTPStatus.PRECONDITION_REQUIRED)
        objs = service.obterLinksPorIntervaloDeIdentificacao(id1, id2)
        list = []
        for obj in objs:
            print(obj.url)
            list.append(obj.linkToJson())
        return jsonify(list)
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@link_controller.route('/link/intervalo/<id1>/<id2>')
def contarLinkPorIntervalo(id1, id2):
    try:
        if int(id1) is None or int(id2) is None:
            abort(http.HTTPStatus.PRECONDITION_REQUIRED)
        objs = service.obterLinksPorIntervaloDeIdentificacao(id1, id2)
        list = []
        for obj in objs:
            print(obj.url)
            list.append(obj.linkToJson())
        return jsonify(list)
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@link_controller.route('/urlSementes', methods=["POST"])
def inserirUrlSemente():
    if request.get_json() is None:
        abort(http.HTTPStatus.PRECONDITION_REQUIRED)
    try:
        body = request.get_json()
        obj = Link()
        obj.dictToLink(body)
        obj = service.inserirSemente(obj.url)
        return jsonify(obj.linkToJson())
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)



@link_controller.route('/link/encontrarSemente/<host>')
def encontrarSementePorHost(host):
    try:
        if host is None:
            raise Exception('entrada não é válida')
        objs = service.encontrarSementePorHost(host)
        list = []
        for obj in objs:
            print(obj.url)
            list.append(obj.linkToJson())
        return jsonify(list)
    except ModuleNotFoundError:
        abort(http.HTTPStatus.BAD_REQUEST)
    except Exception:
        abort(http.HTTPStatus.BAD_REQUEST)


@link_controller.route('/link/sementes/datas/<dt1>/<dt2>')
def encontrarSementesPorIntervaloDatas(dt1, dt2):
    try:
        if dt1 is None or dt2 is None:
            abort(http.HTTPStatus.PRECONDITION_REQUIRED)
        objs = service.encontrarSementesPorIntervaloDatas(dt1, dt2)
        list = []
        for obj in objs:
            print(obj.url)
            list.append(obj.linkToJson())
        return jsonify(list)
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)


@link_controller.route('/link/ultima/coleta/<link>/<data>', methods=["PUT"])
def atualizaDataUltimaColeta(host, data):
    try:
        if host is None or data is None:
            raise ModuleNotFoundError
        n = service.atualizaDataUltimaColeta(host, data)
        return "sucesso", "número de registros atualizados: " + n
    except ModuleNotFoundError:
        abort(http.HTTPStatus.BAD_REQUEST)
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)