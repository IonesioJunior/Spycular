from typing import Any

from ..pointer.abstract import Pointer
from ..pointer.object_pointer import GetPointer
from .abstract import AbstractProducer


class VirtualProducer(AbstractProducer):
    def __init__(self, message_queue, reply_queue):
        super().__init__()
        self.message_queue = message_queue
        self.reply_queue = reply_queue

    def send(self, ptr: Pointer) -> None:
        self.message_queue.append(ptr)

    def request(self, ptr: GetPointer) -> Any:
        self.message_queue.append(ptr)
        return self.reply_queue.get(ptr)
