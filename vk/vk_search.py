from datetime import datetime
import requests
import tqdm as tqdm
from vk_info import VKInfo
# from vk_auth import user_token

def vk_search(age_from, age_to, gendor, city):
    if gendor == 'женщина':
        gendor = 1
    elif gendor == 'мужчина':
        gendor = 2
    url = 'https://api.vk.com/method/users.search'
    user_params = {'sort': 0, 'fields': 'bdate, city, sex',
                   'hometown': city, 'age_from': age_from, 'age_to': age_to, 'sex': gendor}
    vk_params = {'access_token': user_token, 'v': 5.131, 'lang': 'ru'}
    users_id = requests.get(url, params={**user_params, **vk_params}).json()

    result = []
    for user in tqdm(users_id['response']['items']):
        try:
            if user['is_closed']:
                continue

            user_id = user['id']
            bdate = datetime.strptime(user['bdate'], '%d.%m.%Y')
            age = int((datetime.now() - bdate).days / 365)
            city = user['city']['title']
            sex = 'женский' if user['sex'] == 1 else 'мужской'
            name = user['first_name']
            surname = user['last_name']
            url = f'https://vk.com/id{user["id"]}'

            vk_user = VKInfo(user_token, user_id)
            user_photo = vk_user.get_photos()

            user_data = {
                'user_id': user_id, 'name': name,
                'surname': surname, 'sex': sex,
                'age': age, 'city': city,
                'url': url
            }
            user_info = [user_data, user_photo]
            if user_info not in result:
                result.append(user_info)

        except:
            continue

    return result



