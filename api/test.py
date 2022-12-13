from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import vk_group_token, group_id
from keyboard import UserKeyboard
from keyboard_setings import keyboard_cmd



'''Создаем класс бота'''
class VkBot:
    def __init__(self, vk_group_token):
        self.vk_session = vk_api.VkApi(token=vk_group_token)

    '''Функция по распознованию сообщений и событий'''
    def reader(self):
        try:
            for event in VkLongPoll(self.vk_session, group_id=group_id).listen():
                #обработчик сообщений
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    if event.text != '':
                        self.vk_session.method('messages.send',
                                               {
                                                   'user_id': event.user_id,
                                                   'message': 'Меню бота!',
                                                   'random_id': randrange(10 ** 7),
                                                   'keyboard': UserKeyboard.get_keyboard(type_keyboard='menu')
                                               }
                                               )

                    elif event.text in keyboard_cmd['search']['in']:
                        self.vk_session.method('messages.send',
                                               {
                                                   'user_id': event.user_id,
                                                   'message': "Нашли!\n",
                                                   'random_id': randrange(10 ** 7),
                                                   'keyboard': UserKeyboard.get_keyboard(type_keyboard='search')
                                               }
                                               )

        except Exception as ex:
            print(ex)



def main():
    vk_client = VkBot(vk_group_token)
    vk_client.reader()



if __name__ == '__main__':
    main()