from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
import os

# Инициализация расширений
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()

def create_app(config_class='app.config.Config'):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Загрузка конфигурации из .env файла
    if os.path.exists('.env'):
        from dotenv import load_dotenv
        load_dotenv()
        app.config.from_prefixed_env()
    
    # Инициализация расширений с приложением
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    
    # Настройка Flask-Login
    login_manager.login_view = 'auth.login' # Перенаправление неавторизованных
    login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'
    login_manager.login_message_category = 'info'
    
    from app.utils.login_manager import setup_login_manager
    setup_login_manager(login_manager)
    
    # Регистрация blueprint'ов
    register_blueprints(app)
    
    # Создание таблиц базы данных
    with app.app_context():
        db.create_all()
    
    return app

def register_blueprints(app):
    """Регистрация всех blueprint'ов"""
    from app.routes.main import main_bp
    from app.routes.auth import auth_bp
    from app.routes.search import search_bp
    from app.routes.friends import friends_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(friends_bp)