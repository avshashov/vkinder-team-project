from random import randrange
import vk_api
import random
from vk_api.longpoll import VkLongPoll, VkEventType
from config import vk_group_token, gr_token
from keyboard import UserKeyboard
from keyboard_setings import keyboard_cmd



'''Создаем класс бота'''
class VkBot:
    def __init__(self, token):
        self.vk_session = vk_api.VkApi(token=gr_token)

    def get_msg(self, cmd):
        self.msg = f'{random.choice(cmd["out"])} {cmd.get("content")}'
        return self.msg

    '''Функция по распознованию сообщений и событий'''
    def reader(self):
        try:
            for event in VkLongPoll(self.vk_session).listen():
                #обработчик сообщений
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
        except Exception as ex:
            print(ex)



def main():
    vk_client = VkBot(gr_token)
    vk_client.reader()



if __name__ == '__main__':
    main()