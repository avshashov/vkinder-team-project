from random import randrange
import vk_api
import random
from vk_api.longpoll import VkLongPoll, VkEventType

import vkinderdb.db_functions
from config import vk_group_token
from keyboard import UserKeyboard
from keyboard_setings import keyboard_cmd
from vkinderdb import main, db_functions


'''Создаем класс бота'''
class VkBot:
    def __init__(self, token):
        self.vk_session = vk_api.VkApi(token=vk_group_token)

    '''Функция по распознованию сообщений и user_id. '''

    def get_msg(self, cmd):
        self.msg = f'{random.choice(cmd["out"])} {cmd.get("content")}'
        return self.msg

    '''Функция по распознованию сообщений и событий'''

    def reader(self):
        try:
            for event in VkLongPoll(self.vk_session).listen():
                # обработчик сообщений
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    if event.text != '':
                        self.vk_session.method('messages.send',
                                               {
                                                   'user_id': event.user_id,
                                                   'message': self.get_msg(keyboard_cmd),
                                                   'random_id': randrange(10 ** 7),
                                                   'keyboard': UserKeyboard.get_keyboard(type_keyboard='menu')
                                               }
                                               )
                        vkinderdb.db_functions.VkinderDB.add_new_user(event.user_id)
        except Exception as ex:
            print(ex)

    '''функция ответа на сообщения'''
    def sender(self, user_id, message):
        self.params = {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7)}
        self.vk_session.method('messages.send', self.params)

    '''Функция поиска пары (взаимодействует с модулем обращений к БД)'''
    def find_a_couple(self):
        pass


    '''Функция добавления в черный список (взаимодействует с модулем обращений к БД)'''
    def add_black_lst(self, user_id):
        pass

    '''Функция добавления в избранное (взаимодействует с модулем обращений к БД)'''
    def add_favourites(self):
        pass

    '''Функция получения результатов поиска '''
    def search_result(self):
        # search_lst = [] # список id найденных пользователей передается из модуля взаимодействия с БД
        # return search_lst
        pass



def main():
    vk_client = VkBot(vk_group_token)
    vk_client.reader()



if __name__ == '__main__':
    main()