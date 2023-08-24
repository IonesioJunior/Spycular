from types import ModuleType
from typing import Any, Callable, Dict, List, Union

from ..serde.capnp.recursive import serializable
from ..store.abstract import AbstractStore
from .abstract import Pointer


@serializable
class CallablePointer(Pointer):
    """CallablePointer represents a specific kind of pointer that
    references callable objects in a given module or library.

    The pointer can have arguments and keyword arguments associated with it,
    which can be used when invoking the callable.
    """

    def __init__(
        self,
        path: str = "",
        pointer_id: str = "",
        args: List[Any] = [],
        kwargs: Dict[str, Any] = {},
    ):
        """Initialize the CallablePointer.

        Args:
            path (str, optional): Path to the library callable object.
            pointer_id (str, optional): Unique identifier for the pointer.
            args (List[Any], optional): List of arguments for the callable.
            kwargs (Dict[str, Any], optional): Callable keyword arguments.
        """
        super().__init__(path, pointer_id)
        self.args = args
        self.kwargs = kwargs

    def __repr__(self) -> str:
        """Provide a developer-friendly representation of the object."""
        return f"<CallablePointer {self.id} path={self.path}\
        args={self.args} kwargs={self.kwargs}>"

    def solve(
        self,
        lib: ModuleType,
        storage: AbstractStore,
        reply_callback: Callable,
    ) -> Union[None, Any]:
        """Resolve the pointer, invoking the referenced callable with
        the specified arguments and keyword arguments.

        Args:
            lib (ModuleType): Library or module where the callable is located.
            storage (AbstractStore): Storage to save results.
            reply_callback (Callable): Callback for any replies.

        Returns:
            Union[None, Any]: Result of the callable invocation, or None.
        """
        obj = lib

        attributes = self.path.split(".")
        for attr in attributes:
            obj = getattr(obj, attr)

        result = obj(*self.args, **self.kwargs) if callable(obj) else obj
        storage.save(self.id, result)
        return None


@serializable
class BuiltinPointer(CallablePointer):
    """BuiltinPointer is a specific kind of CallablePointer representing
    built- in Python functions or methods."""

    def __init__(
        self,
        path: str = "",
        pointer_id: str = "",
        args: List[Any] = [],
        kwargs: Dict[str, Any] = {},
    ):
        super().__init__(path, pointer_id, args, kwargs)

    def __repr__(self) -> str:
        """Provide a developer-friendly representation of the object."""
        return f"<BuiltinPointer {self.id} path={self.path}\
        args={self.args} kwargs={self.kwargs}>"


@serializable
class FunctionPointer(CallablePointer):
    """FunctionPointer is a specific kind of CallablePointer that
    represents standard Python functions."""

    def __init__(
        self,
        path: str = "",
        pointer_id: str = "",
        args: List[Any] = [],
        kwargs: Dict[str, Any] = {},
    ):
        super().__init__(path, pointer_id, args, kwargs)

    def __repr__(self) -> str:
        """Provide a developer-friendly representation of the object."""
        return f"<FunctionPointer {self.id} path={self.path}\
        args={self.args} kwargs={self.kwargs}>"


@serializable
class MethodPointer(CallablePointer):
    """MethodPointer is a specific kind of CallablePointer representing
    methods of Python objects or classes."""

    def __init__(
        self,
        path: str = "",
        pointer_id: str = "",
        args: List[Any] = [],
        kwargs: Dict[str, Any] = {},
    ):
        super().__init__(path, pointer_id, args, kwargs)

    def __repr__(self) -> str:
        """Provide a developer-friendly representation of the object."""
        return f"<MethodPointer {self.id} path={self.path} \
        args={self.args} kwargs={self.kwargs}>"
