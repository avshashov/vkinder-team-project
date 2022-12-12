from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import emoji
from api.keyboard_setings import settings

class UserKeyboard:

    def __init__(self):
        pass

    @staticmethod
    def keyboard_menu():

        search = emoji.emojize(":growing_heart:")
        star = emoji.emojize(":glowing_star:")
        black_lst = emoji.emojize(":black_nib:")
        keyboard = VkKeyboard(**settings)
        keyboard.add_callback_button(label=f'{search}Поиск', color=VkKeyboardColor.POSITIVE, payload={"type": "search", "text": "Ищем"})
        keyboard.add_line()
        keyboard.add_callback_button(label=f'{star}Избранное', color=VkKeyboardColor.POSITIVE, payload={"type": "favorites", "text": "Избранное"})
        keyboard.add_callback_button(label=f'{black_lst}Чёрный список', color=VkKeyboardColor.POSITIVE, payload={"type": "black_list", "text": "Черный список"})
        keyboard.add_line()
        keyboard.add_callback_button(label='Меню', color=VkKeyboardColor.NEGATIVE, payload={"type": "menu"})
        return keyboard

    @staticmethod
    def keyboard_search():
        left_arrow = emoji.emojize(":left_arrow:")
        right_arrow = emoji.emojize(":left_arrow:")
        star = emoji.emojize(":glowing_star:")
        black_lst = emoji.emojize(":black_nib:")
        keyboard = VkKeyboard(**settings)
        keyboard.add_callback_button(label=f'{left_arrow}Предыдущий', color=VkKeyboardColor.PRIMARY, payload={"type": "previous", "text": "Ищем"})
        keyboard.add_line()
        keyboard.add_callback_button(label=f'{right_arrow}Следующий', color=VkKeyboardColor.PRIMARY, payload={"type": "next", "text": "Ищем"})
        keyboard.add_callback_button(label=f'{star}В избранное', color=VkKeyboardColor.POSITIVE, payload={"type": "in_favorites", "text": "Добавлено"})
        keyboard.add_callback_button(label=f'{black_lst}В чёрный список', color=VkKeyboardColor.SECONDARY, payload={"type": "in_black_lst", "text": "Добавлено"})
        keyboard.add_line()
        keyboard.add_callback_button(label='Меню', color=VkKeyboardColor.NEGATIVE, payload={"type": "menu"})
        return keyboard

    @staticmethod
    def get_keyboard(type_keyboard: str):
        if type_keyboard == 'menu':
            keyboard = UserKeyboard.menu()
        elif type_keyboard == 'search':
            keyboard = UserKeyboard.search()
        else:
            keyboard = UserKeyboard.menu()
        return keyboard.get_keyboard()