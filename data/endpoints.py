# URL-адреса эндпоинтов Stellar Burgers API


BASE_URL = "https://stellarburgers.education-services.ru/api"

# Регистрация и авторизация
AUTH = {
    "register": f"{BASE_URL}/auth/register",
    "login": f"{BASE_URL}/auth/login",
    "logout": f"{BASE_URL}/auth/logout",
    "refresh": f"{BASE_URL}/auth/token",
    "user": f"{BASE_URL}/auth/user",  # GET/PATCH/DELETE
}

# Заказ и ингредиенты
ORDERS = {
    "list": f"{BASE_URL}/orders",           # GET - заказы пользователя
    "create": f"{BASE_URL}/orders",         # POST - создание заказа
    "all": f"{BASE_URL}/orders/all",        # GET - все заказы (публичные)
}

INGREDIENTS = f"{BASE_URL}/ingredients"