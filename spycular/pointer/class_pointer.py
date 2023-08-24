from types import ModuleType
from typing import Any, Callable, Union

from ..store.abstract import AbstractStore
from .abstract import Pointer


class ClassPointer(Pointer):
    """ClassPointer represents a specific type of pointer that
    references classes within a given module or library.

    This pointer is capable of retrieving a reference to the class it points to
    and can be equipped with a broker for additional functionalities.
    """

    def __init__(self, path: str = "", pointer_id: str = "", broker=None):
        """Initialize the ClassPointer.

        Args:
            path (str, optional): Path to the class within the library.
            pointer_id (str, optional): Unique identifier for the pointer.
            broker (optional): Broker for producing module tasks/events.
        """
        super().__init__(path, pointer_id)
        self.broker = broker

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        """Allows the ClassPointer to be callable. This method can be
        extended to make use of `args` and `kwds` for instantiation.

        Args:
            args (Any): Positional arguments.
            kwds (Any): Keyword arguments.

        Returns:
            Any: Currently returns None by default.
        """
        return None

    def solve(
        self,
        lib: ModuleType,
        storage: AbstractStore,
        reply_callback: Callable,
    ) -> Union[None, Any]:
        """Resolve the pointer, retrieving the referenced class from the
        provided library.

        Args:
            lib (ModuleType): Library or module where the class is located.
            storage (AbstractStore): Storage to get/save the class reference.
            reply_callback (Callable): Callback for replies.

        Returns:
            Union[None, Any]: A reference to the class or None if not found.
        """
        if storage.has(self.id):
            return storage.get(self.id)
        else:
            obj = lib

            for attr in self.path.split("."):
                obj = getattr(obj, attr)

            storage.save(self.id, obj)
            return obj
