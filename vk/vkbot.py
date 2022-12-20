from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk.vk_info import VKInfo
from vk.vk_auth import token_group, service_key, user_db, password_db
from keyboard import UserKeyboard
from vkinderdb.db_functions import VkinderDB


class VkBot:
    db = VkinderDB(user=user_db, password=password_db)
    keyboard = UserKeyboard

    def __init__(self, token_group, service_key):
        self.vk_session = vk_api.VkApi(token=token_group)
        self.token_group = token_group
        self.service_key = service_key

    def bot_session(self):
        '''Функция устанавливает сессию и опрашивает longpoll-сервер на предмет новых сообщений.'''

        for event in VkLongPoll(self.vk_session).listen():

            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                self.user_id = event.user_id

                if event.text.lower() in ('старт', 'начать', 'start'):
                    self._sender(user_id=self.user_id, message='Привет. Это бот для знакомств - VKinder!!!',
                                 keyboard=VkBot.keyboard.keyboard_menu())
                    self._add_user_to_db()

                if event.text in ('✅Задать критерии поиска', '🔁Изменить критерии поиска'):
                    self._sender(user_id=self.user_id, message='Введите параметры поиска',
                                 keyboard=VkBot.keyboard.search_ok())
                    self._get_search_params()

                if event.text == '💗Найти пару':
                    self._sender(user_id=self.user_id, message='Начинаем поиск',
                                 keyboard=VkBot.keyboard.keyboard_search())
                    if not VkBot.db.search_params_exists(self.user_id):
                        self._sender(user_id=self.user_id,
                                     message='Параметры поиска не заданы. Нажмите '
                                             'кнопку "Назад", а затем нажмите "Задать '
                                             'критерии поиска"',
                                     keyboard=VkBot.keyboard.keyboard_search())
                        continue

                    else:
                        self._download_pairs_from_db()
                        self._return_pair()

                if event.text == '➡️Следующий':
                    self._return_pair()

                if event.text == '🌟Избранное':
                    self._show_favorites()

                if event.text == '🌟В избранное':
                    VkBot.db.add_to_favorites(self.user_id, self.partner_id)
                    self._sender(user_id=self.user_id, message='Пользователь добавлен в избранное')

                if event.text == '❌Удалить из избранного':
                    self._del_from_favorites()

                if event.text == 'Назад':
                    self._sender(user_id=self.user_id, message='Главное меню', keyboard=VkBot.keyboard.keyboard_menu())

    def _sender(self, user_id, message, keyboard=None, attachment=None):
        '''Функция отправки сообщения пользователю.'''
        sender_params = {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)}
        if keyboard:
            sender_params['keyboard'] = keyboard.get_keyboard()
        self.vk_session.method('messages.send', sender_params)

    def _add_user_to_db(self):
        '''Функция получает информацию (user_id, имя, фамилия, возраст, пол, город, url профиля, фотографии профиля)
         со страницы пользователя и добавляет в базу данных.'''
        handler_info = VKInfo(self.service_key, self.user_id)
        user_data = handler_info.get_user_info()
        photos = handler_info.get_photos()

        if isinstance(user_data, dict):
            VkBot.db.add_new_user(user_data, photos)

        elif user_data == 1:
            vk_error = VkBot(self.token_group, self.service_key)
            vk_error._sender(user_id=self.user_id,
                             message='Для корректной работы приложения сделайте профиль открытым :)')
        elif user_data == 2:
            vk_error = VkBot(self.token_group, self.service_key)
            vk_error._sender(user_id=self.user_id, message='Ошибка получения информации о пользователе.'
                                                           '\nДля корректной работы необходимо в настройках профиля заполнить следующую '
                                                           'информацию: \n\n1) Дата рождения (формат ДД.ММ.ГГГГ); \n2) '
                                                           'Город.')

    def _del_from_favorites(self):
        '''Функция удаления пользователя из избранного.'''
        self._sender(user_id=self.user_id, message='Введите номер пользователя')
        for event in VkLongPoll(self.vk_session).listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                number = event.text
                if number.isdigit() and int(number) in self.favorites_ids:
                    partner_id = int(self.favorites_ids[int(number)])
                    VkBot.db.del_from_favorites(self.user_id, partner_id)
                    self._sender(user_id=self.user_id, message='Пользователь удален из избранного')
                    break
                elif number == 'Назад':
                    break
                else:
                    self._sender(user_id=self.user_id, message='Некорректный ввод. Повторите попытку.')
                    continue

    def _show_favorites(self):
        '''Функция выводит пользователю список избранного.'''
        favorites_users = VkBot.db.show_favorites_users(finder_id=self.user_id)
        if favorites_users:
            self.favorites_ids, string_list_users = {}, []
            for number, user in enumerate(favorites_users, 1):
                self.favorites_ids[number] = user[0]
                string_list_users.append('\n'.join([f'{str(number)}.', *user[1:]]))

            result_favorites = '\n\n'.join(string_list_users)
            self._sender(user_id=self.user_id,
                         message=f'Список избранных пользователей:\n\n{result_favorites}',
                         keyboard=VkBot.keyboard.favorites())

        else:
            self._sender(user_id=self.user_id, message='Список пуст')

    def _get_search_params(self):
        '''Функция получает от пользователя критерии поиска и заносит их в базу данных.'''

        params = {}
        self._sender(user_id=self.user_id, message='Возраст от... (число)')
        for event in VkLongPoll(self.vk_session).listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.text == 'Назад':
                    return
                age_from = event.text
                if age_from.isdigit():
                    age_from = int(age_from)
                    if age_from >= 18:
                        params['from_age'] = age_from
                        break
                    else:
                        self._sender(user_id=self.user_id, message='Пользователь должен быть старше 18, '
                                                                   'повторите попытку.')
                else:
                    self._sender(user_id=self.user_id, message='Некорректный ввод, повторите попытку.')

        self._sender(user_id=self.user_id, message='Возраст до... (число) ')
        for event in VkLongPoll(self.vk_session).listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.text == 'Назад':
                    return
                age_to = event.text
                if age_to.isdigit():
                    age_to = int(age_to)
                    if age_to >= 18:
                        params['to_age'] = age_to
                        break
                    else:
                        self._sender(user_id=self.user_id, message='Пользователь должен быть старше 18, '
                                                                   'повторите попытку.')
                else:
                    self._sender(user_id=self.user_id, message='Некорректный ввод, повторите попытку.')

        self._sender(user_id=self.user_id, message='Пол (женский или мужской)')
        for event in VkLongPoll(self.vk_session).listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.text == 'Назад':
                    return
                gender = event.text.lower()
                if gender in ('женский', 'мужской'):
                    params['sex'] = gender
                    break
                else:
                    self._sender(user_id=self.user_id, message='Некорректный ввод, повторите попытку.')

        self._sender(user_id=self.user_id, message='Город ')
        for event in VkLongPoll(self.vk_session).listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.text == 'Назад':
                    return
                if event.text != '':
                    params['city'] = event.text.title()
                    break
                else:
                    self._sender(user_id=self.user_id, message='Некорректный ввод, повторите попытку.')
        params['user_id'] = self.user_id

        VkBot.db.add_search_params(params=params)
        self._sender(user_id=self.user_id, message='Данные получены, нажмите кнопку "Назад", а затем "Найти пару"!')

    def _download_pairs_from_db(self):
        '''Функция получает из базы данных подхящих под критерии поиска партнеров и создает итератор.'''
        self.pairs = VkBot.db.find_a_couple(self.user_id)
        self.pair_iter = iter([])
        if self.pairs:
            self.pair_iter = iter(self.pairs)

    def _output_pair(self, pair):
        '''Функция выводит пользователю результат поиска пары'''
        user = list(pair)
        message = '\n'.join([str(param) for param in user[1:-1]])
        self._sender(user_id=self.user_id, message=f'💗\n{message}', attachment=user[-1])
        self.partner_id = user[0]

    def _return_pair(self):
        '''Функция получает из итератора партнера и выводит пользователю.'''
        try:
            pair = next(self.pair_iter)
            self._output_pair(pair=pair)

        except StopIteration:
            self._download_pairs_from_db()

            if self.pairs:
                pair = next(self.pair_iter)
                self._output_pair(pair=pair)

            else:
                self._sender(user_id=self.user_id,
                             message='Никто не найден, проверьте корректность критериев поиска и повторите попытку.')

        except AttributeError:
            self._sender(user_id=self.user_id,
                         message='Никто не найден, проверьте корректность критериев поиска и повторите попытку.')


def main():
    vk_client = VkBot(token_group, service_key)
    vk_client.bot_session()


if __name__ == '__main__':
    main()
