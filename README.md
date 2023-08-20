# Pynocchio: Making remote calls as easy-peasy as pie!

Pynocchio offers an innovative way to use Python libraries remotely through RPC. Inspired by the idea of puppets and puppeteers, it provides unparalleled flexibility, allowing you to customize the communication protocol, serialization method, and even the way objects are managed and stored on the remote side.

## 📑 Table of Contents

- [🔧 Installation](#installation)
- [🚀 Getting Started](#getting-started)
- [📡 Communication](#communication)
- [💾 Storage](#storage)
- [🔄 Serialization](#serialization)

## 🔧 Installation

📦 Pynocchio is available on PyPI. Get it in no time:

```bash
pip install pynocchio
```


## 🚀 Getting Started

Dive into Pynocchio and tap into its powerful features! This simple guide will use virtual **producer (client)** and **consumer (server)** abstractions to help you grasp its core concepts and functionalities.

1 - **Server Side**
```python
import pynocchio as pn
import numpy as local_numpy

message_queue = []
reply_queue = {}

# Memory Server Type
consumer = pn.VirtualConsumer(
  pn.VirtualStorage(), # Memory Storage Type
  message_queue,
  reply_queue)

# Assign the lib tree you'll accept to execute
pn.serve(local_numpy, consumer)

# Consume Client's requests
consumer.listen()
```


2 - **Client Side**
```python
import pynocchio as pn
import numpy as local_numpy

message_queue = []
reply_queue = {}


# Memory Client type
producer = pn.VirtualProducer(message_queue, reply_queue)

# Mirror all numpy classes, functions and attributes
np = pn.control(local_numpy, producer)

# Run as if you were executing it locally
x_ptr = np.array([1, 2, 3])
y_ptr = np.array([4, 5, 6])
result = x_ptr + y_ptr

result.retrieve()
```


## 📡 Choose how you send and receive the remote calls!

  Picking a protocol is a breeze! Pynocchio provides the flexibility to use your preferred communication protocol. To give an example, this is how we can send and receive our commands using WebSockets.

1 - **Pynocchio Websocket Server**
```python
import asyncio

import numpy as local_numpy
import pynocchio as pn
from pynocchio.consumer.abstract import AbstractConsumer
from pynocchio.store.virtual_store import VirtualStore
from pynocchio.serde.capnp.deserialize import _deserialize
from pynocchio.serde.capnp.serialize import _serialize
from typing import Any
from websockets.server import serve


class WebsocketConsumer(AbstractConsumer):
    def __init__(self, storage, websocket):
        super().__init__(storage)
        self.websocket = websocket
        self.reply_queue = []

    async def execute(self, ptr: bytes):
        ptr = _deserialize(ptr, from_bytes=True)
        self.puppet_module.execute(
            pointer=ptr,storage=self.storage,
            reply_callback=self.reply,
        )
        if self.reply_queue:
            message = _serialize(self.reply_queue.pop(0), to_bytes=True)
            await self.websocket.send(message)

    def reply(self, obj_id: str, obj: Any):
        self.reply_queue.append(obj)


async def listen(websocket):
    consumer = WebsocketConsumer(VirtualStore(), websocket=websocket)
    pn.serve(module=local_numpy,consumer=consumer)
    async for message in websocket:
        await consumer.execute(message)

async def main():
    async with serve(listen, "localhost", 8765):
        await asyncio.Future()  # run forever


asyncio.run(main())

```

2 - **Pynocchio Websocket Client**
```python
import numpy as local_numpy
import pynocchio as pn
from pynocchio.producer.abstract import AbstractProducer
from pynocchio.pointer.abstract import Pointer
from pynocchio.pointer.object_pointer import GetPointer
from pynocchio.serde.capnp.deserialize import _deserialize
from pynocchio.serde.capnp.serialize import _serialize
from websockets.sync.client import connect



class WebSocketsProducer(AbstractProducer):
    def __init__(self):
        self.socket = connect("ws://localhost:8765")
        super().__init__()

    def send(self, ptr: Pointer):
        msg = _serialize(ptr, to_bytes=True)
        self.socket.send(msg)

    def request(self, ptr: GetPointer):
        msg = _serialize(ptr, to_bytes=True)
        self.socket.send(msg)
        response = self.socket.recv()
        return _deserialize(response, from_bytes=True)

# Parse Numpy Library and set the Websocket Producer.
producer = WebSocketsProducer()
np = pn.control(module=local_numpy, producer=producer)

# Perform remote numpy calls and retrieve the result!
np.ALLOW_THREADS
x_ptr = np.array([1, 2, 3, 4, 5, 6])
x_ptr = x_ptr + x_ptr
my_result = x_ptr.retrieve()
producer.socket.close()
```

## 💾 Storage

Store your way! Pynocchio lets you be in charge:

- **Relational Databases** 🗃:
  - e.g., MySQL, PostgreSQL
- **NoSQL Databases** 📊:
  - e.g., MongoDB, Cassandra
- **In-memory** 🚀:
  - e.g., Redis
- **Custom Storage** 🔒:
  - Craft your own storage backend.

```python
# Switching storage backends is straightforward
remote.configure(storage=pynocchio.storage.MongoDB)
```

## 🔄 Serialization

Encode and decode your data your way:

- **JSON** 📝:
  - The universal choice.
- **MessagePack** 🎛:
  - Compact binary format.
- **Protobuf** 📦:
  - For those intricate data structures.
- **Custom Serialization** ⚙️:
  - Roll your own encoder-decoder combo.

```python
# Shifting serialization methods is a snap
remote.configure(serialization=pynocchio.serialization.MessagePack)
```

## 📚 Documentation

For more detailed insights, head over to our [Wiki](your_wiki_link_here) or peek into the [docs/](./docs) directory.

## 🤝 Contributing

Wish to contribute to Pynocchio? Fantastic! Check our [CONTRIBUTING.md](./CONTRIBUTING.md) guide to get started.


## 🙏 Acknowledgements

A massive shoutout to [Name](profile_link) and all our wonderful contributors.

## 📃 License

Pynocchio is under the Apache 2.0 License. Delve into [LICENSE.md](./LICENSE.md) for all the legalities.

## 📞 Contact

Queries? Suggestions? Drop us an email at [ionesiojr@gmail.com](mailto:ionesiojr@gmail.com).

## 🎉 Special Thanks

Kudos to all our backers, contributors, and supporters for making Pynocchio a reality. You rock!
