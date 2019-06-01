from src.model.models import Documento
from src.service.database import db_session

class DocumentoService:

    def listAll(self):
        return Documento.query.all()

    def findById(self, id):
        return Documento.query.filter_by(id=id).first()

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
        return Documento.query.filter_by(url=url).first()