from flask import Flask
from flask_login import LoginManager
from models import db, User

def create_app():
    app = Flask(__name__)

    app.config.from_pyfile('config.py')

    # Инициализация расширений
    db.init_app(app)

    # Настройка Flask-Login
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Регистрация маршрутов
    from routes.main_routes import main_bp
    from routes.search_routes import search_bp
    from routes.auth_routes import auth_bp
    from routes.friends_routes import friends_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(search_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(friends_bp)    

    # Создание таблиц базы данных
    with app.app_context():
        db.create_all()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=app.config['DEBUG'])