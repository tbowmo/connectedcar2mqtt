ConnectedCar2Mqtt
=================

Publish data to MQTT from connected car GraphQL api.

ConnectedCar is a small dongle that is mainly an offering from VW, Audi Skoda etc. dealerships in Denmark, that is installed in the car for easier customer 2 workshop communication.

The product is sold as MinSkoda, MinAudi, MinVolkswagen etc. But all is the same.

This project queries the publicly available graphql endpoint, about status of the car, including position, and publishes this on MQTT for the car.


