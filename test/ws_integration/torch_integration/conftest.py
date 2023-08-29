import pytest

local_torch = pytest.importorskip("torch")

from spycular import strike  # noqa: E402
from spycular.producer.websocket import WebSocketsProducer  # noqa: E402


@pytest.fixture(scope="session")
def ws_th_client():
    producer = WebSocketsProducer("localhost:8765")
    np = strike(module=local_torch, producer=producer)
    yield np
    producer.close()


@pytest.fixture(scope="session")
def ws_th_client2():
    producer = WebSocketsProducer("localhost:8765")
    np = strike(module=local_torch, producer=producer)
    yield np
    producer.close()
