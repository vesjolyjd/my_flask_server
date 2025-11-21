import pytest
from app import create_app, db
from app.models.user import User

class TestAuth:
    def setup_method(self):
        self.app = create_app('app.config.TestingConfig')
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def teardown_method(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_register_user(self):
        response = self.client.post('/register', data={
            'username': 'newuser',
            'email': 'new@example.com',
            'password': 'Password123',
            'password2': 'Password123'
        }, follow_redirects=True)
        
        assert response.status_code == 200
        assert User.query.filter_by(username='newuser').first() is not None

    def test_login_user(self):
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        response = self.client.post('/login', data={
            'email': 'test@example.com',
            'password': 'password123'
        }, follow_redirects=True)
        
        assert response.status_code == 200