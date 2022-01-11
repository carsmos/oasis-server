class EnvCreateError(Exception):
    message = "environment create error"

    def __str__(self):
        return EnvCreateError.message
