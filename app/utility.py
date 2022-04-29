import os
import json
from pika import URLParameters, BlockingConnection, BasicProperties
from pika.spec import PERSISTENT_DELIVERY_MODE

marketplaces = ["americanas", "amazon"]


def get_marketplace_index(url: str):
    for index, marketplace in enumerate(marketplaces):
        if marketplace in url:
            return index
    return 0


def publish_on_queue(message: dict, queue: str):
    message = json.dumps(message)
    parameters = URLParameters(os.environ["RABBIT_URI"])
    connection = BlockingConnection(parameters=parameters)
    channel = connection.channel()
    channel.basic_publish(
        exchange="amqp_direct",
        routing_key=queue,
        body=message,
        properties=BasicProperties(delivery_mode=PERSISTENT_DELIVERY_MODE, priority=1),
    )
    channel.close()
