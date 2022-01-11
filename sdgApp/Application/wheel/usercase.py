import shortuuid

from sdgApp.Application.wheel.CommandDTOs import WheelCreateDTO, WheelUpdateDTO
from sdgApp.Domain.wheel.wheel import WheelAggregate
from sdgApp.Infrastructure.MongoDB.wheel.wheel_repoImpl import WheelRepoImpl


def DTO_assembler(wheel: WheelAggregate):
    return wheel.shortcut_DO

class WheelCommandUsercase(object):

    def __init__(self, db_session, user, repo=WheelRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session, user)

    def create_wheel(self, dto: WheelCreateDTO):
        try:
            uuid = shortuuid.uuid()
            wheel_dict = dto.dict()
            wheel = WheelAggregate(id=uuid,
                                name=wheel_dict["name"],
                                position=wheel_dict["position"],
                                car_name=wheel_dict["car_name"],
                                car_id=wheel_dict["car_id"],
                                desc=wheel_dict["desc"],
                                param=wheel_dict["param"])
            self.repo.create(wheel)
        except:
            raise

    def delete_wheel(self, wheel_id: str):
        try:
            self.repo.delete(wheel_id)
        except:
            raise

    def update_wheel(self, wheel_id:str, dto: WheelUpdateDTO):
        try:
            wheel_update_dict = dto.dict()
            update_wheel = WheelAggregate(wheel_id,
                                            name=wheel_update_dict["name"],
                                            car_name=wheel_update_dict["car_name"],
                                            car_id=wheel_update_dict["car_id"],
                                            desc=wheel_update_dict["desc"],
                                            param=wheel_update_dict["param"])
            self.repo.update(update_wheel)
        except:
            raise


class WheelQueryUsercase(object):

    def __init__(self, db_session, user, repo=WheelRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session, user)

    def get_wheel(self, wheel_id:str):
        try:
            wheel = self.repo.get(wheel_id)
            if wheel:
                response_dto = DTO_assembler(wheel)
                return response_dto
        except:
            raise

    def list_wheel(self, query_param: dict):
        try:
            response_dto_lst = []
            wheel_lst = self.repo.list(query_param=query_param)
            if wheel_lst:
                for wheel in wheel_lst:
                    response_dto = DTO_assembler(wheel)
                    response_dto_lst.append(response_dto)
                return response_dto_lst
        except:
            raise

