from typing import Any

from .abstract import AbstractConsumer


class VirtualConsumer(AbstractConsumer):
    def __init__(self, storage, message_queue, reply_queue):
        super().__init__(storage)
        self.message_queue = message_queue
        self.reply_queue = reply_queue

    def listen(self):
        while len(self.message_queue):
            ptr = self.message_queue.pop(0)
            self.execute(ptr)

    def execute(self, ptr):
        self.puppet_module.execute(
            pointer=ptr,
            storage=self.storage,
            reply_callback=self.reply,
        )

    def reply(self, obj_id: str, obj: Any):
        self.reply_queue[obj_id] = obj
