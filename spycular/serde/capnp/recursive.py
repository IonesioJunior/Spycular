# stdlib
import sys
import types
from enum import Enum, EnumMeta
from typing import Any, Callable, List, Optional, Set, Type, Union

# third party
from capnp.lib.capnp import _DynamicStructBuilder
from pydantic import BaseModel

from .serialize import _serialize

# syft absolute
from .util import get_capnp_schema

TYPE_BANK = {}

recursive_scheme = get_capnp_schema(
    "recursive_serde.capnp",
).RecursiveSerde  # type: ignore


def serializable(cls):
    """Decorator to make a class serializable"""
    exclude = getattr(cls, "__exclude__", [])
    recursive_serde_register(
        cls,
        serialize_attrs=list(cls.__annotations__.keys()),
        exclude_attrs=exclude,
    )
    return cls


def get_fully_qualified_name(obj: object) -> str:
    """Return the full path and name of a class

    Sometimes we want to return the entire path and name encoded
    using periods.

    Args:
        obj: the object we want to get the name of

    Returns:
        the full path and name of the object

    """

    fqn = obj.__class__.__module__

    try:
        fqn += "." + obj.__class__.__name__
    except Exception as e:
        raise Exception(f"Failed to get FQN: {e}")
    return fqn


def get_types(
    cls: Type,
    keys: Optional[List[str]] = None,
) -> Optional[List[Type]]:
    if keys is None:
        return None
    types = []
    for key in keys:
        _type = None
        annotations = getattr(cls, "__annotations__", None)
        if annotations and key in annotations:
            _type = annotations[key]
        else:
            for parent_cls in cls.mro():
                sub_annotations = getattr(parent_cls, "__annotations__", None)
                if sub_annotations and key in sub_annotations:
                    _type = sub_annotations[key]
        if _type is None:
            return None
        types.append(_type)
    return types


def check_fqn_alias(cls: Union[object, type]) -> Optional[tuple]:
    """Currently, typing.Any has different metaclasses in
    different versions of Python 🤦‍♂️.
    For Python <=3.10
    Any is an instance of typing._SpecialForm

    For Python >=3.11
    Any is an instance of typing._AnyMeta
    Hence adding both the aliases to the type bank.

    This would cause issues, when the server and client
    have different python versions.

    As their serde is same, we can use the same serde for both of them.
    with aliases for  fully qualified names in type bank

    In a similar manner for Enum.

    For Python<=3.10:
    Enum is metaclass of enum.EnumMeta

    For Python>=3.11:
    Enum is metaclass of enum.EnumType
    """
    if cls == Any:
        return ("typing._AnyMeta", "typing._SpecialForm")
    if cls == EnumMeta:
        return ("enum.EnumMeta", "enum.EnumType")

    return None


def recursive_serde_register(
    cls: Union[object, type],
    serialize: Optional[Callable] = None,
    deserialize: Optional[Callable] = None,
    serialize_attrs: Optional[List] = None,
    exclude_attrs: Optional[List] = None,
    inherit_attrs: Optional[bool] = True,
    inheritable_attrs: Optional[bool] = True,
) -> None:
    attribute_list: Set[str] = set()

    alias_fqn = check_fqn_alias(cls)
    cls = type(cls) if not isinstance(cls, type) else cls
    fqn = f"{cls.__module__}.{cls.__name__}"

    nonrecursive = bool(serialize and deserialize)
    _serialize = serialize if nonrecursive else rs_object2proto
    _deserialize = deserialize if nonrecursive else rs_proto2object
    hash_exclude_attrs = getattr(cls, "__hash_exclude_attrs__", [])

    if serialize_attrs:
        # If serialize_attrs is provided, append it to our attr list
        attribute_list.update(serialize_attrs)

    if issubclass(cls, Enum):
        attribute_list.update(["value"])

    exclude_attrs = [] if exclude_attrs is None else exclude_attrs
    attribute_list = attribute_list - set(exclude_attrs)

    attributes = list(set(list(attribute_list))) if attribute_list else None
    attribute_types = get_types(cls, attributes)
    serde_overrides = getattr(cls, "__serde_overrides__", {})

    # without fqn duplicate class names overwrite
    serde_attributes = (
        nonrecursive,
        _serialize,
        _deserialize,
        attributes,
        exclude_attrs,
        serde_overrides,
        hash_exclude_attrs,
        cls,
        attribute_types,
    )

    TYPE_BANK[fqn] = serde_attributes

    if isinstance(alias_fqn, tuple):
        for alias in alias_fqn:
            TYPE_BANK[alias] = serde_attributes


def chunk_bytes(
    data: bytes,
    field_name: Union[str, int],
    builder: _DynamicStructBuilder,
) -> None:
    CHUNK_SIZE = int(5.12e8)  # capnp max for a List(Data) field
    list_size = len(data) // CHUNK_SIZE + 1
    data_lst = builder.init(field_name, list_size)
    END_INDEX = CHUNK_SIZE
    for idx in range(list_size):
        START_INDEX = idx * CHUNK_SIZE
        END_INDEX = min(START_INDEX + CHUNK_SIZE, len(data))
        data_lst[idx] = data[START_INDEX:END_INDEX]


