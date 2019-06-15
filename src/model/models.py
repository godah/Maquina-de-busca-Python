import base64
import math
from flask_login import UserMixin
from sqlalchemy.dialects import mysql
from sqlalchemy import Column, ForeignKey
from sqlalchemy.orm import relationship
from src.service.database import Base
from src.service.UtilsService import UtilsService

us = UtilsService()

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
        documento['texto'] = base64.b64decode(self.texto[2:])
        documento['url'] = self.url
        documento['visao'] = self.visao
        #print(repr(documento))
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
        #print(repr(host))
        return host
    
    def dictToHost(self, udict):
        self.id = udict.get("id")
        self.count = udict.get("count")
        self.url = udict.get("url")

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
        #print(repr(termoDocumento))
        return termoDocumento
    
    def dictToTermoDocumento(self, udict):
        self.id = udict.get("id")
        self.n = udict.get("n")
        self.texto = udict.get("texto")




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
        if self.ultimaColeta is not None:
            link['ultimaColeta'] = us.dateToIso(self.ultimaColeta)
        link['url'] = self.url
        link['host_id'] = self.host_id
        #print(repr(link))
        return link

    def dictToLink(self, udict):
        self.id = udict.get("id")
        self.ultimaColeta = us.isoToDate(udict.get("ultimaColeta"))
        self.url = udict.get("url")
        self.host_id = udict.get("host_id")

    def __repr__(self):
        return '<Link %r>' % self.url


class DocumentoLink(Base):
    __tablename__ = 'documento_link'
    id = Column(mysql.BIGINT, primary_key=True)
    documento_id = Column('documento_id',mysql.BIGINT, ForeignKey('Documento.id'))
    documento = relationship(Documento)
    link_id = Column('link_id',mysql.BIGINT, ForeignKey('Link.id'))
    link = relationship(Link)

    def documentoLinkToJson(self):
        documentoLink = {}
        documentoLink['id'] = self.id
        documentoLink['documento_id'] = self.documento_id
        documentoLink['documento'] = self.documento.documentoToJson()
        documentoLink['link_id'] = self.link_id
        documentoLink['link'] = self.link.linkToJson()
        #print(repr(documentoLink))
        return documentoLink

    def dictToDocumento(self, udict):
        self.id = udict.get("id")
        self.documento_id = udict.get("documento_id")
        self.link_id = udict.get("link_id")

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
        indiceInvertido['documento'] = self.documento.documentoToJson()
        indiceInvertido['termo_id'] = self.termo_id
        indiceInvertido['termo'] = self.termo.termoDocumentoToJson()
        indiceInvertido['frequencia'] = self.frequencia
        indiceInvertido['peso'] = self.peso
        #print(repr(indiceInvertido))
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
class Role(Base):
    __tablename__ = 'roles'
    id = Column(mysql.INTEGER, primary_key=True)
    name = Column(mysql.VARCHAR(50), unique=True)

# Define User data-model
class User(Base, UserMixin):
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
class UserRoles(Base):
    __tablename__ = 'user_roles'
    id = Column(mysql.INTEGER, primary_key=True)
    user_id = Column(mysql.INTEGER, ForeignKey('users.id', ondelete='CASCADE'))
    role_id = Column(mysql.INTEGER, ForeignKey('roles.id', ondelete='CASCADE'))


class Consulta:
    texto = ""
    visao = ""
    termosConsulta = []
    ranking = []

    def __init__(self, texto, visao):
        self.texto = texto
        self.visao = visao

    def getListaTermos(self):
        termos = []
        for termo in self.termosConsulta:
            termos.append(termo)
        return termos

    def getSomaQuadradosPesos(self):
        somaQuadradosPesos = 0
        for termo in self.termosConsulta:
            somaQuadradosPesos = somaQuadradosPesos + math.pow(termo.peso, 2)
        return somaQuadradosPesos

    def consultaToJson(self):
        consulta = {}
        consulta['texto'] = self.texto
        consulta['visao'] = self.visao
        termos = []
        for termo in self.termosConsulta:
            termos.append(termo.termoConsultaToJson())
        consulta['termosConsulta'] = termos
        ranks = []
        for rank in self.ranking:
            ranks.append(rank.entradaRankingToJson())
        consulta['ranking'] = ranks
        return consulta

class TermoConsulta:
    texto = ""
    frequencia = 0
    tf = 0.0
    idf = 0.0
    peso = 0.0

    def __init__(self, texto, frequencia, idf):
        self.texto = texto
        self.frequencia = frequencia
        self.idf = idf
        self.tf = 1 + (math.log(frequencia) / math.log(2))
        self.peso = self.tf * self.idf

    def termoConsultaToJson(self):
        termoConsulta = {}
        termoConsulta['texto'] = self.texto
        termoConsulta['frequencia'] = self.frequencia
        termoConsulta['tf'] = self.tf
        termoConsulta['idf'] = self.idf
        termoConsulta['peso'] = self.peso
        return termoConsulta

class EntradaRanking:
    url = ""
    produtoPesos = []
    somaQuadradosPesosDocumento = 0.0
    somaQuadradosPesosConsulta = 0.0
    similaridade = 0.0

    def __init__(self, url, produtoPesos, somaQuadradosPesosDocumento, somaQuadradoPesosConsulta):
        self.url = url
        self.produtoPesos = produtoPesos
        self.somaQuadradosPesosConsulta = somaQuadradoPesosConsulta
        self.somaQuadradosPesosDocumento = somaQuadradosPesosDocumento

    def entradaRankingToJson(self):
        entradaRanking = {}
        entradaRanking['url'] = self.url
        entradaRanking['produtoPesos'] = self.produtoPesos
        entradaRanking['somaQuadradosPesosDocumento'] = self.somaQuadradosPesosDocumento
        entradaRanking['somaQuadradosPesosConsulta'] = self.somaQuadradosPesosConsulta
        entradaRanking['similaridade'] = self.similaridade
        return entradaRanking

    def computarSimilaridade(self):
        if self.somaQuadradosPesosDocumento > 0 and self.somaQuadradosPesosConsulta > 0:
            numerador = 0.0
            denominador = 0.0
            for produtoPeso in self.produtoPesos:
                numerador = numerador + produtoPeso
            denominador = math.sqrt(self.somaQuadradosPesosDocumento) * math.sqrt(self.somaQuadradosPesosConsulta)
            self.similaridade = numerador / denominador
        else:
            self.similaridade = 0

    def computarSimilaridadeSemiNormalizada(self):
        if self.somaQuadradosPesosDocumento > 0 and self.somaQuadradosPesosConsulta > 0:
            numerador = 0.0
            denominador = 0.0
            for produtoPeso in self.produtoPesos:
                numerador = numerador + produtoPeso
            denominador = math.sqrt(self.somaQuadradosPesosDocumento)
            self.similaridade = numerador / denominador
        else:
            self.similaridade = 0

    def clone(self):
        retorno = EntradaRanking('', [], 0.0, 0.0)
        retorno.produtoPesos = self.produtoPesos
        retorno.similaridade = self.similaridade
        retorno.somaQuadradosPesosConsulta = self.somaQuadradosPesosConsulta
        retorno.somaQuadradosPesosDocumento = self.somaQuadradosPesosDocumento
        retorno.url = self.url
        return retorno

