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