from typing import Any

from ..pointer.abstract import Pointer
from ..pointer.object_pointer import GetPointer
from .abstract import AbstractProducer


class VirtualProducer(AbstractProducer):
    """VirtualProducer is an implementation of the AbstractProducer that
    manages communication using in-memory message and reply queues.

    It allows sending pointers to a message queue and requesting data based on
    pointers by interacting with a reply queue.
    """

    def __init__(self, message_queue, reply_queue):
        """Initialize the VirtualProducer.

        Args:
            message_queue: In-memory queue where pointers wait for processing.
            reply_queue: In-memory queue where results/responses are stored.
        """
        super().__init__()
        self.message_queue = message_queue
        self.reply_queue = reply_queue

    def send(self, ptr: Pointer) -> None:
        """Send or enqueue a pointer to the message queue.

        Args:
            ptr (Pointer): The pointer to be sent or enqueued.
        """
        self.message_queue.append(ptr)

    def request(self, ptr: GetPointer) -> Any:
        """Request or retrieve data based on a given pointer. The method
        enqueues the pointer to the message queue and waits for a
        corresponding reply in the reply queue.

        Args:
            ptr (GetPointer): Pointer containing information about the data
            to be retrieved.

        Returns:
            Any: The data retrieved based on the pointer.
        """
        self.message_queue.append(ptr)
        return self.reply_queue.get(ptr)
