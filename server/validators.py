import re
from werkzeug.exceptions import BadRequest

# Проверка email
def validate_email(email):
    if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
        raise BadRequest("Неверный формат email")

# Проверка ID
def validate_id(id):
    if not isinstance(id, int) or id <= 0:
        raise BadRequest("ID должен быть положительным числом")

# Проверка строковых полей
def validate_string(value, field_name, min_length=1, max_length=255):
    if not isinstance(value, str):
        raise BadRequest(f"{field_name} должен быть строкой")
    if len(value) < min_length or len(value) > max_length:
        raise BadRequest(f"{field_name} должен быть длиной от {min_length} до {max_length} символов")