# object_pointer.pyx

from types import ModuleType
from typing import Any, Callable, Dict, List, Tuple

from .abstract_store import AbstractStore
from .object_pointer import GetPointer, ObjectActionPointer


cdef class ObjectPointer:
    cdef public bytes path, pointer_id, target_id
    cdef public tuple parents
    cdef public object broker
    cdef public bint __registered
    cdef Dict[str, Any] kwargs_dict

    def __init__(self,
                 path: str = "",
                 pointer_id: str = "",
                 parents: tuple = tuple(),
                 broker: Any = None,
                 target_id=None,
                 register=False):
        self.path = path.encode('utf-8')
        self.pointer_id = pointer_id.encode('utf-8')
        self.target_id = target_id.encode('utf-8') if target_id else None
        self.parents = parents
        self.broker = broker
        self.__registered = register
        self.kwargs_dict = Dict[str, Any]()

    @property
    def args(self) -> tuple:
        return tuple()

    @property
    def kwargs(self) -> Dict[str, Any]:
        return {}

    def __getattr__(self, name: str) -> 'ObjectPointer':
        prefix = self.target_id or self.id
        path = f"{self.path}.{name}" if self.target_id else name
        return ObjectPointer(
            target_id=prefix,
            path=path,
            parents=(self,),
            broker=self.broker,
        )

    def __getattr__(self, name: str) -> ObjectPointer:
        cdef bytes prefix = self.target_id or self.id
        cdef bytes full_path
        if self.target_id:
            full_path = self.path + b"." + name.encode('utf-8')
        else:
            full_path = name.encode('utf-8')

        return ObjectPointer(
            target_id=prefix,
            path=full_path.decode('utf-8'),
            parents=(self,),
            broker=self.broker,
        )

    def __wrap_pointer_action(
        self,
        path: str,
        args: tuple = tuple(),
        kwargs: Dict[str, Any] = {},
        temp_obj: 'ObjectPointer' = None,
        parents: tuple = tuple()) -> 'ObjectPointer':
        # Original implementation
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

    def __call__(self, *args, **kwargs: Dict[str, Any]) -> 'ObjectPointer':
        return self.__wrap_pointer_action(
            path=self.path,
            args=args,
            kwargs=kwargs,
        )

    def __getitem__(self, key: tuple) -> 'ObjectPointer':
        return self.__wrap_pointer_action(
            path=self.path + "." + "__getitem__"
            if self.target_id
            else "__getitem__",
            args=(key,),
            temp_obj=self
            if not self.__registered and not self.target_id
            else None,
        )

    def __setitem__(self, key: tuple, value: Any) -> 'ObjectPointer':
        self.__wrap_pointer_action(
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
        storage: 'AbstractStore' = None,
        reply_callback: Callable = None) -> Any:
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
        else:
            obj = lib
            for attr in attrs:
                obj = getattr(obj, attr)
        return obj

    def register(self) -> 'ObjectPointer':
        self.broker.send(self)
        self.__registered = True
        return self

    def retrieve(self) -> 'ObjectPointer':
        if not self.__registered:
            self.register()
        obj = self.broker.request(GetPointer(target_id=self.id))
        return obj
