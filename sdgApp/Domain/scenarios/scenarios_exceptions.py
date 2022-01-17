class ScenarioCreateError(Exception):
    message = "scenario create error"

    def __str__(self):
        return ScenarioCreateError.message
