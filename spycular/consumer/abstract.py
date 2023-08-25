from abc import ABCMeta, abstractmethod
from types import ModuleType
from typing import Any

from ..pointer.abstract import Pointer
from ..pointer.graph.abstract import PointerGraph
from ..reflection.reflected import ReflectedModule


class AbstractConsumer(metaclass=ABCMeta):
    """An abstract class representing a Consumer.

    This class defines the interface for consumers that interact with storage
    and modules using reflected module and pointers.
    """

    def __init__(self, storage):
        """Initialize the consumer with given storage.

        Args:
            storage: Storage instance to be used by the consumer.
        """
        self.storage = storage
        super().__init__()

    def set_module(self, module: ModuleType) -> None:
        """Set the module for the consumer and wrap it as a
        ReflectedModule object.

        Args:
            module (ModuleType): The python module to be used by the consumer.
        """
        self.reflected_module = ReflectedModule(module)

    @abstractmethod
    def execute(self, ptr: Pointer) -> None:
        """Abstract method to execute operations on the given pointer.

        Args:
            ptr (Pointer): Pointer instance pointing to a specific resource.

        Returns:
            None
        """

    @abstractmethod
    async def execute_graph(self, ptr: PointerGraph) -> None:
        """Abstract method to execute operations on a given pointer
        graph.

        Args:
            ptr (PointerGraph): PointerGraph instance representing a set
            of resources.

        Returns:
            None
        """

    @abstractmethod
    def reply(self, obj_id: str, obj: object) -> Any:
        """Abstract method to handle replies with given object ID and
        object.

        Args:
            obj_id (str): Unique identifier for the object.
            obj (object): The object to be replied with.

        Returns:
            None
        """
