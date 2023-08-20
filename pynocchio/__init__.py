from types import ModuleType

from .consumer.abstract import AbstractConsumer
from .producer.abstract import AbstractProducer
from .puppetry.puppeteer import Puppeteer


def control(module: ModuleType, producer: AbstractProducer):
    return Puppeteer(lib=module, broker=producer)


def serve(module: ModuleType, consumer: AbstractConsumer):
    consumer.set_module(module)
    return consumer
