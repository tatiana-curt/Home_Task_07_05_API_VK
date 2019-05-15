from urllib.parse import urlencode
from pprint import pprint
import requests

APP_ID = 6983474

BASE_URL = 'https://oauth.vk.com/authorize'
auth_data = {
    'client_id': APP_ID,
    'display': 'page',
    'response_type': 'token',
    'scope': 'friends',
    'v': '5.95'
}
# print('?'.join((BASE_URL, urlencode(auth_data))))

# TOKEN_friends_tatiana_job = '3fa953cc44e68ebafe377963e13cc32fe20df17a0ce3cefc39dc3a29320d14c0a303dd3e00c62ed8f5f79'
TOKEN_friends_tatiana = 'ca5ac1c6fae87df133c4adb356b924c0c8e1f6c7f1abee56a7e98ae00bf3333e1dc6ad7a3d8ac06ef5d82'

## Блок для проверки работы токена
# params = {
#     'access_token': TOKEN_friends_tatiana,
#     'v': '5.95',
#     'target_uid': '544755074'
# }
# response = requests.get('https://api.vk.com/method/friends.getMutual', params)
# pprint(response.json())

class User:
    def __init__(self, token, user_fio='Маша Золотова', user_id=None):
        self.token = token
        self.user_id = user_id
        self.user_fio = user_fio

    def get_params(self):
        return dict(
            access_token=self.token,
            v='5.95',
            target_uid=self.user_id,
            q=self.user_fio,
            fields='screen_name'
        )

    def get_params_2(self):
        return dict(
            access_token=self.token,
            v='5.95',
            count='1000'
        )

    # Ищем ID введенного пользователя среди друзей и подставляем в self.user_id. необходимо для params
    def friends_search(self):
        params = self.get_params()
        response = requests.get('https://api.vk.com/method/friends.search', params)
        self.user_id = response.json()['response']['items'][0]['id']

    # Для задачи 3
    def get_link(self):
        params = self.get_params()
        response = requests.get('https://api.vk.com/method/users.search', params)
        # pprint (response.json()['response']['items'])
        for user in response.json()['response']['items']:
            print(user['first_name'], user['last_name'],''.join(('https://vk.com/', user['screen_name'])))

    def get_shared_friends(self):
        self.friends_search()
        params = self.get_params()
        response = requests.get('https://api.vk.com/method/friends.getMutual', params)
        shared_id = response.json()['response']

        # Расширим информацию об общих друзьях, добавив к найденым ID Имя и Фамилию
        params = self.get_params_2()
        response_2 = requests.get('https://api.vk.com/method/friends.search', params)
        friends_list = response_2.json()['response']['items']

        for friends in friends_list:
            for id in shared_id:
                if id == friends['id']:
                    print(friends['first_name'], friends['last_name'], 'id =', friends['id'])

    # Для задачи 2
    def __and__(self, other):
        self.get_shared_friends()

    # Для задачи 3
    def __str__(self):
        self.get_link()


# Для задачи 2
user_2 = input('Введите имя и фамилию одного из ваших друзей для отображения ваших общих друзей: ')
tatiana = User(TOKEN_friends_tatiana, user_fio=user_2)
tatiana & user_2

# Для задачи 3
user_2 = input('Введите любые имя и фамилию для получения ссылки: ')
user_2 = User(TOKEN_friends_tatiana, user_fio=user_2)

try:
    print(user_2)
except TypeError as e:
    print('Представлены все найденые результаты поиска')


