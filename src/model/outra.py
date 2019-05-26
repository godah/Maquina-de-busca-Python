
from .pessoa import Pessoa

class Outra:
    def __init__(self, idade):
        self.idade = idade

    def imprime(self):
        pessoa = Pessoa("22", self.idade)
        return pessoa