import pytest

np = pytest.importorskip("numpy")
capnp = pytest.importorskip("capnp")
th = pytest.importorskip("torch")

from pynocchio.serde.capnp.deserialize import _deserialize  # noqa: E402
from pynocchio.serde.capnp.serialize import _serialize  # noqa: E402


def test_simple_numpy_array():
    x = th.tensor([1, 2, 3, 4, 5, 6])

    serialized_x = _serialize(x, to_bytes=True)
    assert th.equal(x, _deserialize(serialized_x, from_bytes=True))
