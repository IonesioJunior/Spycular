import numpy as local_numpy
import pyarrow
import pytest
import torch as th

from pynocchio.consumer.virtual_consumer import VirtualConsumer
from pynocchio.producer.virtual_producer import VirtualProducer
from pynocchio.reflection.incident import IncidentLib
from pynocchio.reflection.reflected import ReflectedLib
from pynocchio.store.virtual_store import VirtualStore

message_queue = []
reply_queue = {}


@pytest.fixture
def np():
    pub = VirtualProducer(message_queue=message_queue, reply_queue=reply_queue)
    return IncidentLib(local_numpy, pub)


@pytest.fixture
def consumer():
    remote_np = ReflectedLib(local_numpy)
    return VirtualConsumer(
        VirtualStore(),
        remote_np,
        message_queue=message_queue,
        reply_queue=reply_queue,
    )


@pytest.fixture
def replies():
    return reply_queue
