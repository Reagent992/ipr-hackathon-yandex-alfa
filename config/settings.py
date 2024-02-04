import os
from logging.handlers import RotatingFileHandler  # noqa
from pathlib import Path

from django.utils.timezone import timedelta
from environs import Env

env = Env()
env.read_env()

# ---------------------------------------------------------LOAD ENVIRONMENT VAR
SECRET_KEY = env.str(
    "SECRET_KEY",
    default="django-insecure-pp6rzgeb5sjtbhfs(d-3*ibq67#0c-8jsd82@65!+=$satw167",
)
USE_POSTGRESQL = env.bool("USE_POSTGRESQL", default=False)
DEBUG = env.bool("DEBUG", default=False)
ALLOWED_HOSTS = env.list(
    "ALLOWED_HOSTS",
    default=[
        "localhost",
        "127.0.0.1",
        "[::1]",
        "testserver",
    ],
)
DB_NAME = env.str("DB_NAME", default="IPR")
DB_USER = env.str("POSTGRES_USER", default="username")
DB_PASSWORD = env.str("POSTGRES_PASSWORD", default="smart-password123")
DB_HOST = env.str("DB_HOST", default="db")
DB_PORT = env.int("DB_PORT", default=5432)
CORS_ALLOWED_ORIGINS = env.list(
    "CORS_ALLOWED_ORIGINS",
    default=["http://localhost:80", "http://127.0.0.1:80"],
)
CSRF_TRUSTED_ORIGINS = CORS_ORIGINS_WHITELIST = CORS_ALLOWED_ORIGINS
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent


DJANGO_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]
THIRD_PARTY_APPS = [
    "rest_framework",
    "rest_framework.authtoken",
    "djoser",
    "django_filters",
    "drf_spectacular",
    "notifications",
    "corsheaders",
]
LOCAL_APPS = [
    "api.v1.apps.ApiConfig",
    "comments.apps.CommentsConfig",
    "ipr.apps.IprConfig",
    "tasks.apps.TasksConfig",
    "users.apps.UsersConfig",
    "ratings.apps.RatingsConfig",
    "core.apps.CoreConfig",
]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

if USE_POSTGRESQL:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.postgresql",
            "NAME": DB_NAME,
            "USER": DB_USER,
            "PASSWORD": DB_PASSWORD,
            "HOST": DB_HOST,
            "PORT": DB_PORT,
        }
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


LANGUAGE_CODE = env.str("LANGUAGE_CODE", default="ru-RU")
TIME_ZONE = env.str("TIME_ZONE", default="Europe/Moscow")
TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

STATIC_URL = "/static/"

STATIC_ROOT = os.path.join(BASE_DIR, "static/")

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
#  -------------------------------------------------------------CUSTOM SETTINGS
MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

AUTH_USER_MODEL = "users.User"
# -----------------------------------------------------------------DRF SETTINGS
REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "PAGE_SIZE": 10,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
# Выключено предупреждение об отсутствие DEFAULT_PAGINATION_CLASS
SILENCED_SYSTEM_CHECKS = ["rest_framework.W001"]
# Время жизни токена увеличено, для упрощения тестирования.
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
}
# --------------------------------------------------------------DJOSER SETTINGS
DJOSER = {
    "LOGIN_FIELD": "email",
    "SERIALIZERS": {
        "current_user": "api.v1.serializers.api.users_serializer.CustomUserSerializer",
    },
    "PERMISSIONS": {
        "user": ["rest_framework.permissions.IsAuthenticated"],
        "user_list": ["rest_framework.permissions.IsAuthenticated"],
    },
    "HIDE_USERS": False,
}
# -------------------------------------------------------------ALTER USER MODEL
SPECTACULAR_SETTINGS = {
    "TITLE": "IPR API",
    "DESCRIPTION": (
        "API-Документация для SPA ИПР.<br>"
        "Хакатон Яндекс-Практикум/Альфа-Банк 2024. Команда № 8."
    ),
    "VERSION": "0.1.0",
    "SCHEMA_PATH_PREFIX": "/api/v1/",
    "SERVE_INCLUDE_SCHEMA": False,
}
# --------------------------------------------------------------------CONSTANTS
EMAIL_LENGTH = 254
NAME_LENGTH = 150
MAX_LEN_COMMENT_TEXT = 200
DESCRIPTION_LEN = 500
SKILL_LEN = 255
RESTRICTED_USERNAMES = (
    "me",
    "admin",
    "administrator",
    "root",
)
RATING_CHOICES = (
    (1, "1 звезда"),
    (2, "2 звезды"),
    (3, "3 звезды"),
    (4, "4 звезды"),
    (5, "5 звезд"),
)
# ----------------------------------------------------------------------LOGGING
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "rotating_file": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": "./log_file.log",
            "maxBytes": 1024 * 1024,  # 1 MB
            "backupCount": 5,         # 5 files
        },
    },
    "loggers": {
        "django": {
            "handlers": ["rotating_file"],
            "level": "INFO",
            "propagate": True,
        },
    },
}
