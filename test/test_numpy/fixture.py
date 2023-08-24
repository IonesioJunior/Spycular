import pytest

local_numpy = pytest.importorskip("numpy")
from spycular import control, serve  # noqa: E402
from spycular.consumer.virtual_consumer import VirtualConsumer  # noqa: E402
from spycular.producer.virtual_producer import VirtualProducer  # noqa: E402
from spycular.store.virtual_store import VirtualStore  # noqa: E402

message_queue = []
reply_queue = {}


@pytest.fixture
def np():
    pub = VirtualProducer(message_queue=message_queue, reply_queue=reply_queue)
    return control(local_numpy, pub)


@pytest.fixture
def consumer():
    consumer = VirtualConsumer(
        VirtualStore(),
        message_queue=message_queue,
        reply_queue=reply_queue,
    )
    return serve(local_numpy, consumer)


@pytest.fixture
def replies():
    return reply_queue
