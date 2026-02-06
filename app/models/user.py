from app import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False, index=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # Отношения
    sent_requests = db.relationship(
        'Friendship', 
        foreign_keys='Friendship.sender_id',
        backref='sender', 
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    received_requests = db.relationship(
        'Friendship', 
        foreign_keys='Friendship.receiver_id', 
        backref='receiver', 
        lazy='dynamic',
        cascade='all, delete-orphan'
    )
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password) # Хэширование
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password) # Верификация
    
    def get_friends(self):
        from .friendship import Friendship
        sent = Friendship.query.filter_by(
            sender_id=self.id, 
            status='accepted'
        ).all()
        received = Friendship.query.filter_by(
            receiver_id=self.id, 
            status='accepted'
        ).all()
        
        friends = []
        for friendship in sent:
            friends.append(friendship.receiver)
        for friendship in received:
            friends.append(friendship.sender)
        
        return friends
    
    def get_pending_requests(self):
        from .friendship import Friendship
        return Friendship.query.filter_by(
            receiver_id=self.id, 
            status='pending'
        ).all()
    
    def get_sent_requests(self):
        from .friendship import Friendship
        return Friendship.query.filter_by(
            sender_id=self.id, 
            status='pending'
        ).all()
    
    def is_friends_with(self, user):
        from .friendship import Friendship
        friendship1 = Friendship.query.filter_by(
            sender_id=self.id, 
            receiver_id=user.id, 
            status='accepted'
        ).first()
        friendship2 = Friendship.query.filter_by(
            sender_id=user.id, 
            receiver_id=self.id, 
            status='accepted'
        ).first()
        return friendship1 is not None or friendship2 is not None
    
    def has_pending_request_from(self, user):
        from .friendship import Friendship
        return Friendship.query.filter_by(
            sender_id=user.id, 
            receiver_id=self.id, 
            status='pending'
        ).first()
    
    def has_sent_request_to(self, user):
        from .friendship import Friendship
        return Friendship.query.filter_by(
            sender_id=self.id, 
            receiver_id=user.id, 
            status='pending'
        ).first()
    
    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat(),
            'friends_count': len(self.get_friends())
        }
    
    def __repr__(self):
        return f'<User {self.username}>'