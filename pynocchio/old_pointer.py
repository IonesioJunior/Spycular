import random

from .serde.capnp.recursive import serializable


def generate_uuid():
    # Generate random values for each section of a UUID
    parts = [
        random.randint(0, 0xFFFF),  # 4 hex digits
        random.randint(0, 0xFFFF),  # 4 hex digits
        random.randint(0, 0x0FFF) | 0x4000,  # 4 hex digits, version 4
        random.randint(0, 0x3FFF)
        | 0x8000,  # 4 hex digits, two most significant bits set to 10
        random.randint(0, 0xFFFFFFFFFFFF),  # 12 hex digits
    ]

    # Convert to a string and format as a UUID
    return "{:04x}-{:04x}-{:04x}-{:04x}-{:012x}".format(*parts)


class GetPointer:
    def __init__(self, ptr_id: str):
        self.ptr_id = ptr_id

    def __repr__(self):
        return f"<GetPointer {self.ptr_id}>"


@serializable
class Pointer:
    __exclude__ = ["broker"]

    def __init__(
        self,
        path="",
        pointer_id="",
        call=False,
        obj_id=None,
        is_obj_ptr=False,
        extending=False,
        class_pointer=None,
        **kwargs,
    ):
        if not pointer_id:
            self.id = generate_uuid()
        else:
            self.id = pointer_id

        self.path = path
        self.args = kwargs.get("args", [])
        self.kwargs = kwargs.get("kwargs", {})
        self.broker = kwargs.get("broker", None)
        self.call = call
        self.obj_id = obj_id
        self.is_obj_ptr = is_obj_ptr

        if extending:
            extending_class = class_pointer
            self.id = class_pointer.id
            self.broker = extending_class.broker
            return

    def __repr__(self) -> str:
        return f"<Pointer {self.id}  path={self.path} args={self.args}  kwrags={self.kwargs} call={self.call} is_obj_ptr={self.is_obj_ptr}>"

    def get(self):
        get_ptr = GetPointer(ptr_id=self.id)
        return self.broker.request(get_ptr)

    def obj_pointer(self):
        return Pointer(
            pointer_id=self.id,
            path=self.path,
            broker=self.broker,
            args=self.args,
            kwargs=self.kwargs,
            call=self.call,
            obj_id=self.obj_id,
            is_obj_ptr=True,
        )

    def __getattr__(self, name):
        ptr = Pointer(obj_id=self.id, path=name, broker=self.broker, call=True)
        self.broker.send(ptr)
        return ptr

    def __call__(self, *args, **kwargs):
        ptr = Pointer(
            obj_id=self.obj_id,
            path=self.path,
            broker=self.broker,
            args=args,
            kwargs=kwargs,
            call=True,
        )
        self.broker.send(ptr)
        return ptr.obj_pointer()

    def __iter__(self):
        ptr = Pointer(
            obj_id=self.id,
            path="__iter__",
            broker=self.broker,
            call=True,
        )
        self.broker.send(ptr)
        return ptr

    def __next__(self):
        ptr = Pointer(
            obj_id=self.id,
            path="__next__",
            broker=self.broker,
            call=True,
        )
        self.broker.send(ptr)
        return ptr

    def __getitem__(self, key):
        ptr = Pointer(
            obj_id=self.id,
            path="__getitem__",
            broker=self.broker,
            args=(key,),
            kwargs={},
            call=True,
        )
        self.broker.send(ptr)
        return ptr

    def __setitem__(self, key, value):
        ptr = Pointer(
            obj_id=self.id,
            path="__setitem__",
            broker=self.broker,
            args=(key, value),
            kwargs={},
            call=True,
        )
        self.broker.send(ptr)
        return ptr

    def __add__(self, other):
        ptr = Pointer(
            obj_id=self.id,
            path="__add__",
            broker=self.broker,
            args=(other,),
            kwargs={},
            call=True,
        )
        self.broker.send(ptr)
        return ptr

    def __sub__(self, other):
        ptr = Pointer(
            obj_id=self.id,
            path="__sub__",
            broker=self.broker,
            args=(other,),
            kwargs={},
            call=True,
        )
        self.broker.send(ptr)
        return ptr

    def __mul__(self, other):
        ptr = Pointer(
            obj_id=self.id,
            path="__mul__",
            broker=self.broker,
            args=(other,),
            kwargs={},
            call=True,
        )
        self.broker.send(ptr)
        return ptr

    def __truediv__(self, other):
        ptr = Pointer(
            obj_id=self.id,
            path="__truediv__",
            broker=self.broker,
            args=(other,),
            kwargs={},
            call=True,
        )
        self.broker.send(ptr)
        return ptr

    def __floordiv__(self, other):
        ptr = Pointer(
            obj_id=self.id,
            path="__floordiv__",
            broker=self.broker,
            args=(other,),
            kwargs={},
            call=True,
        )
        self.broker.send(ptr)
        return ptr

    def __mod__(self, other):
        ptr = Pointer(
            obj_id=self.id,
            path="__mod__",
            broker=self.broker,
            args=(other,),
            kwargs={},
            call=True,
        )
        self.broker.send(ptr)
        return ptr

    def __pow__(self, other):
        ptr = Pointer(
            obj_id=self.id,
            path="__pow__",
            broker=self.broker,
            args=(other,),
            kwargs={},
            call=True,
        )
        self.broker.send(ptr)
        return ptr

    def __mro_entries__(self, bases):
        return (self,)
