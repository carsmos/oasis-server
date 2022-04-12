class ScenarioNotFoundError(Exception):
    message = "场景不存在"
    def __str__(self):
        return ScenarioNotFoundError.message