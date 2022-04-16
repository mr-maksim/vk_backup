import json
import config
import requests
import datetime


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
        
    def __date_convert(self,ts):
        date = str(datetime.datetime.fromtimestamp(ts).strftime('%d.%m.%Y'))
        return date


    def upload_json(self):
        photo_list = []
        last_name = []
        response = self.__vk_response()["response"]
        file_extension = '.jpg'
        for image in response['items']:
            size = image['sizes']
            size_url = max(size, key=VkBackup.__big_party)
            if str(image['likes']['count'])+file_extension in last_name:
                date = self.__date_convert(image['date'])
                photo_list.append({'file_name': date + '_' + str(
                    image['likes']['count']) + file_extension, 'size': size_url['type'], 'url': size_url['url']})
                last_name.append(str(image['likes']['count'])+file_extension)
            elif str(image['likes']['count'])+file_extension not in last_name:
                photo_list.append({'file_name': str(
                    image['likes']['count']) + file_extension, 'size': size_url['type'], 'url': size_url['url']})
                last_name.append(str(image['likes']['count'])+file_extension)
        with open(f'{config.JSON_PATH}/upload_json.json', 'w') as file:
            file.write(json.dumps(photo_list, indent=4))
            return photo_list


class YaLoader:
    def __init__(self, ya_token, api, path):
        self.token = ya_token
        self.base_url = api
        self.folder = path

    def _get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': self.token
        }

    def _create_upload_folder(self):
        href = self.base_url + 'v1/disk/resources?path=' + self.folder
        response = requests.put(href, headers=self._get_headers())

    def _get_link(self,file_path, name):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {
            'path': f'{file_path}/{name}',
            'overwrite': 'true'
        }
        response = requests.get(upload_url, headers=self._get_headers(), params=params)
        return response.json()

    def upload(self,photo_list):
            for item in photo_list:
                dict = self._get_link(file_path=self.folder, name=item['file_name'])
                href = dict['href']
                image = requests.get(item['url'])
                response = requests.put(href, data=image.content)
                response.raise_for_status()
                if response.status_code == 201:
                    print('Uploaded')


if __name__ == "__main__":
    vk_back = VkBackup(config.VK_TOKEN, config.API_VK)
    ya_back = YaLoader(config.YA_TOKEN,config.API_YAD,config.YA_FOLDER)
    ya_back._create_upload_folder()
    ya_back.upload(vk_back.upload_json())
