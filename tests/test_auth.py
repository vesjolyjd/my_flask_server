import pytest
import os
import sys

# Fix import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.user import User

class TestAuth:
    """Тесты для аутентификации и авторизации"""
    
    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.app = create_app('app.config.TestingConfig')
        self.app.config['WTF_CSRF_ENABLED'] = False  # Отключаем CSRF для тестов
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        
        # Создаем тестового пользователя
        self.test_user = User(username='testuser', email='test@example.com')
        self.test_user.set_password('TestPass123')
        db.session.add(self.test_user)
        db.session.commit()

    def teardown_method(self):
        """Очистка после каждого теста"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        """Тест главной страницы (русский язык)"""
        response = self.client.get('/')
        assert response.status_code == 200
        # Проверяем русский текст
        html = response.data.decode('utf-8')
        assert 'Mind Roadmap' in html
        assert 'Добро пожаловать' in html or 'поиск' in html.lower()

    def test_register_page(self):
        """Тест страницы регистрации (русский язык)"""
        response = self.client.get('/register')
        assert response.status_code == 200
        html = response.data.decode('utf-8')
        assert 'Регистрация' in html or 'зарегистрироваться' in html.lower()

    def test_valid_registration(self):
        """Тест успешной регистрации"""
        response = self.client.post('/register', data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'ValidPass123',
            'password2': 'ValidPass123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert User.query.filter_by(username='newuser').first() is not None
        # Проверяем русское сообщение об успехе
        html = response.data.decode('utf-8')
        assert 'успешна' in html.lower() or 'успешно' in html.lower()

    def test_invalid_registration_duplicate_username(self):
        """Тест регистрации с существующим username"""
        response = self.client.post('/register', data={
            'username': 'testuser',  # Уже существует
            'email': 'different@example.com',
            'password': 'password123',
            'password2': 'password123'
        })
        
        html = response.data.decode('utf-8')
        # Проверяем русское сообщение об ошибке
        assert 'занято' in html.lower() or 'существует' in html.lower()

    def test_login_page(self):
        """Тест страницы входа"""
        response = self.client.get('/login')
        assert response.status_code == 200
        html = response.data.decode('utf-8')
        assert 'Вход' in html or 'войти' in html.lower()

    def test_valid_login(self):
        """Тест успешного входа"""
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'TestPass123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        html = response.data.decode('utf-8')
        assert 'Добро пожаловать' in html or 'привет' in html.lower()

    def test_invalid_login_wrong_password(self):
        """Тест входа с неверным паролем"""
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'WrongPass123'
        })
        
        html = response.data.decode('utf-8')
        assert 'Неверный' in html or 'ошибка' in html.lower()

    def test_protected_route_redirects_when_not_logged_in(self):
        """Тест что защищенный маршрут перенаправляет на логин"""
        response = self.client.get('/profile', follow_redirects=False)
        assert response.status_code == 302  # Redirect
        assert '/login' in response.location

    def test_logout(self):
        """Тест выхода из системы"""
        # Сначала логинимся
        self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'TestPass123'
        })
        
        # Затем выходим
        response = self.client.get('/logout', follow_redirects=True)
        assert response.status_code == 200
        html = response.data.decode('utf-8')
        assert 'вышли' in html.lower() or 'выход' in html.lower()

    def test_user_model_password_hashing(self):
        """Тест хеширования паролей в модели User"""
        user = User(username='testhash', email='hash@test.com')
        password = 'MySecretPass123'
        user.set_password(password)
        
        assert user.password_hash != password  # Должен быть захеширован
        assert user.check_password(password)  # Должен возвращать True
        assert not user.check_password('WrongPassword')  # Должен возвращать False

if __name__ == '__main__':
    pytest.main()