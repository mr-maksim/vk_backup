import requests
from tqdm import tqdm


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

    def _get_link(self, file_path, name):
        upload_url = 'https://cloud-api.yandex.net/v1/disk/resources/upload'
        params = {
            'path': f'{file_path}/{name}',
            'overwrite': 'true'
        }
        response = requests.get(
            upload_url, headers=self._get_headers(), params=params)
        return response.json()

    def upload(self, photo_list):
        for item in tqdm(photo_list, desc='Загрузка на Ядиск'):
            dict = self._get_link(file_path=self.folder,
                                  name=item['file_name'])
            href = dict['href']
            image = requests.get(item['url'])
            response = requests.put(href, data=image.content)
            response.raise_for_status()
