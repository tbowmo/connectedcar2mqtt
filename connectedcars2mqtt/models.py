"""GraphQL model importer"""
import datetime
import attr
import dateutil.parser
from connectedcars.models import VehicleFuelLevel, VehiclePosition, VehicleOdometer


@attr.s
class VehicleBattery: #pylint: disable=too-few-public-methods
    """Represents a single voltage measurement at a specific measurement time."""
    time: datetime.datetime = attr.ib()
    voltage: float = attr.ib()

    @classmethod
    def create_from_dict(cls, value):
        """Creates an instance from data in dictionary"""
        return VehicleBattery(
            dateutil.parser.parse(value['time']),
            float(value['voltage']),
        )


@attr.s
class VehicleIgnition: #pylint: disable=too-few-public-methods
    """Represents a single voltage measurement at a specific measurement time."""
    time: datetime.datetime = attr.ib()
    on: bool = attr.ib()

    @classmethod
    def create_from_dict(cls, value):
        """Creates an instance from data in dictionary"""

        return VehicleIgnition(
            dateutil.parser.parse(value['time']),
            bool(value['on']),
        )

@attr.s
class Vehicle: #pylint: disable=too-few-public-methods, invalid-name
    """Represents a vehicle overview."""

    fuelEconomy: float = attr.ib(init=False)
    position: VehiclePosition = attr.ib(init=False)
    fuelLevel: VehicleFuelLevel = attr.ib(init=False)
    odometer: VehicleOdometer = attr.ib(init=False)
    ignition: VehicleIgnition = attr.ib(init=False)
    battery: VehicleBattery = attr.ib(init=False)
    licensePlate: str = attr.ib()


    @classmethod
    def check_value(cls, value, key) -> bool:
        """Check if key is valid for dict"""
        return key in value and value[key] is not None

    @classmethod
    def create_from_dict(cls, value):
        """Creates an instance from data in dictionary"""

        vehicle = Vehicle(str(value['licensePlate']))

        vehicle.fuelEconomy = float(value['fuelEconomy']) if cls.check_value(
            value, 'fuelEconomy') is True else None

        if cls.check_value(value, 'position'):
            vehicle.position = VehiclePosition.create_from_dict(
                value['position'])

        if cls.check_value(value, 'fuelLevel'):
            vehicle.fuelLevel = VehicleFuelLevel.create_from_dict(
                value['fuelLevel'])

        if cls.check_value(value, 'odometer'):
            vehicle.odometer = VehicleOdometer.create_from_dict(
                value['odometer'])
        if cls.check_value(value, 'ignition'):
            vehicle.ignition = VehicleIgnition.create_from_dict(
                value['ignition'])
        if cls.check_value(value, 'latestBatteryVoltage'):
            vehicle.battery = VehicleBattery.create_from_dict(
                value['latestBatteryVoltage'])
        return vehicle
