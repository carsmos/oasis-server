class EnvCreateError(Exception):
    message = "env create error"

    def __str__(self):
        return EnvCreateError.message
