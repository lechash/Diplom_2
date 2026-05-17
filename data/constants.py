
# === HTTP статус-коды ===
HTTP = {
    "OK": 200,
    "CREATED": 201,
    "BAD_REQUEST": 400,
    "UNAUTHORIZED": 401,
    "FORBIDDEN": 403,
    "NOT_FOUND": 404,
    "INTERNAL_ERROR": 500,
}

# === Сообщения об ошибках (из документации API) ===
ERROR_MESSAGES = {
    "user_exists": "User already exists",
    "required_fields": "Email, password and name are required fields",
    "ingredients_required": "Ingredient ids must be provided",
    "unauthorized": "You should be authorised",
    "invalid_credentials": "email or password are incorrect",
    "email_exists": "User with such email already exists",
}

# === Ключи в ответах API ===
API_KEYS = {
    "success": "success",
    "message": "message",
    "user": "user",
    "email": "email",
    "name": "name",
    "access_token": "accessToken",
    "refresh_token": "refreshToken",
    "order": "order",
    "number": "number",
    "ingredients": "ingredients",
    "orders": "orders",
    "data": "data",
}

# === Обязательные поля для регистрации ===
REQUIRED_REGISTRATION_FIELDS = ["email", "password", "name"]