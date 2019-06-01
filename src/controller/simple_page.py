import http

from flask import Blueprint, abort, jsonify, request
from jinja2 import TemplateNotFound

from src.model.models import Users

simple_page = Blueprint('simple_page', __name__, template_folder='templates')


@simple_page.route('/', defaults={'page': 'index'})
@simple_page.route('/<page>')
def show(page):
    try:
        abort(404)
    except TemplateNotFound:
        abort(404)


@simple_page.route('/userTest')
def user():
    try:
        u = Users.query.filter_by(username='teste').first()
        a = u.userToJson()
        return jsonify(a)
    except Exception:
        abort(404)

@simple_page.route('/', methods=["POST"])
def post():
    if request.get_json() is None:
        abort(http.HTTPStatus.PRECONDITION_REQUIRED)
    try:
        body = request.get_json()
        print(body.get('username'))
        return body
    except Exception:
        abort(http.HTTPStatus.INTERNAL_SERVER_ERROR)
