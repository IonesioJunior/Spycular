import pytest

np = pytest.importorskip("numpy")
capnp = pytest.importorskip("capnp")
th = pytest.importorskip("torch")

print("My Capnp: ", capnp)
from pynocchio.serde.capnp.deserialize import _deserialize
from pynocchio.serde.capnp.serialize import _serialize


def test_simple_numpy_array():
    x = th.tensor([1, 2, 3, 4, 5, 6])

    serialized_x = _serialize(x, to_bytes=True)
    assert th.equal(x, _deserialize(serialized_x, from_bytes=True))
