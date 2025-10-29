from flask import Flask, request
from markupsafe import escape # Для экранирования

app = Flask(__name__)

# Главная страница
@app.route('/')
def hello():
    return '<h1>Привет! Это мой сервер!</h1> <a href="/search">Перейти к поиску</a>'

# Страница поиска
@app.route('/search')
def search():
    user_query = request.args.get('query', '')
    safe_query = escape(user_query) # Позволяет экранировать пользовательский ввод формы

    output = f"""
    <h2>Результаты поиска</h2>
    <p>Вы искали: <b>{safe_query}</b></p>
    <br>
    <form action="/search">
        <input type="text" name="query" placeholder="Введите запрос...">
        <button type="submit">Искать снова</button>
    </form>
    """
    return output

if __name__ == '__main__':
    app.run(debug=True)