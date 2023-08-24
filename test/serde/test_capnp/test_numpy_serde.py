import pytest

np = pytest.importorskip("numpy")
capnp = pytest.importorskip("capnp")

from spycular.serde.capnp.deserialize import _deserialize  # noqa: E402
from spycular.serde.capnp.serialize import _serialize  # noqa: E402


def test_simple_numpy_array():
    x = np.array([1, 2, 3, 4, 5, 6])

    serialized_x = _serialize(x, to_bytes=True)
    assert np.array_equal(x, _deserialize(serialized_x, from_bytes=True))


def test_uint32_numpy_array():
    x = np.array([1, 2, 3, 4, 5, 6], dtype=np.uint32)

    serialized_x = _serialize(x, to_bytes=True)
    assert np.array_equal(x, _deserialize(serialized_x, from_bytes=True))


def test_uint64_numpy_array():
    x = np.array([1, 2, 3, 4, 5, 6], dtype=np.uint32)

    serialized_x = _serialize(x, to_bytes=True)
    assert np.array_equal(x, _deserialize(serialized_x, from_bytes=True))


def test_float32_numpy_array():
    x = np.array([1, 2, 3, 4, 5, 6], np.float32)

    serialized_x = _serialize(x, to_bytes=True)
    assert np.array_equal(x, _deserialize(serialized_x, from_bytes=True))


def test_float64_numpy_array():
    x = np.array([1, 2, 3, 4, 5, 6], np.float64)

    serialized_x = _serialize(x, to_bytes=True)
    assert np.array_equal(x, _deserialize(serialized_x, from_bytes=True))


def test_bool_numpy_array():
    x = np.array([True, False, True, True], np.bool_)

    serialized_x = _serialize(x, to_bytes=True)
    assert np.array_equal(x, _deserialize(serialized_x, from_bytes=True))
