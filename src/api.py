from flask import Flask
from src.controller.UserController import user_controller
from src.controller.ColetorController import coletor_controller
from src.controller.DocumentoController import documento_controller
from src.controller.HostController import host_controller
from src.controller.LinkController import link_controller
from src.controller.ProcessadorConsultaController import processadorconsulta_controller
from src.controller.IndexadorController import indexador_controller
from src.controller.LoginController import login_controller


app = Flask(__name__)
app.register_blueprint(user_controller)
app.register_blueprint(coletor_controller)
app.register_blueprint(host_controller)
app.register_blueprint(documento_controller)
app.register_blueprint(link_controller)
app.register_blueprint(processadorconsulta_controller)
app.register_blueprint(indexador_controller)
app.register_blueprint(login_controller)

if __name__ == "__main__":
    app.run(debug=True)
