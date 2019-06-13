import base64
import datetime

import requests
from bs4 import BeautifulSoup

from src.model.models import Link, Documento, DocumentoLink
from src.service.DocumentoService import DocumentoService
from src.service.LinkService import LinkService
from src.service.HostService import HostService
from src.service.UtilsService import UtilsService
from src.service.RobotsService import RobotsService
from src.service.StopwordService import StopwordsService
from src.service.DocumentoLinkService import DocumentoLinkService


ds = DocumentoService()
ls = LinkService()
dls = DocumentoLinkService()
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
            while len(self.sementes) > 0:
                try:
                    us.verificaColetaConsecultiva(self.urlStringAnterior, self.sementes[0].url)
                    if robotsService.verificaPermissaoRobots(self.sementes[0].url):
                        documentos.append(self.coletar(self.sementes[0].url))
                except Exception:
                    print('falha a coletar: '+self.sementes[0].url)
                    ls.remove(self.sementes[0])
                finally:
                    del self.sementes[0]
                print(str(len(self.sementes))+" Sementes restantes.")
        except Exception:
            print("Erro ao executar o serviço de coleta!")
        return documentos

    def coletar(self, url):
        documento = None
        print('Iniciando coleta url: ['+url+"]")
        try:
            documento = Documento()
            requisicao = requests.get(url, verify=True, timeout=5)
            print("Código HTTP de resposta: " + str(requisicao.status_code))
            pagina = requisicao.text
            soup = BeautifulSoup(pagina)
            urls = us.obterLinks(soup)

            documento = self.loadOrNewDoc(url, soup, pagina)

            self.trataLinksColetados(url, documento, urls)

            ds.update(documento)
        except Exception:
            ls.atualizaDataUltimaColeta(url, datetime.datetime.now())
            print("Erro ao coletar a página!")
        finally:
            self.urlStringAnterior = self.sementes[0]
            self.sementes = ls.obterLinksNaoColetados()
            self.sementes = us.removeLinksRepetidos(self.sementes)
        return documento


    def loadOrNewDoc(self, url, soup, pagina):
        docold = ds.findByUrl(url)
        if(docold is not None):
            documento = docold
            data = base64.b64encode(pagina.encode())
            documento.texto = str(data)
            documento.visao = stopwordsService.tratarVisao(soup)
            self.loadOrNewLink(url, documento)
            ds.update(documento)
        else:
            documentoLink = DocumentoLink()
            documento = Documento()
            documento.url = url
            data = base64.b64encode(pagina.encode())
            documento.texto = str(data)
            documento.visao = stopwordsService.tratarVisao(soup)
            documento = ds.save(documento)
            link = self.loadOrNewLink(url, documento)
            documentoLink.documento = documento
            documentoLink.documento_id = documento.id
            documentoLink.link = link
            documentoLink.link_id = link.id
            dls.save(link)

        return documento



    def loadOrNewLink(self, url, documento):
        link = ls.findByUrl(url)
        if link is None:
            link = Link()
            link.url = url
            host = hs.findByUrl(url)
            link.host = host
            link.host_id = host.id
            link.ultimaColeta = datetime.datetime.now()
            link = ls.save(link)
        else:
            link.ultimaColeta = datetime.datetime.now()
            link = ls.update(link)
        return link

    def trataLinksColetados(self, url, documento, urls):
        urls = us.removeElementosRepetidos(urls)
        for url in urls:
            if len(url) > 253:
                continue
            if url is not None and url is not '':
                link = ls.inserirSemente(url)
                dls.inserirDocumentoLink(documento, link)
        docLinkList = dls.findByDocId(documento.id)
        print('Finalizando coleta de ['+url+']')
        print('Número de links coletados: ['+str(len(urls))+']')
        print('Tamanho da lista de links: ['+str(len(docLinkList))+']')


