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
        map_aggregate_list = []
        maps_DO = self.maps_collection.find({}, {'_id': 0})
        for map in maps_DO:
            one_map = MapsAggregate()
            one_map.save_DO_shortcut(map)
            map_aggregate_list.append(one_map)
        return map_aggregate_list

    def find_map_by_id(self, map_id: int):
        map_DO = self.maps_collection.find_one({"id": map_id})
        map = MapsAggregate()
        map.save_DO_shortcut(map_DO)
        return map

    def find_map_by_name(self, name: str):
        map_DO = self.maps_collection.find_one({"map_name": name})
        map = MapsAggregate()
        map.save_DO_shortcut(map_DO)
        return map
