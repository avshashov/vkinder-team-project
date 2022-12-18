from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import emoji

settings = dict(one_time=False, inline=False)

class UserKeyboard:

    def __init__(self):
        pass

    @staticmethod
    def keyboard_menu():
        search = emoji.emojize(":growing_heart:")
        star = emoji.emojize(":glowing_star:")
        check = emoji.emojize(":check_mark_button:")
        keyboard = VkKeyboard(**settings)
        keyboard.add_button(label=f'{check}Задать критерии поиска', color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
        keyboard.add_button(label=f'{search}Найти пару', color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
        keyboard.add_button(label=f'{star}Избранное', color=VkKeyboardColor.POSITIVE)
        return keyboard

    @staticmethod
    def keyboard_search():
        right_arrow = emoji.emojize(":right_arrow:")
        star = emoji.emojize(":glowing_star:")
        keyboard = VkKeyboard(**settings)
        keyboard.add_button(label=f'{right_arrow}Следующий', color=VkKeyboardColor.PRIMARY)
        keyboard.add_line()
        keyboard.add_button(label=f'{star}В избранное', color=VkKeyboardColor.POSITIVE)
        keyboard.add_line()
        keyboard.add_button(label='Назад', color=VkKeyboardColor.SECONDARY)
        return keyboard

    @staticmethod
    def favorites():
        check_mark = emoji.emojize(":cross_mark:")
        keyboard = VkKeyboard(**settings)
        # keyboard.add_button(label=f'{check_mark}Удалить из избранного', color=VkKeyboardColor.PRIMARY)
        # keyboard.add_line()
        keyboard.add_button(label='Назад', color=VkKeyboardColor.SECONDARY)
        return keyboard

    @staticmethod
    def search_ok():
        repeat = emoji.emojize(":repeat_button:")
        keyboard = VkKeyboard(**settings)
        keyboard.add_button(label='Назад', color=VkKeyboardColor.SECONDARY)
        keyboard.add_line()
        keyboard.add_button(label=f'{repeat}Изменить критерии поиска', color=VkKeyboardColor.SECONDARY)
        return keyboard
