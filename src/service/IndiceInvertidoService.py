from sqlalchemy import text

from src.model.models import IndiceInvertido
from src.service.database import db_session

class IndiceInvertidoService:

    def listAll(self):
        return IndiceInvertido.query.all()

    def findById(self, id):
        return IndiceInvertido.query.filter_by(id=id).first()

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

    def deleteAllNativeQuery(self):
        try:
            IndiceInvertido.query.delete()
            db_session.commit()
        except Exception:
            db_session.rollback()

    def inserirEntradaIndiceInvertido(self, termo, documento, f, peso):
        iv = IndiceInvertido()
        iv.documento = documento
        iv.documento_id = documento.id
        iv.frequencia = f
        iv.termo = termo
        iv.termo_id = termo.id
        iv.peso = peso
        self.save(iv)