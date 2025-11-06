# Базовые настройки
DEBUG = True
SECRET_KEY = '12345678'

# Настройки для будущей базы данных
DATABASE_CONFIG = {
    'host': 'localhost',
    'database': 'search_app',
    'user': 'username',
    'password': 'password'
}

# Настройки поиска
SEARCH_CONFIG = {
    'results_per_page': 10,
    'snippet_length': 150
}