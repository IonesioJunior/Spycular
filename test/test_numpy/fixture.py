import pytest

local_numpy = pytest.importorskip("numpy")
from pynocchio.consumer.virtual_consumer import VirtualConsumer
from pynocchio.producer.virtual_producer import VirtualProducer
from pynocchio.puppetry.puppeteer import Puppeteer
from pynocchio.store.virtual_store import VirtualStore

message_queue = []
reply_queue = {}


@pytest.fixture
def np():
    pub = VirtualProducer(message_queue=message_queue, reply_queue=reply_queue)
    print("My Local Numpy: ", local_numpy)
    return Puppeteer(local_numpy, broker=pub)


@pytest.fixture
def consumer():
    return VirtualConsumer(
        VirtualStore(),
        local_numpy,
        message_queue=message_queue,
        reply_queue=reply_queue,
    )


@pytest.fixture
def replies():
    return reply_queue
