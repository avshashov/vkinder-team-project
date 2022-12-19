from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk.vk_info import VKInfo
from vk.vk_auth import token_group, service_key, user_db, password_db
from keyboard import UserKeyboard
from vkinderdb.db_functions import VkinderDB


class VkBot:
    db = VkinderDB(user=user_db, password=password_db)

    def __init__(self, token, service_key):
        self.vk_session = vk_api.VkApi(token=token)

    def bot_session(self):
        '''Функция по распознаванию сообщений и событий'''

        for event in VkLongPoll(self.vk_session).listen():

            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                self.user_id = event.user_id

                if event.text.lower() in ('старт', 'начать', 'start'):
                    keyboard = UserKeyboard.keyboard_menu()
                    self.sender(user_id=self.user_id, message='Привет. Это бот для знакомств - VKinder!!!',
                                keyboard=keyboard)
                    self.new_user()

                if event.text.lower() in ('✅задать критерии поиска', '🔁изменить критерии поиска'):
                    keyboard = UserKeyboard.search_ok()
                    self.sender(user_id=self.user_id, message='Введите параметры поиска', keyboard=keyboard)
                    self.search_params()

                if event.text.lower() == '💗найти пару':
                    keyboard = UserKeyboard.keyboard_search()
                    self.sender(user_id=self.user_id, message='Начинаем поиск', keyboard=keyboard)
                    if self._check_search_params(self.user_id):
                        self.sender(user_id=self.user_id, message='Параметры поиска не заданы. Нажмите'
                                                                  'кнопку "Назад", а затем нажмите "Задать'
                                                                  'критерии поиска"',
                                    keyboard=keyboard)
                        continue

                    else:
                        self._download_pairs()
                        self._return_pair()

                if event.text == 'Следующий':
                    if self.pairs is None:
                        self.sender(user_id=self.user_id,
                                    message='Никто не найден, проверьте корректность критериев поиска и повторите попытку.')
                        continue
                    self.sender(user_id=self.user_id, message='💗')
                    self._return_pair()

                if event.text.lower() == '🌟избранное':
                    keyboard = UserKeyboard.favorites()
                    self.sender(user_id=self.user_id, message='Список избранных пользователей:', keyboard=keyboard)
                    self.show_favourites()

                if event.text == '🌟В избранное':
                    self.sender(user_id=self.user_id, message='Пользователь добавлен в избранное', keyboard=keyboard)
                    self.add_favourites()

                # if event.text == '❌Удалить из избранного':
                #     self.sender(user_id=self.user_id, message='Пользователь удален из избранного', keyboard=keyboard)
                #     self.del_favourites()

                if event.text.lower() == 'назад':
                    keyboard = UserKeyboard.keyboard_menu()
                    self.sender(user_id=self.user_id, message='Главное меню', keyboard=keyboard)

    def sender(self, user_id, message, keyboard=None, attachment=None):
        '''Функция ответа на сообщения'''
        self.params = {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)}

        if keyboard:
            self.params['keyboard'] = keyboard.get_keyboard()
        self.vk_session.method('messages.send', self.params)

    def new_user(self):
        info_user = VKInfo(service_key, self.user_id)
        user_data = info_user.get_user_info()
        photos = info_user.get_photos()

        if isinstance(user_data, dict):
            VkBot.db.add_new_user(user_data, photos)

        elif user_data == 1:
            vk_error = VkBot(token_group, service_key)
            vk_error.sender(user_id=self.user_id,
                            message='Для корректной работы приложения сделайте профиль открытым :)')
        elif user_data == 2:
            vk_error = VkBot(token_group, service_key)
            vk_error.sender(user_id=self.user_id, message='Ошибка получения информации о пользователе.'
                                                          '\nДля корректной работы необходимо в настройках профиля заполнить следующую '
                                                          'информацию: \n\n1) Дата рождения (формат ДД.ММ.ГГГГ); \n2) '
                                                          'Город.')

    def add_favourites(self):
        '''Функция добавления в избранное (взаимодействует с модулем обращений к БД)'''
        VkBot.db.add_to_favorites(self.user_id, self.partner_id)

    def show_favourites(self):
        '''Функция показа списка избранное (взаимодействует с модулем обращений к БД)'''
        favourites_users = VkBot.db.show_favorites_users(finder_id=self.user_id)
        if favourites_users:
            result = '\n\n'.join(['\n'.join(list(user)) for user in favourites_users])
            keyboard = UserKeyboard.favorites()
            self.sender(user_id=self.user_id, message=result, keyboard=keyboard)
        else:
            self.sender(user_id=self.user_id, message='Список пуст')

    def _check_search_params(self, user_id):
        '''Проверить наличие параметров поиска в БД'''

        if not VkBot.db.search_params_exists(user_id):
            self.sender(user_id=self.user_id, message='Задайте параметры поиска')
        return

    def search_params(self):
        '''Функция получения настроек поиска '''

        params = {}
        self.sender(user_id=self.user_id, message='Возраст от... (число)')
        for event in VkLongPoll(self.vk_session).listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                age_from = event.text
                if age_from.isdigit():
                    age_from = int(age_from)
                    if age_from >= 18:
                        params['from_age'] = age_from
                        break
                    else:
                        self.sender(user_id=self.user_id, message='Пользователь должен быть старше 18, '
                                                                  'повторите попытку.')
                else:
                    self.sender(user_id=self.user_id, message='Некорректный ввод, повторите попытку.')

        self.sender(user_id=self.user_id, message='Возраст до... (число) ')
        for event in VkLongPoll(self.vk_session).listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                age_to = event.text
                if age_to.isdigit():
                    age_to = int(age_to)
                    if age_to >= 18:
                        params['to_age'] = age_to
                        break
                    else:
                        self.sender(user_id=self.user_id, message='Пользователь должен быть старше 18, '
                                                                  'повторите попытку.')
                else:
                    self.sender(user_id=self.user_id, message='Некорректный ввод, повторите попытку.')

        self.sender(user_id=self.user_id, message='Пол (женский или мужской)')
        for event in VkLongPoll(self.vk_session).listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                gender = event.text.lower()
                if gender in ('женский', 'мужской'):
                    params['sex'] = gender
                    break
                else:
                    self.sender(user_id=self.user_id, message='Некорректный ввод, повторите попытку.')

        self.sender(user_id=self.user_id, message='Город ')
        for event in VkLongPoll(self.vk_session).listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                if event.text != '':
                    params['city'] = event.text.title()
                    break
                else:
                    self.sender(user_id=self.user_id, message='Некорректный ввод, повторите попытку.')
        params['user_id'] = self.user_id

        VkBot.db.add_search_params(params=params)
        self.sender(user_id=self.user_id, message='Данные получены, нажмите кнопку "Назад", а затем "Найти пару"!')

    def _return_pair(self):
        try:
            pair = next(self.pair_iter)
            user = list(pair)
            message = '\n'.join([str(param) for param in user[1:-1]])
            self.sender(user_id=self.user_id, message=message, attachment=user[-1])
            self.partner_id = user[0]

        except StopIteration:
            self._download_pairs()

            if self.pairs:
                pair = next(self.pair_iter)
                user = list(pair)
                message = '\n'.join([str(param) for param in user[1:-1]])
                self.sender(user_id=self.user_id, message=message, attachment=user[-1])
                self.partner_id = user[0]
            else:
                self.sender(user_id=self.user_id,
                            message='Никто не найден, проверьте корректность критериев поиска и повторите попытку.')

        except AttributeError:
            self.sender(user_id=self.user_id,
                        message='Никто не найден, проверьте корректность критериев поиска и повторите попытку.')

    def _download_pairs(self):
        self.pairs = VkBot.db.find_a_couple(self.user_id)
        self.pair_iter = iter([])
        if self.pairs:
            self.pair_iter = iter(self.pairs)


def main():
    vk_client = VkBot(token_group, service_key)
    vk_client.bot_session()


if __name__ == '__main__':
    main()
