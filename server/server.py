from flask import Flask
from routes import register_route, login_route, protected_route, token_required, news_route, search_news

app = Flask(__name__)

# Регистрация маршрутов
@app.route('/register', methods=['POST'])
def register():
    return register_route()

@app.route('/login', methods=['POST'])
def login():
    return login_route()

@app.route('/news', methods=['GET'])
def get_news():
    return news_route()

@app.route('/search', methods=['GET'])
def get_search():
    return search_news()

@app.route('/news/category/<category>', methods=['GET'])
def get_new_by_categ():
    return get_news_by_category_route()

@app.route('/protected', methods=['GET'])
@token_required
def protected(user_id):
    return protected_route(user_id)

if __name__ == '__main__':
    app.run(debug=True)