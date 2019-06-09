from bs4 import BeautifulSoup
from src.service.UtilsService import UtilsService

class StopwordsService:

    stopwords = []
    utilsService = UtilsService()

    def readStopWords(self):
        try:
            f = open("./resources/stopwords.txt","r")
            for line in f:
                self.stopwords.append(line[0:len(line)-1])
        except Exception:
            print('Falha ao tentar ler arquivo stopwords.txt')
        finally:
            return self.stopwords

    def getStopwords(self):
        if self.stopwords.count() <= 0:
            self.readStopWords()
        return self.stopwords

    def isStopword(self, word):
        if len(self.stopwords) <= 0:
            self.readStopWords()
        try:
            if self.stopwords.index(word) >= 0:
                return True
            return False
        except Exception:
            return False

    def removerStoprWords(self, visao):
        words = visao.split()
        novoVisao = []
        retorno = ""
        for wd in words:
            if not self.isStopword(wd):
                novoVisao.append(wd)
        for wd in novoVisao:
            retorno = retorno+wd+" "
        return retorno

    #requisicao.text
    def tratarVisao(self, soup):
        text = soup.get_text()
        txtlimpo = self.utilsService.removerPontuacao(text)
        txttratado = self.removerStoprWords(txtlimpo)
        return txttratado
