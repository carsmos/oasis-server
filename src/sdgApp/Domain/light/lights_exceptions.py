class LightNotFoundError(Exception):
    message = "Lighting does not exist"

    def __str__(self):
        return LightNotFoundError.message
