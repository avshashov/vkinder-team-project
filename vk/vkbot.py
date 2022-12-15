import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_auth import token_group
from random import randint


class VkBot:
    def __init__(self, token_group):
        self.vk_session = vk_api.VkApi(token=token_group)

    def bot_session(self):
        longpoll = VkLongPoll(self.vk_session)

        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    if event.text in ('старт', 'Старт', 'start', 'Начать', 'начать'):
                        self._send_message(event.user_id, 'Привет! Я бот для знакомств :)')


        except Exception as ex:
            print(ex)

    def _send_message(self, user_id, message):
        vk = self.vk_session.get_api()
        vk.messages.send(user_id=user_id, message=message, random_id=randint(1, user_id))


bot = VkBot(token_group)
bot.bot_session()
