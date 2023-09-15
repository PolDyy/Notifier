# Notifier

Сервис уведомлений
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