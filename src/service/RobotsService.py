import urllib
import urllib.robotparser
from urllib.parse import urlparse
import socket


class RobotsService:

    def verificaPermissaoRobots(self, url):
        try:
            socket.setdefaulttimeout(2)
            uri = urlparse(url)
            host = uri.scheme+"://"+uri.netloc
            robots = host + "/robots.txt"
            rp = urllib.robotparser.RobotFileParser()
            rp.set_url(robots)
            rp.read()
            return rp.can_fetch("*", url)
        except Exception:
            print("Falha ao coletar o arquivo robots.txt da url: " + url)
            return True