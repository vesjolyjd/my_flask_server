from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime

db = SQLAlchemy()

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Отношения для друзей
    sent_requests = db.relationship('Friendship', 
                                  foreign_keys='Friendship.sender_id',
                                  backref='sender', 
                                  lazy='dynamic')
    received_requests = db.relationship('Friendship', 
                                      foreign_keys='Friendship.receiver_id', 
                                      backref='receiver', 
                                      lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def get_friends(self):
        """Возвращает список подтвержденных друзей"""
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
        """Возвращает входящие заявки в друзья"""
        return Friendship.query.filter_by(
            receiver_id=self.id, 
            status='pending'
        ).all()
    
    def get_sent_requests(self):
        """Возвращает исходящие заявки в друзья"""
        return Friendship.query.filter_by(
            sender_id=self.id, 
            status='pending'
        ).all()
    
    def is_friends_with(self, user):
        """Проверяет, являются ли пользователи друзьями"""
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
        return friendship1 or friendship2
    
    def has_pending_request_from(self, user):
        """Проверяет, есть ли входящая заявка от пользователя"""
        return Friendship.query.filter_by(
            sender_id=user.id, 
            receiver_id=self.id, 
            status='pending'
        ).first()
    
    def has_sent_request_to(self, user):
        """Проверяет, отправлял ли заявку этому пользователю"""
        return Friendship.query.filter_by(
            sender_id=self.id, 
            receiver_id=user.id, 
            status='pending'
        ).first()
    
    def __repr__(self):
        return f'<User {self.username}>'

class Friendship(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, accepted, rejected
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Уникальность комбинации отправитель-получатель
    __table_args__ = (db.UniqueConstraint('sender_id', 'receiver_id', name='unique_friendship'),)