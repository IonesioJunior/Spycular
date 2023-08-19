from abc import ABCMeta, abstractmethod
from typing import Any

from ..pointer.abstract import Pointer
from ..pointer.object_pointer import GetPointer


class AbstractProducer(metaclass=ABCMeta):
    def __init__(self):
        super().__init__()

    @abstractmethod
    def send(self, ptr: Pointer) -> None:
        pass

    @abstractmethod
    def request(self, ptr: GetPointer) -> Any:
        pass
