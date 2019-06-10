#testado
import http
from flask import Blueprint, abort, jsonify, request
from src.service.ProcessadorConsultaService import ProcessadorConsulta
from src.model.models import Consulta, EntradaRanking

pcs = ProcessadorConsulta()

processadorconsulta_controller = Blueprint('processadorconsulta_controller', __name__, template_folder='templates')

@processadorconsulta_controller.route('/processador/consulta/<consultadousuario>')
def consultar(consultadousuario):
    try:
        consulta = Consulta('', '')
        consulta = pcs.processarConsulta(consultadousuario)
        if consulta.ranking is not None:
            return jsonify(consulta.consultaToJson())
        else:
            raise Exception('o índice invertido não pode ser criado')
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@processadorconsulta_controller.route('/processador/ranking/<tipo>')
def ranking(tipo):
    try:
        ranking = EntradaRanking('', [], 0.0, 0.0)
        ranking = pcs.ranking(tipo)
        if ranking.ranking is not None:
            return jsonify(ranking.entradaRankingToJson())
        else:
            raise Exception('tipo de ranking não encontrado')
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

@processadorconsulta_controller.route('/processador/ranking')
def rankingnormal():
    try:
        ranking = EntradaRanking('', [], 0.0, 0.0)
        ranking = pcs.ranking(1)
        if ranking.ranking is not None:
            return jsonify(ranking.entradaRankingToJson())
        else:
            raise Exception('falha ao obter ranking')
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)
