from __future__ import annotations

from types import ModuleType
from typing import Any, Callable, Dict, Tuple

from ..serde.capnp.recursive import serializable
from ..store.abstract import AbstractStore
from .abstract import Pointer


@serializable
class ObjectPointer(Pointer):
    __exclude__ = ["broker"]

    def __init__(
        self,
        path: str = "",
        pointer_id: str = "",
        parents: Tuple[Any, ...] = tuple(),
        broker: Any = None,
        target_id=None,
        register=False,
    ):
        super().__init__(path, pointer_id)
        self.parents = parents
        self.broker = broker
        self.__registered = register
        self.target_id = target_id

    @property
    def args(self) -> tuple[Any, ...]:
        return tuple()

    @property
    def kwargs(self) -> Dict[str, Any]:
        return dict()

    def __getattr__(self, name: str) -> ObjectPointer:
        prefix = self.target_id or self.id
        path = f"{self.path}.{name}" if self.target_id else name
        return ObjectPointer(
            target_id=prefix,
            path=path,
            parents=(self,),
            broker=self.broker,
        )

    def __wrap_pointer_action(
        self,
        path: str,
        args: tuple = tuple(),
        kwargs: Dict[str, Any] = {},
        temp_obj: ObjectPointer | None = None,
        parents: Tuple[Any, ...] = tuple(),
    ) -> ObjectPointer:
        obj_action = ObjectActionPointer(
            target_id=self.target_id if self.target_id else self.id,
            path=path,
            args=args,
            kwargs=kwargs,
            parents=(self,) + parents,
            temp_obj=temp_obj,
        )
        self.broker.send(obj_action)
        obj = ObjectPointer(
            pointer_id=obj_action.id,
            parents=(self,),
            broker=self.broker,
            register=True,
        )
        return obj

    def __call__(self, *args, **kwargs: Dict[str, Any]) -> ObjectPointer:
        return self.__wrap_pointer_action(
            path=self.path,
            args=args,
            kwargs=kwargs,
        )

    def __getitem__(self, key: tuple) -> ObjectPointer:
        return self.__wrap_pointer_action(
            path=self.path + "." + "__getitem__"
            if self.target_id
            else "__getitem__",
            args=(key,),
            temp_obj=self
            if not self.__registered and not self.target_id
            else None,
        )

    def __setitem__(self, key: tuple, value: Any) -> ObjectPointer:
        return self.__wrap_pointer_action(
            path="__setitem__",
            args=(key, value),
        )

    def __add__(self, other):
        return self.__wrap_pointer_action(
            path="__add__",
            args=(other,),
            parents=(other,),
        )

    def __sub__(self, other):
        return self.__wrap_pointer_action(
            path="__sub__",
            args=(other,),
            parents=(other,),
        )

    def __mul__(self, other):
        return self.__wrap_pointer_action(
            path="__mul__",
            args=(other,),
            parents=(other,),
        )

    def __truediv__(self, other):
        return self.__wrap_pointer_action(
            path="__truediv__",
            args=(other,),
            parents=(other,),
        )

    def __floordiv__(self, other):
        return self.__wrap_pointer_action(
            path="__floordiv__",
            args=(other,),
            parents=(other,),
        )

    def __mod__(self, other):
        return self.__wrap_pointer_action(
            path="__mod__",
            args=(other,),
            parents=(other,),
        )

    def __pow__(self, other):
        return self.__wrap_pointer_action(
            path="__pow__",
            args=(other,),
            parents=(other,),
        )

    def solve(
        self,
        lib: ModuleType,
        storage: AbstractStore | None = None,
        reply_callback: Callable | None = None,
    ) -> None | Any:
        attrs = self.path.split(".")

        if storage:
            # If object is stored, retrieve it.
            if storage.has(self.id):
                return storage.get(self.id)
            # If object isn't stored but pointing to another object.
            elif storage.has(self.target_id):
                obj = storage.get(self.target_id)
                for attr in attrs:
                    obj = getattr(obj, attr)
            # If object isn't stored and isn't pointing to another object.
            # Process it and save it
            else:
                obj = lib
                for attr in attrs:
                    obj = getattr(obj, attr)

            storage.save(self.id, obj)
        # If storage is None, just process the object.
        # This aims to provide temp variables without storing them
        # in the storage.
        else:
            obj = lib
            for attr in attrs:
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
        return f"<ObjectPointer {self.id} \
           path={self.path} parents={self.parents}>"


@serializable
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


@serializable
class ObjectActionPointer(Pointer):
    def __init__(
        self,
        target_id: str,
        path: str = "",
        pointer_id: str = "",
        parents: Tuple[Any, ...] = tuple(),
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
