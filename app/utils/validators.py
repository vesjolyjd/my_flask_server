import re
from wtforms import ValidationError

def validate_password_strength(password):
    """
    Валидация сложности пароля
    """
    if len(password) < 8:
        raise ValidationError('Пароль должен содержать минимум 8 символов')
    
    if not re.search(r'[A-Z]', password):
        raise ValidationError('Пароль должен содержать хотя бы одну заглавную букву')
    
    if not re.search(r'[a-z]', password):
        raise ValidationError('Пароль должен содержать хотя бы одну строчную букву')
    
    if not re.search(r'\d', password):
        raise ValidationError('Пароль должен содержать хотя бы одну цифру')

def validate_username(username):
    """
    Валидация имени пользователя
    """
    if len(username) < 3:
        raise ValidationError('Имя пользователя должно быть не менее 3 символов')
    
    if not re.match(r'^[a-zA-Z0-9_]+$', username):
        raise ValidationError('Имя пользователя может содержать только буквы, цифры и подчеркивания')
    
    if username.startswith('_') or username.endswith('_'):
        raise ValidationError('Имя пользователя не может начинаться или заканчиваться подчеркиванием')

def validate_no_profanity(text):
    """
    Проверка на отсутствие нецензурной лексики
    """
    profanity_words = ['badword1', 'badword2']
    
    for word in profanity_words:
        if word in text.lower():
            raise ValidationError('Обнаружены недопустимые слова')