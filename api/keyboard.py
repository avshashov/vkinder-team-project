from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import emoji

class UserKeyboard:

    def __init__(self):
        print('init')

    @staticmethod
    def keyboard_menu():

        keyboard = VkKeyboard()
        keyboard.add_button(label='Поиск', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(label='Избранное', color=VkKeyboardColor.POSITIVE)
        keyboard.add_button(label='Чёрный список', color=VkKeyboardColor.POSITIVE)
        return keyboard

    @staticmethod
    def keyboard_search():
        pass