def combine_bytes(capnp_list: List[bytes]) -> bytes:
    # TODO: make sure this doesn't copy, perhaps allocate a fixed size buffer
    # and move the bytes into it as we go
    bytes_value = b""
    for value in capnp_list:
        bytes_value += value
    return bytes_value


def rs_object2proto(
    self: Any,
    for_hashing: bool = False,
) -> _DynamicStructBuilder:
    is_type = False
    if isinstance(self, type):
        is_type = True

    msg = recursive_scheme.new_message()
    fqn = get_fully_qualified_name(self)
    if fqn not in TYPE_BANK:
        # third party
        raise Exception(f"{fqn} not in TYPE_BANK")

    msg.fullyQualifiedName = fqn
    (
        nonrecursive,
        serialize,
        deserialize,
        attribute_list,
        exclude_attrs_list,
        serde_overrides,
        hash_exclude_attrs,
        cls,
        attribute_types,
    ) = TYPE_BANK[fqn]

    if nonrecursive or is_type:
        if serialize is None:
            raise Exception(
                f"Cant serialize {type(self)} nonrecursive without serialize.",
            )
        chunk_bytes(serialize(self), "nonrecursiveBlob", msg)
        return msg

    if attribute_list is None:
        attribute_list = self.__dict__.keys()

    hash_exclude_attrs_set = set(hash_exclude_attrs) if for_hashing else set()
    new_attribute_list = (
        set(attribute_list) - set(exclude_attrs_list) - hash_exclude_attrs_set
    )

    msg.init("fieldsName", len(new_attribute_list))
    msg.init("fieldsData", len(new_attribute_list))

    for idx, attr_name in enumerate(sorted(new_attribute_list)):
        if not hasattr(self, attr_name):
            raise ValueError(
                f"{attr_name} on {type(self)} does not exist,\
                serialization aborted!",
            )

        field_obj = getattr(self, attr_name)
        transforms = serde_overrides.get(attr_name, None)

        if transforms is not None:
            field_obj = transforms[0](field_obj)

        if isinstance(field_obj, types.FunctionType):
            continue

        serialized = _serialize(
            field_obj,
            to_bytes=True,
            for_hashing=for_hashing,
        )
        msg.fieldsName[idx] = attr_name
        chunk_bytes(serialized, idx, msg.fieldsData)

    return msg


def rs_bytes2object(blob: bytes) -> Any:
    MAX_TRAVERSAL_LIMIT = 2**64 - 1

    with recursive_scheme.from_bytes(  # type: ignore
        blob,
        traversal_limit_in_words=MAX_TRAVERSAL_LIMIT,
    ) as msg:
        return rs_proto2object(msg)


def rs_proto2object(proto: _DynamicStructBuilder) -> Any:
    # relative
    from .deserialize import _deserialize

    # clean this mess, Tudor
    module_parts = proto.fullyQualifiedName.split(".")
    klass = module_parts.pop()
    class_type: Type = type(None)

    if klass != "NoneType":
        try:
            class_type = getattr(
                sys.modules[".".join(module_parts)],
                klass,
            )
        except Exception:  # nosec
            try:
                class_type = getattr(
                    sys.modules[".".join(module_parts)],
                    klass,
                )
            except Exception:  # nosec
                pass

    if proto.fullyQualifiedName not in TYPE_BANK:
        raise Exception(f"{proto.fullyQualifiedName} not in TYPE_BANK")

    (
        nonrecursive,
        serialize,
        deserialize,
        attribute_list,
        exclude_attrs_list,
        serde_overrides,
        hash_exclude_attrs,
        cls,
        attribute_types,
    ) = TYPE_BANK[proto.fullyQualifiedName]

    if class_type == type(None):  # noqa: E721
        # yes this looks stupid but it works and the opposite breaks
        class_type = cls

    if nonrecursive:
        if deserialize is None:
            raise Exception(
                f"Cant serialize {type(proto)} \
            nonrecursive without serialize.",
            )

        return deserialize(combine_bytes(proto.nonrecursiveBlob))

    kwargs = {}

    for attr_name, attr_bytes_list in zip(proto.fieldsName, proto.fieldsData):
        if attr_name != "":
            attr_bytes = combine_bytes(attr_bytes_list)
            attr_value = _deserialize(attr_bytes, from_bytes=True)
            transforms = serde_overrides.get(attr_name, None)

            if transforms is not None:
                attr_value = transforms[1](attr_value)
            kwargs[attr_name] = attr_value

    if hasattr(class_type, "serde_constructor"):
        return class_type.serde_constructor(kwargs)

    obj: BaseModel | None | object = None
    if issubclass(class_type, Enum) and "value" in kwargs:
        obj = class_type.__new__(class_type, kwargs["value"])  # type: ignore
    elif issubclass(class_type, BaseModel):
        # if we skip the __new__ flow of BaseModel we get the error
        # AttributeError: object has no attribute '__fields_set__'
        obj = class_type(**kwargs)
    else:
        obj = class_type.__new__(class_type)  # type: ignore
        for attr_name, attr_value in kwargs.items():
            vars(obj)[attr_name] = attr_value

    return obj


# how else do you import a relative file to execute it?
NOTHING = None
