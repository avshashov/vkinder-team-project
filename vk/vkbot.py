import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_auth import token_group, service_key
from random import randint
from vk_info import VKInfo


class VkBot:
    # def __init__(self, service_token):
    def __init__(self, token_group, service_token):
        self.token_group = token_group
        self.service_token = service_token
        self.vk_session = vk_api.VkApi(token=token_group)

    def bot_session(self):
        longpoll = VkLongPoll(self.vk_session)

        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    if event.text in ('старт', 'Старт', 'start', 'Начать', 'начать'):
                        self._send_message(event.user_id, 'Привет! Я бот для знакомств :)')
                        vk = VKInfo(user_id=event.user_id, access_token=self.service_token)
                        # vk = VKInfo(user_id=event.user_id, access_token=self.token_group)
                        user_data = vk.get_user_info()
                        user_photo = vk.get_photos()

        except Exception as ex:
            print(ex)

    def _send_message(self, user_id, message):
        vk = self.vk_session.get_api()
        vk.messages.send(user_id=user_id, message=message, random_id=randint(1, user_id))


bot = VkBot(token_group, service_key)
bot.bot_session()
