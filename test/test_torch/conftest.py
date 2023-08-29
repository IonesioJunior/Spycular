import pytest

local_torch = pytest.importorskip("torch")

from spycular import reflect, strike  # noqa: E402
from spycular.consumer.virtual import VirtualConsumer  # noqa: E402
from spycular.producer.virtual import VirtualProducer  # noqa: E402
from spycular.store.virtual import VirtualStore  # noqa: E402

torch_message_queue = []
torch_reply_queue = {}


@pytest.fixture
def th():
    pub = VirtualProducer(
        message_queue=torch_message_queue,
        reply_queue=torch_reply_queue,
    )
    return strike(local_torch, pub)


@pytest.fixture
def torch_consumer():
    consumer = VirtualConsumer(
        VirtualStore(),
        message_queue=torch_message_queue,
        reply_queue=torch_reply_queue,
    )
    return reflect(local_torch, consumer)


@pytest.fixture
def torch_replies():
    return torch_reply_queue
