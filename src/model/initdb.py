#for use virtualenv/virtualenvwrapper
#mkvirtualenv <name>
#workon <name>
#disable
#
#$pip install venv 
#$source /bin/activate
#$deactivate
#
#$pip install Flask flask_sqlalchemy mysql-connector-python pymysql robotparser
#For install dialect

import base64

import math
from flask_login import UserMixin
from sqlalchemy.dialects import mysql
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#For use sqlite
sqlite = 'sqlite:///F:\\test.db'
localhost = 'mysql+pymysql://root:roota1b2c3@localhost:3306/maquinadebuscaPython'
maquinadebuscapy = 'mysql+pymysql://root1a2b3c:root1a2b3c@85.10.205.173:3306/maquinadebuscapy'
maquinapython = 'mysql+pymysql://maquinapython:rootroot@85.10.205.173:3306/maquinapython'
pythonmaquina = 'mysql+pymysql://pythonmaquina:rootroot@85.10.205.173:3306/pythonmaquina'
app.config['SQLALCHEMY_DATABASE_URI'] = maquinadebuscapy
db = SQLAlchemy(app)



class Documento(db.Model):
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
        documento['texto'] = base64.b64decode(self.texto[2:])
        documento['url'] = self.url
        documento['visao'] = self.visao
        # print(repr(documento))
        return documento

    def dictToDocumento(self, udict):
        self.id = udict.get("id")
        self.frequenciaMaxima = udict.get("frequenciaMaxima")
        self.somaQuadradosPesos = udict.get("somaQuadradosPesos")
        self.texto = udict.get("texto")
        self.url = udict.get("url")
        self.visao = udict.get("visao")

    def adicionarPeso(self, peso):
        self.somaQuadradosPesos = float(self.somaQuadradosPesos) + math.sqrt(peso)

    def __repr__(self):
        return '<Documento %r>' % self.url


class Host(db.Model):
    __tablename__ = 'Host'
    id = Column(mysql.BIGINT, primary_key=True)
    count = Column(mysql.BIGINT)
    url = Column(mysql.VARCHAR(255), unique=True)

    def hostToJson(self):
        host = {}
        host['id'] = self.id
        host['count'] = self.count
        host['url'] = self.url
        # print(repr(host))
        return host

    def dictToHost(self, udict):
        self.id = udict.get("id")
        self.count = udict.get("count")
        self.url = udict.get("url")

    def __repr__(self):
        return '<Host %r>' % self.url


class TermoDocumento(db.Model):
    __tablename__ = 'TermoDocumento'
    id = Column(mysql.BIGINT, primary_key=True)
    n = Column(mysql.BIGINT)
    texto = Column(mysql.LONGTEXT)

    def termoDocumentoToJson(self):
        termoDocumento = {}
        termoDocumento['id'] = self.id
        termoDocumento['n'] = self.n
        termoDocumento['texto'] = self.texto
        # print(repr(termoDocumento))
        return termoDocumento

    def dictToTermoDocumento(self, udict):
        self.id = udict.get("id")
        self.n = udict.get("n")
        self.texto = udict.get("texto")

    def __repr__(self):
        return '<TermoDocumento %r>' % self.texto


class Link(db.Model):
    __tablename__ = 'Link'
    id = Column(mysql.BIGINT, primary_key=True)
    ultimaColeta = Column(mysql.DATETIME)
    url = Column(mysql.VARCHAR(255), unique=True)
    host_id = Column(mysql.BIGINT, ForeignKey('Host.id'))
    host = relationship(Host)


    def __repr__(self):
        return '<Link %r>' % self.url


