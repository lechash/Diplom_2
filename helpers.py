import uuid
from faker import Faker

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
