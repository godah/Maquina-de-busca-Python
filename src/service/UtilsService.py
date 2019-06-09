from bs4 import BeautifulSoup
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
            if len(novaLista) == 0:
                novaLista.append(old)
            else:
                count = 0
                for nova in novaLista:
                    if old.lower() == nova.lower():
                        count += 1
                        break
                if count == 0:
                    novaLista.append(old)
        return novaLista

    def obterLinks(self, soup):
        links = []
        linksRaw = soup.findAll('a', attrs={'href': re.compile("^http://")})
        for link in linksRaw:
            links.append(link.get('href'))
            print(link.get('href'))
        return links

    def removeLinksRepetidos(self, links):
        novaLista = []
        for old in links:
            if len(novaLista) == 0:
                novaLista.append(old)
            else:
                count = 0
                for nova in novaLista:
                    if old.url == nova.url:
                        count += 1
                        break
                if count == 0:
                    novaLista.append(old)
        return novaLista