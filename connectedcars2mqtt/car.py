"""Module something"""
from attrs import define, field
from connectedcars import ConnectedCarsClient
from .models import Vehicle
from .constants import FULL

@define
class Car:
    """Fetches data from connected cars API and transforms this to a more sensible format"""
    car_client: ConnectedCarsClient = field()
    home_pos: tuple[float, float] = field()

    def query(self, query) -> dict:
        """Executes the actual query and returns the first vehicle in the list"""
        return self.car_client.query(
            query)['data']['viewer']['vehicles'][0]['vehicle']

    def get_full(self) -> Vehicle:
        """Returns the transformed vehicle data"""
        response = self.query(FULL)
        return Vehicle.create_from_dict(response, self.home_pos)
