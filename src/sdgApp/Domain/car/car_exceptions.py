class CarNotFoundError(Exception):
    message = "车辆不存在"
    def __str__(self):
        return CarNotFoundError.message