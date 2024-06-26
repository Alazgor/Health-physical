from flask import Flask
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from config import Config

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bootstrap = Bootstrap()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Инициализация расширений Flask
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bootstrap.init_app(app)

    # Регистрация Blueprints
    from app.routes import main
    app.register_blueprint(main)

    # Импорт моделей внутри функции create_app() после инициализации db и login_manager
    from app import models

    return app


