import torch as th

from pynocchio.serde.capnp.deserialize import _deserialize
from pynocchio.serde.capnp.primitives import load_primitives_serde
from pynocchio.serde.capnp.serialize import _serialize
from pynocchio.serde.capnp.torch import load_torch_serde

load_primitives_serde()
load_torch_serde()


def test_simple_numpy_array():
    x = th.tensor([1, 2, 3, 4, 5, 6])

    serialized_x = _serialize(x, to_bytes=True)
    assert th.equal(x, _deserialize(serialized_x, from_bytes=True))
