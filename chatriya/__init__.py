from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_login import LoginManager

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
app.secret_key = '9b907c7aff32d2ce5acebd1ec1bf6f67'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login = LoginManager(app)

from chatriya import routes
