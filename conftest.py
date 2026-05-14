import pytest
import logging
from data.constants import HTTP, API_KEYS
from api_client import StellarBurgersAPI
from helpers import generate_unique_user, get_random_ingredient_id

logger = logging.getLogger(__name__)


@pytest.fixture(scope="function")
def api_client():
    # Фикстура: экземпляр API-клиента для тестов
    return StellarBurgersAPI()


@pytest.fixture
def user_cleanup_list():
    # Фикстура для отслеживания пользователей, требующих удаления после теста.
    # Гарантирует очистку тестовых данных даже при падении теста.
    
    users_to_delete = []
    yield users_to_delete
    
    # Пост-условие: удаление всех зарегистрированных пользователей
    api = StellarBurgersAPI()
    for user in users_to_delete:
        try:
            if user.get("access_token"):
                response = api.delete_user(user["access_token"])
                logger.info(f"Пользователь {user.get('email')} удалён: {response.status_code}")
        except Exception as e:
            logger.warning(f"Не удалось удалить пользователя {user.get('email')}: {e}")


@pytest.fixture
def created_user(api_client, user_cleanup_list):
    # Фикстура: создаёт нового пользователя и возвращает данные с access_token. 
    # Автоматически регистрирует пользователя для последующего удаления.
    
    user_data = generate_unique_user()
    
    # Pre-condition: регистрация пользователя
    response = api_client.register(**user_data)
    assert response.status_code == HTTP["OK"], (
        f"Pre-condition failed: не удалось зарегистрировать пользователя. "
        f"Код: {response.status_code}, Ответ: {response.text}"
    )
    
    # Извлекаем токены из ответа
    response_json = response.json()
    access_token = response_json.get(API_KEYS["access_token"])
    refresh_token = response_json.get(API_KEYS["refresh_token"])
    
    assert access_token, "Pre-condition failed: не получен access_token"
    
    # Формируем полные данные пользователя для тестов
    user_with_tokens = {
        **user_data,
        "access_token": access_token,
        "refresh_token": refresh_token,
    }
    
    # Регистрируем для автоматического удаления после теста
    user_cleanup_list.append(user_with_tokens)
    
    logger.info(f"Создан тестовый пользователь: {user_data['email']}")
    yield user_with_tokens


@pytest.fixture
def ingredients_list(api_client):
    # Фикстура: возвращает список ID доступных ингредиентов
    response = api_client.get_ingredients()
    assert response.status_code == HTTP["OK"], "Не удалось получить список ингредиентов"
    
    data = response.json()
    assert data.get(API_KEYS["success"]), "API вернул ошибку при получении ингредиентов"
    
    ingredients = data.get(API_KEYS["data"], [])
    assert ingredients, "Список ингредиентов пуст"
    
    # Возвращаем только первые 5 для оптимизации
    return [ing["_id"] for ing in ingredients[:5]]