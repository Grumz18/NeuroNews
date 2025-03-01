import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Загрузка переменных окружения
load_dotenv()

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

# функция для получения новостей с пагинацией
def get_news_with_pagination(connection, page, per_page):
    try:
        cursor = connection.cursor(dictionary=True)
        offset = (page - 1) * per_page
        query = "SELECT * FROM news LIMIT %s OFFSET %s"
        cursor.execute(query, (per_page, offset))
        news = cursor.fetchall()
        return news
    except mysql.connector.Error as e:
        print(f"Ошибка при получении новостей: {e}")
        return []