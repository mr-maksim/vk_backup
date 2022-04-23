import json
import modules.config as config
import requests
import datetime
from tqdm import tqdm


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

    def __date_convert(self, ts):
        date = str(datetime.datetime.fromtimestamp(ts).strftime('%d.%m.%Y'))
        return date

    def upload_json(self):
        photo_list = []
        save_json = []
        last_name = []
        response = self.__vk_response()["response"]
        file_extension = '.jpg'
        for image in tqdm(response['items'], desc='Получение url максимального размера'):
            size = image['sizes']
            size_url = max(size, key=VkBackup.__big_party)
            if str(image['likes']['count'])+file_extension in last_name:
                date = self.__date_convert(image['date'])
                photo_list.append({'file_name': date + '_' + str(
                    image['likes']['count']) + file_extension, 'size': size_url['type'], 'url': size_url['url']})
                save_json.append({'file_name': date + '_' + str(
                    image['likes']['count']) + file_extension, 'size': size_url['type']})
                last_name.append(str(image['likes']['count'])+file_extension)
            elif str(image['likes']['count'])+file_extension not in last_name:
                photo_list.append({'file_name': str(
                    image['likes']['count']) + file_extension, 'size': size_url['type'], 'url': size_url['url']})
                save_json.append({'file_name': str(
                    image['likes']['count']) + file_extension, 'size': size_url['type']})
                last_name.append(str(image['likes']['count'])+file_extension)
        with open(f'{config.JSON_PATH}/upload_json.json', 'w') as file:
            file.write(json.dumps(save_json, indent=4))
            return photo_list
