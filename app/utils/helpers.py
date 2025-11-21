import os
from datetime import datetime, timedelta
from flask import request, current_app

def format_datetime(value, format='%d.%m.%Y %H:%M'):
    """
    Форматирование даты для шаблонов
    """
    if value is None:
        return ""
    return value.strftime(format)

def get_client_ip():
    """
    Получение реального IP клиента
    """
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    return request.remote_addr

def is_safe_url(target):
    """
    Проверка безопасности URL для редиректов
    """
    from urllib.parse import urlparse, urljoin
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc

def generate_username_from_email(email):
    """
    Генерация username из email
    """
    return email.split('@')[0].replace('.', '_').lower()

def calculate_age(birth_date):
    """
    Расчет возраста по дате рождения
    """
    today = datetime.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))