import urllib.robotparser
from urllib.parse import urlparse


class RobotsService:

    def verificaPermissaoRobots(self, url):
        try:
            uri = urlparse(url)
            host = uri.scheme+"://"+uri.netloc
            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(host+"/robots.txt")
            rp.read()
            return rp.can_fetch("*", url)
        except Exception:
            print("Falha ao coletar o arquivo robots.txt da url: " + url)
            return True