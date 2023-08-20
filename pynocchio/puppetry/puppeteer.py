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


class Puppeteer:
    def __init__(
        self,
        lib,
        broker,
        modules=set(),
        parent_path: str = "",
    ):
        self.callable_members: Set[Callable] = set()
        self.variable_members: List[Any] = list()
        self.class_members: Set[Type[Any]] = set()
        self.remains: List[Any] = list()
        self.path: str = parent_path
        self.modules: Set[ModuleType] = modules
        self.broker: AbstractProducer = broker
        self._mirror_class(lib, parent_path)

    def _mirror_class(self, lib, parent_path: str = ""):
        """'This method creates a placeholder for module's member."""
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
                    vars(self)[name] = Puppeteer.inject_callable_member(
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
                    vars(self)[name] = Puppeteer.placeholder_class(
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
                        vars(self)[name] = Puppeteer.inject_callable_member(
                            member,
                            current_path,
                            self.broker,
                        )
                    else:
                        self.variable_members.append((name, member))
                        vars(self)[name] = Puppeteer.placeholder_variable(
                            current_path,
                            self.broker,
                        )
                # If the member is another module
                elif inspect.ismodule(member) and member not in self.modules:
                    # self.modules.add((name, member))
                    vars(self)[name] = Puppeteer.placeholder_module(
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
    def placeholder_module(member, path, modules, broker) -> Puppeteer:
        return Puppeteer(
            lib=member,
            modules=modules,
            parent_path=path,
            broker=broker,
        )

    @staticmethod
    def placeholder_variable(path, broker) -> ObjectPointer:
        return ObjectPointer(path=path, broker=broker)
