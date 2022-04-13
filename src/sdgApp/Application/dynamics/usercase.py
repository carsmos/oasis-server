import shortuuid

from sdgApp.Application.car.usercase import split_page
from sdgApp.Application.dynamics.CommandDTOs import DynamicsCreateDTO, DynamicsUpdateDTO
from sdgApp.Application.dynamics.RespondsDTOs import DynamicsReadDTO
from sdgApp.Domain.dynamics.dynamics import DynamicsAggregate
from sdgApp.Domain.dynamics.dynamics_exceptions import DynamicsNotFoundError
from sdgApp.Infrastructure.MongoDB.dynamics.dynamics_repoImpl import DynamicsRepoImpl


class DynamicsCommandUsercase(object):

    def __init__(self, db_session, user, repo=DynamicsRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session, user)

    def create_dynamics(self, dynamics_create_model: DynamicsCreateDTO):
        try:
            uuid = shortuuid.uuid()
            dynamics = DynamicsAggregate(id=uuid,
                                name=dynamics_create_model.name,
                                desc=dynamics_create_model.desc,
                                param=dynamics_create_model.param)
            self.repo.create(dynamics)
        except:
            raise

    def delete_dynamics(self, dynamics_id: str):
        try:
            self.repo.delete(dynamics_id)
        except:
            raise

    def update_dynamics(self, dynamics_id:str, dynamics_update_model: DynamicsUpdateDTO):
        try:
            dynamics_retrieved = self.repo.get(dynamics_id=dynamics_id)
            dynamics_retrieved.name = dynamics_update_model.name
            dynamics_retrieved.desc = dynamics_update_model.desc
            dynamics_retrieved.param = dynamics_update_model.param
            self.repo.update(dynamics_retrieved)
        except:
            raise


class DynamicsQueryUsercase(object):

    def __init__(self, db_session, user, repo=DynamicsRepoImpl):
        self.db_session = db_session
        self.user = user
        self.dynamics_collection = self.db_session['dynamics']

    def get_dynamics(self, dynamics_id:str):
        try:
            filter = {'id': dynamics_id}
            filter.update({"usr_id": self.user.id})

            result_dict = self.dynamics_collection.find_one(filter, {'_id': 0, 'usr_id':0})
            if result_dict is None:
                raise DynamicsNotFoundError
            return DynamicsReadDTO(**result_dict)
        except:
            raise

    def list_dynamics(self, p_num):
        try:
            response_dto_lst = []
            filter = {"usr_id": self.user.id}
            results_dict = self.dynamics_collection.find(filter, {'_id': 0, 'usr_id':0}).sort([('last_modified', -1)])
            if results_dict:
                for one_result in results_dict:
                    response_dto_lst.append(DynamicsReadDTO(**one_result))

                response_dto_lst = split_page(p_num,  response_dto_lst)
                return response_dto_lst
        except:
            raise

