import modules.config as config
import modules.vk_class as VkBackup
import modules.ya_class as YaLoader


if __name__ == "__main__":
    vk_back = VkBackup(config.VK_TOKEN, config.API_VK)
    ya_back = YaLoader(config.YA_TOKEN, config.API_YAD, config.YA_FOLDER)
    ya_back._create_upload_folder()
    ya_back.upload(vk_back.upload_json())
    print('Работа завершена')
