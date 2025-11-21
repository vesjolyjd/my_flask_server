from flask import Blueprint, render_template, request
from markupsafe import escape

search_bp = Blueprint('search', __name__)

@search_bp.route('/search')
def search():
    user_query = request.args.get('query', '')
    safe_query = escape(user_query) # Санитизация HTML
    
    return render_template('search/search.html', query=safe_query)