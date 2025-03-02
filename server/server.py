from flask import Flask
from routes import register_route, login_route, protected_route, token_required, news_route, search_news, get_news_by_category_route, get_categories_routes,add_category_route
from routes import add_news_route
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)

limiter = Limiter(
    app,
    key_func=get_remote_address,
    default_limits=["200 per day", "50 per hour"]
)

# Регистрация маршрутов
@app.route('/register', methods=['POST'])
@limiter.limit("10 per minute")
def register():
    return register_route()

@app.route('/login', methods=['POST'])
@limiter.limit("10 per minute")
def login():
    return login_route()

@app.route('/news', methods=['GET'])
def get_news():
    return news_route()

@app.route('/news/add', methods=['POST'])
def add_news():
    return add_news_route()

@app.route('/search', methods=['GET'])
def get_search():
    return search_news()

@app.route('/news/category/<category>', methods=['GET'])
def get_new_by_categ():
    return get_news_by_category_route()

@app.route('/categories', methods=['GET'])
def get_categories():
    return get_categories_routes()

@app.route('/categories/add', methods=['POST'])
def add_category():
    return add_category_route()

@app.route('/protected', methods=['GET'])
@token_required
def protected(user_id):
    return protected_route(user_id)

if __name__ == '__main__':
    app.run(debug=True)