from __future__ import annotations

from types import ModuleType
from typing import Any, Callable, Dict, Tuple

from ..serde.capnp.recursive import serializable
from ..store.abstract import AbstractStore
from .abstract import Pointer


@serializable
class ObjectPointer(Pointer):
    """A pointer representation for an object, supporting a range of
    Python magic methods to emulate object behavior, while remaining a
    pointer.

    The main use case is for remote or deferred execution where the real
    objects might be elsewhere.
    """

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
        """Initialize an ObjectPointer.

        Args:
            path (str): Path to the object.
            pointer_id (str): ID for the pointer.
            parents (Tuple): Ancestral pointers leading to this pointer.
            broker (Any): Broker facilitating communication.
            target_id: The ID of the target object.
            register (bool): Whether this object is registered.
        """
        super().__init__(path, pointer_id)
        self.parents = parents
        self.broker = broker
        self.__registered = register
        self.target_id = target_id

    @property
    def args(self) -> tuple[Any, ...]:
        """
        Returns:
            tuple: Arguments for the object.
        """
        return tuple()

    @property
    def kwargs(self) -> Dict[str, Any]:
        """
        Returns:
            dict: Keyword arguments for the object.
        """
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
        """Create and send an ObjectActionPointer based on the provided
        arguments, then return a new ObjectPointer associated with that
        action.

        Args:
            path (str): The path to the object action.
            args (tuple, optional):  ObjectAction positional args.
            Defaults to an empty tuple.
            kwargs (Dict[str, Any], optional): ObjectAction keyword args.
            Defaults to an empty dictionary.
            temp_obj (ObjectPointer, optional): A temporary object for storing
            intermediate states. Defaults to None.
            parents (Tuple[Any, ...], optional): Ancestral pointers leading to
            this action. By default, it only includes the current object.

        Returns:
            ObjectPointer: A new ObjectPointer associated with the action.
        """
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
        """Dunder method that aims to represent any pointer call.

        Args:
            args (tuple, optional): Positional args for object the action.
            Defaults to an empty tuple.
            kwargs (Dict[str, Any], optional): Keyword args for object action.
            Defaults to an empty dictionary.
        """
        return self.__wrap_pointer_action(
            path=self.path,
            args=args,
            kwargs=kwargs,
        )

    def __getitem__(self, key: tuple) -> ObjectPointer:
        """Dunder method that aims to represent any pointer __getitem__.

        Args:
            key (tuple): Key used to get the proper item.
        """
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
        """Dunder method that aims to represent any pointer __setitem__.

        Args:
            key (tuple): Key used to set the proper item.
        """
        return self.__wrap_pointer_action(
            path="__setitem__",
            args=(key, value),
        )

    def __add__(self, other: Any) -> ObjectPointer:
        """Dunder method that aims to represent any pointer add
        operation.

        Args:
            other (Any): Object used to perform add operation.
        """
        return self.__wrap_pointer_action(
            path="__add__",
            args=(other,),
            parents=(other,),
        )

    def __sub__(self, other: Any) -> ObjectPointer:
        """Dunder method that aims to represent any pointer sub
        operation.

        Args:
            other (Any): Object used to perform sub operation.
        """
        return self.__wrap_pointer_action(
            path="__sub__",
            args=(other,),
            parents=(other,),
        )

    def __mul__(self, other: Any) -> ObjectPointer:
        """Dunder method that aims to represent any pointer mul
        operation.

        Args:
            other (Any): Object used to perform mul operation.
        """
        return self.__wrap_pointer_action(
            path="__mul__",
            args=(other,),
            parents=(other,),
        )

    def __truediv__(self, other: Any) -> ObjectPointer:
        """Dunder method that aims to represent any pointer __truediv__
        operation.

        Args:
            other (Any): Object used to perform __truediv__ operation.
        """
        return self.__wrap_pointer_action(
            path="__truediv__",
            args=(other,),
            parents=(other,),
        )

    def __floordiv__(self, other: Any) -> ObjectPointer:
        """Dunder method that aims to represent any pointer __floordiv__
        operation.

        Args:
            other (Any): Object used to perform __floordiv__ operation.
        """
        return self.__wrap_pointer_action(
            path="__floordiv__",
            args=(other,),
            parents=(other,),
        )

    def __mod__(self, other: Any) -> ObjectPointer:
        """Dunder method that aims to represent any pointer __mod__
        operation.

        Args:
            other (Any): Object used to perform __mod__ operation.
        """
        return self.__wrap_pointer_action(
            path="__mod__",
            args=(other,),
            parents=(other,),
        )

    def __pow__(self, other):
        """Dunder method that aims to represent any pointer __pow__
        operation.

        Args:
            other (Any): Object used to perform __pow__ operation.
        """
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
        """ObjectPointer abstract method implementation to resolve this
        Object Pointer.

        This method aims to resolve the object pointed by this Object Pointer.
        This is how each pointer in our stack knows how to solve themselves.

        In case of ObjectPointer, we'll try to retrieve the object from the
        storage. If it's not there, we'll try to retrieve the object pointed
        by this Object Pointer (by target_id). If it's not there either, we'll
        process the object and save it in the storage.

        Args:
            lib (ModuleType): The module the consumer is reflecting.
            storage (AbstractStore, optional): The storage  where we'll
            get/retrieve data. Defaults to None.
            reply_callback (Callable, optional): The callback to reply
            to the broker. Defaults to None.
        Returns:
            None | Any: The object pointed by this Object Pointer.
        """
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
        """Force register this Object Pointer. In case it wasn't
        registered before.

        Returns:
            ObjectPointer: This Object Pointer.
        """
        self.broker.send(self)
        self.__registered = True
        return self

    def retrieve(self) -> None | ObjectPointer:
        """Retrieve the Object Pointer value from the consumer.

        Returns:
            None | ObjectPointer: The Object Pointer value.
        """
        if not self.__registered:
            self.register()

        obj = self.broker.request(GetPointer(target_id=self.id))
        return obj

    def __repr__(self) -> str:
        """Object Pointer representation.

        Returns:
            str: Object Pointer representation.
        """
        return f"<ObjectPointer {self.id} \
           path={self.path} parents={self.parents}>"


