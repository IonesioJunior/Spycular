from __future__ import annotations

import inspect
from types import ModuleType
from typing import Any, Callable, List, Set, Type

from ..pointer.callable_pointer import (
    BuiltinPointer,
    FunctionPointer,
    MethodPointer,
)
from ..pointer.class_pointer import ClassPointer
from ..pointer.object_pointer import ObjectPointer
from ..producer.abstract import AbstractProducer


class IncidentModule:
    """IncidentModule dynamically mirrors the structure of a given
    module or class.

    It creates placeholders (or 'reflections') for the members of the module
    or class, allowing for dynamic interaction and control over the
    mirrored module or class.

    Attributes:
        callable_members (Set[Callable]): A set of all callable members.
        variable_members (List[Any]): A list of non-callable members.
        class_members (Set[Type[Any]]): A set of class-type members.
        remains (List[Any]): Members that don't fit into the previous sets.
        path (str): The current path or namespace of the module instance.
        modules (Set[ModuleType]): Modules that have been processed or are
        being processed.
        broker (AbstractProducer): An instance responsible for producing
        module tasks/events.

    Methods:
        _mirror_class: Mirrors the structure of the provided module.
        placeholder_class: Creates a placeholder for a class-type member.
        inject_callable_member: Generates a placeholder function or method.
        placeholder_module: Creates a incident instance for another module.
        placeholder_variable: Creates a placeholder for a variable member.
    """

    def __init__(
        self,
        lib,
        broker,
        modules=set(),
        parent_path: str = "",
    ):
        """Initializes the IncidentModule instance.

        Args:
            lib: The target library or module to mirror.
            broker: An instance responsible for producing module tasks/events.
            modules (set, optional): Previously processed modules.
            parent_path (str, optional): The parent namespace or path for
            the current IncidentModule instance. Defaults to an empty string.
        """
        self.callable_members: Set[Callable] = set()
        self.variable_members: List[Any] = list()
        self.class_members: Set[Type[Any]] = set()
        self.remains: List[Any] = list()
        self.path: str = parent_path
        self.modules: Set[ModuleType] = modules
        self.broker: AbstractProducer = broker
        self._mirror_class(lib, parent_path)

    def _mirror_class(self, lib, parent_path: str = ""):
        """Reflects or mirrors the structure of the provided library or
        module.

        Iterates over the members of the library/module and creates
        placeholders for each member based on its type (function, method,
        class, module, variable, etc.)

        Args:
            lib: The target library or module to mirror.
            parent_path (str): The namespace or path for the current
            mirroring process.
        """
        self.modules.add(lib)
        # Iterates over the target module members
        try:
            for name, member in inspect.getmembers(lib):
                current_path = f"{parent_path}.{name}" if parent_path else name
                # If member is a function or method or is builtin
                if (
                    inspect.isfunction(member)
                    or inspect.ismethod(member)
                    or inspect.isbuiltin(member)
                ):
                    # self.callable_members.add((name, member))
                    vars(self)[name] = IncidentModule.inject_callable_member(
                        member,
                        current_path,
                        self.broker,
                    )
                # If member is a class and not already in class members
                elif (
                    inspect.isclass(member)
                    and member not in self.class_members
                ):
                    # self.class_members.add((name, member))
                    vars(self)[name] = IncidentModule.placeholder_class(
                        member,
                        current_path,
                        self.broker,
                        self.class_members,
                    )
                # Member is module or starts with __ (to avoid python vars)
                elif not name.startswith("__") and not inspect.ismodule(
                    member,
                ):
                    if callable(member):
                        vars(self)[
                            name
                        ] = IncidentModule.inject_callable_member(
                            member,
                            current_path,
                            self.broker,
                        )
                    else:
                        self.variable_members.append((name, member))
                        vars(self)[name] = IncidentModule.placeholder_variable(
                            current_path,
                            self.broker,
                        )
                # If the member is another module
                elif inspect.ismodule(member) and member not in self.modules:
                    # self.modules.add((name, member))
                    vars(self)[name] = IncidentModule.placeholder_module(
                        member,
                        current_path,
                        self.modules,
                        self.broker,
                    )
                # If isn't anything above
                else:
                    self.remains.append((name, member))
        except TypeError:
            pass

    @staticmethod
    def placeholder_class(
        cls,
        parent_path,
        broker,
        processed_classes,
    ) -> ClassPointer:
        return ClassPointer(path=parent_path, broker=broker)

    @staticmethod
    def inject_callable_member(member, path, broker) -> Callable:
        """Generates and returns a placeholder function or method for a
        given callable member.

        Depending on the type of the provided member (function, method,
        or builtin), the method creates a corresponding placeholder to mimic
        its behavior. When the placeholder is called, it interacts with the
        provided broker and follows a specified path.

        Args:
            member: Original callable member (function, method, or builtin)
            for which the placeholder is to be created.
            path (str): Specific mirrored module path/namespace.
            broker: An instance responsible for producing module tasks/events.

        Returns:
            Callable: A placeholder function/method mimicking the original.

        Raises:
            None: This method does not explicitly raise any exceptions.
        """
        result_function = None
        if inspect.isfunction(member):

            def placeholder_function(*args, **kwargs):
                function_pointer = FunctionPointer(
                    path=path,
                    args=args,
                    kwargs=kwargs,
                )
                broker.send(function_pointer)
                return ObjectPointer(
                    pointer_id=function_pointer.id,
                    parents=[function_pointer],
                    broker=broker,
                )

            result_function = placeholder_function
        elif inspect.ismethod(member):

            def placeholder_method(*args, **kwargs):
                method_pointer = MethodPointer(
                    path=path,
                    args=args,
                    kwargs=kwargs,
                )
                broker.send(method_pointer)
                return ObjectPointer(
                    pointer_id=method_pointer.id,
                    parents=[method_pointer],
                    broker=broker,
                )

            result_function = placeholder_method
        else:

            def placeholder_builtin(*args, **kwargs):
                builtin_pointer = BuiltinPointer(
                    path=path,
                    args=args,
                    kwargs=kwargs,
                )
                broker.send(builtin_pointer)
                return ObjectPointer(
                    pointer_id=builtin_pointer.id,
                    parents=[builtin_pointer],
                    broker=broker,
                )

            result_function = placeholder_builtin

        return result_function

    @staticmethod
    def placeholder_module(member, path, modules, broker) -> IncidentModule:
        """Create and return a IncidentModule instance for a given
        module member.

        This method mirrors the structure and behavior of a module within
        the IncidentModule context, essentially acting as a placeholder for
        that module.

        Args:
            member: Module for which the IncidentModule is to be created.
            path (str): Specific mirrored module path/namespace.
            modules (Set[ModuleType]): Modules already processed.
            broker: An instance responsible for producing module tasks/events.

        Returns:
            IncidentModule: A new IncidentModule representing the given module.
        """
        return IncidentModule(
            lib=member,
            modules=modules,
            parent_path=path,
            broker=broker,
        )

    @staticmethod
    def placeholder_variable(path, broker) -> ObjectPointer:
        """Create and return an ObjectPointer as a placeholder for a
        variable.

        This method produces a proxy representation of a variable in the
        IncidentModule context.The generated ObjectPointer acts as a stand-in
        for the original variable, facilitating its interactions and
        management within the IncidentModule system.

        Args:
            path (str): Specific mirrored module path/namespace.
            broker: An instance responsible for producing module tasks/events.

        Returns:
            ObjectPointer: A new pointer representing the given variable.
        """
        return ObjectPointer(path=path, broker=broker)
