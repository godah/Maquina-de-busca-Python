from flask import Blueprint, render_template, abort, jsonify
from jinja2 import TemplateNotFound

from src.model.models import Users

simple_page = Blueprint('simple_page', __name__, template_folder='templates')


@simple_page.route('/', defaults={'page': 'index'})
@simple_page.route('/<page>')
def show(page):
    try:
        return 'funciona'
    except TemplateNotFound:
        abort(404)


@simple_page.route('/user')
def user():
    try:
        #users = Users()
        u = Users().query.all()
        return jsonify(u)
    except Exception:
        abort(404)
