from flask import Flask, render_template
import os

def create_app():
    app = Flask(__name__, 
                template_folder='templates',
                static_folder='static')
    
    app.config.from_pyfile('config.py')
    
    # Регистрация маршрутов
    from routes.main_routes import main_bp
    from routes.search_routes import search_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(search_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=app.config['DEBUG'])