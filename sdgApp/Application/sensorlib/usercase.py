from CommandDTOs import SensorBaseCreateDTO

class SensorCommandUserCase(object):
    def __init__(self, repo):
        self.repo = repo

    def create_sensor(self, dto:SensorBaseCreateDTO):
        '''
        DTO command -> Domain -> Repo -> DTO response
        '''