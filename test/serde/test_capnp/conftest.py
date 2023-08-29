import pytest

from spycular.producer.virtual import VirtualProducer  # noqa: E402

message_queue = []
reply_queue = {}


@pytest.fixture
def producer():
    return VirtualProducer(
        message_queue=message_queue,
        reply_queue=reply_queue,
    )
