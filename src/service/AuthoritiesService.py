from src.model.models import Authorities
from src.service.database import db_session

class AuthoritiesService:

    def listAll(self):
        return Authorities.query.all()

    def findById(self, id):
        return Authorities.query.filter_by(id=id).first()

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
