from random import randint
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_auth import token_group, service_key, user_db, password_db
from vk_info import VKInfo
from vkinderdb.db_functions import VkinderDB


class VkBot:
    def __init__(self, token_group, service_token, user_db, password_db):
        self.token_group = token_group
        self.service_token = service_token
        self.user_db = user_db
        self.password_db = password_db
        self.vk_session = vk_api.VkApi(token=token_group)

    def bot_session(self):
        longpoll = VkLongPoll(self.vk_session)

        try:
            for event in longpoll.listen():
                if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                    if event.text.lower() in ('старт', 'start', 'начать'):
                        self._send_message(event.user_id, 'Привет! Я бот для знакомств :)')
                        vk = VKInfo(user_id=event.user_id, access_token=self.service_token)
                        user_data = vk.get_user_info()
                        user_photo = vk.get_photos()

                        db = VkinderDB(self.user_db, self.password_db)
                        db.add_new_user(user_data, user_photo)

        except Exception as ex:
            print(ex)

    def _send_message(self, user_id, message):
        '''Отправить текстовое сообщение'''
        session = self.vk_session.get_api()
        session.messages.send(user_id=user_id, message=message, random_id=randint(1, user_id))

    def _check_search_params(self, user_id):
        '''Проверить наличие параметров поиска в БД'''
        if not VkinderDB(self.user_db, self.password_db).search_params_exists(user_id):
            pass
        return


bot = VkBot(token_group, service_key, user_db, password_db)
bot.bot_session()
