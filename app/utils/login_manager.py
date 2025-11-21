from app.models.user import User

def setup_login_manager(login_manager):
    ''' Загрузка пользователя из сессии '''
    @login_manager.user_loader 
    def load_user(user_id):
        return User.query.get(int(user_id))