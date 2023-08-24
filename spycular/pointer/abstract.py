from abc import ABCMeta, abstractmethod
from types import ModuleType
from typing import Any, Callable, Union

from ..store.abstract import AbstractStore
from ..utils.uuid_gen import generate_uuid


class Pointer(metaclass=ABCMeta):
    """Abstract class representing a Pointer.

    A Pointer is an abstract reference that points to a location or resource,
    identifiable with an ID and path. This class provides a common interface
    for different types of pointers to solve or resolve the resource they point
    to.
    """

    def __init__(self, path: str = "", pointer_id: str = ""):
        """Initialize the pointer with a given path and pointer ID.

        Args:
            path (str, optional): Pointer path. Defaults to an empty string.
            pointer_id (str, optional): A unique identifier for the pointer.
        """
        if not pointer_id:
            self.id = generate_uuid()
        else:
            self.id = pointer_id
        self.path = path

    @abstractmethod
    def solve(
        self,
        lib: ModuleType,
        storage: AbstractStore,
        reply_callback: Callable,
    ) -> Union[None, Any]:
        """Abstract method to resolve or dereference the resource the
        pointer references.

        Args:
            lib (ModuleType): Module with functionality to solve pointers.
            storage (AbstractStore): A storage instance used solve pointers.
            reply_callback (Callable): A callback method to handle replies.

        Returns:
            Union[None, Any]: The result of solving the pointer or None.
        """