@serializable
class GetPointer(Pointer):
    """A specialized pointer that requests or fetches a target object
    based on its ID."""

    def __init__(self, target_id: str, path: str = "", pointer_id: str = ""):
        """Initialize a GetPointer.

        Args:
            target_id (str): The ID of the target object to get.
            path (str): Path to the object. Optional.
            pointer_id (str): ID for the pointer. Optional.
        """
        super().__init__(path, pointer_id)
        self.target_id = target_id

    def solve(
        self,
        lib: ModuleType,
        storage: AbstractStore | None = None,
        reply_callback: Callable | None = None,
    ) -> None | Any:
        """GetPointer abstract method implementation to resolve this
        Object Pointer.

        This method aims to resolve the object pointed by this GetPointer.
        This is how each pointer in our stack knows how to solve themselves.

        In case of GetPointer, we'll try to retrieve the object from the
        storage. If it's not there, we'll try to retrieve the object
        pointed by this GetPointer.

        Args:
            lib (ModuleType): The module the consumer is reflecting.
            storage (AbstractStore, optional): The storage  where we'll
            get/retrieve data. Defaults to None.
            reply_callback (Callable, optional): The callback to reply to
            the broker. Defaults to None.
        Returns:
            None | Any: The object pointed by this Object Pointer.
        """
        if storage and storage.has(self.target_id) and reply_callback:
            reply_callback(self.target_id, storage.get(self.target_id))
        return None


@serializable
class ObjectActionPointer(Pointer):
    """Represents a pointer that is intended to perform an action on the
    object it points to.

    This action can be calling a method, accessing an attribute, or performing
    an operation.
    """

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
        """Initialize an ObjectActionPointer.

        Args:
            target_id (str): The ID of the target object.
            path (str): Path to the object action.
            pointer_id (str): ID for the pointer.
            parents (Tuple): Ancestral pointers leading to this
            action pointer.
            args (tuple): Arguments for the object action.
            kwargs (dict): Keyword arguments for the object action.
            temp_obj (ObjectPointer): Temporary object for storing
            intermediate states.
        """
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
        """ActionPointer abstract method implementation to resolve this
        Object Pointer.

        This method aims to resolve the object pointed by this ActionPointer.
        This is how each pointer in our stack knows how to solve themselves.

        In case of ActionPointer, each ActionPointer represents an action to
        be performed on the object pointed by this ActionPointer. We'll try to
        retrieve the object from the storage. If it's not there, we'll try to
        retrieve the object pointed by this ActionPointer (by target_id).
        If it's not there either, we'll process the object and save it in
        the storage.

        Args:
            lib (ModuleType): The module the consumer is reflecting.
            storage (AbstractStore, optional): The storage  where we'll get or
            retrieve data. Defaults to None.
            reply_callback (Callable, optional): The callback to reply to the
            broker. Defaults to None.
        Returns:
            None | Any: The object pointed by this Object Pointer.
        """
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
