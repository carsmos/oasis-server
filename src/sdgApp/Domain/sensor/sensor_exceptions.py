class SensorNotFoundError(Exception):
    message = "传感器模型不存在"
    def __str__(self):
        return SensorNotFoundError.message