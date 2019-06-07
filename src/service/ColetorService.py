import requests
from bs4 import BeautifulSoup
from src.service.DocumentoService import DocumentoService
from src.service.LinkService import LinkService
from src.service.HostService import HostService
from src.service.UtilsService import UtilsService
from src.service.RobotsService import RobotsService
from src.service.StopwordService import StopwordsService


ds = DocumentoService()
ls = LinkService()
hs = HostService()
us = UtilsService()
robotsService = RobotsService()
stopwordsService = StopwordsService()



class ColetorService:
    urlStringAnterior = None
    sementes = []

    def executar(self):
        documentos = []
        try:
            self.sementes = ls.obterLinksNaoColetados()
            while self.sementes.count() > 0:
                us.verificaColetaConsecultiva(self.urlStringAnterior, self.sementes[0])
                if robotsService.verificaPermissaoRobots(self.sementes[0]):
                    documentos.append(self.coletar(self.sementes[0]))
                else:
                    self.sementes.pop()
                print(self.sementes.count()+" Sementes restantes.")
        except Exception:
            print("Erro ao executar o serviço de coleta!")
        return documentos

    def coletar(self, url):
        documento = None
        print('Iniciando coleta url: ['+url+"]")
        try:
            requisicao = requests.get(url)
            print("Código HTTP de resposta: " + str(requisicao.status_code))
            pagina = requisicao.text
            soup = BeautifulSoup(pagina)
            urls = us.obterLinks(soup)

            documento = loadOrNewDoc(url)

            #TODO
            txt = soup.get_text()
        except Exception:
            print("Erro ao coletar a página!")
        finally:
            self.urlStringAnterior = self.sementes.pop()
            self.sementes = ls.obterLinksNaoColetados()
            self.sementes = us.removeElementosRepetidos(self.sementes)

        return documento

    #TODO
    def loadOrNewDoc(url):
        pass

