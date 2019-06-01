from sqlalchemy.dialects import mysql
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship
from src.service.database import Base


class Documento(Base):
    __tablename__ = 'Documento'
    id = Column(mysql.BIGINT, primary_key=True)
    frequenciaMaxima = Column(mysql.DOUBLE)
    somaQuadradosPesos = Column(mysql.DOUBLE)
    texto = Column(mysql.LONGTEXT)
    url = Column(mysql.VARCHAR(255))
    visao = Column(mysql.LONGTEXT)

    def documentoToJson(self):
        documento = {}
        documento['id'] = self.id
        documento['frequenciaMaxima'] = self.frequenciaMaxima
        documento['somaQuadradosPesos'] = self.somaQuadradosPesos
        documento['texto'] = self.texto
        documento['url'] = self.url
        documento['visao'] = self.visao
        return documento

    def __repr__(self):
        return '<Documento %r>' % self.url


class Host(Base):
    __tablename__ = 'Host'
    id = Column(mysql.BIGINT, primary_key=True)
    count = Column(mysql.BIGINT)
    url = Column(mysql.VARCHAR(255), unique=True)

    def hostToJson(self):
        host = {}
        host['id'] = self.id
        host['count'] = self.count
        host['url'] = self.url
        return host

    def __repr__(self):
        return '<Host %r>' % self.url


class TermoDocumento(Base):
    __tablename__ = 'TermoDocumento'
    id = Column(mysql.BIGINT, primary_key=True)
    n = Column(mysql.BIGINT)
    texto = Column(mysql.LONGTEXT)

    def termoDocumentoToJson(self):
        termoDocumento = {}
        termoDocumento['id'] = self.id
        termoDocumento['n'] = self.n
        termoDocumento['texto'] = self.texto
        return termoDocumento

    def __repr__(self):
        return '<TermoDocumento %r>' % self.texto


class Link(Base):
    __tablename__ = 'Link'
    id = Column(mysql.BIGINT, primary_key=True)
    ultimaColeta = Column(mysql.DATETIME)
    url = Column(mysql.VARCHAR(255), unique=True)
    host_id = Column(mysql.BIGINT, ForeignKey('Host.id'))
    host = relationship(Host)

    def linkToJson(self):
        link = {}
        link['id'] = self.id
        link['ultimaColeta'] = self.ultimaColeta
        link['url'] = self.url
        link['host_id'] = self.host_id
        link['host'] = self.host
        return link

    def __repr__(self):
        return '<Link %r>' % self.url


class DocumentoLink(Base):
    __tablename__ = 'documento_link'
    id = Column(mysql.BIGINT, primary_key=True)
    documumento_id = Column(mysql.BIGINT, ForeignKey('Documento.id'))
    documento = relationship(Documento)
    link_id = Column(mysql.BIGINT, ForeignKey('Link.id'))
    link = relationship(Link)

    def documentoLinkToJson(self):
        documentoLink = {}
        documentoLink['id'] = self.id
        documentoLink['documumento_id'] = self.documumento_id
        documentoLink['documento'] = self.documento
        documentoLink['link_id'] = self.link_id
        documentoLink['link'] = self.link
        return documentoLink

    def __repr__(self):
        return '<documento_link %r>' % self.id


class IndiceInvertido(Base):
    __tablename__ = 'IndiceInvertido'
    id = Column(mysql.BIGINT, primary_key=True)
    documento_id = Column(mysql.BIGINT, ForeignKey('Documento.id'))
    documento = relationship(Documento)
    termo_id = Column(mysql.BIGINT, ForeignKey('TermoDocumento.id'))
    termo = relationship(TermoDocumento)
    frequencia = Column(mysql.INTEGER)
    peso = Column(mysql.DOUBLE)

    def indiceInvertidoToJson(self):
        indiceInvertido = {}
        indiceInvertido['id'] = self.id
        indiceInvertido['documento_id'] = self.documento_id
        indiceInvertido['documento'] = self.documento
        indiceInvertido['termo_id'] = self.termo_id
        indiceInvertido['termo'] = self.termo
        indiceInvertido['frequencia'] = self.frequencia
        indiceInvertido['peso'] = self.peso
        return indiceInvertido


    def __repr__(self):
        return '<IndiceInvertido %r>' % self.peso


class Authorities(Base):
    __tablename__ = 'authorities'
    id = Column(mysql.BIGINT, primary_key=True)
    authority = Column(mysql.VARCHAR(255))
    username = Column(mysql.VARCHAR(255), unique=True)

    def authoritiesToJson(self):
        authorities = {}
        authorities['id'] = self.id
        authorities['authority'] = self.authority
        authorities['username'] = self.username
        #print(repr(authorities))
        return authorities

    def __repr__(self):
        return '<Authorities %r>' % self.authority


class Users(Base):
    __tablename__ = "users"
    id = Column(mysql.BIGINT, primary_key=True)
    email = Column(mysql.VARCHAR(255))
    enabled = Column(mysql.BOOLEAN)    
    username = Column(mysql.VARCHAR(255))
    password = Column(mysql.VARCHAR(255))
    authorities_id = Column(mysql.BIGINT, ForeignKey('authorities.id'))
    authorities = relationship(Authorities)

    def userToJson(self):
        users = {}
        users['id'] = self.id
        users['email'] = self.email
        users['enabled'] = self.enabled
        users['username'] = self.username
        users['password'] = self.password
        users['authorities_id'] = self.authorities_id
        users['authorities'] = self.authorities.authoritiesToJson()
        #print(repr(users))
        return users

    def __repr__(self):
        return '<Users %r>' % self.username
