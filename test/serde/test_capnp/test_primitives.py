import pytest

np = pytest.importorskip("numpy")
capnp = pytest.importorskip("capnp")

from pynocchio.serde.capnp.deserialize import _deserialize  # noqa: E402
from pynocchio.serde.capnp.serialize import _serialize  # noqa: E402


def test_int():
    x = 10
    serialized_x = _serialize(x, to_bytes=True)
    assert x == _deserialize(serialized_x, from_bytes=True)


def float():
    x = 10.5
    serialized_x = _serialize(x, to_bytes=True)
    assert x == _deserialize(serialized_x, from_bytes=True)


def test_bool():
    x = True
    serialized_x = _serialize(x, to_bytes=True)
    y = False
    serialized_y = _serialize(y, to_bytes=True)

    assert x == _deserialize(serialized_x, from_bytes=True)
    assert y == _deserialize(serialized_y, from_bytes=True)


def test_tuple():
    x = (2, 1)
    serialized_x = _serialize(x, to_bytes=True)
    y = (2,)
    serialized_y = _serialize(y, to_bytes=True)

    assert x == _deserialize(serialized_x, from_bytes=True)
    assert y == _deserialize(serialized_y, from_bytes=True)


def test_int_list():
    x = [1, 2, 3]
    serialized_x = _serialize(x, to_bytes=True)
    y = []
    serialized_y = _serialize(y, to_bytes=True)

    assert x == _deserialize(serialized_x, from_bytes=True)
    assert y == _deserialize(serialized_y, from_bytes=True)


def test_diff_types_list():
    x = [False, 2, "Hello"]
    serialized_x = _serialize(x, to_bytes=True)

    assert x == _deserialize(serialized_x, from_bytes=True)


def test_lists_of_lists():
    x = [[1, 2, 3], [4, 5, 6]]
    serialized_x = _serialize(x, to_bytes=True)

    assert x == _deserialize(serialized_x, from_bytes=True)


def test_dict():
    x = {"a": 1, "b": 2}
    serialized_x = _serialize(x, to_bytes=True)

    assert x == _deserialize(serialized_x, from_bytes=True)


def test_diff_keys_dict():
    x = {True: 1, "b": True, 2: False, 3.5: "test"}
    serialized_x = _serialize(x, to_bytes=True)

    assert x == _deserialize(serialized_x, from_bytes=True)
