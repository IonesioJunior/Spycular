# stdlib
import sys
from collections import defaultdict
from enum import Enum
from pathlib import PurePath
from typing import GenericAlias  # type: ignore
from typing import (
    Any,
    Collection,
    Dict,
    List,
    Mapping,
    Optional,
    Type,
    TypeVar,
    cast,
)

from ..recursive import chunk_bytes, combine_bytes
from ..util import get_capnp_schema

iterable_schema = get_capnp_schema("iterable.capnp").Iterable  # type: ignore
kv_iterable_schema = get_capnp_schema(
    "kv_iterable.capnp",
).KVIterable  # type: ignore


def serialize_iterable(iterable: Collection) -> bytes:
    # relative
    from ..serialize import _serialize

    message = iterable_schema.new_message()

    message.init("values", len(iterable))

    for idx, it in enumerate(iterable):
        serialized = _serialize(it, to_bytes=True)
        chunk_bytes(serialized, idx, message.values)

    return message.to_bytes()


def deserialize_iterable(iterable_type: type, blob: bytes) -> Collection:
    # relative
    from ..deserialize import _deserialize

    MAX_TRAVERSAL_LIMIT = 2**64 - 1
    values = []

    with iterable_schema.from_bytes(  # type: ignore
        blob,
        traversal_limit_in_words=MAX_TRAVERSAL_LIMIT,
    ) as msg:
        for element in msg.values:
            values.append(
                _deserialize(combine_bytes(element), from_bytes=True),
            )

    return iterable_type(values)


def serialize_kv(map: Mapping) -> bytes:
    # relative
    from ..serialize import _serialize

    message = kv_iterable_schema.new_message()

    message.init("keys", len(map))
    message.init("values", len(map))

    for index, (k, v) in enumerate(map.items()):
        message.keys[index] = _serialize(k, to_bytes=True)
        serialized = _serialize(v, to_bytes=True)
        chunk_bytes(serialized, index, message.values)

    return message.to_bytes()


def get_deserialized_kv_pairs(blob: bytes) -> List[Any]:
    # relative
    from ..deserialize import _deserialize

    MAX_TRAVERSAL_LIMIT = 2**64 - 1
    pairs = []

    with kv_iterable_schema.from_bytes(  # type: ignore
        blob,
        traversal_limit_in_words=MAX_TRAVERSAL_LIMIT,
    ) as msg:
        for key, value in zip(msg.keys, msg.values):
            pairs.append(
                (
                    _deserialize(key, from_bytes=True),
                    _deserialize(combine_bytes(value), from_bytes=True),
                ),
            )
    return pairs


def deserialize_kv(mapping_type: type, blob: bytes) -> Mapping:
    pairs = get_deserialized_kv_pairs(blob=blob)
    return mapping_type(pairs)


def serialize_defaultdict(df_dict: defaultdict) -> bytes:
    # relative
    from ..serialize import _serialize

    df_type_bytes = _serialize(df_dict.default_factory, to_bytes=True)
    df_kv_bytes = serialize_kv(df_dict)
    return _serialize((df_type_bytes, df_kv_bytes), to_bytes=True)


def deserialize_defaultdict(blob: bytes) -> Mapping:
    # relative
    from ..deserialize import _deserialize

    df_tuple = _deserialize(blob, from_bytes=True)
    df_type_bytes, df_kv_bytes = df_tuple[0], df_tuple[1]
    df_type = _deserialize(df_type_bytes, from_bytes=True)
    mapping: Dict = defaultdict(df_type)

    pairs = get_deserialized_kv_pairs(blob=df_kv_bytes)
    mapping.update(pairs)

    return mapping


def serialize_enum(enum: Enum) -> bytes:
    # relative
    from ..serialize import _serialize

    return cast(bytes, _serialize(enum.value, to_bytes=True))


def deserialize_enum(enum_type: type, enum_buf: bytes) -> Enum:
    # relative
    from ..deserialize import _deserialize

    enum_value = _deserialize(enum_buf, from_bytes=True)
    return enum_type(enum_value)


def serialize_type(serialized_type: type) -> bytes:
    # relative
    from ..util.util import full_name_with_qualname

    fqn = full_name_with_qualname(klass=serialized_type)
    module_parts = fqn.split(".")
    return ".".join(module_parts).encode()


def deserialize_type(type_blob: bytes) -> type:
    deserialized_type = type_blob.decode()
    module_parts = deserialized_type.split(".")
    klass = module_parts.pop()
    klass = "None" if klass == "NoneType" else klass
    exception_type = getattr(sys.modules[".".join(module_parts)], klass)
    return exception_type


TPath = TypeVar("TPath", bound=PurePath)


def serialize_path(path: PurePath) -> bytes:
    # relative
    from ..serialize import _serialize

    return cast(bytes, _serialize(str(path), to_bytes=True))


def deserialize_path(path_type: Type[TPath], buf: bytes) -> TPath:
    # relative
    from ..deserialize import _deserialize

    path: str = _deserialize(buf, from_bytes=True)
    return path_type(path)


def serialize_generic_alias(serialized_type: GenericAlias) -> bytes:
    # relative
    from ..serialize import _serialize
    from ..util.util import full_name_with_name

    fqn = full_name_with_name(klass=serialized_type)
    module_parts = fqn.split(".")

    obj_dict = {
        "path": ".".join(module_parts),
        "__origin__": serialized_type.__origin__,
        "__args__": serialized_type.__args__,
    }
    if hasattr(serialized_type, "_paramspec_tvars"):
        obj_dict["_paramspec_tvars"] = serialized_type._paramspec_tvars
    return _serialize(obj_dict, to_bytes=True)


def deserialize_generic_alias(type_blob: bytes) -> type:
    # relative
    from ..deserialize import _deserialize

    obj_dict = _deserialize(type_blob, from_bytes=True)
    deserialized_type = obj_dict.pop("path")
    module_parts = deserialized_type.split(".")
    klass = module_parts.pop()
    type_constructor = getattr(sys.modules[".".join(module_parts)], klass)
    # does this apply to all _SpecialForm?

    # Note: Some typing constructors are callable while
    # some use custom __getitem__ implementations
    # to initialize the type 😭

    try:
        return type_constructor(**obj_dict)
    except TypeError:
        _args = obj_dict["__args__"]
        # Again not very consistent 😭
        if type_constructor == Optional:
            _args = _args[0]
        return type_constructor[_args]
    except Exception as e:
        raise e
