import redis
from dotenv import load_dotenv
import os

# Загрузка переменных окружения
load_dotenv()

class Cache:
    def __init__(self):
        self.client = redis.StrictRedis(
            host=os.getenv("REDIS_HOST", "localhost"),
            port=int(os.getenv("REDIS_PORT", 6379)),
            decode_responses=True
        )

    def get(self, key):
        return self.client.get(key)

    def set(self, key, value, expire=None):
        self.client.set(key, value, ex=expire)

    def delete(self, key):
        self.client.delete(key)