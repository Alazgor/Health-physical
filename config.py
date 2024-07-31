import os
from dotenv import load_dotenv
from datetime import timedelta

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

    # class Config:
    #     MAIL_SERVER = 'smtp.gmail.com'
    #     MAIL_PORT = 587
    #     MAIL_USE_TLS = True
    #     MAIL_USE_SSL = False
    #     MAIL_USERNAME = 'aleksejkolpakov88@gmail.com'  # Ваш реальный email
    #     MAIL_PASSWORD = 'your-app-password'  # Пароль приложений
    #     MAIL_DEFAULT_SENDER = 'aleksejkolpakov88@gmail.com'
    #
    # # Token expiration for security purposes
    # TOKEN_EXPIRATION = int(timedelta(minutes=30).total_seconds())
