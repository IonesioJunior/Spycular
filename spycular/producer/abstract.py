from abc import ABCMeta, abstractmethod
from typing import Any

from ..pointer.abstract import Pointer
from ..pointer.object_pointer import GetPointer


class AbstractProducer(metaclass=ABCMeta):
    """AbstractProducer represents the base for classes that are
    responsible for producing or sending data based on pointers.

    It provides abstract methods for sending data and requesting specific
    data,which must be implemented by subclasses.
    """

    def __init__(self):
        """Initialize the AbstractProducer."""
        super().__init__()

    @abstractmethod
    def send(self, ptr: Pointer) -> None:
        """Abstract method to send or process data based on a given
        pointer.

        Args:
            ptr (Pointer): Pointer containing information about the data
            to be processed.

        Returns:
            None: This method should not return anything.
        """

    @abstractmethod
    def request(self, ptr: GetPointer) -> Any:
        """Abstract method to request or retrieve data based on a given
        pointer.

        Args:
            ptr (GetPointer): Pointer containing information about the data
            to be retrieved.

        Returns:
            Any: The requested data.
        """
