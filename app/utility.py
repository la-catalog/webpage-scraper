import os

from pika import BasicProperties, BlockingConnection, URLParameters
from pika.spec import PERSISTENT_DELIVERY_MODE

marketplaces = ["americanas", "amazon", "rihappy"]


def get_marketplace_index(url: str):
    for index, marketplace in enumerate(marketplaces):
        if marketplace in url:
            return index
    return 0


def publish_on_queue(message: str, queue: str):
    parameters = URLParameters(os.environ["RABBIT_URI"])
    connection = BlockingConnection(parameters=parameters)
    channel = connection.channel()

    channel.queue_declare(queue=queue, durable=True)
    channel.basic_publish(
        exchange="",
        routing_key=queue,
        body=message,
        properties=BasicProperties(delivery_mode=PERSISTENT_DELIVERY_MODE, priority=1),
        mandatory=True,
    )
    channel.close()
