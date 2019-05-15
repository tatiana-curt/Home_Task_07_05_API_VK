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

TOKEN_friends_tatiana_job = '3fa953cc44e68ebafe377963e13cc32fe20df17a0ce3cefc39dc3a29320d14c0a303dd3e00c62ed8f5f79'
# TOKEN_friends_tatiana = '1a88cb1b058babee3d7406a253fb9a39e52d6e6895ccee46d12b627988110716831b698f075d17c5b23e1'
# TOKEN_status_agnia = '37b1cce19f73d918b8abeb6fc0401f56ec8d182c7473edc510698be31c1332864afe111a8195711100cd7'
# TOKEN_friends_agnia = 'fba939b6154ca9c6d1a1ebbe1fdeb8a37a72a6479170b672b84779cd9eed04a896be37ea2125a1a0507f1'
#
# params = {
#     'access_token': TOKEN_friends_tatiana_job,
#     'v': '5.95',
#     'target_uid': '544755074',
#
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
        return response.json()['response']

    # Для задачи 2
    def __and__(self, other):
        return self.get_shared_friends()


user_2 = input('Введите имя и фамилию одного из ваших друзей для отображения ID ваших общих друзей: ')
tatiana = User(TOKEN_friends_tatiana_job, user_fio=user_2)
pprint('ID общих друзей: {}'.format(tatiana & user_2))

user_2 = input('Введите любые имя и фамилию для получения ссылки: ')
tatiana = User(TOKEN_friends_tatiana_job, user_fio=user_2)
tatiana.get_link()


