from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import mysql
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root1a2b3c:root1a2b3c@85.10.205.173:3306/maquinadebuscapy'
db = SQLAlchemy(app)

class Documento(db.Model):
    __tablename__ = 'Documento'
    id = Column(mysql.BIGINT, primary_key=True)
    frequenciaMaxima = Column(mysql.DOUBLE)
    somaQuadradosPesos = Column(mysql.DOUBLE)
    texto = Column(mysql.LONGTEXT)
    url = Column(mysql.VARCHAR(255))
    visao = Column(mysql.LONGTEXT)

    def __repr__(self):
        return '<Documento %r>' % self.url

class Host(db.Model):
    __tablename__ = 'Host'
    id = Column(mysql.BIGINT, primary_key=True)
    count = Column(mysql.BIGINT)
    url = Column(mysql.VARCHAR(255), unique=True)
    
    def __repr__(self):
        return '<Host %r>' % self.url


class TermoDocumento(db.Model):
    __tablename__ = 'TermoDocumento'
    id = Column(mysql.BIGINT, primary_key=True)
    n = Column(mysql.BIGINT)
    texto = Column(mysql.LONGTEXT)

    def __repr__(self):
        return '<TermoDocumento %r>' % self.texto


class DocumentoLink(db.Model):
    __tablename__ = 'documento_link'
    id = Column(mysql.BIGINT, primary_key=True)
    documumento_id = Column(mysql.BIGINT, ForeignKey('Documento.id'))
    documento = relationship(Documento)
    link_id = Column(mysql.BIGINT, ForeignKey('Link.id'))
    link = relationship(Link)

    def __repr__(self):
        return '<documento_link %r>' % self.id


class IndiceInvertido(db.Model):
    __tablename__ = 'IndiceInvertido'
    id = Column(mysql.BIGINT, primary_key=True)
    documento_id = Column(mysql.BIGINT, ForeignKey('Documento.id'))
    documento = relationship(Documento)
    termo_id = Column(mysql.BIGINT, ForeignKey('TermoDocumento.id'))
    termo = relationship(TermoDocumento)
    frequencia = Column(mysql.INTEGER)
    peso = Column(mysql.DOUBLE)

    def __repr__(self):
        return '<IndiceInvertido %r>' % self.peso


class Link(db.Model):
    __tablename__ = 'Link'
    id = Column(mysql.BIGINT, primary_key=True)
    ultimaColeta = Column(mysql.DATETIME)
    url = Column(mysql.VARCHAR(255), unique=True)
    host_id = Column(mysql.BIGINT, ForeignKey('Host.id'))
    host = relationship(Host)
    
    def __repr__(self):
        return '<Link %r>' % self.url

class Authorities(db.Model):
    __tablename__ = 'authorities'
    id = Column(mysql.BIGINT, primary_key=True)
    authority = Column(mysql.VARCHAR(255))
    username = Column(mysql.VARCHAR(255), unique=True)

class Users(db.Model):
    __tablename__ = "users"
    id = Column(mysql.BIGINT, primary_key=True)
    email = Column(mysql.VARCHAR(255))
    enabled = Column(mysql.BOOLEAN)    
    username = Column(mysql.VARCHAR(255))
    password = Column(mysql.VARCHAR(255))
    authorities_id = Column(mysql.BIGINT, ForeignKey('authorities.id'))
    authorities = relationship(Authorities)

    def __repr__(self):
        return '<Users %r>' % self.username