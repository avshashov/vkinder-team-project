from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import vk.vk_info
from vk_auth import alt_token, service_key, user_db, password_db
from keyboard import UserKeyboard
from vkinderdb import main, db_functions
from vkinderdb.db_functions import VkinderDB

'''Создаем класс бота'''
class VkBot:
    def __init__(self, token, service_key):
        self.vk_session = vk_api.VkApi(token=token)
        self.user_id = self.get_user_id()

    def get_user_id(self):
        try:
            for self.event in VkLongPoll(self.vk_session).listen():
                if self.event.type == VkEventType.MESSAGE_NEW and self.event.to_me:
                    return self.event.user_id
        except Exception as ex:
            print(ex)

    '''Функция по распознованию сообщений и событий'''

    def launch_bot(self):
        for self.event in VkLongPoll(self.vk_session).listen():
            if self.user_id:
                if self.event.type == VkEventType.MESSAGE_NEW and self.event.to_me:
                    # Если пришло новое сообщение
                    if self.event.text.lower() == 'старт':
                        keyboard = UserKeyboard.keyboard_menu()
                        self.sender(user_id=self.user_id, message='Привет это бот VKinder!!!', keyboard=keyboard)
                        self.new_user()
                    if self.event.text.lower() == '💗найти пару':
                        keyboard = UserKeyboard.keyboard_search()
                        self.sender(user_id=self.user_id, message='Начинаем поиск', keyboard=keyboard)
                        self._check_search_params(self.user_id)
                        self.find_users()
                    if self.event.text.lower() in ('✅задать критерии поиска', '🔁изменить критерии поиска'):
                        keyboard = UserKeyboard.search_ok()
                        self.sender(user_id=self.user_id, message='Введите параметры поиска', keyboard=keyboard)
                        self.search_params()
                    if self.event.text.lower() == '🌟избранное':
                        keyboard = UserKeyboard.favorites()
                        self.sender(user_id=self.user_id, message='Список избранных пользователей:', keyboard=keyboard)
                        self.favourites()
                    if self.event.text == '➡Следующий':
                        self.sender(user_id=self.user_id, message='', keyboard=keyboard)
                        self._return_pair(self.user_id)
                    if self.event.text == '🌟В избранное':
                        self.sender(user_id=self.user_id, message='Добавили в избранное', keyboard=keyboard)
                        self.add_favourites()
                    if self.event.text.lower() == 'назад':
                        keyboard = UserKeyboard.keyboard_menu()
                        self.sender(user_id=self.user_id, message='Главное меню', keyboard=keyboard)
                    if self.event.text == '❌Удалить из избранного':
                        self.sender(user_id=self.user_id, message='Удалили', keyboard=keyboard)
                        self.del_favourites()


    '''функция ответа на сообщения'''
    def sender(self, user_id, message, keyboard=None, attachment=None):
        self.params = {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)}
        if keyboard != None:
            self.params['keyboard'] = keyboard.get_keyboard()
        self.vk_session.method('messages.send', self.params)


    '''Функция добавления в избранное (взаимодействует с модулем обращений к БД)'''
    def add_favourites(self):
        db = VkinderDB(user=user_db, password=password_db)
        db.add_to_favorites(self.user_id, self.partner_id)

    '''Функция удаления из избранного (взаимодействует с модулем обращений к БД)'''
    def del_favourites(self):
        pass

    '''Функция показа списка избранное (взаимодействует с модулем обращений к БД)'''
    def favourites(self):
        show_favourites = db_functions.VkinderDB(user=user_db, password=password_db)
        favourites_users = show_favourites.show_favorites_users(finder_id=self.user_id)
        if len(favourites_users) > 0:
            result = ','.join([','.join(list(user)) for user in favourites_users])
            keyboard = UserKeyboard.favorites()
            self.sender(user_id=self.user_id, message=result, keyboard=keyboard)
        else:
            self.sender(user_id=self.user_id, message='Список пуст')
        # pass




    '''Проверить наличие параметров поиска в БД'''
    def _check_search_params(self, user_id):
        if not VkinderDB(user_db, password_db).search_params_exists(user_id):
            self.sender(user_id=self.user_id, message='Задайте параметры поиска')
        return


    '''Функция получения настроек поиска '''
    def search_params(self):
        params = {}
        self.sender(user_id=self.user_id, message='Возраст от... (число)')
        for self.event in VkLongPoll(self.vk_session).listen():
            if self.event.type == VkEventType.MESSAGE_NEW and self.event.to_me:
                age_from = self.event.text
                if age_from.isdigit():
                    age_from = int(age_from)
                    if age_from >= 18:
                        params['from_age'] = age_from
                        break
                else:
                    self.sender(user_id=self.user_id, message='Некорректный ввод, повторите попытку.')

        self.sender(user_id=self.user_id, message='Возраст до... (число) ')
        for self.event in VkLongPoll(self.vk_session).listen():
            if self.event.type == VkEventType.MESSAGE_NEW and self.event.to_me:
                age_to = self.event.text
                if age_to.isdigit():
                    age_to = int(age_to)
                    if age_to >= 18:
                        params['to_age'] = age_to
                        break
                else:
                    self.sender(user_id=self.user_id, message='Некорректный ввод, повторите попытку.')

        self.sender(user_id=self.user_id, message='Пол (женский или мужской)')
        for self.event in VkLongPoll(self.vk_session).listen():
            if self.event.type == VkEventType.MESSAGE_NEW and self.event.to_me:
                gender = self.event.text.lower()
                if gender in ['женский', 'мужской']:
                    params['sex'] = gender
                    break
                else:
                    self.sender(user_id=self.user_id, message='Некорректный ввод, повторите попытку.')

        self.sender(user_id=self.user_id, message='Город ')
        for self.event in VkLongPoll(self.vk_session).listen():
            if self.event.type == VkEventType.MESSAGE_NEW and self.event.to_me:
                if self.event.text != '':
                    params['city'] = self.event.text.title()
                    break
                else:
                    self.sender(user_id=self.user_id, message='Некорректный ввод, повторите попытку.')
        params['user_id'] = self.user_id

        params_db = db_functions.VkinderDB(user=user_db, password=password_db)
        params_db.add_search_params(params=params)
        self.sender(user_id=self.user_id, message='Данные получены, нажмите кнопку "Назад", а затем "Найти пару"!')
        self._download_pairs(self.user_id)

    def _return_pair(self, user_id):
        try:
            pair = next(self.pair_iter)
            print(pair)
            if len(pair) > 0:
                user = list(pair)
                self.sender(user_id=self.user_id, message=user[1:-1], attachment=user[-1])
                self.partner_id = user[0]
            else:
                self.sender(user_id=self.user_id,
                            message='Никто не найден, проверьте корректность критериев поиска и повторите попытку.')
        except StopIteration:
            self._download_pairs(user_id)
            pair = next(self.pair_iter)
            if len(pair) > 0:
                user = list(pair)
                self.sender(user_id=self.user_id, message=user[1:-1], attachment=user[-1])
                self.partner_id = user[0]
            else:
                self.sender(user_id=self.user_id, message='Никто не найден, проверьте корректность критериев поиска и повторите попытку.')
            print(pair)

    def _download_pairs(self, user_id):
        # Функция должна быть внутри search_params()
        db = VkinderDB(user_db, password_db)
        self.pairs = db.find_a_couple(user_id)
        self.pair_iter = iter(self.pairs)

    def new_user(self):
        info_usr = vk.vk_info.VKInfo(service_key, self.user_id)
        user_data = info_usr.get_user_info()
        photos = info_usr.get_photos()
        # params_db = db_functions.VkinderDB(user=user_db, password=password_db)
        # params_db.add_new_user(user_data, photos)





def main():
    vk_client = VkBot(alt_token, service_key)
    vk_client.launch_bot()



if __name__ == '__main__':
    main()