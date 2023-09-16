import pytest

from spycular import reflect, strike  # noqa: E402
from spycular.consumer.virtual import VirtualConsumer  # noqa: E402
from spycular.producer.virtual import VirtualProducer  # noqa: E402
from spycular.store.virtual import VirtualStore  # noqa: E402

from . import module_mock  # noqa: E402

message_queue = []
reply_queue = {}


@pytest.fixture
def producer():
    pub = VirtualProducer(message_queue=message_queue, reply_queue=reply_queue)
    return strike(module_mock, pub)


@pytest.fixture
def consumer():
    consumer = VirtualConsumer(
        VirtualStore(),
        message_queue=message_queue,
        reply_queue=reply_queue,
    )
    return reflect(module_mock, consumer)


@pytest.fixture
def replies():
    return reply_queue
