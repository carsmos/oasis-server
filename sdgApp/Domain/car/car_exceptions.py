class CarCreateError(Exception):
    message = "car create error"
    def __str__(self):
        return CarCreateError.message