from types import ModuleType
from typing import Any, Callable, Union

from ..store.abstract import AbstractStore
from .abstract import Pointer


class ClassPointer(Pointer):
    def __init__(self, path: str = "", pointer_id: str = "", broker=None):
        super().__init__(path, pointer_id)
        self.broker = broker

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        return None

    def solve(
        self,
        lib: ModuleType,
        storage: AbstractStore,
        reply_callback: Callable,
    ) -> Union[None, Any]:
        if storage.has(self.id):
            return storage.get(self.id)
        else:
            obj = lib

            for attr in self.path.split("."):
                obj = getattr(obj, attr)

            storage.save(self.id, obj)
            return obj
