"""This folder contains message format for captian proto serialization.

    Note: Each capnp message format should have unique hex identifier
    (ex: @0xcd0709e35fffa8d8)
    These can be generated in terminal by the command `capnp id` after pycapnp installation.
"""
from .primitives import load_primitives_serde

load_primitives_serde()

try:
    import numpy
    import pyarrow

    from .numpy import load_numpy_serde

    load_numpy_serde()
except ImportError:
    # Handle the case where `some_package` or `mysubmodule` is not available
    pass


try:
    import numpy
    import pyarrow
    import torch

    from .torch import load_torch_serde

    load_torch_serde()
except ImportError:
    # Handle the case where `some_package` or `mysubmodule` is not available
    pass
