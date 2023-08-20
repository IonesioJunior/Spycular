import pytest

local_torch = pytest.importorskip("torch")

from pynocchio import control, serve  # noqa: E402
from pynocchio.consumer.virtual_consumer import VirtualConsumer  # noqa: E402
from pynocchio.producer.virtual_producer import VirtualProducer  # noqa: E402
from pynocchio.store.virtual_store import VirtualStore  # noqa: E402

torch_message_queue = []
torch_reply_queue = {}


@pytest.fixture
def th():
    pub = VirtualProducer(
        message_queue=torch_message_queue,
        reply_queue=torch_reply_queue,
    )
    return control(local_torch, pub)


@pytest.fixture
def torch_consumer():
    consumer = VirtualConsumer(
        VirtualStore(),
        message_queue=torch_message_queue,
        reply_queue=torch_reply_queue,
    )
    return serve(local_torch, consumer)


@pytest.fixture
def torch_replies():
    return torch_reply_queue
