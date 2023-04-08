"""GraphQL model importer"""
import datetime
import json
from attrs import define, field, asdict, fields_dict
import dateutil.parser

@define
class BaseModel:
    '''Base model with parser build in'''
    # time: datetime.datetime = field(default=None)
    # id: str = field(default=None)

    def json_serial(self, obj):
        """JSON serializer for objects not serializable by default json code"""

        if isinstance(obj, (datetime.datetime, datetime.date)):
            return obj.isoformat()
        raise TypeError ("Type %s not serializable" % type(obj))

    def json(self):
        '''Return a json serialized presentation of the object'''
        return json.dumps(asdict(self), default=self.json_serial)

    @classmethod
    def create_from_dict(cls, values: dict):
        '''Parse dict according to fields defined in derived classes,
        only basic types is converted
        '''
        all_fields = fields_dict(cls)
        print(all_fields)
        parsed = cls()
        for key in all_fields:
            if key not in values:
                continue
            field_type = all_fields[key].type
            if field_type == float:
                setattr(parsed, key, float(values[key]))
            elif field_type == int:
                setattr(parsed, key, int(values[key]))
            elif field_type == str:
                setattr(parsed, key, str(values[key]))
            elif field_type == bool:
                setattr(parsed, key, bool(values[key]))
            elif field_type == datetime.datetime:
                setattr(parsed, key, dateutil.parser.parse(values[key]))
        return parsed

@define
class VehicleFuelLevel(BaseModel):
    """Represents the fuel level of a vehicle at a specific measurement time."""
    liter : float = field(init=False)

@define
class VehiclePosition(BaseModel):
    """Represents a single position of a vehicle at a specific mesurement time."""
    latitude : float = field(init=False)
    longitude : float = field(init=False)

@define
class VehicleBattery(BaseModel): #pylint: disable=too-few-public-methods
    """Represents a single voltage measurement at a specific measurement time."""
    voltage: float = field(init=False)


@define
class VehicleIgnition(BaseModel): #pylint: disable=too-few-public-methods
    """Represents a single voltage measurement at a specific measurement time."""
    on: bool = field(init=False) #pylint: disable=invalid-name

@define
class VehicleOdometer(BaseModel):
    """Represents the odometer state of a vehicle at a specific measurement time."""
    odometer : float = field(init=False)

@define
class Vehicle(BaseModel): #pylint: disable=too-few-public-methods, invalid-name
    """Represents a vehicle overview."""

    fuelEconomy: float = field(init=False)
    position: VehiclePosition = field(init=False)
    fuelLevel: VehicleFuelLevel = field(init=False)
    odometer: VehicleOdometer = field(init=False)
    ignition: VehicleIgnition = field(init=False)
    battery: VehicleBattery = field(init=False)
    licensePlate: str = field(init=False)

    @classmethod
    def check_value(cls, value, key) -> bool:
        """Check if key is valid for dict"""
        return key in value and value[key] is not None

    @classmethod
    def create_from_dict(cls, values: dict):
        """Creates an instance from data in dictionary"""

        # Lets create an object with the most basic data structures
        vehicle = super(Vehicle, cls).create_from_dict(values)

        vehicle.fuelEconomy = float(values['fuelEconomy']) if cls.check_value(
            values, 'fuelEconomy') is True else None

        if cls.check_value(values, 'position'):
            vehicle.position = VehiclePosition.create_from_dict(
                values['position'])

        if cls.check_value(values, 'fuelLevel'):
            vehicle.fuelLevel = VehicleFuelLevel.create_from_dict(
                values['fuelLevel'])
        if cls.check_value(values, 'odometer'):
            vehicle.odometer = VehicleOdometer.create_from_dict(
                values['odometer'])
        if cls.check_value(values, 'ignition'):
            vehicle.ignition = VehicleIgnition.create_from_dict(
                values['ignition'])
        if cls.check_value(values, 'latestBatteryVoltage'):
            vehicle.battery = VehicleBattery.create_from_dict(
                values['latestBatteryVoltage'])
        return vehicle
