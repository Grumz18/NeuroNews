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
    
# Функция поиска новостей
def search_news_by_keyword(connection, keyword):
    try:
        cursor = connection.cursor(dictionary=True)
        query = "SELECT * FROM news WHERE title LIKE %s OR content LIKE %s"
        cursor.execute(query, (f"%{keyword}%", f"%{keyword}%"))
        results = cursor.fetchall()
        return results
    except mysql.connector.Error as e:
        print(f"Ошибка при поиске новостей: {e}")
        return []
    
# функция для получения новостей по категории
def get_news_by_category(connection, category_name):
    try:
        cursor = connection.cursor(dictionary=True)
        query = """
            SELECT n.* FROM news n
            JOIN categories c ON n.category_id = c.id
            WHERE c.name = %s
        """
        cursor.execute(query, (category_name,))
        news = cursor.fetchall()
        return news
    except mysql.connector.Error as e:
        print(f"Ошибка при получении новостей по категории: {e}")
        return []