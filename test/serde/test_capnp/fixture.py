import pytest

from pynocchio.producer.virtual_producer import VirtualProducer  # noqa: E402

message_queue = []
reply_queue = {}


@pytest.fixture
def producer():
    return VirtualProducer(
        message_queue=message_queue,
        reply_queue=reply_queue,
    )
