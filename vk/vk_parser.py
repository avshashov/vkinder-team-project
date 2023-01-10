from datetime import datetime
import requests
from tqdm import tqdm
from vk_auth import user_token, user_db, password_db
from vk_info import VKInfo
from vkinderdb.db_functions import VkinderDB


def friends_parser(user_id, user_token):
    url = 'https://api.vk.com/method/friends.get'
    user_params = {'user_ids': user_id, 'fields': 'bdate, city, sex'}
    vk_params = {'access_token': user_token, 'v': 5.131, 'lang': 'ru'}

    friends_id = requests.get(url, params={**user_params, **vk_params}).json()

    result = []
    for friend in tqdm(friends_id['response']['items']):
        try:
            if friend['is_closed']:
                continue

            friend_id = friend['id']
            bdate = datetime.strptime(friend['bdate'], '%d.%m.%Y')
            age = int((datetime.now() - bdate).days / 365)
            city = friend['city']['title']
            sex = 'женский' if friend['sex'] == 1 else 'мужской'
            name = friend['first_name']
            surname = friend['last_name']
            url = f'https://vk.com/id{friend["id"]}'

            vk_user = VKInfo(user_token, friend_id)
            user_photo = vk_user.get_photos()

            user_data = {
                'user_id': friend_id, 'name': name,
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


def upload_friend_to_db(friends):
    db = VkinderDB(user_db, password_db)
    for friend in friends:
        db.add_new_user(friend[0], friend[1])


def search_users(user_token, user_id):
    url = 'https://api.vk.com/method/users.search'
    db = VkinderDB(user_db, password_db)
    users_params = db.get_search_params(user_id)

    sex = 1 if users_params[2] == 'женский' else 2
    search_params = {
        'age_from': users_params[0], 'age_to': users_params[1],
        'sex': sex, 'hometown': users_params[3],
        'has_photo': 1, 'count': 1000,
        'fields': 'bdate, city, sex'
    }
    vk_params = {'access_token': user_token, 'v': 5.131, 'lang': 'ru'}

    response = requests.get(url, params={**search_params, **vk_params}).json()
    # print(response)

    result = []
    for friend in tqdm(response['response']['items']):
        try:
            if friend['is_closed']:
                continue

            friend_id = friend['id']
            bdate = datetime.strptime(friend['bdate'], '%d.%m.%Y')
            age = int((datetime.now() - bdate).days / 365)
            city = friend['city']['title']
            sex = 'женский' if friend['sex'] == 1 else 'мужской'
            name = friend['first_name']
            surname = friend['last_name']
            url = f'https://vk.com/id{friend["id"]}'

            vk_user = VKInfo(user_token, friend_id)
            user_photo = vk_user.get_photos()

            user_data = {
                'user_id': friend_id, 'name': name,
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


# if __name__ == '__main__':
    # user_id = int(input())
    # upload_friend_to_db(friends_parser(user_id, user_token))
    # upload_friend_to_db(search_users(user_token, 108062987))
