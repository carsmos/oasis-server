import shortuuid

from sdgApp.Application.dynamics.CommandDTOs import DynamicsCreateDTO, DynamicsUpdateDTO
from sdgApp.Domain.dynamics.dynamics import DynamicsAggregate
from sdgApp.Infrastructure.MongoDB.dynamics.dynamics_repoImpl import DynamicsRepoImpl


def dto_assembler(dynamics: DynamicsAggregate):
    return dynamics.shortcut_DO

class DynamicsCommandUsercase(object):

    def __init__(self, db_session, user, repo=DynamicsRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session, user)

    def create_dynamics(self, dto: dict):
        try:
            uuid = shortuuid.uuid()
            dynamics_dict = dto
            dynamics = DynamicsAggregate(id=uuid,
                                name=dynamics_dict["name"],
                                car_name=dynamics_dict["car_name"],
                                car_id=dynamics_dict["car_id"],
                                desc=dynamics_dict["desc"],
                                param=dynamics_dict["param"])
            self.repo.create(dynamics)

            dynamics = self.repo.get(dynamics_id=uuid)
            if dynamics:
                response_dto = dto_assembler(dynamics)
                return response_dto
        except:
            raise

    def delete_dynamics(self, dynamics_id: str):
        try:
            self.repo.delete(dynamics_id)
        except:
            raise

    def update_dynamics(self, dynamics_id:str, dto: dict):
        try:
            dynamics_update_dict = dto
            update_dynamics = DynamicsAggregate(dynamics_id,
                                            name=dynamics_update_dict["name"],
                                            car_name=dynamics_update_dict["car_name"],
                                            car_id=dynamics_update_dict["car_id"],
                                            desc=dynamics_update_dict["desc"],
                                            param=dynamics_update_dict["param"])
            self.repo.update(update_dynamics)

            dynamics = self.repo.get(dynamics_id=dynamics_id)
            if dynamics:
                response_dto = dto_assembler(dynamics)
                return response_dto
        except:
            raise


class DynamicsQueryUsercase(object):

    def __init__(self, db_session, user, repo=DynamicsRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session, user)

    def get_dynamics(self, dynamics_id:str):
        try:
            dynamics = self.repo.get(dynamics_id)
            if dynamics:
                response_dto = dto_assembler(dynamics)
                return response_dto
        except:
            raise

    def list_dynamics(self, query_param: dict):
        try:
            response_dto_lst = []
            dynamics_lst = self.repo.list(query_param=query_param)
            if dynamics_lst:
                for dynamics in dynamics_lst:
                    response_dto = dto_assembler(dynamics)
                    response_dto_lst.append(response_dto)
                return response_dto_lst
        except:
            raise

