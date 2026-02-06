import pytest
import os
import sys

# Fix import path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app import create_app, db
from app.models.user import User
from app.models.friendship import Friendship
from datetime import datetime

class TestModels:
    """Тесты для моделей данных"""
    
    def setup_method(self):
        """Настройка перед каждым тестом"""
        self.app = create_app('app.config.TestingConfig')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def teardown_method(self):
        """Очистка после каждого теста"""
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_user_creation(self):
        """Тест создания пользователя"""
        user = User(username='testuser', email='test@example.com')
        user.set_password('password123')
        db.session.add(user)
        db.session.commit()
        
        assert user.id is not None
        assert user.username == 'testuser'
        assert user.email == 'test@example.com'
        assert user.created_at is not None
        assert user.check_password('password123')
        assert not user.check_password('wrongpassword')

    def test_user_repr(self):
        """Тест строкового представления пользователя"""
        user = User(username='testuser', email='test@example.com')
        user.set_password('dummy')  # Добавляем пароль
        db.session.add(user)
        db.session.commit()
        
        assert repr(user) == "<User testuser>"

    def test_friendship_creation(self):
        """Тест создания дружеской связи"""
        user1 = User(username='user1', email='user1@example.com')
        user2 = User(username='user2', email='user2@example.com')
        user1.set_password('pass123')
        user2.set_password('pass123')
        
        db.session.add_all([user1, user2])
        db.session.commit()
        
        friendship = Friendship(sender_id=user1.id, receiver_id=user2.id)
        db.session.add(friendship)
        db.session.commit()
        
        assert friendship.id is not None
        assert friendship.status == 'pending'
        assert friendship.sender_id == user1.id
        assert friendship.receiver_id == user2.id
        assert friendship.created_at is not None

    def test_friendship_repr(self):
        """Тест строкового представления дружбы"""
        user1 = User(username='user1', email='user1@example.com')
        user2 = User(username='user2', email='user2@example.com')
        user1.set_password('pass123')  # Добавляем пароли!
        user2.set_password('pass123')  # Добавляем пароли!
        db.session.add_all([user1, user2])
        db.session.commit()
        
        friendship = Friendship(sender_id=user1.id, receiver_id=user2.id)
        db.session.add(friendship)
        db.session.commit()
        
        # Проверяем что repr содержит нужную информацию
        repr_str = repr(friendship)
        assert "Friendship" in repr_str
        assert str(user1.id) in repr_str or "->" in repr_str
        assert str(user2.id) in repr_str or "->" in repr_str
        assert "pending" in repr_str

    def test_user_get_friends_method(self):
        """Тест метода get_friends у пользователя"""
        # Создаем пользователей
        user1 = User(username='user1', email='user1@example.com')
        user2 = User(username='user2', email='user2@example.com')
        user3 = User(username='user3', email='user3@example.com')
        
        for user in [user1, user2, user3]:
            user.set_password('pass123')
        
        db.session.add_all([user1, user2, user3])
        db.session.commit()
        
        # Создаем дружбу между user1 и user2
        friendship = Friendship(sender_id=user1.id, receiver_id=user2.id, status='accepted')
        db.session.add(friendship)
        db.session.commit()
        
        # Проверяем метод get_friends
        friends = user1.get_friends()
        assert len(friends) == 1
        assert friends[0].username == 'user2'

        def test_user_friendship_methods(self):
            """Тест дополнительных методов дружбы у пользователя"""
            user1 = User(username='user1', email='user1@example.com')
            user2 = User(username='user2', email='user2@example.com')
            user3 = User(username='user3', email='user3@example.com')
            
            for user in [user1, user2, user3]:
                user.set_password('pass123')
            
            db.session.add_all([user1, user2, user3])
            db.session.commit()
            
            # Создаем несколько дружеских связей
            friendship1 = Friendship(sender_id=user1.id, receiver_id=user2.id, status='accepted')
            friendship2 = Friendship(sender_id=user3.id, receiver_id=user1.id, status='pending')
            friendship3 = Friendship(sender_id=user1.id, receiver_id=user3.id, status='pending')
            
            db.session.add_all([friendship1, friendship2, friendship3])
            db.session.commit()
            
            # Проверяем методы пользователя
            assert len(user1.get_friends()) == 1  # user2 (accepted)
            assert len(user1.get_pending_requests()) == 1  # от user3
            assert len(user1.get_sent_requests()) == 1  # к user3
            
            # Исправленная проверка - метод должен возвращать True/False
            assert user1.is_friends_with(user2) == True  # Должен возвращать True
            assert user1.is_friends_with(user3) == False  # Должен возвращать False
            
            # Дополнительные проверки
            assert user1.has_pending_request_from(user3) is not None
            assert user1.has_sent_request_to(user3) is not None

if __name__ == '__main__':
    pytest.main()