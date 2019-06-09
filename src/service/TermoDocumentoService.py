from src.model.models import TermoDocumento
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