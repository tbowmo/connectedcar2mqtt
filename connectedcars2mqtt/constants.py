"""GraphQL queries"""

FULL = """
query User {
    viewer {
        vehicles {
            vehicle {
                id
                licensePlate
                fuelEconomy
                odometer {
                    odometer
                }
                fuelLevel {
                    liter
                }
                position {
                    latitude
                    longitude
                }
                latestBatteryVoltage {
                    voltage
                }
                ignition {
                    on
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
