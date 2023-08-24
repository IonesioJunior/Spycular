import torch as th

from ..recursive import recursive_serde_register

# relative
from .serde import tensor_deserialize, tensor_serialize


def load_torch_serde():
    recursive_serde_register(
        th.Tensor,
        serialize=tensor_serialize,
        deserialize=tensor_deserialize,
    )
