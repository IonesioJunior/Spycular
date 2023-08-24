from typing import Any

from ..pointer.abstract import Pointer
from ..pointer.graph.abstract import PointerGraph
from .abstract import AbstractConsumer


class VirtualConsumer(AbstractConsumer):
    """VirtualConsumer is an implementation of the AbstractConsumer that
    interacts virtually with message and reply queues.

    This class can listen to messages, execute them, and handle replies using
    the underlying reflected module and storage system.
    """

    def __init__(self, storage, message_queue, reply_queue):
        """Initialize the virtual consumer with given storage, message
        queue, and reply queue.

        Args:
            storage: Storage instance to be used by the consumer.
            message_queue (list): List-based queue for incoming messages.
            reply_queue (dict): Dictionary-based queue for outgoing replies.
        """
        super().__init__(storage)
        self.message_queue = message_queue
        self.reply_queue = reply_queue

    def listen(self):
        """Continuously listen and process messages from the message
        queue.

        Messages are expected to be of type Pointer.
        """
        while len(self.message_queue):
            ptr = self.message_queue.pop(0)
            self.execute(ptr)

    async def listen_graph(self):
        """Asynchronously listen and process graph-based messages from
        the message queue.

        Messages are expected to be of type PointerGraph.
        """
        while len(self.message_queue):
            graph = self.message_queue.pop(0)
            await self.execute_graph(graph)

    def execute(self, ptr: Pointer):
        """Execute operations on the given pointer using the reflected
        module.

        Args:
            ptr (Pointer): Pointer instance pointing to a specific resource.
        """
        self.reflected_module.execute(
            pointer=ptr,
            storage=self.storage,
            reply_callback=self.reply,
        )

    async def execute_graph(self, graph: PointerGraph):
        """Asynchronously execute operations on a given pointer graph
        using the reflected module.

        Args:
            graph (PointerGraph): PointerGraph instance representing a set
            of resources.
        """
        await graph.async_solve(
            reflected_module=self.reflected_module,
            storage=self.storage,
            reply_callback=self.reply,
        )

    def reply(self, obj_id: str, obj: Any):
        """Handle replies by storing them in the reply queue with the
        corresponding object ID.

        Args:
            obj_id (str): Unique identifier for the object.
            obj (Any): The object to be stored as a reply.
        """
        self.reply_queue[obj_id] = obj
