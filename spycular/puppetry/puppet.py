from types import ModuleType
from typing import Any, Callable, Dict, Iterable, Tuple

from ..pointer.abstract import Pointer
from ..pointer.callable_pointer import CallablePointer
from ..pointer.object_pointer import ObjectActionPointer
from ..store.abstract import AbstractStore


class Puppet:
    """Puppet manages and executes pointers relative to an external
    library or module.

    The Puppet class is responsible for taking pointers which might represent
    actions or callable tasks and ensuring they are executed in the context of
    a given library/module. It can also handle nested pointers, iterating
    through them recursively and resolving their arguments.

    Attributes:
        _original_module (ModuleType): The external library or module in which
        pointers are to be executed.

    Methods:
        execute: Executes the given pointer within original module context.
        _resolve_pointer_args: Resolves and returns the arguments and
        keyword arguments of a pointer.
    """

    def __init__(self, lib: ModuleType):
        """Initialize the Puppet with an external library or module.

        Args:
            lib (ModuleType): The original library or module.
        """
        self._original_module = lib

    def execute(
        self,
        pointer: Pointer,
        storage: AbstractStore,
        reply_callback: Callable,
    ) -> None:
        """Executes the given pointer within the context of the original
        module.

        If the pointer is of type ObjectActionPointer or CallablePointer,
        its arguments are first resolved.

        Args:
            pointer (Pointer): The pointer to be executed.
            storage (AbstractStore): The storage mechanism to use while
            executing the pointer.
            reply_callback (Callable): Callback function to handle the
            results or replies from pointer execution.
        """
        if isinstance(pointer, ObjectActionPointer) or isinstance(
            pointer,
            CallablePointer,
        ):
            pointer.args, pointer.kwargs = self._resolve_pointer_args(
                pointer,
                storage,
                reply_callback,
            )
        pointer.solve(
            lib=self._original_module,
            storage=storage,
            reply_callback=reply_callback,
        )

    def _resolve_pointer_args(
        self,
        pointer: Pointer,
        storage: AbstractStore,
        reply_callback: Callable,
    ) -> Tuple[Tuple[Any, ...], Dict[str, Any]]:
        """Resolves and returns the arguments and keyword arguments of a
        pointer.

        For pointers that have other pointers as arguments, this method will
        recursively resolve them.

        Args:
            pointer (Pointer): Pointer whose arguments need to be resolved.
            storage (AbstractStore): The storage mechanism used store results.
            reply_callback (Callable): Callback function to handle the results
            or replies from pointer resolution.

        Returns:
            Tuple[Tuple[Any, ...], Dict[str, Any]]: A tuple containing the
            resolved positional and keyword arguments.
        """
        args = []
        for arg in getattr(pointer, "args", []):
            if isinstance(arg, Pointer):
                # Solve and add pointer args to args
                args.append(
                    arg.solve(
                        self._original_module,
                        storage=storage,
                        reply_callback=reply_callback,
                    ),
                )
            elif isinstance(arg, Iterable):
                new_args = []
                for argument in arg:
                    if isinstance(argument, Pointer):  # if arg is a pointer
                        local_args, local_kwargs = self._resolve_pointer_args(
                            argument,
                            storage,
                            reply_callback,
                        )
                        if isinstance(
                            argument,
                            ObjectActionPointer,
                        ) or isinstance(argument, CallablePointer):
                            argument.args = local_args
                            argument.kwargs = local_kwargs

                        new_arg = argument.solve(
                            self._original_module,
                            storage=storage,
                            reply_callback=reply_callback,
                        )
                        new_args.append(new_arg)
                    else:  # if arg isn't a pointer
                        new_args.append(argument)
                # Add iterable args to args
                args.append(tuple(new_args))
            else:
                # Add std args to args
                args.append(arg)

        args_tuple = tuple(args)

        kwargs = {}
        for key, val in getattr(pointer, "kwargs", {}).items():
            if isinstance(val, Pointer):
                kwargs[key] = val.solve(
                    self._original_module,
                    storage=storage,
                    reply_callback=reply_callback,
                )
            else:
                kwargs[key] = val
        return args_tuple, kwargs
