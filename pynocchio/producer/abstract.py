from abc import ABC, abstractclassmethod

from ..pointer import GetPointer, Pointer


class AbstractProducer(ABC):
    def __init__(self):
        super().__init__()

    @abstractclassmethod
    def send(self, ptr: Pointer):
        pass

    @abstractclassmethod
    async def send(self, ptr: Pointer):
        pass

    @abstractclassmethod
    def request(self, ptr: GetPointer):
        pass

    @abstractclassmethod
    async def request(self, ptr: GetPointer):
        pass
