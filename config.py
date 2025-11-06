import os

# Базовые настройки
DEBUG = True
SECRET_KEY = 'dev-secret-key-change-in-production'

# Настройки базы данных
basedir = os.path.abspath(os.path.dirname(__file__))
SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'app.db')
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Настройки аутентификации
WTF_CSRF_ENABLED = True

# Настройки поиска
SEARCH_CONFIG = {
    'results_per_page': 10,
    'snippet_length': 150
}