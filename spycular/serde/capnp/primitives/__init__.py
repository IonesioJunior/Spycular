import functools
import pathlib
import weakref
from collections import OrderedDict, defaultdict
from enum import EnumMeta
from types import MappingProxyType
from typing import GenericAlias  # type: ignore
from typing import Any, List, Optional, TypeVar, Union, _SpecialForm

from ..recursive import recursive_serde_register
from .serde import (
    deserialize_defaultdict,
    deserialize_generic_alias,
    deserialize_iterable,
    deserialize_kv,
    deserialize_path,
    deserialize_type,
    serialize_defaultdict,
    serialize_generic_alias,
    serialize_iterable,
    serialize_kv,
    serialize_path,
    serialize_type,
)


def load_primitives_serde():
    # bit_length + 1 for signed
    recursive_serde_register(
        int,
        serialize=lambda x: x.to_bytes(
            (x.bit_length() + 7) // 8 + 1,
            "big",
            signed=True,
        ),
        deserialize=lambda x_bytes: int.from_bytes(
            x_bytes,
            "big",
            signed=True,
        ),
    )

    recursive_serde_register(
        float,
        serialize=lambda x: x.hex().encode(),
        deserialize=lambda x: float.fromhex(x.decode()),
    )

    recursive_serde_register(
        bytes,
        serialize=lambda x: x,
        deserialize=lambda x: x,
    )

    recursive_serde_register(
        str,
        serialize=lambda x: x.encode(),
        deserialize=lambda x: x.decode(),
    )

    recursive_serde_register(
        list,
        serialize=serialize_iterable,
        deserialize=functools.partial(deserialize_iterable, list),
    )

    recursive_serde_register(
        tuple,
        serialize=serialize_iterable,
        deserialize=functools.partial(deserialize_iterable, tuple),
    )

    recursive_serde_register(
        dict,
        serialize=serialize_kv,
        deserialize=functools.partial(deserialize_kv, dict),
    )

    recursive_serde_register(
        defaultdict,
        serialize=serialize_defaultdict,
        deserialize=deserialize_defaultdict,
    )

    recursive_serde_register(
        OrderedDict,
        serialize=serialize_kv,
        deserialize=functools.partial(deserialize_kv, OrderedDict),
    )

    recursive_serde_register(
        type(None),
        serialize=lambda _: b"1",
        deserialize=lambda _: None,
    )

    recursive_serde_register(
        bool,
        serialize=lambda x: b"1" if x else b"0",
        deserialize=lambda x: False if x == b"0" else True,
    )

    recursive_serde_register(
        set,
        serialize=serialize_iterable,
        deserialize=functools.partial(deserialize_iterable, set),
    )

    recursive_serde_register(
        weakref.WeakSet,
        serialize=serialize_iterable,
        deserialize=functools.partial(deserialize_iterable, weakref.WeakSet),
    )

    recursive_serde_register(
        frozenset,
        serialize=serialize_iterable,
        deserialize=functools.partial(deserialize_iterable, frozenset),
    )

    recursive_serde_register(
        complex,
        serialize=lambda x: serialize_iterable((x.real, x.imag)),
        deserialize=lambda x: complex(*deserialize_iterable(tuple, x)),
    )

    recursive_serde_register(
        range,
        serialize=lambda x: serialize_iterable((x.start, x.stop, x.step)),
        deserialize=lambda x: range(*deserialize_iterable(tuple, x)),
    )

    recursive_serde_register(
        slice,
        serialize=lambda x: serialize_iterable((x.start, x.stop, x.step)),
        deserialize=lambda x: slice(*deserialize_iterable(tuple, x)),
    )

    recursive_serde_register(
        slice,
        serialize=lambda x: serialize_iterable((x.start, x.stop, x.step)),
        deserialize=lambda x: slice(*deserialize_iterable(tuple, x)),
    )

    recursive_serde_register(
        type,
        serialize=serialize_type,
        deserialize=deserialize_type,
    )
    recursive_serde_register(
        MappingProxyType,
        serialize=serialize_kv,
        deserialize=functools.partial(deserialize_kv, MappingProxyType),
    )

    for __path_type in (
        pathlib.PurePath,
        pathlib.PurePosixPath,
        pathlib.PureWindowsPath,
        pathlib.Path,
        pathlib.PosixPath,
        pathlib.WindowsPath,
    ):
        recursive_serde_register(
            __path_type,
            serialize=serialize_path,
            deserialize=functools.partial(deserialize_path, __path_type),
        )

    def recursive_serde_register_type(
        t: type,
        serialize_attrs: Optional[List] = None,
    ) -> None:
        if (isinstance(t, type) and issubclass(t, GenericAlias)) or issubclass(
            type(t),
            GenericAlias,
        ):
            recursive_serde_register(
                t,
                serialize=serialize_generic_alias,
                deserialize=deserialize_generic_alias,
                serialize_attrs=serialize_attrs,
            )
        else:
            recursive_serde_register(
                t,
                serialize=serialize_type,
                deserialize=deserialize_type,
                serialize_attrs=serialize_attrs,
            )

    recursive_serde_register_type(_SpecialForm)
    recursive_serde_register_type(GenericAlias)
    recursive_serde_register_type(Union)
    recursive_serde_register_type(TypeVar)

    recursive_serde_register_type(Any)
    recursive_serde_register_type(EnumMeta)
