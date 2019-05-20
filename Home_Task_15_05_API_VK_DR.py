from urllib.parse import urlencode
from pprint import pprint
import requests
import time
import json

TOKEN = '73eaea320bdc0d3299faa475c196cfea1c4df9da4c6d291633f9fe8f83c08c4de2a3abf89fbc3ed8a44e1'

## Блок для проверки работы токена
# params = {
#     'access_token': TOKEN,
#     'v': '5.95',
#     'extended': '1',
#     'fields': 'members_count'
#
# }
# response = requests.get('https://api.vk.com/method/groups.get', params)
# pprint(response.json())

class User:
    def __init__(self, token, user_id=171691064):
        self.token = token
        self.user_id = user_id

    def get_params(self):
        return dict(
            access_token=self.token,
            v='5.95',
            extended=1,
            fields='members_count'
        )
    def get_groups(self):
        params = self.get_params()
        response = requests.get('https://api.vk.com/method/groups.get', params)
        groups = response.json()['response']['items']
        for group in groups:
            del group['is_closed'], group['photo_100'], group['photo_200'],group['photo_50'],group['screen_name'],group['type']
        return groups

    def get_friends(self):
        params = self.get_params()
        response = requests.get('https://api.vk.com/method/friends.get', params)
        return response.json()['response']['items']

    def search_for_friends_in_the_group(self):
        params = self.get_params()
        groups = self.get_groups()
        friends = self.get_friends()
        groups_with_friends_list = []
        for group in groups:
            for friend in friends:
                params['group_id'] = group['id']
                params['user_id'] = friend['id']
                # params['code'] = 'return API.groups.isMember()'
                response = requests.get('https://api.vk.com/method/groups.isMember', params)
                if response.json()['response']['member'] == 1:
                    groups_with_friends_list.append(group['name'])
                    pprint('OK!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
                    break
                pprint(group['name'])
                pprint(response.json())
                time.sleep(0.9)
        print(groups_with_friends_list)
        return groups_with_friends_list

    def write_to_file(self):
        groups = self.get_groups()
        groups_with_friends_list = self.search_for_friends_in_the_group()
        for group_list in groups_with_friends_list:
            for group in groups:
                if group_list != group['name']:
                    with open('groups.json', 'a') as f:
                        json.dump(group, f, ensure_ascii=False, indent=2)


# user_input = input('Введите имя и фамилию одного из ваших друзей для отображения ваших общих друзей: ')
user = User(TOKEN)
pprint(user.get_groups())
user.write_to_file()

#
# with open("groups.json", encoding="cp1251") as datafile:
#   json_data = json.load(datafile)
# print(json_data)
# pprint(json_data)



