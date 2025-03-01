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