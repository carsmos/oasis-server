from abc import ABC, abstractmethod
from sdgApp.Domain.weather.weathers import WeatherAggregate


class WeatherRepo(ABC):

    @abstractmethod
    def create_weather(self, weather: WeatherAggregate):
        raise NotImplementedError

    @abstractmethod
    def update_weather(self, weather_id: str, env: WeatherAggregate):
        raise NotImplementedError

    @abstractmethod
    def delete_weather(self, id: str):
        raise NotImplementedError

    @abstractmethod
    def get(self, id: str):
        raise NotImplementedError

    @abstractmethod
    def list(self):
        raise NotImplementedError