class DocumentoLink(db.Model):
    __tablename__ = 'documento_link'
    id = Column(mysql.BIGINT, primary_key=True)
    documento_id = Column('documento_id', mysql.BIGINT, ForeignKey('Documento.id'))
    documento = relationship(Documento)
    link_id = Column('link_id', mysql.BIGINT, ForeignKey('Link.id'))
    link = relationship(Link)

    def documentoLinkToJson(self):
        documentoLink = {}
        documentoLink['id'] = self.id
        documentoLink['documento_id'] = self.documento_id
        documentoLink['documento'] = self.documento.documentoToJson()
        documentoLink['link_id'] = self.link_id
        documentoLink['link'] = self.link.linkToJson()
        # print(repr(documentoLink))
        return documentoLink

    def dictToDocumento(self, udict):
        self.id = udict.get("id")
        self.documento_id = udict.get("documento_id")
        self.link_id = udict.get("link_id")

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

    def indiceInvertidoToJson(self):
        indiceInvertido = {}
        indiceInvertido['id'] = self.id
        indiceInvertido['documento_id'] = self.documento_id
        indiceInvertido['documento'] = self.documento.documentoToJson()
        indiceInvertido['termo_id'] = self.termo_id
        indiceInvertido['termo'] = self.termo.termoDocumentoToJson()
        indiceInvertido['frequencia'] = self.frequencia
        indiceInvertido['peso'] = self.peso
        # print(repr(indiceInvertido))
        return indiceInvertido

    def dictToIndiceInvertido(self, udict):
        self.id = udict.get("id")
        self.documento_id = udict.get("documento_id")
        self.termo_id = udict.get("termo_id")
        self.frequencia = udict.get("frequencia")
        self.peso = udict.get("peso")

    def __repr__(self):
        return '<IndiceInvertido %r>' % self.peso


# Define the Role data-model
class Role(db.Model):
    __tablename__ = 'roles'
    id = Column(mysql.INTEGER, primary_key=True)
    name = Column(mysql.VARCHAR(50), unique=True)

# Define User data-model
class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = Column(mysql.INTEGER, primary_key=True)
    email = Column(mysql.VARCHAR(255), nullable=False, unique=True)
    email_confirmed_at = Column(mysql.DATETIME)
    username = Column(mysql.VARCHAR(50), nullable=False, unique=True)
    password = Column(mysql.VARCHAR(255), nullable=False)
    first_name = Column(mysql.VARCHAR(50), nullable=False)
    last_name = Column(mysql.VARCHAR(50), nullable=False)
    roles = relationship('Role', secondary='user_roles')

    def userToJson(self):
        users = {}
        users['id'] = self.id
        users['email'] = self.email
        users['email_confirmed_at'] = self.email_confirmed_at
        users['username'] = self.username
        users['password'] = self.password
        users['first_name'] = self.first_name
        users['last_name'] = self.last_name
        users['roles'] = self.roles.authoritiesToJson()
        return users

    def dictToUser(self, udict):
        self.id = udict.get("id")
        self.email = udict.get("email")
        self.username = udict.get("username")
        self.password = udict.get("password")
        self.email_confirmed_at = udict.get("email_confirmed_at")
        self.first_name = udict.get("first_name")
        self.last_name = udict.get("last_name")

    def __repr__(self):
        return '<Users %r>' % self.username


# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = Column(mysql.INTEGER, primary_key=True)
    user_id = Column(mysql.INTEGER, ForeignKey('users.id', ondelete='CASCADE'))
    role_id = Column(mysql.INTEGER, ForeignKey('roles.id', ondelete='CASCADE'))


#for create
#from api import db
#db.create_all()


#for use
#$python
#>>>from api import Link
#>>>Link.query.all()



#erro pip
#
#$ mkdir ~/.pip 
#$ vim ~/.pip/pip.conf
#----------------------------------
#[global]
#index-url = http://mirrors.aliyun.com/pypi/simple/
#[install]
#trusted-host = mirrors.aliyun.com
#----------------------------------


#$ python -m pip install --trusted-host pypi.python.org --trusted-host files.pythonhosted.org --trusted-host pypi.org --upgrade pip









