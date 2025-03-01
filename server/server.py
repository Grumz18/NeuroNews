from flask import Flask, request, jsonify
from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error
import bcrypt
import jwt
import datetime
import logging
from functools import wraps

load_dotenv()
app = Flask(__name__)

# Настройка логирования
logging.basicConfig(
    filename='app.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

sk = os.getenv("SECRET_KEY")

# Подключение к базе данных
def create_connection():
    try:
        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            database=os.getenv("DB_NAME")
        )
        if connection.is_connected():
            print("Успешное подключение к базе данных")
        return connection
    except Error as e:
        print(f"Ошибка подключения: {e}")
        return None

# Хэширование пароля
def hash_password(password):
    password_bytes = password.encode('utf-8')
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password_bytes, salt)
    return hashed_password.decode('utf-8')

# Проверка пароля
def verify_password(stored_hash, provided_password):
    stored_hash_bytes = stored_hash.encode('utf-8')
    provided_password_bytes = provided_password.encode('utf-8')
    return bcrypt.checkpw(provided_password_bytes, stored_hash_bytes)

# Генерация JWT
def generate_token(user_id):
    payload = {
        "user_id": user_id,
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=24)
    }
    token = jwt.encode(payload, sk, algorithm="HS256")
    return token

# Проверка JWT
def verify_token(token):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return payload.get("user_id")
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None

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
@app.route('/register', methods=['POST'])
def register():
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
        except Error as e:
            connection.close()
            return jsonify({"error": f"Ошибка при регистрации: {e}"}), 500
    else:
        return jsonify({"error": "Не удалось подключиться к базе данных"}), 500

# Маршрут для входа
@app.route('/login', methods=['POST'])
def login():
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
        except Error as e:
            connection.close()
            return jsonify({"error": f"Ошибка при входе: {e}"}), 500
    else:
        return jsonify({"error": "Не удалось подключиться к базе данных"}), 500

# Защищенный маршрут
@app.route('/protected', methods=['GET'])
@token_required
def protected_route(user_id):
    return jsonify({"message": f"Доступ разрешен! Ваш ID: {user_id}"}), 200

# Логирование
@app.route('/test_logging', methods=['GET'])
def test_logging():
    logging.info("Это информационное сообщение")
    logging.warning("Это предупреждение")
    logging.error("Это сообщение об ошибке")
    return jsonify({"message": "Логирование выполнено!"}), 200

if __name__ == '__main__':
    app.run(debug=True)