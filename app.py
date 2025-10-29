from flask import Flask, request

# Создаем объект приложения Flask
app = Flask(__name__)

# Главная страница
@app.route('/')
def hello():
    return '<h1>Привет! Это мой сервер!</h1> <a href="/search">Перейти к поиску</a>'

# Страница поиска (уязвима к XSS)
@app.route('/search')
def search():
    # Получаем то, что пользователь ввел в строке ?query=...
    user_query = request.args.get('query', '')  # Если параметра нет, будет пустая строка

    # ОПАСНО: мы вставляем пользовательский ввод прямо в HTML без проверки!
    output = f"""
    <h2>Результаты поиска</h2>
    <p>Вы искали: <b>{user_query}</b></p>
    <br>
    <form action="/search">
        <input type="text" name="query" placeholder="Введите запрос...">
        <button type="submit">Искать снова</button>
    </form>
    """
    return output

# Запускаем сервер, если файл запущен напрямую
if __name__ == '__main__':
    app.run(debug=True)