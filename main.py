import json
import config
import requests


class VkBackup:
    def __init__(self, vk_token, api, count=2) -> None:
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


back = VkBackup(config.VK_TOKEN, config.API_VK)
back.photo_json_response()
