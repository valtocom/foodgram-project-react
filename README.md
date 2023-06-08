![example event parameter](https://github.com/valtocom/yamdb_final/actions/workflows/main.yml/badge.svg?event=push)

# Проект Foodgram

[![Python](https://img.shields.io/badge/-Python-464641?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Docker](https://img.shields.io/badge/Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![Pytest](https://img.shields.io/badge/-Pytest-464646?style=flat-square&logo=pytest)](https://docs.pytest.org/en/6.2.x/)
[![Postman](https://img.shields.io/badge/Postman-464646?style=flat-square&logo=postman)](https://www.postman.com/)

Яндекс Практикум. Спринт 17. Дипломный проект

## Описание

Проект "Foodgram" – это "Продуктовый помощник".

## Функционал

На этом сервисе авторизированные пользователи могут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд. Для неавторизированных пользователей доступны просмотр рецептов и страниц авторов.

## Установка

1. Клонировать репозиторий:

    ```python
    git clone git@github.com:valtocom/foodgram-project-react.git
    ```

2. Создать и активировать виртуальное пространство, установить зависимости и запустить тесты:

    Для Windows:

    ```python
    cd foodgram-project-react
    python -m venv venv
    source venv/Scripts/activate
    cd backend
    pip install -r requirements.txt
    ```

    Для Mac/Linux:

    ```python
    cd foodgram-project-react
    python3 -m venv venv
    source venv/bin/activate
    cd backend
    pip install -r requirements.txt
    ```

3. Запустить контейнер Docker:

    - Проверить статус Docker:

    ```python
    docker --version
    ```

    - Запустить docker-compose:

    ```python
    cd infra/
    docker-compose up -d
    ```

4. Выполнить миграции, создать суперпользователя и собрать статику:

    ```python
    docker-compose exec web python manage.py migrate
    docker-compose exec web python manage.py createsuperuser
    docker-compose exec web python manage.py collectstatic --no-input
    ```

5. Для запуска в виртуальном окружении, после создания и активации виртуального пространства, установки зависимостей, запустить проект локально:

    Для Windows:

    ```python
    python manage.py runserver
    ```

    Для Mac/Linux:

    ```python
    python3 manage.py runserver
    ```

6. Проверить доступность сервиса:

* ```/api/users/```  Get-запрос – получение списка пользователей. POST-запрос – регистрация нового пользователя. Доступно без токена.

* ```/api/users/{id}``` GET-запрос – персональная страница пользователя с указанным id (доступно без токена).

* ```/api/users/me/``` GET-запрос – страница текущего пользователя. PATCH-запрос – редактирование собственной страницы. Доступно авторизированным пользователям. 

* ```/api/users/set_password``` POST-запрос – изменение собственного пароля. Доступно авторизированным пользователям. 

* ```/api/auth/token/login/``` POST-запрос – получение токена. Используется для авторизации по емейлу и паролю, чтобы далее использовать токен при запросах.

* ```/api/auth/token/logout/``` POST-запрос – удаление токена. 

* ```/api/tags/``` GET-запрос — получение списка всех тегов. Доступно без токена.

* ```/api/tags/{id}``` GET-запрос — получение информации о теге о его id. Доступно без токена. 

* ```/api/ingredients/``` GET-запрос – получение списка всех ингредиентов. Подключён поиск по частичному вхождению в начале названия ингредиента. Доступно без токена. 

* ```/api/ingredients/{id}/``` GET-запрос — получение информации об ингредиенте по его id. Доступно без токена. 

* ```/api/recipes/``` GET-запрос – получение списка всех рецептов. Возможен поиск рецептов по тегам и по id автора (доступно без токена). POST-запрос – добавление нового рецепта (доступно для авторизированных пользователей).

* ```/api/recipes/?is_favorited=1``` GET-запрос – получение списка всех рецептов, добавленных в избранное. Доступно для авторизированных пользователей. 

* ```/api/recipes/is_in_shopping_cart=1``` GET-запрос – получение списка всех рецептов, добавленных в список покупок. Доступно для авторизированных пользователей. 

* ```/api/recipes/{id}/``` GET-запрос – получение информации о рецепте по его id (доступно без токена). PATCH-запрос – изменение собственного рецепта (доступно для автора рецепта). DELETE-запрос – удаление собственного рецепта (доступно для автора рецепта).

* ```/api/recipes/{id}/favorite/``` POST-запрос – добавление нового рецепта в избранное. DELETE-запрос – удаление рецепта из избранного. Доступно для авторизированных пользователей. 

* ```/api/recipes/{id}/shopping_cart/``` POST-запрос – добавление нового рецепта в список покупок. DELETE-запрос – удаление рецепта из списка покупок. Доступно для авторизированных пользователей. 

* ```/api/recipes/download_shopping_cart/``` GET-запрос – получение текстового файла со списком покупок. Доступно для авторизированных пользователей. 

* ```/api/users/{id}/subscribe/``` GET-запрос – подписка на пользователя с указанным id. POST-запрос – отписка от пользователя с указанным id. Доступно для авторизированных пользователей

* ```/api/users/subscriptions/``` GET-запрос – получение списка всех пользователей, на которых подписан текущий пользователь Доступно для авторизированных пользователей.
