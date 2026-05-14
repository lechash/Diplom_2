import uuid
import requests
from faker import Faker
from data.endpoints import INGREDIENTS

fake = Faker()


def generate_unique_user():
    # Генерирует данные уникального пользователя
    # Использует uuid для гарантии уникальности email между запусками
    
    unique_id = uuid.uuid4().hex[:8]
    return {
        "email": f"test_{unique_id}@yandex.ru",
        "password": "Password123!",
        "name": fake.name()
    }


def get_random_ingredient_id():
    # Получает ID первого доступного ингредиента для создания заказа
    response = api_client.get_ingredients()
    if response.status_code == 200:
        data = response.json()
        if data.get("success") and data.get("data"):
            return data["data"][0]["_id"]
    raise RuntimeError("Не удалось получить список ингредиентов")