from modules.vk_class import VkBackup
import modules.config as config
from modules.ya_class import YaLoader


if __name__ == "__main__":
    vk_back = VkBackup(config.VK_TOKEN, config.API_VK)
    ya_back = YaLoader(config.YA_TOKEN, config.API_YAD, config.YA_FOLDER)
    ya_back._create_upload_folder()
    ya_back.upload(vk_back.upload_json())
    print('Работа завершена')
