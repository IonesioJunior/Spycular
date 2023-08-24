from types import ModuleType

from .consumer.abstract import AbstractConsumer
from .producer.abstract import AbstractProducer
from .reflection.incident import IncidentModule


def strike(module: ModuleType, producer: AbstractProducer):
    return IncidentModule(lib=module, broker=producer)


def reflect(module: ModuleType, consumer: AbstractConsumer):
    consumer.set_module(module)
    return consumer
