from sqlalchemy import text

from src.model.models import Link
from src.service.database import db_session

class LinkService:

    def listAll(self):
        return Link.query.all()

    def findById(self, id):
        return Link.query.filter_by(id=id).first()

    def remove(self, obj):
        try:
            ret = db_session.delete(obj)
            db_session.commit()
            return ret
        except Exception:
            db_session.rollback()
            return 'fail'

    def save(self, obj):
        try:
            u = db_session.add(obj)
            db_session.commit()
            return u
        except Exception:
            db_session.rollback()
            return 'fail'

    def update(self, obj):
        try:
            u = db_session.merge(obj)
            db_session.commit()
            return u
        except Exception:
            db_session.rollback()
            return 'fail'

    def findByUrl(self, url):
        return Link.query.filter_by(url=url).first()

    def listarEmOrdemAlfabetica(self):
        return Link.query.order_by(Link.url).all()

    def obterLinksNaoColetados(self):
        sql = ' SELECT l FROM Link l WHERE l.ultimaColeta IS NULL '
        return db_session.query(Link).from_statement(text(sql)).all()

    def listarPagina(self):
        return Link.query.order_by(Link.url).all().paginate(1, 15, error_out=False)

    def buscarPagina(self, pageFlag):
        return Link.query.order_by(Link.url).all().paginate(int(pageFlag), 15, error_out=False)

    def obterLinksPorIntervaloDeIdentificacao(self, id1, id2):
        sql = ' SELECT l FROM Link l WHERE l.id BETWEEN :id1 AND :id2 '
        return db_session.query(Link).from_statement(text(sql)).params(id1=id1, id2=id2).all()

    def contarLinksPorIntervaloDeIdentificacao(self, id1, id2):
        sql = ' SELECT COUNT(l.id) FROM Link l WHERE l.id BETWEEN :id1 AND :id2 '
        return db_session.query(Link).from_statement(text(sql)).params(id1=id1, id2=id2).all()

    def encontrarSementePorHost(self, link):
        sql = ' SELECT l FROM Link l WHERE l.url LIKE "%:link%" AND l.ultimaColeta IS NULL '
        return db_session.query(Link).from_statement(text(sql)).params(link=link).all()

    def encontrarSementesPorIntervaloDatas(self, dt1, dt2):
        sql = ' SELECT l FROM Link l WHERE l.id BETWEEN :dt1 AND :dt2 AND l.ultimaColeta IS NULL '
        return db_session.query(Link).from_statement(text(sql)).params(dt1=dt1, dt2=dt2).all()

    def atualizaDataUltimaColeta(self, host, data):
        sql = ' UPDATE Link l SET l.ultimaColeta = :data WHERE l.url LIKE CONCAT ('%',:host,'%') '
        return db_session.query(Link).from_statement(text(sql)).params(host=host, data=data)