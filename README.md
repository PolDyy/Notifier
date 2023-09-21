# Notifier

Сервис уведомлений  
Версия python: python 3.10.12  
Версия node: 16.20.2  
______________________

## Запуск проекта

1) Клонировать репозиторий и перейти в него в командной строке:
    
    `git init`

    `git clone https://github.com/PolDyy/Notifier.git`

2) Cоздать и активировать виртуальное окружение в корне проекта:

    `python -m venv venv`

    `source venv/Scripts/activate` или `source venv/bin/activate`

3) Установить зависимости:

    `python -m pip install --upgrade pip`

    `pip install -r requirements/base.txt`

4) Создаем файл .env на основе env_example.txt

5) Активируем докер окружение: 

    `docker compose up -d --build`

6) Проводим миграции

## Для запуска frontend

1) Установить node.js (https://nodejs.org/en/download/).

2) Перейти в директорию frontend.

    `cd frontend/`

3) Установить зависимости:

    `npm install`

4) Скомпелировать assets:

    `npm start`


## Примечание 

В методах отправки сообщений на почту оставил print, чтобы сообщение выводилось в консоль,  
чтобы для проверки не нужно было настраивать SMTP не обязательно

Для проверки можете воспользоваться написанными тестами:

   `python manage.py test`

## Эндпоинты

|   | uri                              | Methods |      Access level | Description                               |
|---|----------------------------------|:-------:|------------------:|-------------------------------------------|
| 1 | /                                |   GET   |         all users | Для получения страницы входа              |
| 2 | api/auth/send-email/             |  POST   |         all users | Для отправки сообщения с ссылкой на почту |
| 3 | api/auth/login/<str:unique_hash> |   GET   |         all users | Для аутентификации                        |
| 4 | api/auth/refresh                 |   GET   |   IsAuthenticated | Для обновления токена                     |
| 5 | message/<str:unique_hash>        |   GET   |   IsAuthenticated | Для получения всех сообщений канала       |
| 6 | channel/                         |  POST   |   IsAuthenticated | Создание канала                           |
| 7 | channel/                         |   GET   |   IsAuthenticated | Получение списка каналов                  |
| 8 | channel/<str:unique_hash>        |   GET   |   IsAuthenticated | Получение канала                          |
| 8 | channel/<str:unique_hash>        |  PATCH  |   IsAuthenticated | Запрос на вход в канал                    |
| 9 | add/<str:token>                  |   GET   |   IsAuthenticated | Для подтверждения входа в закрытый канал  |
