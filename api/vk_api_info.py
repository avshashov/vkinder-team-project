import vk_api
from config import vk_group_token
import vk_bot
import requests

class VkInfo:

    def __init__(self, vk_group_token):
        self.vk_session = vk_api.VkApi(token=vk_group_token)

    '''Функция получения информации о пользоваетеле с его аккаунта ВК'''
    def get_info(self):
        try:
            self.id_lst = vk_bot.VkBot.search_result()
            for item in self.id_lst:
                user_ids = item
                self.req = self.vk_session.method('users.get', {
                'user_ids': user_ids,
                'fields': 'screen_name, city, bdata, sex, relation',
                }).json
                self.info_json = self.req['response']
            return self.info_json
        except Exception as ex:
            print(ex)

    '''Функция получения фото пользователя'''
    def photos_get(self, count=3):
        try:
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
        except Exception as ex:
            print(ex)


    '''Фуекция обрабатывает полученные из функций photos_get и get_info данные'''
    def get_user_data(self):
        attachments = []
        content = ''
        self.id_lst = vk_bot.VkBot.search_result()
        for id_ in self.id_lst:
            params = self.get_info()
            if params:
                if params.get('city'):
                    city = params.get('city').get('title')
                if params.get('bdate'):
                    bdata = params.get('bdate')
                content = f'\n[id{id_}|{params.get("first_name")} {params.get("last_name")}] {city} {bdata}'
                photos = self.photos_get(3)
                if photos.get('response') is not None:
                    items = photos['response']['items']
                    for item in items:
                        attachments.append(f'photo{id_}_{item.get("id")}')
            return [','.join(attachments), content]

def main():
    vk_info_user = VkInfo(vk_group_token)
    # vk_info_user.photos_get()


if __name__ == '__main__':
    main()