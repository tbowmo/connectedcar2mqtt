"""Main runner for project"""
import argparse
import sys
import json
import logging.config
import logging
import socket
import signal
import time
import copy
from os import path
from geopy.distance import geodesic
from deepdiff import DeepDiff
from connectedcars import ConnectedCarsClient
from connectedcars2mqtt.car import Car
from connectedcars2mqtt.mqtt import MQTT

__version__ = __VERSION__ = "0.0.1"

def parse_args(argv=None):
    #pylint: disable=line-too-long
    """ Command line argument parser """
    client = f'{socket.gethostname()}-car'
    parser = argparse.ArgumentParser(prog='connectedCar2mqtt',
                                     formatter_class=argparse.RawDescriptionHelpFormatter,
                                     description='chrome2mqtt\n\nConnects your chromecasts to a mqtt-broker',
                                     epilog='See more on https://github.com/tbowmo/chrome2mqtt/README.md'
                                     )
    parser.add_argument('--mqttport', action="store", default=1883, type=int, help="MQTT port on host")
    parser.add_argument('--mqttclient', action="store", default=client, help="Client name for mqtt")
    parser.add_argument('--mqttroot', action="store", default="connectedcar", help="MQTT root topic")
    parser.add_argument('--mqttuser', action="store", default=None, help="MQTT user (if authentication is enabled for the broker)")
    parser.add_argument('--mqttpass', action="store", default=None, help="MQTT password (if authentication is enabled for the broker)")
    parser.add_argument('-H', '--mqtthost', action="store", default="127.0.0.1", help="MQTT Host")
    parser.add_argument('-V', '--version', action='version', version=f'%(prog)s {__VERSION__}')
    parser.add_argument('-u', '--user', action="store", help="Connected car username")
    parser.add_argument('-p', '--password', action="store", help="Connected car password")
    parser.add_argument('-n', '--namespace', action="store", default="semler:minskoda", help="Connected car namespace")
    parser.add_argument('--latitude', action="store", default=56.00, type=float, help="Home position latitude")
    parser.add_argument('--longitude', action="store", default=9.00, type=float, help="Home position longitude")

    return parser.parse_args(argv)

def start_banner(args):
    """ Print banner message for the programme """
    print('ConnectedCar2MQTT')
    print('Connecting to mqtt host ' + args.mqtthost + ' port ' + str(args.mqttport))
    print('Using mqtt root ' + args.mqttroot)

def setup_logging(
        file=None,
        level=logging.WARNING
    ):
    """ Initialize logging """
    if path.isfile('./logsetup.json'):
        with open(file='./logsetup.json', mode='rt', encoding='utf-8') as options_file:
            config = json.load(options_file)
        logging.config.dictConfig(config)
    elif file is not None:
        logging.basicConfig(level=level,
                            filename=file,
                            format='%(asctime)s %(name)-16s %(levelname)-8s %(message)s')
    else:
        logging.basicConfig(level=level,
                            format='%(asctime)s %(name)-16s %(levelname)-8s %(message)s')


def main_loop(): #pylint: disable=too-many-locals
    """Main runner for the programme"""
    assert sys.version_info >= (3, 6), "You need at least python 3.6 to run this program"

    args = parse_args()
    start_banner(args)

    try:
        mqtt = MQTT(
            host=args.mqtthost,
            port=args.mqttport,
            client=args.mqttclient,
            root=args.mqttroot,
            user=args.mqttuser,
            password=args.mqttpass
            )
    except ConnectionError as exception:
        print(f'Error connecting to mqtt host {args.mqtthost} on port {args.mqttport}')
        print(exception)
        sys.exit(1)

    client = ConnectedCarsClient(
        username = args.user,
        password = args.password,
        namespace = args.namespace
        )

    car = Car(client)

    old_data = None

    delay = 300

    def signal_handler(sig, frame): #pylint: disable=unused-argument
        print('Shutting down')
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    while True:
        data = car.get_full()
        print(data)
        if old_data is None:
            old_data = copy.deepcopy(data)
            old_data.battery.voltage = 1.1
            old_data.battery.time = '0'

        differences = DeepDiff(old_data, data)
        print(differences)
        if 'values_changed' in differences:
            for key in differences['values_changed']:
                if 'time' not in key: # Do not publish time events to mqtt
                    new_value = differences['values_changed'][key]['new_value']
                    topic = key.replace('root.', f'{data.licensePlate}/').replace('.', '_')
                    mqtt.publish(topic, new_value, 0, True) # Retain last value received
        else:
            print(f'no change at : {time.time()}')

        if not data.ignition.on:
            delay = 300
        else:
            home_pos = (args.latitude, args.longitude)
            car_pos = (data.position.latitude, data.position.longitude)
            distance = geodesic(home_pos, car_pos).km
            mqtt.publish(f'{data.licensePlate}/distance', distance, 0, True)
            # Seconds to sleep depends on distance to home, closer to home the more frequent updates
            if distance > 30:
                delay = 300
            elif distance >10:
                delay = 60
            elif distance > 5:
                delay = 30
            else:
                delay = 10

        old_data = copy.deepcopy(data)
        time.sleep(delay)
