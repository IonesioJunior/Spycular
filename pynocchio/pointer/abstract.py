from abc import ABCMeta, abstractmethod
from types import ModuleType
from typing import Any, Callable, Union

from ..store.abstract import AbstractStore
from ..utils.uuid_gen import generate_uuid


class Pointer(metaclass=ABCMeta):
    def __init__(self, path: str = "", pointer_id: str = ""):
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
        pass
