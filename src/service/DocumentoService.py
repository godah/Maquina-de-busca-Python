from sqlalchemy import text

from src.model.models import Documento, DocumentoLink, IndiceInvertido
from src.service.database import db_session

class DocumentoService:

    def listAll(self):
        return Documento.query.all()

    def findById(self, ident):
        return Documento.query.filter_by(id=ident).first()

    def remove(self, obj):
        try:
            doclinks = DocumentoLink.query.filter_by(documento_id=obj.id).all()
            for doc in doclinks:
                db_session.delete(doc)
            indInv = IndiceInvertido.query.filter_by(documento_id=obj.id).all()
            for ind in indInv:
                db_session.delete(ind)
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
        return Documento.query.filter_by(url=url).first()
