#for use virtualenv/virtualenvwrapper
#mkvirtualenv <name>
#workon <name>
#disable
#
#$pip install venv 
#$source /bin/activate
#$deactivate
#
#$pip install Flask flask_sqlalchemy mysql-connector-python pymysql
#For install dialect

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
#For use sqlite
#app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///F:\\test.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root1a2b3c:root1a2b3c@85.10.205.173:3306/maquinadebuscapy'
db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.username

class Link(db.Model):
    __tablename__ = 'Link'
    id = db.Column(db.Integer, primary_key=True)
    ultimaColeta = db.Column(db.Date)
    url = db.Column(db.String(255))
    #host_id = Column(Integer, ForeignKey('Host.id'))
    
    def __repr__(self):
        return '<Link %r>' % self.url


#for create
#from api import db
#db.create_all()


#for use
#$python
#>>>from api import Link
#>>>Link.query.all()