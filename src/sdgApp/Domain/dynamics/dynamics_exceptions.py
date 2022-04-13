class DynamicsNotFoundError(Exception):
    message = "动力学模型不存在"
    def __str__(self):
        return DynamicsNotFoundError.message