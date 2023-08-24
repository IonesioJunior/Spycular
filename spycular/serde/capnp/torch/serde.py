from typing import cast

import numpy as np
import pyarrow as pa
import torch as th

from ..deserialize import _deserialize
from ..serialize import _serialize


def tensor_serialize(obj: th.Tensor) -> bytes:
    return arrow_serialize(obj)


def tensor_deserialize(buf: bytes) -> th.Tensor:
    deser = _deserialize(buf, from_bytes=True)
    if isinstance(deser, tuple):
        return arrow_deserialize(*deser)
    else:
        raise ValueError(
            f"Invalid type:{type(deser)} for numpy deserialization",
        )


def arrow_serialize(tensor: th.Tensor) -> bytes:
    obj = th.Tensor.numpy(tensor)
    original_dtype = obj.dtype
    apache_arrow = pa.Tensor.from_numpy(obj=obj)
    sink = pa.BufferOutputStream()
    pa.ipc.write_tensor(apache_arrow, sink)
    buffer = sink.getvalue()
    numpy_bytes = pa.compress(buffer, asbytes=True, codec="snappy")
    dtype = original_dtype.name
    return cast(
        bytes,
        _serialize((numpy_bytes, buffer.size, dtype), to_bytes=True),
    )


def arrow_deserialize(
    numpy_bytes: bytes,
    decompressed_size: int,
    dtype: str,
) -> th.Tensor:
    original_dtype = np.dtype(dtype)
    numpy_bytes = pa.decompress(
        numpy_bytes,
        decompressed_size=decompressed_size,
        codec="snappy",
    )

    result = pa.ipc.read_tensor(numpy_bytes)
    np_array = result.to_numpy()
    np_array.setflags(write=True)
    array = np_array.astype(original_dtype)
    return th.from_numpy(array)
