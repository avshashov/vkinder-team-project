from random import randrange
import vk_api
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
from vk_api.longpoll import VkLongPoll, VkEventType
from config import vk_group_token
import emoji
from vktools import Keyboard, Carousel, ButtonColor, Text
import vk_api_info


'''Создаем класс бота'''
class VkBot:
    def __init__(self, vk_group_token):
        self.vk_session = vk_api.VkApi(token=vk_group_token)

    '''Функция создания кнопок клавиатуры бота'''
    def keyboard_bot(self):
        emoji_info_user = emoji.emojize(":check_mark_button:")
        emoji_find_a_couple = emoji.emojize(":couple_with_heart_woman_man:")
        self.button_bot = VkKeyboard(one_time=False)
        name_btn = [f'{emoji_info_user}Заполнить данные о себе!', f'{emoji_find_a_couple}Найти пару!']
        colors_btn = [VkKeyboardColor.PRIMARY, VkKeyboardColor.NEGATIVE]
        for btn, btn_color in zip(name_btn, colors_btn):
            self.button_bot.add_button(btn, btn_color)


    '''Функция по распознованию сообщений и user_id. '''
    def reader(self):
        try:
            for self.event in VkLongPoll(self.vk_session).listen():
                if self.event.type == VkEventType.MESSAGE_NEW and self.event.type == self.event.to_me:
                    self.user_id = self.event.user_id
                    self.text = self.event.text.lower()
        except Exception as ex:
            print(ex)

    def hello(self):
        self.reader()
        if self.text in ['старт', 'начать', 'start']:
            self.sender(self.user_id, "Привет я просто бот!!!")
        elif self.text == 'заполнить данные о себе':
            self.add_info_user()
        elif self.text == 'найти пару':
            self.find_a_couple()

    '''функция ответа на сообщения'''
    def sender(self, user_id, message, keyboard=None):
        self.params = {'user_id': user_id, 'message': message, 'random_id': randrange(10 ** 7),}
        if keyboard != None:
            keyboard = self.keyboard_bot()
            self.params['keyboard'] = keyboard
        self.vk_session.method('messages.send', self.params)

    '''функция заполнения данных о пользователе (взаимодействует с модулем обращений к БД)'''
    def add_info_user(self):#логику нужно доработать
        while True:
            self.sender(self.user_id, 'Ведите имя: ')
            self.reader()
            if self.text != '':
                self.name = self.text
                break
            else:
                print('Ведите имя повторно')
        while True:
            self.sender(self.user_id, 'Ведите фамилию: ')
            self.reader()
            if self.text != '':
                self.lost_name = self.text
                break
            else:
                print('Ведите фамилию повторно')
        while True:
            self.sender(self.user_id, 'Укажите ваш пол: ')
            self.reader()
            if self.text == 'женский' or 'мужской':
                self.gender = self.text
                break
            else:
                print('Ведите данные повторно')
        while True:
            self.sender(self.user_id, 'Ваш возраст(цифрой): ')
            self.reader()
            if self.text.isdigit():
                self.age = self.text
                break
            else:
                print('Ведите данные повторно')
        while True:
            self.sender(self.user_id, 'Ведите название города: ')
            self.reader()
            if self.text != '':
                self.city = self.text
                break
            else:
                print('Ведите город повторно')
        #далее запуск модуля взаимодействия с БД


    '''Функция поиска пары (взаимодействует с модулем обращений к БД)'''
    def find_a_couple(self):
        self.sender(self.user_id, 'Задайте критерии для поиска: ')
        while True:
            self.sender(self.user_id, 'Укажите пол: ')
            self.reader()
            if self.text == 'женский' or 'мужской':
                self.search_gender = self.text
                break
            else:
                print('Ведите данные повторно')
        while True:
            self.sender(self.user_id, 'Возраст(цифрой): ')#доработать логику диапозоном возраста
            self.reader()
            if self.text.isdigit():
                self.search_age = self.text
                break
            else:
                print('Ведите данные повторно')
        while True:
            self.sender(self.user_id, 'Город для поиска: ')
            self.reader()
            if self.text != '':
                self.city = self.text
                break
            else:
                print('Ведите город повторно')
            # далее запуск модуля взаимодействия с БД


    '''Функция добавления в черный список (взаимодействует с модулем обращений к БД)'''
    def add_black_lst(self):
        pass

    '''Функция добавления в избранное (взаимодействует с модулем обращений к БД)'''
    def add_favourites(self):
        pass

    '''Функция получения результатов поиска '''
    def search_result(self):
        search_lst = [] # список id найденных пользователей передается из модуля взаимодействия с БД
        return search_lst




def main():
    vk_client = VkBot(vk_group_token)
    vk_client.reader()



if __name__ == '__main__':
    main()