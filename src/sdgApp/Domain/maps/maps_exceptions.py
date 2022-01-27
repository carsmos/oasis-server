class MapQueryError(Exception):
    message = "map find error"

    def __str__(self):
        return MapQueryError.message
