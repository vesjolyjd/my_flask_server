import pytest
from app import create_app, db
from app.models.user import User

class TestRoutes:
    def setup_method(self):
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
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_home_page(self):
        response = self.client.get('/')
        assert response.status_code == 200
        assert b'Mind Roadmap' in response.data

    def test_protected_route_redirect(self):
        response = self.client.get('/profile', follow_redirects=False)
        assert response.status_code == 302  # Redirect to login