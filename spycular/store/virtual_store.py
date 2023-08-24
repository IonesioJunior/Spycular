from .abstract import AbstractStore


class VirtualStore(AbstractStore):
    """A concrete implementation of the AbstractStore that uses an in-
    memory dictionary as its storage backend. This provides quick
    storage and retrieval but lacks persistence across sessions.

    Methods:
        get: Retrieve an object by its ID from the store.
        save: Store an object with a given ID.
        delete: Remove an object using its ID from the store.
        has: Check if an object with a given ID exists in the store.
    """

    def __init__(self) -> None:
        """Initialize the VirtualStore with an empty dictionary as its
        storage backend."""
        super().__init__(store={})

    def get(self, obj_id):
        """Retrieve an object from the store by its ID.

        Args:
            obj_id: The unique identifier for the object.

        Returns:
            The object associated with the provided ID or None.
        """
        return self.store.get(obj_id, None)

    def save(self, obj_id, obj):
        """Store an object in the store with a given ID.

        Args:
            obj_id: The unique identifier for the object.
            obj: The actual object to store.
        """
        self.store[obj_id] = obj

    def delete(self, obj_id):
        """Remove an object from the store using its ID.

        Args:
            obj_id: The unique identifier for the object.

        Raises:
            KeyError: If the object with the provided ID does not exist.
        """
        del self.store[obj_id]

    def has(self, obj_id) -> bool:
        """Check if the store contains an object with the provided ID.

        Args:
            obj_id: The unique identifier for the object.

        Returns:
            bool: True if the object exists in the store, otherwise False.
        """
        return obj_id in self.store.keys()
