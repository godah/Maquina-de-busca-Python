
import re, time

class UtilsService:

    def removerPontuacao(self, visao):
        return re.sub("[^A-Z a-z \u00C0-\u00ff 0-9 ]", "", visao)

    def verificaColetaConsecultiva(self, urlStringAnterior, url):
        if urlStringAnterior is not None:
            if urlStringAnterior is url:
                print('Host consecultivo esperando 10 segundos.')
                time.sleep(10)

    def removeElementosRepetidos(self, urls):
        novaLista = []
        for old in urls:
            if novaLista.count() == 0:
                novaLista.append(old)
            else:
                count = 0
                for nova in novaLista:
                    if old.lower() is nova.lower():
                        count += 1
                if count == 0:
                    novaLista.append(old)
        return novaLista
