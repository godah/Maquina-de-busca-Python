from src.model.models import Users
from src.service.database import db_session

class UserService:

    def listAll(self):
        return Users.query.all()

    def findById(self, id):
        return Users.query.filter_by(id=id).first()

    def remove(self, user):
        try:
            ret = db_session.delete(user)
            db_session.commit()
            return ret
        except Exception:
            db_session.rollback()
            return 'fail'


    def save(self, user):
        try:
            u = db_session.add(user)
            db_session.commit()
            return u
        except Exception:
            db_session.rollback()
            return 'fail'

    def findByUsername(self, username):
        return Users.query.filter_by(username=username).first()