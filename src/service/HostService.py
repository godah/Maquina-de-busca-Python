from src.model.models import Host, Link, DocumentoLink
from src.service.database import db_session
from urllib.parse import urlparse

class HostService:

    def listAll(self):
        return Host.query.all()

    def findById(self, id):
        return Host.query.filter_by(id=id).first()

    def remove(self, obj):
        try:
            links = Link.query.filter_by(host_id=obj.id).all()
            for link in links:
                doclinks = DocumentoLink.query.filter_by(link_id=link.id).all()
                for doclink in doclinks:
                    db_session.delete(doclink)
                db_session.delete(link)
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
            return obj

    def update(self, obj):
        try:
            db_session.merge(obj)
            db_session.commit()
            return obj
        except Exception:
            db_session.rollback()
            return 'fail'

    def findByUrl(self, url):
        return Host.query.filter_by(url=url).first()

    def findByUrlLike(self, url):
        return Host.query.filter(Host.url.like("%"+url+"%")).all()

    def listarEmOrdemAlfabetica(self):
        return Host.query.order_by(Host.url).all()

    def createUpdateHost(self, url):
        host = Host()
        uri = urlparse(url)
        h = uri.scheme + "://" + uri.netloc
        host = self.findByUrl(h)
        if host is None:
            host = Host()
            host.url = h
            host.count = 1
            host = self.save(host)
        else:
            host.count += 1
            host = self.update(host)
        return host