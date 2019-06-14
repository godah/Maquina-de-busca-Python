from sqlalchemy import text
from src.model.models import Link, Host
from src.service.database import db_session
from src.service.HostService import HostService
from src.service.DocumentoLinkService import DocumentoLinkService

hs = HostService()
dls = DocumentoLinkService()

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
        return Link.query.order_by(Link.url).all().paginate(1, 15, error_out=False)

    def buscarPagina(self, pageFlag):
        return Link.query.order_by(Link.url).all().paginate(int(pageFlag), 15, error_out=False)

    def obterLinksPorIntervaloDeIdentificacao(self, id1, id2):
        sql = ' SELECT l.* FROM Link l WHERE l.id BETWEEN :id1 AND :id2 '
        return db_session.query(Link).from_statement(text(sql)).params(id1=id1, id2=id2).all()

    def contarLinksPorIntervaloDeIdentificacao(self, id1, id2):
        sql = ' SELECT COUNT(l.id) FROM Link l WHERE l.id BETWEEN :id1 AND :id2 '
        return db_session.query(Link).from_statement(text(sql)).params(id1=id1, id2=id2).all()

    def encontrarSementePorHost(self, link):
        sql = ' SELECT l.* FROM Link l WHERE l.url LIKE "%:link%" AND l.ultimaColeta IS NULL '
        return db_session.query(Link).from_statement(text(sql)).params(link=link).all()

    def encontrarSementesPorIntervaloDatas(self, dt1, dt2):
        sql = ' SELECT l.* FROM Link l WHERE l.id BETWEEN :dt1 AND :dt2 AND l.ultimaColeta IS NULL '
        return db_session.query(Link).from_statement(text(sql)).params(dt1=dt1, dt2=dt2).all()

    def atualizaDataUltimaColeta(self, host, data):
        sql = ' UPDATE Link l SET l.ultimaColeta = :data WHERE l.url LIKE CONCAT ('%',:host,'%') '
        db_session.query(Link).from_statement(text(sql)).params(host=host, data=data)
        return self.findByUrl(host)

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
    