import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from config import vk_group_token
import vk_bot

class VkInfo:
    def __init__(self, vk_group_token):
        self.vk_session = vk_api.VkApi(token=vk_group_token)

    def photos_get(self, count=10):
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
            self.req_json = self.req['response']['items']
        return self.req_json

def main():
    vk_info_user = VkInfo(vk_group_token)
    vk_info_user.photos_get()


if __name__ == '__main__':
    main()