from flask import request, jsonify
from functools import wraps
from database import create_connection, get_news_with_pagination
from auth import generate_token, verify_token, hash_password, verify_password

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

    connection = create_connection()
    if connection:
        try:
            news = get_news_with_pagination(connection, page, per_page)
            return jsonify(news), 200
        except Exception as e:
            return jsonify({"error": f"Ошибка: {e}"}), 500
        finally:
            connection.close()
    else:
        return jsonify({"error": "Не удалось подключиться к базе данных"}), 500

# Защищенный маршрут
def protected_route(user_id):
    return jsonify({"message": f"Доступ разрешен! Ваш ID: {user_id}"}), 200