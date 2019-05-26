from flask import Flask, jsonify
from src.model.outra import Outra

#from .model.pessoa import Pessoa
import requests
from bs4 import BeautifulSoup

app = Flask(__name__)

@app.route("/paginaHTML")
def paginaHTML():
    url="http://journals.ecs.soton.ac.uk/java/tutorial/networking/urls/readingWriting.html"
    requisicao = requests.get(url)
    print("Código HTTP de resposta: "+ str(requisicao.status_code))
    pagina = requisicao.text
    return pagina

@app.route("/paginaTXT")
def paginaTXT():
    url="http://journals.ecs.soton.ac.uk/java/tutorial/networking/urls/readingWriting.html"
    requisicao = requests.get(url)
    print("Código HTTP de resposta: " + str(requisicao.status_code))
    pagina = requisicao.text
    soup = BeautifulSoup(pagina)
    txt = soup.get_text()
    return txt


@app.route("/coleta04", methods=['GET', 'POST'])
def iniciar_GET_POST():
    return jsonify({"resp": "Coletor iniciado através do método GET ou POST."})

@app.route("/coleta05", methods=['GET', 'POST'])
def classopa():
    outra = Outra(132)
    pessoa = outra.imprime()
    return jsonify({"idade": pessoa.getIdade()})

if __name__ == "__main__":
    app.run()
