from websockets.sync.client import connect

from ..pointer.abstract import Pointer
from ..pointer.object_pointer import GetPointer
from ..serde.capnp.deserialize import _deserialize
from ..serde.capnp.serialize import _serialize
from .abstract import AbstractProducer


class WebSocketsProducer(AbstractProducer):
    def __init__(self, url: str):
        self.socket = connect(f"ws://{url}")
        super().__init__()

    def send(self, ptr: Pointer):
        msg = _serialize(ptr, to_bytes=True)
        self.socket.send(msg)

    def request(self, ptr: GetPointer):
        msg = _serialize(ptr, to_bytes=True)
        self.socket.send(msg)
        response = self.socket.recv()
        return _deserialize(response, from_bytes=True)

    def close(self):
        self.socket.close()
