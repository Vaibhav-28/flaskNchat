from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from flask_login import LoginManager

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")
app.secret_key = 'changeme'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
login = LoginManager(app)

from flasknchat import routes
