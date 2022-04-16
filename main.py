class VkBackup:
    def __init__(self, vk_token, api, count = 2) -> None:
        self.token = vk_token
        self.base_url = api
        self.count = count

    