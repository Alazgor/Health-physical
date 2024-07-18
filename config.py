import os
from dotenv import load_dotenv

# Loading environment variables from a file .env
load_dotenv()

# Absolute path to current directory
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    # Secret key Flask
    SECRET_KEY = os.getenv('SECRET_KEY', 'your_secret_key_here')

    # URI for database SQLAlchemy
    SQLALCHEMY_DATABASE_URI = 'sqlite:///C:/Users/aleks/CodeAcademy/health&physical/instance/db.sqlite'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Config Flask-Mail
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = 'your-email@gmail.com'
    MAIL_PASSWORD = 'your-email-password'
    MAIL_DEFAULT_SENDER = 'your-email@example.com'


