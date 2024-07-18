# health/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_mail import Mail
from config import Config
import os
from flask_migrate import Migrate
import logging
from flask_session import Session

# Create an instance of the Flask application
app = Flask(__name__)
app.config.from_object(Config)

# Set the URI for the SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///C:/Users/aleks/CodeAcademy/health&physical/instance/db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialising Flask extensions
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login_manager = LoginManager(app)
mail = Mail(app)

# Generate a new secret key if it has not been set in the environment variable
secret_key = os.environ.get('SECRET_KEY', None)
if not secret_key:
    secret_key = os.urandom(24).hex()
app.config['SECRET_KEY'] = secret_key

# Initialise Flask-Migrate for database migration
Migrate(app, db)

# Configuration for Flask-Login: Specify view for login
login_manager.login_view = 'login'

# Initialise Flask-Session for session management
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_FILE_DIR'] = r'C:\Users\aleks\CodeAcademy\health&physical\Session'
Session(app)

# Import routes and models after application initialisation
from health import routes, models
