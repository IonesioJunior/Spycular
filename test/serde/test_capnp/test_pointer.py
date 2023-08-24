import pytest

capnp = pytest.importorskip("capnp")

from spycular.pointer.callable_pointer import BuiltinPointer  # noqa: E402
from spycular.pointer.callable_pointer import FunctionPointer  # noqa: E402
from spycular.pointer.callable_pointer import MethodPointer  # noqa: E402
from spycular.pointer.object_pointer import GetPointer  # noqa: E402
from spycular.pointer.object_pointer import ObjectActionPointer  # noqa: E402
from spycular.pointer.object_pointer import ObjectPointer  # noqa: E402
from spycular.serde.capnp.deserialize import _deserialize  # noqa: E402
from spycular.serde.capnp.serialize import _serialize  # noqa: E402
from spycular.utils.uuid_gen import generate_uuid  # noqa: E402


def test_function_pointer():
    func_ptr = FunctionPointer(
        path="numpy.array",
        args=[[1, 2, 3]],
        kwargs={1: "test", "2": [1, 2, 3, 4]},
    )
    serialized_ptr = _serialize(func_ptr, to_bytes=True)
    deserialized_ptr = _deserialize(serialized_ptr, from_bytes=True)
    assert func_ptr.id == deserialized_ptr.id
    assert func_ptr.path == deserialized_ptr.path
    assert func_ptr.args == deserialized_ptr.args
    assert func_ptr.kwargs == deserialized_ptr.kwargs


def test_method_pointer():
    func_ptr = MethodPointer(
        path="numpy.array",
        args=[[1, 2, 3]],
        kwargs={1: "test", "2": [1, 2, 3, 4]},
    )
    serialized_ptr = _serialize(func_ptr, to_bytes=True)
    deserialized_ptr = _deserialize(serialized_ptr, from_bytes=True)
    assert func_ptr.id == deserialized_ptr.id
    assert func_ptr.path == deserialized_ptr.path
    assert func_ptr.args == deserialized_ptr.args
    assert func_ptr.kwargs == deserialized_ptr.kwargs


def test_builtin_pointer():
    func_ptr = BuiltinPointer(
        path="numpy.array",
        args=[[1, 2, 3]],
        kwargs={1: "test", "2": [1, 2, 3, 4]},
    )
    serialized_ptr = _serialize(func_ptr, to_bytes=True)
    deserialized_ptr = _deserialize(serialized_ptr, from_bytes=True)
    assert func_ptr.id == deserialized_ptr.id
    assert func_ptr.path == deserialized_ptr.path
    assert func_ptr.args == deserialized_ptr.args
    assert func_ptr.kwargs == deserialized_ptr.kwargs


def test_get_pointer():
    get_ptr = GetPointer(path="numpy.array", target_id=generate_uuid())
    serialized_ptr = _serialize(get_ptr, to_bytes=True)
    deserialized_ptr = _deserialize(serialized_ptr, from_bytes=True)
    assert get_ptr.id == deserialized_ptr.id
    assert get_ptr.target_id == deserialized_ptr.target_id


def test_action_pointer():
    action_ptr = ObjectActionPointer(
        path="numpy.array",
        target_id=generate_uuid(),
        args=([1, 2, 3],),
        kwargs={1: "test", "2": [1, 2, 3, 4]},
    )
    serialized_ptr = _serialize(action_ptr, to_bytes=True)
    deserialized_ptr = _deserialize(serialized_ptr, from_bytes=True)
    assert action_ptr.id == deserialized_ptr.id
    assert action_ptr.target_id == deserialized_ptr.target_id
    assert action_ptr.args == deserialized_ptr.args
    assert action_ptr.kwargs == deserialized_ptr.kwargs
    assert action_ptr.temp_obj == deserialized_ptr.temp_obj


def test_object_pointer():
    action_ptr = ObjectPointer(path="numpy.array", target_id=generate_uuid())
    serialized_ptr = _serialize(action_ptr, to_bytes=True)
    deserialized_ptr = _deserialize(serialized_ptr, from_bytes=True)
    assert action_ptr.id == deserialized_ptr.id
    assert action_ptr.target_id == deserialized_ptr.target_id
    assert action_ptr.args == deserialized_ptr.args
    assert action_ptr.kwargs == deserialized_ptr.kwargs


def test_object_pointer_with_producer(producer):
    action_ptr = ObjectPointer(
        path="numpy.array",
        target_id=generate_uuid(),
        broker=producer,
    )
    serialized_ptr = _serialize(action_ptr, to_bytes=True)
    deserialized_ptr = _deserialize(serialized_ptr, from_bytes=True)
    assert action_ptr.id == deserialized_ptr.id
    assert action_ptr.target_id == deserialized_ptr.target_id
    assert action_ptr.args == deserialized_ptr.args
    assert action_ptr.kwargs == deserialized_ptr.kwargs
