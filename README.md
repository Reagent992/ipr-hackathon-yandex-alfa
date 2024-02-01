# Backend Проекта "ИПР". Хакатон Яндекс-Альфа-Банк. Команда №8

[![Code-style/tests](https://github.com/Reagent992/ipr-hackathon-yandex-alfa/actions/workflows/code-style_and_tests.yml/badge.svg)](https://github.com/Reagent992/ipr-hackathon-yandex-alfa/actions/workflows/code-style_and_tests.yml)
[![deploy](https://github.com/Reagent992/ipr-hackathon-yandex-alfa/actions/workflows/deploy.yml/badge.svg)](https://github.com/Reagent992/ipr-hackathon-yandex-alfa/actions/workflows/deploy.yml)\
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![DjangoREST](https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white)
![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white)

TO-DO: Описание проекта.

## [Репозиторий Frontend](https://github.com/NataliyaNikulshina/ipr-hackathon-yandex-alfa)

## Документация API

Пример адреса на запущенном сервере:

- <http://127.0.0.1:8000/api/v1/swagger/>
- <http://127.0.0.1:8000/api/v1/redoc/>

## Используемые библиотеки и зависимости

| Библиотека | Описание |
|-|-|
| [Python 3.12](https://www.python.org/) | Язык программирования Python версии 3.12.|
| [Django](https://pypi.org/project/Django/)| Основной фреймворк для разработки веб-приложений. |
| [DRF](https://pypi.org/project/djangorestframework/)| Фреймворк для создания API в приложениях Django.|
| [Gunicorn](https://pypi.org/project/gunicorn/)| WSGI-сервер для запуска веб-приложений Django. |
| [Environs](https://pypi.org/project/environs/) | Библиотека для управления переменными окружения и хранения секретов. |
| [drf-spectacular](https://drf-spectacular.readthedocs.io/en/latest/index.html) | Генератор документации и Swagger для API в Django. |
| [Djoser](https://pypi.org/project/djoser/) | Библиотека для обеспечения аутентификации в приложениях Django. |
| [Pillow](https://pypi.org/project/pillow/) | Библиотека для обработки изображений в Python. |
| [Django filter](https://pypi.org/project/django-filter/) | Библиотека для фильтрации данных в приложениях Django. |
| [Django Notifications](https://github.com/django-notifications/django-notifications) | Уведомления. |
| [django-cors-headers](https://pypi.org/project/django-cors-headers/) | Что-то делает с headers |
| [django-dirtyfields](https://django-dirtyfields.readthedocs.io/en/stable/quickstart.html) | Для доступа к измененной информации в джанго сигнале `post_save` |
| [Flake8](https://pypi.org/project/flake8/), [black](https://pypi.org/project/black/), [isort](https://pypi.org/project/isort/), [Pre-commit](https://pypi.org/project/pre-commit/) | Инструменты для поддержания Code-Style в проекте. |

## Code-Style при разработке

### Локальный запуск pre-commit

- В начале требует активации хуков `pre-commit install`
- Далее будет запускаться при попытке сделать commit или при запуске `pre-commit`

## Запуск проекта

### 1. Требуется заполнить `.env` файл, пример заполнения находится в `.envexample`

### 2. [Загрузка фикстур в БД](docs/authorization.md) - _Опционально_

## Авторы

- [Miron Sadykov](https://github.com/Reagent992)
- [Mikhail Volkov](https://github.com/greenpandorik)
- [Артур Галиаскаров](https://github.com/Arti1946)
- [Ilya Kotenko](https://github.com/IlyaKotenko)
