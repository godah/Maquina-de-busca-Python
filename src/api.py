import base64

from flask import Flask
from flask_login import LoginManager


from src.controller.UserController import user_controller
from src.controller.ColetorController import coletor_controller
from src.controller.DocumentoController import documento_controller
from src.controller.HostController import host_controller
from src.controller.LinkController import link_controller
from src.controller.ProcessadorConsultaController import processadorconsulta_controller
from src.controller.IndexadorController import indexador_controller
from src.controller.LoginController import login_controller
from src.model.models import User


app = Flask(__name__)
app.register_blueprint(user_controller)
app.register_blueprint(coletor_controller)
app.register_blueprint(host_controller)
app.register_blueprint(documento_controller)
app.register_blueprint(link_controller)
app.register_blueprint(processadorconsulta_controller)
app.register_blueprint(indexador_controller)
app.register_blueprint(login_controller)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.session_protection = "basic"

@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@login_manager.request_loader
def load_user_from_request(request):
    # first, try to login using the api_key url arg
    api_key = request.args.get('api_key')
    if api_key:
        user = User.query.filter_by(api_key=api_key).first()
        if user:
            return user
    # next, try to login using Basic Auth
    api_key = request.headers.get('Authorization')
    if api_key:
        api_key = api_key.replace('Basic ', '', 1)
        try:
            api_key = base64.b64decode(api_key)
        except TypeError:
            pass
        split = str(api_key).split(':')
        user = split[0][2:]
        pwd = split[1][0:len(split[1])-1]
        user = User.query.filter_by(username=user, password=pwd).first()
        if user:
            return user
    # finally, return None if both methods did not login the user
    return None

if __name__ == "__main__":
    app.run(debug=True)
