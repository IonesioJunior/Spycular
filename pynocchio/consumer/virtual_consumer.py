from .abstract import AbstractConsumer


class VirtualConsumer(AbstractConsumer):
    def __init__(self, storage, message_queue, reply_queue):
        super().__init__(storage)
        self.message_queue = message_queue
        self.reply_queue = reply_queue

    def listen(self):
        while len(self.message_queue):
            ptr = self.message_queue.pop(0)
            self.puppet_module.execute(
                pointer=ptr,
                storage=self.storage,
                reply_callback=self.reply,
            )

    def reply(self, obj_id, obj):
        self.reply_queue[obj_id] = obj
