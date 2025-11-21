#!/usr/bin/env python3
"""
Точка входа в приложение Mind Roadmap
"""

from app import create_app, db
from app.models.user import User
from app.models.friendship import Friendship

app = create_app()

@app.shell_context_processor
def make_shell_context():
    """Контекст для Flask shell"""
    return {
        'db': db, 
        'User': User, 
        'Friendship': Friendship
    }

if __name__ == '__main__':
    app.run(
        host=app.config.get('HOST', '127.0.0.1'),
        port=app.config.get('PORT', 5000),
        debug=app.config.get('DEBUG', False)
    )