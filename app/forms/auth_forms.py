from flask_wtf import FlaskForm # Защита форм от csrf
from wtforms import StringField, PasswordField, SubmitField, BooleanField # Задаём требования
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from app.models.user import User

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')

class RegistrationForm(FlaskForm):
    username = StringField('Имя пользователя', 
                          validators=[DataRequired(), Length(min=3, max=64)])
    email = StringField('Email', 
                       validators=[DataRequired(), Email()])
    password = PasswordField('Пароль', 
                            validators=[DataRequired(), Length(min=6)])
    password2 = PasswordField('Повторите пароль', 
                             validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Зарегистрироваться')
    
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Это имя пользователя уже занято.')
    
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Этот email уже зарегистрирован.')