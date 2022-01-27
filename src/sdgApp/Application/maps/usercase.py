from sdgApp.Application.maps.RespondsDTOs import MapReadDTO
from sdgApp.Domain.maps.maps import MapsAggregate
from sdgApp.Infrastructure.MongoDB.maps.map_repoImpl import MapRepoImpl


def DTO_assembler(map: MapsAggregate):
    return map.shortcut_DO


class MapQueryUsercase(object):

    def __init__(self, db_session, user, repo=MapRepoImpl):
        self.repo = repo
        self.repo = self.repo(db_session, user)

    def find_all_maps(self):
        try:
            response_dto_list = []
            map_list = self.repo.find_all_maps()
            for map in map_list:
                response_dto = DTO_assembler(map)
                response_dto_list.append(response_dto)
            return response_dto_list
        except:
            raise

    def find_specified_map(self, query_args):
        try:
            if isinstance(query_args, int):
                map = self.repo.find_map_by_id(query_args)
                response_dto = DTO_assembler(map)
                return response_dto
            if isinstance(query_args, str):
                map = self.repo.find_map_by_name(query_args)
                response_dto = DTO_assembler(map)
                return response_dto

        except:
            raise


