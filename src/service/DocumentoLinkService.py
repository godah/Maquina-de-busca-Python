from src.model.models import DocumentoLink
from src.service.database import db_session

class DocumentoLinkService:

    def listAll(self):
        return DocumentoLink.query.all()

    def findById(self, id):
        return DocumentoLink.query.filter_by(id=id).first()

    def remove(self, obj):
        try:
            db_session.delete(obj)
            db_session.commit()
            return obj
        except Exception:
            db_session.rollback()
            return obj

    def save(self, obj):
        try:
            db_session.add(obj)
            db_session.commit()
            return obj
        except Exception:
            db_session.rollback()
            return obj

    def update(self, obj):
        try:
            db_session.merge(obj)
            db_session.commit()
            return obj
        except Exception:
            db_session.rollback()
            return obj

    def findByDocId(self, id):
        return DocumentoLink.query.filter_by(documento_id=id).all()

    def findByLinkId(self, id):
        return DocumentoLink.query.filter_by(link_id=id).all()

    def inserirDocumentoLink(self, documento, link):
        documentoLink = DocumentoLink()
        documentoLink.documento = documento
        documentoLink.documento_id = documento.id
        documentoLink.link = link
        documentoLink.link_id = link.id
        documentoLink = self.save(documentoLink)
        return documentoLink

