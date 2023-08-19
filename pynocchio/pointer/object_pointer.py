from __future__ import annotations

from types import ModuleType
from typing import Any, Callable, Dict, List

from ..store.abstract import AbstractStore
from .abstract import Pointer


class ObjectPointer(Pointer):
    def __init__(
        self,
        path: str = "",
        pointer_id: str = "",
        parents: List[Pointer] = [],
        broker: Any = None,
        target_id=None,
        register=False,
    ):
        super().__init__(path, pointer_id)
        self.parents = parents
        self.broker = broker
        self.__registered = register
        self.target_id = target_id

    def __getattr__(self, name: str) -> ObjectPointer:
        if self.target_id:
            return ObjectPointer(
                target_id=self.target_id,
                path=self.path + "." + name,
                parents=[self],
                broker=self.broker,
            )
        else:
            return ObjectPointer(
                target_id=self.id,
                path=name,
                parents=[self],
                broker=self.broker,
            )

    @property
    def args(self) -> List:
        return []

    @property
    def kwargs(self) -> Dict:
        return {}

    @args.setter
    def args(self, args: List[Any]) -> None:
        pass

    @kwargs.setter
    def kwargs(self, kwargs: Dict[str, Any]) -> None:
        pass

    def __call__(self, *args, **kwargs: Dict[str, Any]) -> ObjectPointer:
        if self.target_id:
            obj_action = ObjectActionPointer(
                target_id=self.target_id,
                path=self.path,
                args=args,
                kwargs=kwargs,
                parents=[self],
            )
        else:
            obj_action = ObjectActionPointer(
                target_id=self.id,
                path=self.path,
                args=args,
                kwargs=kwargs,
                parents=[self],
            )
        self.broker.send(obj_action)
        obj = ObjectPointer(
            pointer_id=obj_action.id,
            parents=[self],
            broker=self.broker,
            register=True,
        )
        return obj

    def __getitem__(self, key: tuple) -> ObjectPointer:
        if self.target_id:
            obj_action = ObjectActionPointer(
                target_id=self.target_id,
                path=self.path + "." + "__getitem__",
                args=(key,),
                parents=[self],
            )
        else:
            temp_obj = self if not self.__registered else None
            obj_action = ObjectActionPointer(
                target_id=self.id,
                path="__getitem__",
                args=(key,),
                parents=[self],
                temp_obj=temp_obj,
            )
        self.broker.send(obj_action)
        obj = ObjectPointer(
            pointer_id=obj_action.id,
            parents=[self],
            broker=self.broker,
            register=True,
        )
        return obj

    def __setitem__(self, key: tuple, value: Any) -> ObjectPointer:
        if self.target_id:
            obj_action = ObjectActionPointer(
                target_id=self.target_id,
                path="__setitem__",
                args=(key, value),
                parents=[self],
            )
        else:
            obj_action = ObjectActionPointer(
                target_id=self.id,
                path="__setitem__",
                args=(key, value),
                parents=[self],
            )
        self.broker.send(obj_action)
        obj = ObjectPointer(
            pointer_id=obj_action.id,
            parents=[self],
            broker=self.broker,
            register=True,
        )
        return obj

    def solve(
        self,
        lib: ModuleType,
        storage: AbstractStore | None = None,
        reply_callback: Callable | None = None,
    ) -> None | Any:
        if storage:
            if storage.has(self.id):
                return storage.get(self.id)
            elif storage.has(self.target_id):
                obj = storage.get(self.target_id)
                for attr in self.path.split("."):
                    obj = getattr(obj, attr)
            else:
                obj = lib

                for attr in self.path.split("."):
                    obj = getattr(obj, attr)

            storage.save(self.id, obj)
        else:
            obj = lib

            for attr in self.path.split("."):
                obj = getattr(obj, attr)

        return obj

    def register(self) -> ObjectPointer:
        self.broker.send(self)
        self.__registered = True
        return self

    def retrieve(self) -> None | ObjectPointer:
        if not self.__registered:
            self.register()

        obj = self.broker.request(GetPointer(target_id=self.id))
        return obj

    def __repr__(self) -> str:
        return f"<ObjectPointer {self.id}  path={self.path}>"


class GetPointer(Pointer):
    def __init__(self, target_id: str, path: str = "", pointer_id: str = ""):
        super().__init__(path, pointer_id)
        self.target_id = target_id

    def solve(
        self,
        lib: ModuleType,
        storage: AbstractStore | None = None,
        reply_callback: Callable | None = None,
    ) -> None | Any:
        if storage and storage.has(self.target_id) and reply_callback:
            reply_callback(self.target_id, storage.get(self.target_id))
        return None


class ObjectActionPointer(Pointer):
    def __init__(
        self,
        target_id: str,
        path: str = "",
        pointer_id: str = "",
        parents: List[Pointer] = [],
        args: tuple[Any, ...] = tuple(),
        kwargs: Dict[str, Any] = {},
        temp_obj: ObjectPointer | None = None,
    ):
        super().__init__(path, pointer_id)
        self.parents = parents
        self.args = args
        self.kwargs = kwargs
        self.target_id = target_id
        self.temp_obj = temp_obj

    def __repr__(self) -> str:
        return f"<ObjectActionPointer {self.id} \
        target_id={self.target_id}  path={self.path} \
        args={self.args}  kwargs={self.kwargs} \
        temp_obj={self.temp_obj}>"

    def solve(
        self,
        lib: ModuleType,
        storage: AbstractStore | None = None,
        reply_callback: Callable | None = None,
    ) -> None | Any:
        if storage:
            if self.temp_obj:
                obj = self.temp_obj.solve(lib)
            else:
                obj = storage.get(self.target_id)

            attributes = self.path.split(".")

            # Parse the entire path using obj as root
            for attr in attributes[:-1]:
                obj = getattr(obj, attr)

            # Get the leaf of the path.
            property = getattr(obj, attributes[-1])

            result = None
            if callable(property):
                result = property(*self.args, **self.kwargs)
            else:
                result = property

            storage.save(self.id, result)

            return result
        else:
            return None
