# third party
import numpy as np
from numpy import frombuffer

from ..recursive import recursive_serde_register

# relative
from .serde import numpy_deserialize, numpy_serialize


def load_numpy_serde():
    recursive_serde_register(
        np.ndarray,
        serialize=numpy_serialize,
        deserialize=numpy_deserialize,
    )

    recursive_serde_register(
        np._globals._NoValueType,
    )
    #  serialize=numpy_serialize, deserialize=numpy_deserialize

    recursive_serde_register(
        np.bool_,
        serialize=lambda x: x.tobytes(),
        deserialize=lambda buffer: frombuffer(buffer, dtype=np.bool_)[0],
    )

    recursive_serde_register(
        np.int8,
        serialize=lambda x: x.tobytes(),
        deserialize=lambda buffer: frombuffer(buffer, dtype=np.int8)[0],
    )

    recursive_serde_register(
        np.int16,
        serialize=lambda x: x.tobytes(),
        deserialize=lambda buffer: frombuffer(buffer, dtype=np.int16)[0],
    )

    recursive_serde_register(
        np.int32,
        serialize=lambda x: x.tobytes(),
        deserialize=lambda buffer: frombuffer(buffer, dtype=np.int32)[0],
    )

    recursive_serde_register(
        np.int64,
        serialize=lambda x: x.tobytes(),
        deserialize=lambda buffer: frombuffer(buffer, dtype=np.int64)[0],
    )

    recursive_serde_register(
        np.uint8,
        serialize=lambda x: x.tobytes(),
        deserialize=lambda buffer: frombuffer(buffer, dtype=np.uint8)[0],
    )

    recursive_serde_register(
        np.uint16,
        serialize=lambda x: x.tobytes(),
        deserialize=lambda buffer: frombuffer(buffer, dtype=np.uint16)[0],
    )

    recursive_serde_register(
        np.uint32,
        serialize=lambda x: x.tobytes(),
        deserialize=lambda buffer: frombuffer(buffer, dtype=np.uint32)[0],
    )

    recursive_serde_register(
        np.uint64,
        serialize=lambda x: x.tobytes(),
        deserialize=lambda buffer: frombuffer(buffer, dtype=np.uint64)[0],
    )

    recursive_serde_register(
        np.single,
        serialize=lambda x: x.tobytes(),
        deserialize=lambda buffer: frombuffer(buffer, dtype=np.single)[0],
    )

    recursive_serde_register(
        np.double,
        serialize=lambda x: x.tobytes(),
        deserialize=lambda buffer: frombuffer(buffer, dtype=np.double)[0],
    )

    recursive_serde_register(
        np.float16,
        serialize=lambda x: x.tobytes(),
        deserialize=lambda buffer: frombuffer(buffer, dtype=np.float16)[0],
    )

    recursive_serde_register(
        np.float32,
        serialize=lambda x: x.tobytes(),
        deserialize=lambda buffer: frombuffer(buffer, dtype=np.float32)[0],
    )

    recursive_serde_register(
        np.float64,
        serialize=lambda x: x.tobytes(),
        deserialize=lambda buffer: frombuffer(buffer, dtype=np.float64)[0],
    )
