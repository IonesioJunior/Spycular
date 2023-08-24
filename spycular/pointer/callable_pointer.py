from types import ModuleType
from typing import Any, Callable, Dict, List, Union

from ..serde.capnp.recursive import serializable
from ..store.abstract import AbstractStore
from .abstract import Pointer


@serializable
class CallablePointer(Pointer):
    def __init__(
        self,
        path: str = "",
        pointer_id: str = "",
        args: List[Any] = [],
        kwargs: Dict[str, Any] = {},
    ):
        super().__init__(path, pointer_id)
        self.args = args
        self.kwargs = kwargs

    def __repr__(self) -> str:
        return f"<CallablePointer {self.id} \
        path={self.path} args={self.args} \
        kwargs={self.kwargs}>"

    def solve(
        self,
        lib: ModuleType,
        storage: AbstractStore,
        reply_callback: Callable,
    ) -> Union[None, Any]:
        obj = lib

        attributes = self.path.split(".")
        for attr in attributes:
            obj = getattr(obj, attr)

        result = obj(*self.args, **self.kwargs) if callable(obj) else obj
        storage.save(self.id, result)
        return None


@serializable
class BuiltinPointer(CallablePointer):
    def __init__(
        self,
        path: str = "",
        pointer_id: str = "",
        args: List[Any] = [],
        kwargs: Dict[str, Any] = {},
    ):
        super().__init__(path, pointer_id, args, kwargs)

    def __repr__(self) -> str:
        return f"<BuiltinPointer {self.id} \
        path={self.path} args={self.args} \
        kwargs={self.kwargs}>"


@serializable
class FunctionPointer(CallablePointer):
    def __init__(
        self,
        path: str = "",
        pointer_id: str = "",
        args: List[Any] = [],
        kwargs: Dict[str, Any] = {},
    ):
        super().__init__(path, pointer_id, args, kwargs)

    def __repr__(self) -> str:
        return f"<FunctionPointer {self.id} \
        path={self.path} args={self.args} \
        kwargs={self.kwargs}>"


@serializable
class MethodPointer(CallablePointer):
    def __init__(
        self,
        path: str = "",
        pointer_id: str = "",
        args: List[Any] = [],
        kwargs: Dict[str, Any] = {},
    ):
        super().__init__(path, pointer_id, args, kwargs)

    def __repr__(self) -> str:
        return f"<MethodPointer {self.id} \
        path={self.path} args={self.args} \
        kwargs={self.kwargs}>"
