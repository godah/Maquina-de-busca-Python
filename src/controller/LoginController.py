#testado
import http
from flask import Blueprint, abort, jsonify
from flask_login import login_required, logout_user
from werkzeug.utils import redirect
from src import app


login_controller = Blueprint('login_controller', __name__, template_folder='templates')


@login_controller.route('/login', methods=["POST"])
@login_required
def login():
    try:
        ok = {}
        ok['status'] = 'OK'
        return jsonify(ok)
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)

    @app.route("/settings")
    @login_required
    def settings(self):
        pass

    @app.route("/logout")
    @login_required
    def logout():
        logout_user()
        return redirect("/")