from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api_.vk_info
from config import alt_token, service_key
from keyboard import UserKeyboard
from vkinderdb import main, db_functions



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
                        self.find_users()
                    if self.event.text.lower() in ('✅задать критерии поиска', '🔁изменить критерии поиска'):
                        keyboard = UserKeyboard.search_ok()
                        self.sender(user_id=self.user_id, message='Укажите пол, возраст и город проживания предпологаемой пары:', keyboard=keyboard)
                        self.search_params()
                    if self.event.text.lower() == '🌟избранное':
                        keyboard = UserKeyboard.favorites()
                        self.sender(user_id=self.user_id, message='Список избранных пользователей:', keyboard=keyboard)
                        self.favourites()
                    if self.event.text == '✔Готово!':#разобратся почему не срабатывает этот ключ
                        keyboard = UserKeyboard.keyboard_search()
                        self.sender(user_id=self.user_id, message='Начинаем поиск', keyboard=keyboard)
                        self.find_users()
                    if self.event.text == '➡Следующий':
                        self.sender(user_id=self.user_id, message='', keyboard=keyboard)
                        self.find_users()
                    if self.event.text == '🌟В избранное':
                        self.sender(user_id=self.user_id, message='Добавили в избранное', keyboard=keyboard)
                        self.add_favourites()
                    if self.event.text.lower() == 'назад':
                        keyboard = UserKeyboard.keyboard_menu()
                        self.sender(user_id=self.user_id, message='Главное меню', keyboard=keyboard)



    '''функция ответа на сообщения'''
    def sender(self, user_id, message, keyboard=None):
        self.params = {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)}
        if keyboard != None:
            self.params['keyboard'] = keyboard.get_keyboard()
        self.vk_session.method('messages.send', self.params)

    '''Функция поиска пары (взаимодействует с модулем обращений к БД)'''
    def find_users(self):
        pass
        # keydoard = UserKeyboard.keyboard_search()
        # find_db = db_functions.VkinderDB()
        # users = find_db.find_a_couple(self.user_id)
        # if len(users) > 0:
        #     for user in users:
        #         user = list(user)
        #         self.sender(user_id=self.user_id, message=user[:-1], attachment=user[-1], keyboard=keydoard)



    '''Функция добавления в избранное (взаимодействует с модулем обращений к БД)'''
    def add_favourites(self):
        pass

    '''Функция показа списка избранное (взаимодействует с модулем обращений к БД)'''
    def favourites(self):
        pass

    '''Функция получения настроек поиска '''
    def search_params(self):
        pass

    def new_user(self):
        info_usr = vk_api_.vk_info.VKInfo(service_key, 268278600)
        info_usr.get_user_info()
        info_usr.get_photos()

def main():
    vk_client = VkBot(alt_token, service_key)
    vk_client.launch_bot()



if __name__ == '__main__':
    main()