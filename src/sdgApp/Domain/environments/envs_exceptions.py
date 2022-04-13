class EnvNotFoundError(Exception):
    message = "场景天气不存在"
    def __str__(self):
        return EnvNotFoundError.message