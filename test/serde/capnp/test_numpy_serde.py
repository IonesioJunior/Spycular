import numpy as np

from pynocchio.serde.capnp.deserialize import _deserialize
from pynocchio.serde.capnp.numpy import load_numpy_serde
from pynocchio.serde.capnp.primitives import load_primitives_serde
from pynocchio.serde.capnp.serialize import _serialize

load_primitives_serde()
load_numpy_serde()


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
