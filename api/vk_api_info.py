import vk_api
from config import vk_group_token
import vk_bot

class VkInfo:

    def __init__(self, vk_group_token):
        self.vk_session = vk_api.VkApi(token=vk_group_token)

    '''Функция получения информации о пользоваетеле с его аккаунта ВК'''
    def get_info(self):
        self.id_lst = vk_bot.VkBot.search_result()
        for item in self.id_lst:
            user_ids = item
            self.req = self.vk_session.method('users.get', {
            'user_ids': user_ids,
            'fields': 'screen_name, city, bdate, sex, relation',
            }).json
            self.info_json = self.req['response']
            return self.info_json

    '''Функция получения фото пользователя'''
    def photos_get(self, count=3):
        self.id_lst = vk_bot.VkBot.search_result()
        for item in self.id_lst:
            owner_id = item
            self.req = self.vk_session.method('photos.get', {
                'owner_id': owner_id,
                'album_id': 'profile',
                'count': count,
                'extended': 'likes',
                'photo_sizes': '1',
            }).json
            self.photo_json = self.req['response']['items']
        return self.photo_json

def main():
    vk_info_user = VkInfo(vk_group_token)
    # vk_info_user.photos_get()


if __name__ == '__main__':
    main()