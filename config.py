import os

from flask import Flask
from flask_socketio import SocketIO
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Configure app
app = Flask(__name__)
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY") or "Thisshouldbeasecret"
app.config['WTF_CSRF_SECRET_KEY'] = os.getenv("WTF_CSRF_SECRET_KEY") or "b'f\xfa\x8b{X\x8b\x9eM\x83l\x19\xad\x84\x08\xaa"

# Configure socketio
socketio = SocketIO(app, manage_session=False)

# Configure database
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("SQLALCHEMY_DATABASE_URI") or 'postgresql://postgres:Promise2022@localhost/postgres'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)


# Initialize login manager
login = LoginManager(app)
login.init_app(app)
