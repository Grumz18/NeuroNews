from flask import request, jsonify
from functools import wraps
from database import create_connection, get_news_with_pagination, search_news_by_keyword, get_news_by_category
from auth import generate_token, verify_token, hash_password, verify_password
from cache import Cache
from validators import validate_email, validate_string, validate_id
import json

cache = Cache()

# Middleware для проверки токена
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Токен отсутствует"}), 401

        if token.startswith("Bearer "):
            token = token.split(" ")[1]

        user_id = verify_token(token)
        if not user_id:
            return jsonify({"error": "Неверный или просроченный токен"}), 401

        kwargs['user_id'] = user_id
        return f(*args, **kwargs)
    return decorated

# Маршрут для регистрации
def register_route():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email и пароль обязательны"}), 400
    
    validate_email(email)
    validate_string(password, "Пароль", min_length=6, max_length=128)

    hashed_password = hash_password(password)
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO users (email, password_hash) VALUES (%s, %s)"
            cursor.execute(query, (email, hashed_password))
            connection.commit()
            connection.close()
            return jsonify({"message": "Пользователь зарегистрирован!"}), 201
        except Exception as e:
            connection.close()
            return jsonify({"error": f"Ошибка при регистрации: {e}"}), 500
    else:
        return jsonify({"error": "Не удалось подключиться к базе данных"}), 500

# Маршрут для входа
def login_route():
    data = request.json
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"error": "Email и пароль обязательны"}), 400
    
    validate_email(email)
    validate_string(password, "Пароль", min_length=6, max_length=128)

    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            query = "SELECT * FROM users WHERE email = %s"
            cursor.execute(query, (email,))
            user = cursor.fetchone()

            if user and verify_password(user['password_hash'], password):
                token = generate_token(user['id'])
                return jsonify({"message": "Вход выполнен успешно!", "token": token}), 200
            else:
                return jsonify({"error": "Неверный email или пароль"}), 401
        except Exception as e:
            connection.close()
            return jsonify({"error": f"Ошибка при входе: {e}"}), 500
    else:
        return jsonify({"error": "Не удалось подключиться к базе данных"}), 500
    
def news_route():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)
    cache_key = f"news_page_{page}_per_page_{per_page}"

    # Проверяем, есть ли данные в кэше
    cached_news = cache.get(cache_key)
    if cached_news:
        return jsonify(json.loads(cached_news)), 200

    # Если данных нет в кэше, получаем их из базы данных
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            offset = (page - 1) * per_page
            query = "SELECT * FROM news LIMIT %s OFFSET %s"
            cursor.execute(query, (per_page, offset))
            news = cursor.fetchall()

            # Сохраняем данные в кэше на 1 час (3600 секунд)
            cache.set(cache_key, json.dumps(news), expire=3600)

            return jsonify(news), 200
        except Exception as e:
            return jsonify({"error": f"Ошибка: {e}"}), 500
        finally:
            connection.close()
    else:
        return jsonify({"error": "Не удалось подключиться к базе данных"}), 500
    
def search_news():
    query = request.args.get('q', '')
    if not query:
        return jsonify({"error": "Параметр 'q' обязателен"}), 400

    connection = create_connection()
    if connection:
        try:
            results = search_news_by_keyword(connection, query)
            return jsonify(results), 200
        except Exception as e:
            return jsonify({"error": f"Ошибка: {e}"}), 500
        finally:
            connection.close()
    else:
        return jsonify({"error": "Не удалось подключиться к базе данных"}), 500
    
def get_news_by_category_route(category):
    connection = create_connection()
    if connection:
        try:
            news = get_news_by_category(connection, category)
            return jsonify(news), 200
        except Exception as e:
            return jsonify({"error": f"Ошибка: {e}"}), 500
        finally:
            connection.close()
    else:
        return jsonify({"error": "Не удалось подключиться к базе данных"}), 500
    
def get_categories_routes():
    cached_categories = cache.get('categories')
    if cached_categories:
        return jsonify(json.loads(cached_categories)), 200

    # Если данных нет в кэше, получаем их из базы данных
    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM categories")
            categories = cursor.fetchall()

            # Сохраняем данные в кэше на 1 час (3600 секунд)
            cache.set('categories', json.dumps(categories), expire=3600)

            return jsonify(categories), 200
        except Exception as e:
            return jsonify({"error": f"Ошибка: {e}"}), 500
        finally:
            connection.close()
    else:
        return jsonify({"error": "Не удалось подключиться к базе данных"}), 500
    
def add_category_route(user_id):
    data = request.json
    category_name = data.get('name')

    if not category_name:
        return jsonify({"error": "Имя категории обязательно"}), 400
    
    validate_string(category_name, "Имя категории", min_length=3, max_length=100)

    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO categories (name) VALUES (%s)"
            cursor.execute(query, (category_name,))
            connection.commit()

            # Очищаем кэш для списка категорий
            cache.delete('categories')

            return jsonify({"message": "Категория добавлена!"}), 201
        except Exception as e:
            connection.rollback()
            return jsonify({"error": f"Ошибка: {e}"}), 500
        finally:
            connection.close()
    else:
        return jsonify({"error": "Не удалось подключиться к базе данных"}), 500
    
def add_news_route():
    data = request.json
    title = data.get('title')
    content = data.get('content')
    category_id = data.get('category_id')

    if not title or not content or not category_id:
        return jsonify({"error": "Все поля обязательны"}), 400
    
    validate_string(title, "Заголовок", min_length=3, max_length=255)
    validate_string(content, "Контент", min_length=10, max_length=10000)
    validate_id(category_id)

    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = "INSERT INTO news (title, content, category_id) VALUES (%s, %s, %s)"
            cursor.execute(query, (title, content, category_id))
            connection.commit()

            # Очищаем кэш для всех страниц новостей
            for page in range(1, 11):  # Предположим, что у нас максимум 10 страниц
                cache_key = f"news_page_{page}_per_page_10"
                cache.delete(cache_key)

            return jsonify({"message": "Новость добавлена!"}), 201
        except Exception as e:
            connection.rollback()
            return jsonify({"error": f"Ошибка: {e}"}), 500
        finally:
            connection.close()
    else:
        return jsonify({"error": "Не удалось подключиться к базе данных"}), 500

# Защищенный маршрут
def protected_route(user_id):
    return jsonify({"message": f"Доступ разрешен! Ваш ID: {user_id}"}), 200