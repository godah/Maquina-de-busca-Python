from bs4 import BeautifulSoup
from src.service.UtilsService import UtilsService

class StopwordsService:

    stopwords = []
    utilsService = UtilsService()

    def readStopWords(self):
        try:
            f = open("../resources/stopwords.txt","r")
            for line in f:
                self.stopwords.append(line)
        except Exception:
            print('Falha ao tentar ler arquivo')
        finally:
            return self.stopwords

    def getStopwords(self):
        if self.stopwords.count() <= 0:
            self.readStopWords()
        return self.stopwords

    def isStopword(self, word):
        if self.stopwords.count() <= 0:
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
        for word in words:
            if not self.isStopword(word):
                novoVisao.append(words)
        for word in novoVisao:
            retorno += word+" "
        return retorno

    #requisicao.text
    def tratarVisao(self, textHtml):
        soup = BeautifulSoup(textHtml)
        text = soup.get_text()
        txtlimpo = self.utilsService.removerPontuacao(text)
        txttratado = self.removerStoprWords(txtlimpo)
        return txttratado
