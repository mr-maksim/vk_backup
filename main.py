import json
import config
import requests


class VkBackup:
    def __init__(self, vk_token, api, count=5) -> None:
        self.token = vk_token
        self.base_url = api
        self.count = count

    def __vk_response(self):
        method = 'photos.get/'
        href = self.base_url + method
        params = {
            'album_id': 'profile',
            'extended': 1,
            'count': self.count,
            'photo_sizes': 1,
            'access_token': self.token,
            'v': 5.131
        }
        response = requests.get(href, params=params)
        return response.json()

    def photo_json_response(self):
        with open(f'{config.JSON_PATH}/photo_json_response.json', 'w') as file:
            file.write(json.dumps(self.__vk_response(), indent=4))

    def __big_party(sizes):
        if sizes['width'] >= sizes['height']:
            return sizes['width']
        else:
            return sizes['height']

    def upload_json(self):
        photo_list = []
        last_name = []
        response = self.__vk_response()["response"]
        file_extension = '.jpg'
        for image in response['items']:
            size = image['sizes']
            size_url = max(size, key=VkBackup.__big_party)
            if str(image['likes']['count'])+file_extension in last_name:
                photo_list.append({'file_name': str(image['date']) + '_' + str(
                    image['likes']['count']) + file_extension, 'size': size_url['type'], 'url': size_url['url']})
                last_name.append(str(image['likes']['count'])+file_extension)
            elif str(image['likes']['count'])+file_extension not in last_name:
                photo_list.append({'file_name': str(
                    image['likes']['count']) + file_extension, 'size': size_url['type'], 'url': size_url['url']})
                last_name.append(str(image['likes']['count'])+file_extension)
        with open(f'{config.JSON_PATH}/upload_json.json', 'w') as file:
            file.write(json.dumps(photo_list, indent=4))


back = VkBackup(config.VK_TOKEN, config.API_VK)
back.upload_json()
