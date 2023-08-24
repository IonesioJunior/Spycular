from abc import ABCMeta, abstractmethod
from typing import Any


class AbstractStore(metaclass=ABCMeta):
    """Abstract base class for store objects. Defines the essential
    methods any concrete store implementation must provide.

    Attributes:
        store: The actual storage mechanism or backend for this store.

    Methods:
        save: Store an object with a given ID.
        get: Retrieve an object by its ID.
        delete: Remove an object using its ID.
        has: Check if an object with a given ID exists in the store.
    """

    def __init__(self, store) -> None:
        """Initialize the AbstractStore with a storage backend.

        Args:
            store: The storage backend or mechanism.
        """
        self.store = store
        super().__init__()

    @abstractmethod
    def save(self, obj_id: str, obj: Any) -> None:
        """Store an object in the store with a given ID.

        Args:
            obj_id (str): The unique identifier for the object.
            obj: The actual object to store.
        """

    @abstractmethod
    def get(self, obj_id: str) -> Any:
        """Retrieve an object from the store by its ID.

        Args:
            obj_id: The unique identifier for the object.

        Returns:
            The object associated with the provided ID.
        """

    @abstractmethod
    def delete(self, obj_id: str) -> None:
        """Remove an object from the store using its ID.

        Args:
            obj_id: The unique identifier for the object.
        """

    @abstractmethod
    def has(self, obj_id: str) -> bool:
        """Check if the store contains an object with the provided ID.

        Args:
            obj_id: The unique identifier for the object.

        Returns:
            bool: True if the object exists in the store, otherwise False.
        """
