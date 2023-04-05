"""Module something"""
import attr
from connectedcars import ConnectedCarsClient
from .models import Vehicle
from .constants import FULL

@attr.s
class Car:
    """Fetches data from connected cars API and transforms this to a more sensible format"""
    car_client: ConnectedCarsClient = attr.ib()

    def query(self, query) -> dict:
        """Executes the actual query and returns the first vehicle in the list"""
        return self.car_client.query(
            query)['data']['viewer']['vehicles'][0]['vehicle']

    def get_full(self) -> Vehicle:
        """Returns the transformed vehicle data"""
        response = self.query(FULL)
        return Vehicle.create_from_dict(response)
