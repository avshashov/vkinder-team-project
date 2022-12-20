# Командный проект по курсу «Профессиональная работа с Python»

## VKinder

### Установка
Перед запуском нужно создать файл корневом каталоге проекта. В котором будт хранится: сервисный токен ВК (servis_key), токен группы ВК (alt_token), юзер базы данных (user_db), пароль базы данных (password_db) 

- Сервисный токен, инструкция получения https://dev.vk.com/mini-apps/management/settings 
- Токен группы, инструкция получения https://dev.vk.com/api/access-token/implicit-flow-community

### Цель проекта

Разработать программу-бота для взаимодействия с базами данных и социальной сети. Бот будет предлагать различные варианты людей для знакомств в социальной сети Вконтакте в виде диалога с пользователем.

Выполненые задачи:
- Спроектирована база данных (БД) для программы
- Создано сообщество ВК https://vk.com/club217757110 с интегрированным в чаты ботом
- Разработана программа-бота на Python с алгоритмом:
1. Используя информацию (возраст, пол, город) о пользователе, который общается с ботом в ВК, производится поиск других людей (других пользователей ВК) для знакомств.
2. У тех людей, которые подошли под критерии поиска, получить три самые популярные фотографии в профиле. Популярность определяется по количеству лайков.
3. Выводить в чат с ботом информацию о пользователе в формате: ФИО, Ссылка, Фото
4. Реализовано меню "Следующий".
5. Реализованы кнопки "Добавить в избранное" и "Показать избранные"
6. Созданы кнопки в чате для взаимодействия с ботом.

## Логика проекта
- Чаты сообщества ВК https://vk.com/club217757110 интегрированны с ботом.
После того как пользователь заходит в чат вся нужная информация(фамилия, имя, возраст, пол, город) парсится с его аккаунта и попадает в отдельную таблицу
базы данных. Любой польователь попаший в это таблицу может как находить других пользователей, так и былть найденным.
- Далее после нажатия пользователем кнопки "Задать критерии поиска" ему предлагается поочередно ввести критерии поиска(возраст от, возраст до, пол, город). Эти данные сохраняются в отдельную таблицу базы данных с привязкой  к этому пользователю по user_id.
- После ввода критериев поиска пользователь может, либо изменить заданные параметры поиска,либо приступить к поиску нажав кнопку "Найти пару".
После нажатия на эту кнопку происходит поиск по заданным параметрам только в ТАБЛИЦЕ ПОЛЬЗОВАТЕЛЕЙ В БАЗЕ ДАННЫХ. Это сделано для того чтобы люди не дававшие согласие на участие в этом боте не попадали под поиск.
- Результаты поиска выводятся по одному на экран в формате: имя, фамилия, пол, ссылка на профиль, 3 фото профиля имющие наибольшое количество лайков.
У пользователя есть возможность добавить понравившегося пользователя в избранное. Также он может вызвать весь список избранного и удалить любого пользователя из этого списка. 

## Техническое описание проекта

### Структура каталога проекта

- main.py
- requirements.txt
- README.md
- vk_auth.py
  - vk
    - vk_info.py
    - vkbot.py
    - keyboard.py
    - vk_auth.py
  - vkinderdb
    - db_functions.py
    - create_tables.sql

  

### Модуль vkbot.py
>Запускает работу бота, также в модуле определяется класс VkBot реализующий логику взаимодействия с API ВКонтакте, для
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
![Структура таблиц](https://github.com/avshashov/vkinder-team-project/blob/main/vkinderdb/vkinder_scheme.png)
### Используемые библиотеки:
- Библиотека [vk_api](https://pypi.org/project/vk-api/) - основная билиотека для постоения логики и взамодействия с ботом
- Библиотека [requests](https://pypi.org/project/requests/) - используется для HTTP запросов
- Библиотека [psycopg2](https://pypi.org/project/psycopg2/) - используется для взаимодействия с базами данных
- Библиотека [emoji](https://pypi.org/project/emoji/) - для улучшения визуальной соствляющей (добавления эмоджи в кнопки)
