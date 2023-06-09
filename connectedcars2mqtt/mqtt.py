''' Internal MQTT handler for the project '''
import logging
from time import sleep
import paho.mqtt.client as mqtt

class MQTT(mqtt.Client):
    ''' Mqtt handler, takes care of adding a root topic to all topics
        managed by this class, so others do not have to be aware of
        this root topic
    '''
    #pylint: disable=too-many-instance-attributes
    __root = ''
    #pylint: disable=too-many-arguments
    def __init__(self,
                 host='127.0.0.1',
                 port=1883,
                 client='chrome',
                 root='',
                 user=None,
                 password=None):  #pylint: disable=too-many-arguments, line-too-long
        super().__init__(host, port)
        self.subscriptions = []
        self.host = host
        self.port = int(port)
        if root != '':
            if root[-1] != '/':
                self.__root = root + '/'
            else:
                self.__root = root
        self.on_log = self.__on_log
        self.on_connect = self.__on_connect
        self.on_disconnect = self.__on_disconnect
        self.log = logging.getLogger('mqtt')
        self._client_id = client
        if user is not None:
            self.username_pw_set(user, password)
        self.__connect()

    def subscribe(self, topic, qos=0):  #pylint: disable=arguments-differ
        ''' subscribe to a topic '''
        if topic not in self.subscriptions:
            self.subscriptions.append(topic)
        topic = self.__root + topic
        self.log.info('subscribing - %s : %s', topic, len(self.subscriptions))
        super().subscribe(topic, qos)

    def message_callback_add(self, sub, callback):
        ''' Add message callbacks, is called when a message matching topic is received '''
        self.subscribe(sub)
        sub = self.__root + sub
        super().message_callback_add(sub, callback)

    def publish(self, topic, payload=None, qos=0, retain=False):  #pylint: disable=arguments-differ
        ''' publish on mqtt, adding root topic to the topic '''
        topic = self.__root + topic
        if self.is_connected:
            super().publish(topic, payload, qos, retain)

    def __on_connect(self, mqttc, obj, flags, rc):  # pylint: disable=unused-argument, invalid-name, arguments-differ
        ''' handle connection established '''
        self.log.warning('Connect %s', rc)
        if rc == 0:
            self.is_connected = True
            for subscription in self.subscriptions:
                self.subscribe(subscription)
        else:
            raise ConnectionError('Connection failed')

    def __on_disconnect(self, client, userdata, rc):  # pylint: disable=unused-argument, invalid-name, arguments-differ
        ''' handle disconnects '''
        self.log.warning('Disconnected, reconnecting')
        self.is_connected = False
        self.reconnect()

    def __on_log(self, mqttc, obj, level, buf):  # pylint: disable=unused-argument, arguments-differ
        ''' Log handler function '''
        self.log.debug(buf)

    def __connect(self):
        ''' Connect to the mqtt broker '''
        self.connect(self.host, self.port, 30)
        self.loop_start()
        while not self.is_connected:
            sleep(1)
            self.log.info('Waiting for connection to %s', self.host)
