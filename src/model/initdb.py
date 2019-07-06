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
host = 'mysql+pymysql://<usuario>:<senha>@<ip_host>:3306/<database>'
app.config['SQLALCHEMY_DATABASE_URI'] = sqlite
db = SQLAlchemy(app)


class Documento(db.Model):
    __tablename__ = 'Documento'
    id = Column(mysql.BIGINT, primary_key=True)
    frequenciaMaxima = Column(mysql.DOUBLE)
    somaQuadradosPesos = Column(mysql.DOUBLE)
    texto = Column(mysql.LONGTEXT)
    url = Column(mysql.VARCHAR(255))
    visao = Column(mysql.LONGTEXT)


class Host(db.Model):
    __tablename__ = 'Host'
    id = Column(mysql.BIGINT, primary_key=True)
    count = Column(mysql.BIGINT)
    url = Column(mysql.VARCHAR(255), unique=True)


class TermoDocumento(db.Model):
    __tablename__ = 'TermoDocumento'
    id = Column(mysql.BIGINT, primary_key=True)
    n = Column(mysql.BIGINT)
    texto = Column(mysql.LONGTEXT)


class Link(db.Model):
    __tablename__ = 'Link'
    id = Column(mysql.BIGINT, primary_key=True)
    ultimaColeta = Column(mysql.DATETIME)
    url = Column(mysql.VARCHAR(255), unique=True)
    host_id = Column(mysql.BIGINT, ForeignKey('Host.id'))
    host = relationship(Host)


class DocumentoLink(db.Model):
    __tablename__ = 'documento_link'
    id = Column(mysql.BIGINT, primary_key=True)
    documento_id = Column('documento_id',mysql.BIGINT, ForeignKey('Documento.id'))
    documento = relationship(Documento)
    link_id = Column('link_id',mysql.BIGINT, ForeignKey('Link.id'))
    link = relationship(Link)


class IndiceInvertido(db.Model):
    __tablename__ = 'IndiceInvertido'
    id = Column(mysql.BIGINT, primary_key=True)
    documento_id = Column(mysql.BIGINT, ForeignKey('Documento.id'))
    documento = relationship(Documento)
    termo_id = Column(mysql.BIGINT, ForeignKey('TermoDocumento.id'))
    termo = relationship(TermoDocumento)
    frequencia = Column(mysql.INTEGER)
    peso = Column(mysql.DOUBLE)


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


# Define the UserRoles association table
class UserRoles(db.Model):
    __tablename__ = 'user_roles'
    id = Column(mysql.INTEGER, primary_key=True)
    user_id = Column(mysql.INTEGER, ForeignKey('users.id', ondelete='CASCADE'))
    role_id = Column(mysql.INTEGER, ForeignKey('roles.id', ondelete='CASCADE'))


#Para criar as tabelas
#Execute no console do Python os comandos abaixo no diretório deste arquivo
#from api import db
#db.create_all()


#para testar uma query
#$python
#>>>from api import Link
#>>>Link.query.all()
