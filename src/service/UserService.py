from src.model.models import Users
from src.service.database import db_session

class UserService:

    def listAll(self):
        return Users.query.all()

    def findById(self, ident):
        return Users.query.filter_by(id=ident).first()

    def remove(self, obj):
        try:
            db_session.delete(obj)
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

    def findByUsername(self, username):
        users = Users.query.filter(Users.username.like("%"+username+"%")).all()
        usersretorno = []
        for user in users:
            usersretorno.append(user.userToJson())
        return usersretorno


    def listaradmin(self):
        try:
            adminsResp = []
            admins = Users.query.filter_by(authorities_id=1)
            for admin in admins:
                adminsResp.append(admin.userToJson())
            return adminsResp
        except Exception:
            return 'fail'

    def listaradminid(self, ident):
        try:
            admin = Users.query.filter_by(authorities_id=1, id=ident).first()
            return admin.userToJson()
        except Exception:
            return 'fail'

    def listarusuarios(self):
        try:
            usuariosResp = []
            usuarios = Users.query.filter_by(authorities_id=2)
            for usuario in usuarios:
                usuariosResp.append(usuario.userToJson())
            return usuariosResp
        except Exception:
            return 'fail'

    def listarusuarioid(self, ident):
        try:
            usuario = Users.query.filter_by(authorities_id=2, id=ident).first()
            return usuario.userToJson()
        except Exception:
            return 'fail'

    def inserirusuario(self, obj):
        try:
            if(obj.authorities_id != 1):
                db_session.add(obj)
                db_session.commit()
                return obj
            raise Exception('Não permitido')
        except Exception:
            db_session.rollback()
            return

    def save(self, obj):
        try:
            db_session.add(obj)
            db_session.commit()
            return obj
        except Exception:
            db_session.rollback()
            return 'fail'
