"""GraphQL queries"""

FULL = """
query User {
viewer {
    vehicles {
    vehicle {
        licensePlate
        fuelEconomy
        odometer {
            odometer
            time
        }
        fuelLevel {
            liter
            time
        }
        position {
            latitude
            longitude
            time
        }
        latestBatteryVoltage {
            voltage
            time
        }
        ignition {
            on
            time
        }
    }
    }
}
}"""

IGNITION = """
query User {
viewer {
    vehicles {
    vehicle {
        licensePlate
        ignition {
        on
        time
        }
    }
    }
}
}
"""
