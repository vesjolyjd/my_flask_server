import pytest
import os
import sys

# Добавляем корневую директорию в PYTHONPATH
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models.user import User

@pytest.fixture
def app():
    """Создает приложение для тестирования"""
    app = create_app('app.config.TestingConfig')
    app.config['WTF_CSRF_ENABLED'] = False  # Отключаем CSRF для тестов
    
    # Создаем контекст приложения
    with app.app_context():
        # Создаем все таблицы
        db.create_all()
        yield app
        # Удаляем все таблицы после теста
        db.drop_all()

@pytest.fixture
def client(app):
    """Тестовый клиент"""
    return app.test_client()

@pytest.fixture
def auth_client(client):
    """Клиент с аутентифицированным пользователем"""
    from app import db
    
    # Создаем тестового пользователя
    user = User(username='testuser', email='test@example.com')
    user.set_password('testpass123')
    
    db.session.add(user)
    db.session.commit()
    
    # Логинимся
    client.post('/login', data={
        'email': 'test@example.com',
        'password': 'testpass123'
    }, follow_redirects=True)
    
    return client

@pytest.fixture
def test_user(app):
    """Тестовый пользователь"""
    with app.app_context():
        user = User(username='fixtureuser', email='fixture@example.com')
        user.set_password('fixturepass123')
        db.session.add(user)
        db.session.commit()
        return user