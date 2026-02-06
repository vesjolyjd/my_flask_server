import pytest
import os
import sys

# Fix import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.user import User

class TestRoutes:
    """Тесты для маршрутов"""
    
    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.app = create_app('app.config.TestingConfig')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Создаем тестового пользователя
        self.user = User(username='testuser', email='test@example.com')
        self.user.set_password('password123')
        db.session.add(self.user)
        db.session.commit()

    def teardown_method(self):
        """Очистка после каждого теста"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_route(self):
        """Тест главной страницы"""
        response = self.client.get('/')
        assert response.status_code == 200
        html = response.data.decode('utf-8')
        assert 'Mind Roadmap' in html

    def test_about_route(self):
        """Тест страницы "О проекте" (русский язык)"""
        response = self.client.get('/about')
        assert response.status_code == 200
        html = response.data.decode('utf-8')
        assert 'О проекте' in html or 'проекте' in html.lower()

    def test_search_route(self):
        """Тест поискового маршрута"""
        response = self.client.get('/search?query=тест')
        assert response.status_code == 200
        html = response.data.decode('utf-8')
        assert 'поиск' in html.lower() or 'найти' in html.lower()

    def test_search_users_route_protected(self):
        """Тест что поиск пользователей защищен"""
        response = self.client.get('/search-users', follow_redirects=False)
        assert response.status_code == 302  # Redirect to login
        assert '/login' in response.location

    def test_friends_route_protected(self):
        """Тест что маршрут друзей защищен"""
        response = self.client.get('/friends', follow_redirects=False)
        assert response.status_code == 302  # Redirect to login
        assert '/login' in response.location

    def test_profile_route_protected(self):
        """Тест что профиль защищен"""
        response = self.client.get('/profile', follow_redirects=False)
        assert response.status_code == 302  # Redirect to login
        assert '/login' in response.location

    def test_authenticated_access(self):
        """Тест доступа к защищенным маршрутам после аутентификации"""
        # Логинимся
        self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        })
        
        # Проверяем доступ к профилю
        response = self.client.get('/profile')
        assert response.status_code == 200
        html = response.data.decode('utf-8')
        assert 'Профиль' in html or 'профиль' in html.lower()

if __name__ == '__main__':
    pytest.main()