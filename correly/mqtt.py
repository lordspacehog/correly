import asyncio
import json
import logging
from queue import Queue
from hbmqtt.client import MQTTClient
from hbmqtt.mqtt.constants import QOS_1


class IoTController(object):
    _mqtt_broker_uri = None
    _msg_queue = None

    """Basic IoT controller"""

    def __init__(self, mqtt_broker_uri: str, msg_queue: Queue):
        """init controller

        :mqtt_broker_uri: TODO

        """
        self._mqtt_broker_uri = mqtt_broker_uri
        self._msg_queue = msg_queue

    async def listen_for_events_coro(self):
        client = MQTTClient()
        await client.connect(self._mqtt_broker_uri)
        await client.subscribe([('sensors/+', QOS_1)])
        while True:
            try:
                message = await client.deliver_message()
                if message:
                    packet = message.publish_packet
                    data = json.loads(packet.payload.data)
                    data['location'] = packet.variable_header.topic_name.split('/')[1]
                    self._msg_queue.put(data)
            except asyncio.CancelledError:
                logging.info('Stopping registration listener...')
                client.disconnect()
                break
