from flask import Flask
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Manager
from flask.ext.shellplus import Shell


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
app.config['SQLALCHEMY_ECHO'] = False
app.config['SHELLPLUS_PRE_IMPORTS'] = [('os', 'path')]
db = SQLAlchemy(app)
manager = Manager(app)


def make_context():
    return dict(app=app, db=db)

manager.add_command('shell', Shell(make_context=make_context))


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)


if __name__ == '__main__':
    manager.run()
