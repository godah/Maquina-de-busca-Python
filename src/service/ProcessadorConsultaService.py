from bs4 import BeautifulSoup

from src.model.models import Consulta, TermoConsulta, EntradaRanking
from src.service.StopwordService import StopwordsService
from src.service.IndexadorService import IndexadorService
from src.service.TermoDocumentoService import TermoDocumentoService
from src.service.IndiceInvertidoService import IndiceInvertidoService

stopwordsService = StopwordsService()
inds = IndexadorService()
iis = IndiceInvertidoService()
ts = TermoDocumentoService()


class ProcessadorConsulta:
    mergeListasInvertidas = {}

    def processarConsulta(self, consultadousuario):
        soup = soup = BeautifulSoup(consultadousuario)
        consulta = Consulta(consultadousuario, stopwordsService.tratarVisao(soup))
        self.iniciarTermosConsulta(consulta)
        self.processarListasInvertidas(consulta)
        self.computarRankingSimilaridade()
        consulta.ranking = self.getRanking()
        return consulta

    def iniciarTermosConsulta(self, consulta):
        visaoConsulta = consulta.visao
        termos = visaoConsulta.split()
        for termo in termos:
            f = inds.frequencia(termo, termos)
            idf = ts.getIdf(termo)
            termoConsulta = TermoConsulta(termo, f, idf)
            consulta.termosConsulta.append(termoConsulta)

    def processarListasInvertidas(self, consulta):
        termosConsulta = consulta.termosConsulta
        for termoConsulta in termosConsulta:
            entradasIndiceInvertido = []
            entradasIndiceInvertido = iis.getEntradasIndiceInvertido(termoConsulta)
            for entradaIndiceInvertido in entradasIndiceInvertido:
                entradaRanking = EntradaRanking('', [], 0.0, 0.0)
                entradaRanking = self.mergeListasInvertidas.get(entradaIndiceInvertido.documento.url)
                if entradaRanking is not None:
                    entradaRanking.produtoPesos.append(termoConsulta.peso * entradaIndiceInvertido.peso)
                else:
                    entradaRanking = EntradaRanking('', [], 0.0, 0.0)
                    entradaRanking.url = entradaIndiceInvertido.documento.url
                    entradaRanking.produtoPesos.append(termoConsulta.peso * entradaIndiceInvertido.peso)
                    entradaRanking.somaQuadradosPesosDocumento = entradaIndiceInvertido.documento.somaQuadradosPesos
                    entradaRanking.somaQuadradosPesosConsulta = consulta.getSomaQuadradosPesos()
                    self.mergeListasInvertidas[entradaIndiceInvertido.documento.url] = entradaRanking



    def computarRankingSimilaridade(self):
        for k, v in self.mergeListasInvertidas.items():
            v.computarSimilaridade()

    def getRanking(self):
        resp = []
        for k, v in self.mergeListasInvertidas.items():
            resp.append(v)
        return self.ordenarRanking(resp)

    def ordenarRanking(self, rankingList):
        return sorted(rankingList, key=lambda x: x.similaridade, reverse=True)

    def getRankingSemiNormalizado(self):
        rankings = self.getRanking()
        retorno = []
        for ranking in rankings:
            novo = EntradaRanking('', [], 0.0, 0.0)
            novo = ranking.clone()
            novo.computarSimilaridadeSemiNormalizada()
            retorno.append(novo)
        return retorno

    def ranking(self, tipo):
        if int(tipo) == 1:
            return self.getRanking()
        if int(tipo) == 2:
            return self.getRankingSemiNormalizado()
        return []
