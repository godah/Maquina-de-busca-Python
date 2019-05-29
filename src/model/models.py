from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects import mysql

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root1a2b3c:root1a2b3c@85.10.205.173:3306/maquinadebuscapy'
db = SQLAlchemy(app)

class Documento(db.Model):
    __tablename__ = 'Documento'
    id = db.Column(mysql.BIGINT, primary_key=True)
    frequenciaMaxima = db.Column(mysql.DOUBLE)
    somaQuadradosPesos = db.Column(mysql.DOUBLE)
    texto = db.Column(mysql.LONGTEXT)
    url = db.Column(mysql.VARCHAR(255))
    visao = db.Column(mysql.LONGTEXT)

    def __repr__(self):
        return '<Documento %r>' % self.url

class Host(db.Model):
    __tablename__ = 'Host'
    id = db.Column(mysql.BIGINT, primary_key=True)
    count = db.Column(mysql.BIGINT)
    url = db.Column(mysql.VARCHAR(255), unique=True)
    
    def __repr__(self):
        return '<Host %r>' % self.url


class TermoDocumento(db.Model):
    __tablename__ = 'TermoDocumento'
    id = db.Column(mysql.BIGINT, primary_key=True)
    n = db.Column(mysql.BIGINT)
    texto = db.Column(mysql.LONGTEXT)

    def __repr__(self):
        return '<TermoDocumento %r>' % self.texto


class DocumentoLink(db.Model):
    __tablename__ = 'documento_link'
    id = db.Column(mysql.BIGINT, primary_key=True)
    documumento_id = db.Column(mysql.BIGINT, db.ForeignKey('Documento.id'))
    link_id = db.Column(mysql.BIGINT, db.ForeignKey('Link.id'))

    def __repr__(self):
        return '<documento_link %r>' % self.id


class IndiceInvertido(db.Model):
    __tablename__ = 'IndiceInvertido'
    id = db.Column(mysql.BIGINT, primary_key=True)
    documento_id = db.Column(mysql.BIGINT, db.ForeignKey('Documento.id'))
    termo_id = db.Column(mysql.BIGINT, db.ForeignKey('TermoDocumento.id'))
    frequencia = db.Column(mysql.INTEGER)
    peso = db.Column(mysql.DOUBLE)

    def __repr__(self):
        return '<IndiceInvertido %r>' % self.peso


class Link(db.Model):
    __tablename__ = 'Link'
    id = db.Column(mysql.BIGINT, primary_key=True)
    ultimaColeta = db.Column(mysql.DATETIME)
    url = db.Column(mysql.VARCHAR(255), unique=True)
    host_id = db.Column(mysql.BIGINT, db.ForeignKey('Host.id'))
    
    def __repr__(self):
        return '<Link %r>' % self.url

class Users(db.Model):
    __tablename__ = "users"
    id = db.Column(mysql.BIGINT, primary_key=True)
    email = db.Column(mysql.VARCHAR(255))
    enabled = db.Column(mysql.BOOLEAN)    
    username = db.Column(mysql.VARCHAR(255))
    password = db.Column(mysql.VARCHAR(255))
    authorities_id = db.Column(mysql.BIGINT, db.ForeignKey('authorities.id'))

    def __repr__(self):
        return '<Users %r>' % self.username

class Authorities(db.Model):
    __tablename__ = 'authorities'
    id = db.Column(mysql.BIGINT, primary_key=True)
    authority = db.Column(mysql.VARCHAR(255))
    username = db.Column(mysql.VARCHAR(255), unique=True)

##TODO ForeignKey com erros