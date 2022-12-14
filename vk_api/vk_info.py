from datetime import datetime
import requests
from vk_auth import TOKEN


class VKInfo:

    def __init__(self, access_token, user_id):
        self.token = access_token
        self.id = user_id
        self.params = {'access_token': self.token, 'v': 5.131}

    def get_user_info(self):
        url = 'https://api.vk.com/method/users.get'
        user_params = {'user_ids': self.id, 'fields': 'bdate, city, sex'}

        try:
            user_json = requests.get(url, params={**self.params, **user_params}).json()

            if self._profile_is_closed(user_json):
                print('[ERROR] Для корректной работы приложения сделайте профиль открытым :)')

            else:
                user_id = user_json['response'][0]['id']
                name = user_json['response'][0]['first_name']
                surname = user_json['response'][0]['last_name']
                sex = 'Женский' if user_json['response'][0]['sex'] == 1 else 'Мужской'
                city = self._parse_city(user_json)
                url = f'https://vk.com/id{user_json["response"][0]["id"]}'
                age = self._age_format(self._parse_bdate(user_json))

                user_data = {
                    'user_id:': user_id, 'name': name,
                    'surname': surname, 'sex': sex,
                    'age': age, 'city': city,
                    'url': url
                }
                print('[INFO] Информация о профиле получена.')
                print(user_data)  # Удалить строку
                return user_data

        except Exception as ex:
            print(f'[ERROR] {ex}')

    def _parse_bdate(self, user_json):
        try:
            bdate = datetime.strptime(user_json['response'][0]['bdate'], '%d.%m.%Y')
            return bdate
        except:
            print('[ERROR] В профиле пользователя скрыт один из параметров: дата/год рождения.')

    def _age_format(self, bdate):
        if bdate:
            age = int((datetime.now() - bdate).days / 365)
            return age
        raise ValueError

    def _profile_is_closed(self, user_json):
        return user_json['response'][0]['is_closed']

    def _parse_city(self, user_json):
        try:
            city = user_json['response'][0]['city']['title']
            return city
        except:
            print('[ERROR] В профиле пользователя не указан город.')
            raise ValueError

    def get_photos(self):
        url = 'https://api.vk.com/method/photos.get'
        photo_params = {'owner_id': self.id, 'album_id': 'profile',
                        'extended': 1}

        response = requests.get(url, params={**self.params, **photo_params})
        print(response.json())


# vk = VKInfo(TOKEN, 'loli_katze')
# vk = VKInfo(TOKEN, 'marialldl')
# vk = VKInfo(TOKEN, 'murz727')
# vk = VKInfo(TOKEN, 'borodina_y')
vk = VKInfo(TOKEN, 108062987)
# vk = VKInfo(TOKEN, 'yvkey')
# vk.get_user_info()
vk.get_photos()


def photos_get(count=3):
    '''Функция получения фото пользователя'''
    pass
