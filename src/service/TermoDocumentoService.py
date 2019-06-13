import math
from sqlalchemy import text

from src.model.models import TermoDocumento, Documento
from src.service.database import db_session

class TermoDocumentoService:

    def listAll(self):
        return TermoDocumento.query.all()

    def findById(self, id):
        return TermoDocumento.query.filter_by(id=id).first()

    def remove(self, obj):
        try:
            db_session.delete(obj)
            db_session.commit()
            return obj
        except Exception:
            db_session.rollback()
            return 'fail'

    def save(self, obj):
        try:
            db_session.add(obj)
            db_session.commit()
            return obj
        except Exception:
            db_session.rollback()
            return 'fail'

    def update(self, obj):
        try:
            db_session.merge(obj)
            db_session.commit()
            return obj
        except Exception:
            db_session.rollback()
            return 'fail'

    def findByUrl(self, url):
        return TermoDocumento.query.filter_by(url=url).first()

    def deleteAllNativeQuery(self):
        try:
            TermoDocumento.query.delete()
            db_session.commit()
        except Exception:
            db_session.rollback()

    def getIdf(self, texto):
        N = len(Documento.query.all())
        termoDocumento = TermoDocumento.query.filter_by(texto=texto).first()
        if termoDocumento is None:
            return 0.0
        n = termoDocumento.n
        return self.calcularIdf(N, n)

    def findByTermo(self, termo):
        sql = " select * from TermoDocumento where lower(texto) = lower(:termo) "
        return db_session.query(TermoDocumento).from_statement(text(sql)).params(termo=termo).first()

    def log(self, x, base):
        a = math.log(x)
        b = math.log(base)
        if a == 0 or b == 0:
            return 0
        return a/b

    def calcularIdf(self, N, n):
        if N == 0 or n == 0:
            return 0
        return self.log((N / n), 2)