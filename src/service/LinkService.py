from paginator import Paginator
from sqlalchemy import text
from src.model.models import Link, Host
from src.service.database import db_session
from src.service.HostService import HostService
from src.service.DocumentoLinkService import DocumentoLinkService
from src.service.UtilsService import UtilsService

hs = HostService()
dls = DocumentoLinkService()
utilsService = UtilsService()

class LinkService:

    def listAll(self):
        return Link.query.all()

    def findById(self, id):
        return Link.query.filter_by(id=id).first()

    def remove(self, obj):
        try:
            documentoLinks = dls.findByLinkId(obj.id)
            for dl in documentoLinks:
                dls.remove(dl)
            db_session.delete(obj)
            db_session.commit()
            return obj
        except Exception:
            db_session.rollback()
            return obj

    def save(self, obj):
        try:
            db_session.add(obj)
            db_session.commit()
            return obj
        except Exception:
            db_session.rollback()
            return obj

    def update(self, obj):
        try:
            db_session.merge(obj)
            db_session.commit()
            return self.findById(obj.id)
        except Exception:
            db_session.rollback()
            return obj

    def findByUrl(self, url):
        return Link.query.filter_by(url=url).first()

    def findByUrlLike(self, key):
        return Link.query.filter(Link.url.like("%"+key+"%")).all()

    def listarEmOrdemAlfabetica(self):
        return Link.query.order_by(Link.url).all()

    def obterLinksNaoColetados(self):
        sql = ' SELECT l.* FROM Link l WHERE l.ultimaColeta IS NULL '
        return db_session.query(Link).from_statement(text(sql)).all()

    def listarPagina(self):
        links = Link.query.order_by(Link.url).all()
        if len(links) == 0:
            return []
        paginator = self.paginator(links, 15)
        return paginator


    def buscarPagina(self, pageFlag):
        links = Link.query.order_by(Link.url).all()
        if len(links) == 0:
            return []
        paginator = self.paginator(links, 15)
        links =[]
        if len(paginator) < int(pageFlag):
            return []
        page = paginator[int(pageFlag)]
        for link in page:
            links.append(link)
        return links

    def paginator(self, links, per_page):
        i = 1
        paginator = []
        subLista = []
        for link in links:
            subLista.append(link)
            if i == per_page:
                paginator.append(subLista)
                subLista = []
                i = 0
            i = i+1
        return  paginator

    def obterLinksPorIntervaloDeIdentificacao(self, id1, id2):
        sql = ' SELECT l.* FROM Link l WHERE l.id BETWEEN :id1 AND :id2 '
        return db_session.query(Link).from_statement(text(sql)).params(id1=id1, id2=id2).all()

    def contarLinksPorIntervaloDeIdentificacao(self, id1, id2):
        sql = ' SELECT COUNT(l.id) FROM Link l WHERE l.id BETWEEN :id1 AND :id2 '
        return len(self.obterLinksPorIntervaloDeIdentificacao(id1, id2))

    def encontrarSementePorHost(self, link):
        sql = ' SELECT l.* FROM Link l WHERE l.url LIKE "%'+link+'%" AND l.ultimaColeta IS NULL '
        return db_session.query(Link).from_statement(text(sql)).all()

    def encontrarSementesPorIntervaloDatas(self, dateIso1, dateIso2):
        sql = ' SELECT l.* FROM Link l WHERE l.ultimaColeta BETWEEN :dt1 AND :dt2 '
        date1 = utilsService.isoToDate(dateIso1)
        date2 = utilsService.isoToDate(dateIso2)
        return db_session.query(Link).from_statement(text(sql)).params(dt1=date1, dt2=date2).all()

    def atualizaDataUltimaColeta(self, host, dataIso):
        sql = ' UPDATE Link l SET l.ultimaColeta = :data WHERE l.url LIKE (%'+host+'%) '
        data = utilsService.isoToDate(dataIso)
        db_session.query(Link).from_statement(text(sql)).params(data=data)
        return len(self.findByUrlLike(host))

    def inserirSemente(self, url):
        link = Link()
        linkOld = Link()
        linkOld = self.findByUrl(url)
        if linkOld is None:
            host = Host()
            host = hs.createUpdateHost(url)
            link.host_id = host.id
            link.host = host
            link.url = url
            link = self.save(link)
        else:
            link = linkOld
        return link
    