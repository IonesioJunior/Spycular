from abc import ABCMeta, abstractmethod
from types import ModuleType

from ..pointer.abstract import Pointer
from ..pointer.graph.abstract import PointerGraph
from ..puppetry.puppet import Puppet


class AbstractConsumer(metaclass=ABCMeta):
    """An abstract class representing a Consumer.

    This class defines the interface for consumers that interact with storage
    and modules using puppetry and pointers.
    """

    def __init__(self, storage):
        """Initialize the consumer with given storage.

        Args:
            storage: Storage instance to be used by the consumer.
        """
        self.storage = storage
        super().__init__()

    def set_module(self, module: ModuleType):
        """Set the module for the consumer and wrap it as a Puppet
        object.

        Args:
            module (ModuleType): The python module to be used by the consumer.
        """
        self.puppet_module = Puppet(module)

    @abstractmethod
    def execute(self, ptr: Pointer):
        """Abstract method to execute operations on the given pointer.

        Args:
            ptr (Pointer): Pointer instance pointing to a specific resource.

        Returns:
            None
        """

    @abstractmethod
    def execute_graph(self, ptr: PointerGraph):
        """Abstract method to execute operations on a given pointer
        graph.

        Args:
            ptr (PointerGraph): PointerGraph instance representing a set
            of resources.

        Returns:
            None
        """

    @abstractmethod
    def reply(self, obj_id: str, obj: object):
        """Abstract method to handle replies with given object ID and
        object.

        Args:
            obj_id (str): Unique identifier for the object.
            obj (object): The object to be replied with.

        Returns:
            None
        """
