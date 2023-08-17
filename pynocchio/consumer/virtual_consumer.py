from .abstract import AbstractConsumer


class VirtualConsumer(AbstractConsumer):
    def __init__(self, storage, reverse_lib, message_queue, reply_queue):
        super().__init__(storage, reverse_lib)
        self.message_queue = message_queue
        self.reply_queue = reply_queue

    def listen(self):
        while len(self.message_queue):
            msg = self.message_queue.pop(0)
            self.execute(msg=msg)

    def reply(self, obj_id, obj):
        self.reply_queue[obj_id] = obj
