from datetime import datetime
import requests


class VKInfo:

    def __init__(self, access_token, user_id):
        self.token = access_token
        self.id = user_id
        self.params = {'access_token': self.token, 'v': 5.131, 'lang': 'ru'}

    def get_user_info(self):
        '''Функция получения информации со страницы пользователя.'''
        url = 'https://api.vk.com/method/users.get'
        user_params = {'user_ids': self.id, 'fields': 'bdate, city, sex'}

        try:
            user_json = requests.get(url, params={**self.params, **user_params}).json()

            if self._profile_is_closed(user_json):
                print('[ERROR] Для корректной работы приложения сделайте профиль открытым :)')
                return 1
            else:
                try:
                    self.id = user_json['response'][0]['id']
                    name = user_json['response'][0]['first_name']
                    surname = user_json['response'][0]['last_name']
                    sex = 'женский' if user_json['response'][0]['sex'] == 1 else 'мужской'
                    city = user_json['response'][0]['city']['title']

                    url = f'https://vk.com/id{user_json["response"][0]["id"]}'
                    age = self._age_format(self._parse_bdate(user_json))

                    user_data = {
                        'user_id': self.id, 'name': name,
                        'surname': surname, 'sex': sex,
                        'age': age, 'city': city,
                        'url': url
                    }
                    print('[INFO] Информация о профиле получена.')
                    return user_data
                except:
                    print('[ERROR] Ошибка получения информации о пользователе.'
                          '\nВ профиле не указана дата рождения или город.')
                    return 2

        except Exception as ex:
            print(f'[ERROR] {ex}. Ошибка request-запроса для get_user_info.')
            return

    def _parse_bdate(self, user_json):
        bdate = datetime.strptime(user_json['response'][0]['bdate'], '%d.%m.%Y')
        return bdate

    def _age_format(self, bdate):
        age = int((datetime.now() - bdate).days / 365)
        return age

    def _profile_is_closed(self, user_json):
        return user_json['response'][0]['is_closed']

    def get_photos(self):
        '''Функция получения 3х фотографий с наибольшим количеством лайков со страницы пользователя.'''
        url = 'https://api.vk.com/method/photos.get'
        photo_params = {'owner_id': self.id, 'album_id': 'profile',
                        'extended': 1}

        try:
            photos_json = requests.get(url, params={**self.params, **photo_params}).json()

            photos = [{'media_id': photo['id'], 'likes_count': photo['likes']['count']} for photo in
                      photos_json['response']['items']]
            photos = sorted(photos, key=lambda photo: photo['likes_count'], reverse=True)[:3]
            attachment = self._photo_processing(photos)

            return (attachment)

        except Exception as ex:
            print(f'[ERROR] {ex}. Ошибка request-запроса для get_photos')

    def _photo_processing(self, photos):
        res = ','.join([f"{'photo'}{self.id}_{photo['media_id']}" for photo in photos])
        return res