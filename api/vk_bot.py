from random import randrange
import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api_.vk_info
import vkinderdb.db_functions
from config import vk_group_token, gr_token
from keyboard import UserKeyboard
from keyboard_setings import keyboard_cmd, callback_typs
from vkinderdb import main, db_functions



'''Создаем класс бота'''
class VkBot:
    def __init__(self, token):
        self.vk_session = vk_api.VkApi(token=token)

    def get_user_id(self):
        try:
            for self.event in VkLongPoll(self.vk_session).listen():
                if self.event.type == VkEventType.MESSAGE_NEW and self.event.to_me:
                    self.user_id = self.event.user_id
                    return self.user_id
        except Exception as ex:
            print(ex)

    '''Функция по распознованию сообщений и событий'''

    def launch_bot(self):
        for self.event in VkLongPoll(self.vk_session).listen():
            self.user_id = self.get_user_id()
            if self.user_id:
                if self.event.type == VkEventType.MESSAGE_NEW:
                    # Если пришло новое сообщение
                    if self.event.text != '':
                        if self.event.from_user:
                            keyboard = UserKeyboard.keyboard_menu()
                            self.sender(user_id=self.user_id, message='Привет это бот VKinder!!!', keyboard=keyboard)
                            self.command_button()
                if self.event.type == VkBotEventType.MESSAGE_EVENT:
                    if self.object.payload.get('type') in callback_typs:
                        if self.event.object.payload.get('type') == 'show_snackbar':
                            if 'черный' in self.event.object.payload.get('text'):
                                self.add_black_list(self.event.object.user_id)
                            elif 'избранное' in self.event.object.payload.get('text'):
                                self.add_favourites(self.event.object.user_id)
    def command_button(self):
        key = keyboard_cmd.get('key')
        if key == 'search':
            keyboard = UserKeyboard.keyboard_search()
            self.vk_session.method('messages.sendMessageEventAnswer', {
                'event_id': str,
                'user_id': self.get_user_id(),
                'peer_id': int
            })
            self.find_a_couple()



    '''функция ответа на сообщения'''
    def sender(self, user_id, message, keyboard=None):
        self.params = {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)}
        if keyboard != None:
            self.params['keyboard'] = keyboard.get_keyboard()
        self.vk_session.method('messages.send', self.params)

    '''Функция поиска пары (взаимодействует с модулем обращений к БД)'''
    def find_a_couple(self):
        pass


    '''Функция добавления в черный список (взаимодействует с модулем обращений к БД)'''
    def add_black_lst(self, user_id):
        pass

    '''Функция добавления в избранное (взаимодействует с модулем обращений к БД)'''
    def add_favourites(self, user_id):
        pass

    '''Функция получения результатов поиска '''
    def search_result(self):
        pass



def main():
    vk_client = VkBot(gr_token)
    vk_client.launch_bot()



if __name__ == '__main__':
    main()