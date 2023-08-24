from types import ModuleType
from typing import Any, Callable, Dict, Iterable, Tuple

from ..pointer.abstract import Pointer
from ..pointer.callable_pointer import CallablePointer
from ..pointer.object_pointer import ObjectActionPointer
from ..store.abstract import AbstractStore


class Puppet:
    def __init__(self, lib: ModuleType):
        self._original_module = lib

    def execute(
        self,
        pointer: Pointer,
        storage: AbstractStore,
        reply_callback: Callable,
    ) -> None:
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
