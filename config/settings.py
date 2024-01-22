import os
from pathlib import Path

from django.utils.timezone import timedelta
from environs import Env

env = Env()
env.read_env()

# ---------------------------------------------------------LOAD ENVIRONMENT VAR
SECRET_KEY = env.str("SECRET_KEY")
USE_POSTGRESQL = env.bool("USE_POSTGRESQL", default=False)
DEBUG = env.bool("DEBUG", default=False)
# -----------------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

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
]
LOCAL_APPS = [
    "api.v1.apps.ApiConfig",
    "ipr.apps.IprConfig",
    "tasks.apps.TasksConfig",
    "users.apps.UsersConfig",

]
INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
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
            "NAME": os.getenv("DB_NAME"),
            "USER": os.getenv("POSTGRES_USER"),
            "PASSWORD": os.getenv("POSTGRES_PASSWORD"),
            "HOST": os.getenv("DB_HOST"),
            "PORT": os.getenv("DB_PORT"),
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
    "PAGE_SIZE": 6,
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
    ],
    "DEFAULT_SCHEMA_CLASS": "drf_spectacular.openapi.AutoSchema",
}
SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=1),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# --------------------------------------------------------------DJOSER SETTINGS

DJOSER = {
    "LOGIN_FIELD": "email",
    # TODO: "PERMISSIONS": {},
    "SERIALIZERS": {
        "current_user": "api.v1.serializers.api.users_serializer.CustomUserSerializer",
    },
    "HIDE_USERS": False,
}

# -------------------------------------------------------------ALTER USER MODEL
SPECTACULAR_SETTINGS = {
    "TITLE": "IPR API",
    "DESCRIPTION": (
        "API-Документация для SPA-приложения ИПР.<br>"
        "Хакатон Яндекс-Практикум/Альфа-Банк 2024. Команда № 8."
    ),
    "VERSION": "0.1.0",
    "SCHEMA_PATH_PREFIX": "/api/v1/",
}
# --------------------------------------------------------------------CONSTANTS
EMAIL_LENGTH = 254
NAME_LENGTH = 150
RESTRICTED_USERNAMES = (
    "me",
    "admin",
    "administrator",
    "root",
)
