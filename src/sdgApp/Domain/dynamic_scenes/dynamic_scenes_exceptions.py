class DynamicScenesNotFoundError(Exception):
    message = "动态场景描述不存在"
    def __str__(self):
        return DynamicScenesNotFoundError.message