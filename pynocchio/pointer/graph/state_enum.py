from enum import Enum

from ...serde.capnp.recursive import serializable


@serializable
class PointerState(Enum):
    PENDING = 0
    RUNNING = 1
    FINISHED = 2
    DELETED = 3
