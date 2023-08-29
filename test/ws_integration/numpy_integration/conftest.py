import pytest

local_numpy = pytest.importorskip("numpy")

from spycular import strike  # noqa: E402
from spycular.producer.websocket import WebSocketsProducer  # noqa: E402


@pytest.fixture(scope="session")
def ws_np_client():
    producer = WebSocketsProducer("localhost:8765")
    np = strike(module=local_numpy, producer=producer)
    yield np
    producer.close()


@pytest.fixture(scope="session")
def ws_np_client2():
    producer = WebSocketsProducer("localhost:8765")
    np = strike(module=local_numpy, producer=producer)
    yield np
    producer.close()
