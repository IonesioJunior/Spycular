from ..pointer import GetPointer, Pointer
from .abstract import AbstractProducer


class VirtualProducer(AbstractProducer):
    def __init__(self, message_queue, reply_queue):
        super().__init__()
        self.message_queue = message_queue
        self.reply_queue = reply_queue

    def send(self, ptr: Pointer):
        self.message_queue.append(ptr)

    def request(self, ptr: GetPointer):
        self.message_queue.append(ptr)
        return self.reply_queue.get(ptr)
