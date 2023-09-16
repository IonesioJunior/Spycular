from types import ModuleType
from typing import Any, Callable, Union

from ..store.abstract import AbstractStore
from ..utils.uuid_gen import generate_uuid
from .abstract import Pointer
from .object_pointer import ObjectActionPointer, ObjectPointer


class ClassPointer(Pointer):
    """ClassPointer represents a specific type of pointer that
    references classes within a given module or library.

    This pointer is capable of retrieving a reference to the class it points to
    and can be equipped with a broker for additional functionalities.
    """

    def __init__(
        self,
        path: str = "",
        pointer_id: str = "",
        broker=None,
        super_pointer=None,
        *args,
        **kwargs,
    ):
        """Initialize the ClassPointer.

        Args:
            path (str, optional): Path to the class within the library.
            pointer_id (str, optional): Unique identifier for the pointer.
            broker (optional): Broker for producing module tasks/events.
        """
        pointer_id = pointer_id or generate_uuid()
        vars(self)["shell"] = False
        vars(self)["args"] = args
        vars(self)["kwargs"] = kwargs

        if super_pointer:
            super().__init__(super_pointer.path, pointer_id)
            self.broker = super_pointer.broker
            super_pointer.id = pointer_id
            super_pointer.path = super_pointer.path + ".__init__"
            super_pointer.args = self.args
            super_pointer.kwargs = self.kwargs
            self.broker.send(super_pointer)
            self.shell = True
        else:
            super().__init__(path, pointer_id)
            self.broker = broker

    def __getattr__(self, name: str) -> ObjectPointer:
        prefix = self.id
        path = name
        return ObjectPointer(
            target_id=prefix,
            path=path,
            parents=(self,),
            broker=self.broker,
            class_attribute=True,
        )

    def __repr__(self) -> str:
        """Object Pointer representation.

        Returns:
            str: Object Pointer representation.
        """
        return f"<ObjectPointer {self.id} \
           path={self.path} >"

    def __setattr__(self, __name: str, __value: Any) -> None:
        if self.shell:
            obj_action = ObjectActionPointer(
                target_id=self.id,
                path="__setattr__",
                args=(__name, __value),
                kwargs={},
                parents=(self,),
            )
            self.broker.send(obj_action)
        else:
            super().__setattr__(__name, __value)

    def __call__(self, *args: Any, **kwds: Any) -> Any:
        """Allows the ClassPointer to be callable. This method can be
        extended to make use of `args` and `kwds` for instantiation.

        Args:
            args (Any): Positional arguments.
            kwds (Any): Keyword arguments.

        Returns:
            Any: Currently returns None by default.
        """
        self.id = generate_uuid()
        self.path = self.path + ".__init__"
        self.args = args
        self.kwargs = kwds
        self.shell = True
        self.broker.send(self)
        return self

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
                old_obj = obj
                new_obj = getattr(obj, attr)
                if attr == "__init__":
                    new_obj = old_obj(  # type: ignore
                        *self.args,
                        **self.kwargs,
                    )
                obj = new_obj
            storage.save(self.id, obj)
            return obj
