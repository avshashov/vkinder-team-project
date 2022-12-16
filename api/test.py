from random import randrange
import vk_api
import random
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_auth import vk_group_token, gr_token
from keyboard import UserKeyboard
from keyboard_setings import keyboard_cmd



'''Создаем класс бота'''
class VkBot:
    def __init__(self, token):
        self.vk_session = vk_api.VkApi(token=gr_token)

    def reader(self):
        try:
            for event in VkLongPoll(self.vk_session).listen():
                # обработчик сообщений
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    if event.text == 'старт':
                        self.sender(event.user_id, 'Ghbdtn', UserKeyboard.get_keyboard(type_keyboard='menu'))
                        # vk_api_.vk_info.VKInfo.get_user_info()
        except Exception as ex:
            print(ex)



def main():
    vk_client = VkBot(gr_token)
    vk_client.reader()



if __name__ == '__main__':
    main()