import math

from src.model.models import TermoDocumento
from src.service.IndiceInvertidoService import IndiceInvertidoService
from src.service.TermoDocumentoService import TermoDocumentoService
from src.service.DocumentoService import DocumentoService

inds = IndiceInvertidoService()
ts = TermoDocumentoService()
ds = DocumentoService()


class IndexadorService:
    termos = []
    documentos = []
    def limpaCriaIndice(self):
        self.termos = []
        inds.deleteAllNativeQuery()
        ts.deleteAllNativeQuery()
        return self.criaIndice()

    def criaIndice(self):
        self.documentos = ds.listAll()
        for documento in self.documentos:
            try:
                print('Processando indice doc.id: ['+str(documento.id)+']')
                documento.frequenciaMaxima = 0
                documento.somaQuadradosPesos = 0
                documento = ds.save(documento)
                self.indexar(documento, len(self.documentos))
            except Exception:
                print('Falha ao indexar o documento id:[' + documento.id + ']')
                return False
        return True

    def indexar(self, documento, N):
        termos = documento.visao.split()
        count = 1
        for word in termos:
            if(word is not None and word != ''):
                print('processando palavra [' + word + '] - '+str(count)+'/'+str(len(termos)))
                termo = TermoDocumento()
                termo = self.getTermo(word)
                f = self.frequencia(termo.texto, termos)
                if f > documento.frequenciaMaxima:
                    documento.frequenciaMaxima = f
                peso = self.calcularPeso(N, termo.n, f)
                documento.adicionarPeso(peso)
                inds.inserirEntradaIndiceInvertido(termo, documento, f, peso)
            count = count+1

    def getTermo(self, word):
        try:
            termo = ts.findByTermo(word)
            termo.n = self.quantDocPorTermo(word)
            termo = ts.update(termo)
            return termo
        except Exception:
            termo = TermoDocumento()
            termo.texto = word
            termo.n = self.quantDocPorTermo(word)
            termo = ts.save(termo)
            self.termos.append(termo)
            return termo

    def quantDocPorTermo(self, word):
        n = 0
        for documento in self.documentos:
            try:
                visaoArray = documento.visao.split()
                indice = visaoArray.index(word)
                n = n+1
            except Exception:
                continue
        return n

    def frequencia(self, texto, termos):
        contador = 0
        i = 0
        while i < len(termos):
            if(termos[i] is not None and termos[i] != " "):
                if termos[i] == texto:
                    contador = contador+1
                    termos[i] = ""
            i = i+1
        return contador

    def getDocumentos(self):
        return self.documentos

    def calcularPeso(self, N, n, f):
        tf = self.cacularTf(f)
        idf = self.calcularIdf(N, n)
        return tf*idf

    def cacularTf(self, f):
        return 1 + self.log(f, 2)

    def log(self, x, base):
        a = math.log(x)
        b = math.log(base)
        if a == 0 or b == 0:
            return 0
        return a/b

    def calcularIdf(self, N, n):
        if N == 0 or n == 0:
            return 0
        return self.log((N / n), 2)

