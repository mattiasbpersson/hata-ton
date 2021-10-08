import json
import pickle
import time
from enum import IntEnum
from pprint import pformat
from typing import Type, Iterable

from paho.mqtt.client import Client as PahoClient, MQTT_ERR_NO_CONN, MQTTMessage

from Event import Event
from EventHandler import EventHandler

class QualityOfService(IntEnum):
    DELIVER_AT_MOST_ONE = 0
    DELIVER_AT_LEAST_ONCE = 1
    DELIVER_EXACTLY_ONCE = 2


class MqttConnectionError(RuntimeError):
    pass


class NotConnectedError(RuntimeError):
    pass


class Client:

    def __init__(self, client_id: str, event_handlers: Iterable[EventHandler] = (), ignore_missed_messages=False,
                 quality_of_service=QualityOfService.DELIVER_AT_LEAST_ONCE):

        self.__client = PahoClient(client_id, ignore_missed_messages)

        self.__subscriptions = dict((event_handler.event_type.topic, event_handler) for event_handler in event_handlers)
        self.__quality_of_service = quality_of_service

        self.__client.on_connect = self.__on_connect
        self.__client.on_message = self.__on_message

        self.__client.connect('localhost')

    def emit_event(self, event: Event, quality_of_service=QualityOfService.DELIVER_AT_LEAST_ONCE, retain=False):
        event_bin = pickle.dumps(event)


        result = self.__client.publish(
            topic=event.topic,
            payload=event_bin,
            qos=quality_of_service,
            retain=retain
        )

    def clear_retained_message(self, topic: str):
        result = self.__client.publish(
            topic=topic,
            payload=None,
            retain=True
        )

    def idle(self, seconds: int):
        for _ in range(seconds):
            self.__idle_1s()

    def listen(self):
        self.__client.loop_forever()

    def __subscribe(self, event_type: Type[Event]):
        result, message_id = self.__client.subscribe(event_type.topic, self.__quality_of_service)
        if result == MQTT_ERR_NO_CONN:
            error_message = 'Cannot subscribe to events before the client is connected!'
            raise NotConnectedError(error_message)

    def __on_connect(self, client, userdata, flags, rc, properties=None):
        class ConnectionResult(IntEnum):
            SUCCESS = 0
            INCORRECT_PROTOCOL_VERSION = 1
            INVALID_CLIENT_ID = 2
            SERVER_UNAVAILABLE = 3
            BAD_USERNAME_OR_PASSWORD = 4
            NOT_AUTHORIZED = 5

        error_messages = {
            ConnectionResult.INCORRECT_PROTOCOL_VERSION: 'Incorrect protocol version',
            ConnectionResult.INVALID_CLIENT_ID: 'Invalid client ID',
            ConnectionResult.SERVER_UNAVAILABLE: 'Mqtt server unavailable',
            ConnectionResult.BAD_USERNAME_OR_PASSWORD: 'Bad username or password',
            ConnectionResult.NOT_AUTHORIZED: 'Not authorized'
        }

        if rc != ConnectionResult.SUCCESS:
            raise MqttConnectionError(error_messages[rc])

        for event_handler in self.__subscriptions.values():
            self.__subscribe(event_handler.event_type)

    def __on_message(self, client, userdata, message: MQTTMessage):
        event_handler = self.__subscriptions[message.topic]
        event_object = pickle.loads(message.payload)
        event_handler.callback(self, event_object)

    def __idle_1s(self):
        start = time.time()
        self.__client.loop(1)
        elapsed = time.time() - start
        remainder = max(1 - elapsed, 0)
        time.sleep(remainder)
