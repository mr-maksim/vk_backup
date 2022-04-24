from modules.vk_class import VkBackup
import modules.config as config
from modules.ya_class import YaLoader


if __name__ == "__main__":
    screen_name = input('Введите Screen Name или ID: ')
    count = int(input('Введите количество загружаемых фото: '))
    vk_back = VkBackup(screen_name, config.VK_TOKEN,
                       config.API_VK, count=count)
    ya_back = YaLoader(config.YA_TOKEN, config.API_YAD, config.YA_FOLDER)
    ya_back._create_upload_folder()
    ya_back.upload(vk_back.upload_json())
    print('Работа завершена')
