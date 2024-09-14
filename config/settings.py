import os
from pathlib import Path
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()

# Базовая директория проекта
BASE_DIR = Path(__file__).resolve().parent.parent

# Секретный ключ для проекта Django
SECRET_KEY = os.getenv("SECRET_KEY")

# Режим отладки. Если DEBUG установлено в "True" в .env, то True, иначе False
DEBUG = os.getenv("DEBUG", False) == "True"

# Список разрешённых хостов
ALLOWED_HOSTS = []

# Установленные приложения
INSTALLED_APPS = [
    "django.contrib.admin",  # Административная панель
    "django.contrib.auth",   # Система аутентификации
    "django.contrib.contenttypes",  # Система типов контента
    "django.contrib.sessions",  # Система сессий
    "django.contrib.messages",  # Система сообщений
    "django.contrib.staticfiles",  # Статические файлы
    "rest_framework",  # Django REST framework
    "users",  # Приложение пользователей
    "learning",  # Приложение обучения
]

# Список промежуточных слоёв (middleware)
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # Безопасность
    "django.contrib.sessions.middleware.SessionMiddleware",  # Сессии
    "django.middleware.common.CommonMiddleware",  # Общие функции
    "django.middleware.csrf.CsrfViewMiddleware",  # Защита от CSRF атак
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # Аутентификация
    "django.contrib.messages.middleware.MessageMiddleware",  # Сообщения
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # Защита от Clickjacking
]

# Основной конфигурационный файл URL
ROOT_URLCONF = "config.urls"

# Настройки шаблонов
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",  # Backend для шаблонов
        "DIRS": [],  # Директории шаблонов
        "APP_DIRS": True,  # Использовать директории шаблонов приложений
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",  # Контекст отладки
                "django.template.context_processors.request",  # Запрос
                "django.contrib.auth.context_processors.auth",  # Аутентификация
                "django.contrib.messages.context_processors.messages",  # Сообщения
            ],
        },
    },
]

# WSGI-приложение для проекта
WSGI_APPLICATION = "config.wsgi.application"

# Настройки базы данных
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",  # Драйвер для PostgreSQL
        "NAME": os.getenv("NAME"),  # Имя базы данных
        "USER": "postgres",  # Пользователь базы данных
        "PASSWORD": os.getenv("PASSWORD"),  # Пароль базы данных
        "HOST": os.getenv("HOST"),  # Хост базы данных
        "PORT": os.getenv("PORT"),  # Порт базы данных
    }
}

# Валидаторы паролей
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # Проверка на схожесть атрибутов
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # Минимальная длина пароля
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # Проверка на общеизвестные пароли
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # Проверка на числовые пароли
    },
]

# Код языка для проекта
LANGUAGE_CODE = "ru-ru"

# Часовой пояс
TIME_ZONE = "Asia/Bangkok"

# Использовать международизацию
USE_I18N = True

# Использовать временные зоны
USE_TZ = True

# URL для статических файлов
STATIC_URL = "static/"

# URL для медиа файлов
MEDIA_URL = "media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")  # Директория для хранения медиа файлов

# Модель пользователя
AUTH_USER_MODEL = "users.Users"

# URL для перенаправления после входа и выхода
# LOGIN_REDIRECT_URL = "/"
# LOGOUT_REDIRECT_URL = "/"

# Поле по умолчанию для автоматических полей
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Настройки для отправки электронной почты
EMAIL_HOST = os.getenv("EMAIL_HOST")
EMAIL_PORT = os.getenv("EMAIL_PORT")
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", False) == "True"
EMAIL_USE_SSL = os.getenv("EMAIL_USE_SSL", False) == "True"

SERVER_EMAIL = EMAIL_HOST_USER  # Адрес отправителя для системных сообщений
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER  # Адрес отправителя по умолчанию
