from random import randrange
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import vk_group_token


'''Создаем класс бота'''
class VkBot:
    def __init__(self, vk_group_token):
        self.vk_session = vk_api.VkApi(token=vk_group_token)

    '''Функция по распознованию сообщений и user_id. '''
    def reader(self):
        try:
            for self.event in VkLongPoll(self.vk_session).listen():
                if self.event.type == VkEventType.MESSAGE_NEW and self.event.to_me:
                    self.user_id = self.event.user_id
                    self.text = self.event.text.lower()
                    if self.text == 'старт':
                        self.sender(self.user_id, "Привет я просто бот!!!")
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