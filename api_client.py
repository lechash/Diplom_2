import requests
import allure
from data.endpoints import AUTH, ORDERS, INGREDIENTS


class StellarBurgersAPI:
   # Клиент для взаимодействия с API через методы с логированием в Allure

    # === Регистрация и авторизация ===
    
    @allure.step("Регистрация пользователя")
    def register(self, email: str = None, password: str = None, name: str = None):
        """POST /api/auth/register - создание нового пользователя"""
        payload = {}
        if email is not None:
            payload["email"] = email
        if password is not None:
            payload["password"] = password
        if name is not None:
            payload["name"] = name
        return requests.post(AUTH["register"], json=payload)

    @allure.step("Авторизация пользователя")
    def login(self, email: str = None, password: str = None):
        # POST /api/auth/login - вход в систему
        payload = {}
        if email is not None:
            payload["email"] = email
        if password is not None:
            payload["password"] = password
        return requests.post(AUTH["login"], json=payload)

    @allure.step("Выход из системы")
    def logout(self, refresh_token: str):
        # POST /api/auth/logout - выход по refresh token
        payload = {"token": refresh_token}
        return requests.post(AUTH["logout"], json=payload)

    @allure.step("Обновление access token")
    def refresh_token(self, refresh_token: str):
        # POST /api/auth/token - получение нового access token
        payload = {"token": refresh_token}
        return requests.post(AUTH["refresh"], json=payload)

    # === Управление профилем пользователя ===
    
    @allure.step("Получение данных пользователя")
    def get_user(self, access_token: str):
        # GET /api/auth/user - получение профиля (требует авторизации)
        headers = {"Authorization": access_token}
        return requests.get(AUTH["user"], headers=headers)

    @allure.step("Обновление данных пользователя")
    def update_user(self, access_token: str = None, email: str = None, name: str = None, password: str = None):
        # PATCH /api/auth/user - обновление профиля
        # Принимает любые из: email, name, password
        # access_token=None для теста неавторизованного запроса
        
        headers = {"Authorization": access_token} if access_token else {}
        payload = {}
        if email is not None:
            payload["email"] = email
        if name is not None:
            payload["name"] = name
        if password is not None:
            payload["password"] = password
        return requests.patch(AUTH["user"], json=payload, headers=headers)

    @allure.step("Удаление пользователя")
    def delete_user(self, access_token: str):
        # DELETE /api/auth/user - удаление аккаунта (требует авторизации)
        headers = {"Authorization": access_token}
        return requests.delete(AUTH["user"], headers=headers)

    # === Заказы ===
    
    @allure.step("Создание заказа")
    def create_order(self, ingredients: list, access_token: str = None):
        # POST /api/orders - создание заказа
        # access_token=None для теста неавторизованного запроса
       
        headers = {"Authorization": access_token} if access_token else {}
        payload = {"ingredients": ingredients}
        return requests.post(ORDERS["create"], json=payload, headers=headers)

    @allure.step("Получение списка заказов пользователя")
    def get_user_orders(self, access_token: str):
        # GET /api/orders - заказы текущего пользователя (требует авторизации)
        headers = {"Authorization": access_token}
        return requests.get(ORDERS["list"], headers=headers)

    @allure.step("Получение публичного списка всех заказов")
    def get_all_orders(self):
        # GET /api/orders/all - публичный эндпоинт всех заказов
        return requests.get(ORDERS["all"])

    # === Ингредиенты ===
    
    @allure.step("Получение списка ингредиентов")
    def get_ingredients(self):
        # GET /api/ingredients - список доступных ингредиентов
        return requests.get(INGREDIENTS)