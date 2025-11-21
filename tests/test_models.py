import pytest
from app import create_app, db
from app.models.user import User
from app.models.friendship import Friendship

class TestModels:
    def setup_method(self):
        self.app = create_app('app.config.TestingConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def teardown_method(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        assert user.id is not None
        assert user.check_password('password123')
        assert not user.check_password('wrongpassword')

    def test_friendship_creation(self):
        user1 = User(username='user1', email='user1@example.com')
        user2 = User(username='user2', email='user2@example.com')
        user1.set_password('pass123')
        user2.set_password('pass123')
        
        db.session.add_all([user1, user2])
        db.session.commit()
        
        friendship = Friendship(sender_id=user1.id, receiver_id=user2.id)
        db.session.add(friendship)
        db.session.commit()
        
        assert friendship.status == 'pending'
        assert friendship.sender_id == user1.id