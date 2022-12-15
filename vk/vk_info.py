from datetime import datetime
import requests
from vkinderdb.db_functions import VkinderDB
from vkinderdb import db_auth
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
                self.id = user_json['response'][0]['id']
                name = user_json['response'][0]['first_name']
                surname = user_json['response'][0]['last_name']
                sex = 'Женский' if user_json['response'][0]['sex'] == 1 else 'Мужской'
                city = self._parse_city(user_json)
                url = f'https://vk.com/id{user_json["response"][0]["id"]}'
                age = self._age_format(self._parse_bdate(user_json))

                user_data = {
                    'user_id': self.id, 'name': name,
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

        try:
            photos_json = requests.get(url, params={**self.params, **photo_params}).json()

            # Возможна долгая отработка цикла при большом количестве фоток, оптимизировать
            photos = [{'media_id': photo['id'], 'likes_count': photo['likes']['count']} for photo in
                      photos_json['response']['items']]
            photos = sorted(photos, key=lambda photo: photo['likes_count'], reverse=True)[:3]
            attachment = self._photo_processing(photos)

            print(attachment)  # удалить строку
            return (attachment)

        except Exception as ex:
            print(f'[ERROR] {ex}')

    def _photo_processing(self, photos):
        res = ','.join([f"{'photo'}{self.id}_{photo['media_id']}" for photo in photos])
        return res


# vk = VKInfo(TOKEN, 'loli_katze')
# vk = VKInfo(TOKEN, 'marialldl')
# vk = VKInfo(TOKEN, 'murz727')
# vk = VKInfo(TOKEN, 'borodina_y')
# vk = VKInfo(TOKEN, 108062987)
# vk = VKInfo(TOKEN, 'yvkey')
# vk = VKInfo(TOKEN, 80821257)
# vk = VKInfo(TOKEN, 1559980)

vk = VKInfo(TOKEN, 268278600)
user_data = vk.get_user_info()
user_photo = vk.get_photos()

# db = VkinderDB(db_auth.USER, db_auth.PASSWORD)
# db.add_new_user(user_data, user_photo)
