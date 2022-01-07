from sdgApp.Application.maps.RespondsDTOs import MapReadDTO
from sdgApp.Domain.maps.maps import MapsAggregate
from sdgApp.Infrastructure.MongoDB.maps.map_repoImpl import MapRepoImpl
from sdgApp.Infrastructure.MongoDB.session_maker import mongo_session


class MapQueryUsercase(object):

    def __init__(self, repo=MapRepoImpl, db_session=mongo_session):
        self.repo = repo
        _, db = db_session()
        self.repo = self.repo(db)

    def find_all_maps(self):
        try:
            return self.repo.find_all_maps()
        except:
            raise

    def find_specified_map(self, query_args):
        try:
            if isinstance(query_args, int):
                return self.repo.find_map_by_id(query_args)
            if isinstance(query_args, str):
                return self.repo.find_map_by_name(query_args)
        except:
            raise


