# Командный проект по курсу «Профессиональная работа с Python»

## VKinder

### Установка
Перед запуском нужно создать файл в корневом каталоге проекта. В котором будут храниться: сервисный токен ВК (service_key), токен группы ВК (token_group), пользователь базы данных (user_db), пароль базы данных (password_db) 

- Сервисный токен, инструкция получения https://dev.vk.com/mini-apps/management/settings 
- Токен группы, инструкция получения https://dev.vk.com/api/access-token/implicit-flow-community

### Цель проекта

Разработать программу-бота для взаимодействия с базами данных и социальной сетью. Бот будет подбирать пару пользователю для знакомств в социальной сети Вконтакте на основании его предпочтений.

Выполненные задачи:
- Спроектирована база данных (БД) для программы
- Создано [сообщество ВК](https://vk.com/club217757110) с интегрированным в чаты ботом
- Разработана программа-бота на Python с алгоритмом:
1. Используя информацию (возраст, пол, город) о пользователе, который общается с ботом в ВК, производится поиск других людей (пользователей) для знакомств.
2. У тех людей, которые подошли под критерии поиска, алгоритм получает три самые популярные фотографии в профиле. Популярность определяется по количеству лайков.
3. Выводит в чат с ботом информацию о пользователе в формате: ФИО, возраст, ссылка, фото.
4. Реализовано меню "Следующий".
5. Реализованы кнопки "Добавить в избранное", "Удалить из избранного" и "Показать избранное".
6. Созданы кнопки в чате для взаимодействия с ботом.

## Логика проекта
- Чаты [сообщества ВК](https://vk.com/club217757110) интегрированны с ботом.
После того, как пользователь заходит в чат, вся нужная информация(фамилия, имя, возраст, пол, город) парсится с его аккаунта и попадает в отдельную таблицу
базы данных. Любой польователь, попавший в это таблицу, может как находить других пользователей, так и быть найденным.
- Далее, после нажатия пользователем кнопки "Задать критерии поиска", ему предлагается поочередно ввести критерии поиска (возраст от, возраст до, пол, город). Эти данные сохраняются в отдельную таблицу базы данных с привязкой к этому пользователю по user_id.
- После ввода критериев поиска пользователь может изменить заданные параметры поиска, либо приступить к поиску, нажав кнопку "Найти пару".
После нажатия на эту кнопку происходит поиск по заданным параметрам в **ТАБЛИЦЕ ПОЛЬЗОВАТЕЛЕЙ В БАЗЕ ДАННЫХ**.
- Результаты поиска выводятся по одному на экран в формате: имя, фамилия, пол, возраст, ссылка на профиль, 3 фото профиля с наибольшим количеством лайков.
У пользователя есть возможность добавить результат поиска в избранное, посмотреть весь список избранного и удалить любого пользователя из этого списка. 

## Техническое описание проекта

### Структура каталога проекта

- requirements.txt
- README.md
  - vk
    - vk_info.py
    - vkbot.py
    - keyboard.py
  - vkinderdb
    - db_functions.py
    - create_tables.sql

  

### Модуль vkbot.py
>Запускает работу бота. В модуле определяется класс VkBot, реализующий логику взаимодействия с API ВКонтакте.
### Модуль keyboard.py
>Определяет вспомогательный класс UserKeyboard: задает в чате кнопки для взаимодействия пользователя с ботом.
### Модуль vk_info.py
>Определяет класс VKInfo, реализующий логику получения информации о пользователе при взаимодействии с API ВКонтакте.
### Модуль db_functions.py
>Определяет класс VkinderDB, содержащий функции взаимодействия бота с базами данных.
### Скрипт create_tables.sql
>Содержит инициализации базы данных проекта.


## Структура таблиц
![Структура таблиц](https://github.com/avshashov/vkinder-team-project/blob/main/vkinderdb/vkinder_scheme.png)
### Используемые библиотеки:
- Библиотека [vk_api](https://pypi.org/project/vk-api/) - основная библиотека для построения логики и взамодействия с ботом.
- Библиотека [requests](https://pypi.org/project/requests/) - используется для работы с HTTP запросами.
- Библиотека [psycopg2](https://pypi.org/project/psycopg2/) - используется для работы с PostgreSQL.
- Библиотека [emoji](https://pypi.org/project/emoji/) - для улучшения визуальной соствляющей (добавления эмоджи в кнопки).
