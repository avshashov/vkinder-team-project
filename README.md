# Командный проект по курсу «Профессиональная работа с Python»

## VKinder

### Установка
Перед запуском нужно создать файл "vk_auth.py" корневом каталоге проекта. В котором будт хранится: сервисный токен ВК (servis_key), токен группы ВК (alt_token), юзер базы данных (user_db), пароль базы данных (password_db) 

- Сервисный токен, инструкция получения https://dev.vk.com/mini-apps/management/settings 
- Токен группы, инструкция получения https://dev.vk.com/api/access-token/implicit-flow-community

### Цель проекта

Разработать программу-бота для взаимодействия с базами данных и социальной сети. Бот будет предлагать различные варианты людей для знакомств в социальной сети Вконтакте в виде диалога с пользователем.

Выполнены задачи:
- Спроектирована база данных (БД) для программы
- Создано сообщество ВК https://vk.com/club217757110 с интегрированным в чаты ботом
- Разработана программа-бота на Python с алгоритмом:
1. Используя информацию (возраст, пол, город) о пользователе, который общается с ботом в ВК, производится поиск других людей (других пользователей ВК) для знакомств.
2. У тех людей, которые подошли под критерии поиска, получить три самые популярные фотографии в профиле. Популярность определяется по количеству лайков.
3. Выводить в чат с ботом информацию о пользователе в формате: ФИО, Ссылка, Фото
4. Реализовано меню "Следующий".
5. Реализованы кнопки "Добавить в избранное" и "Показать избранные"
6. Созданы кнопки в чате для взаимодействия с ботом.

## Техническое описание проекта

### Структура каталога проекта

- main.py
- requirements.txt
- README.md
- vk_auth.py
  - api
    - vk_bot.py
    - keyboard.py
  - vk
    - vk_info.py
  - vkinderdb
    - db_functions.py
    - create_tables.sql

  
### Модуль main.py

>Модуль запускающий работу бота
### Модуль vk_bot.py
>В модуле определяется класс VkBot реализующий логику взаимодействия с API ВКонтакте, для
>работы Бота.
### Модуль keyboard.py
>Определяет вспомогательный класс UserKeyboard: для взаимодействия бота с пользователем.
### Модуль vk_info.py
>Определяет класс VKInfo реализующий логику получения информации о пользователе при взаимодействии с API ВКонтакте.
### Модуль db_functions.py
>Определяет класс VkinderDB который содержит функции взаиподействия бота с базами данных.
### Модуль create_tables.sql
>Содержит инициализации базы данных проекта.


## Структура таблиц