from sdgApp.Domain.maps.maps_repo import MapsRepo
from sdgApp.Domain.maps.maps import MapsAggregate


def DataMapper_to_DO(aggregate):
    pass


def DataMapper_to_Aggregate(DO):
    pass


class MapRepoImpl(MapsRepo):

    def __init__(self, db_session):
        self.db_session = db_session
        self.maps_collection = self.db_session['maps']

    def find_all_maps(self):
        map_list = []
        for map in self.maps_collection.find():
            map_list.append(map)
        return map_list

    def find_map_by_id(self, map_id: int):
        return self.maps_collection.find_one({"map_id": map_id})

    def find_map_by_name(self, name: str):
        return self.maps_collection.find_one({"map_name": name})
