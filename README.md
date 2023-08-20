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

Dive into Pynocchio and tap into its powerful features! This simple guide will help you grasp its core concepts and functionalities.

```python
import pynocchio

remote = pynocchio.RemoteLibrary(...)
```


## 📡 Communication

Choose how you send and receive the remote calls! Pynocchio provides the flexibility to use your preferred communication protocol:

- **HTTP/HTTPS** 🌐:
  - Perfect for web-based services and integrations.
- **WebSockets** ⚡:
  - Tailored for real-time applications.
- **MQTT** 🛰:
  - A top pick for IoT applications.
- **Custom Protocol** 🔗:
  - Craft and use your own unique protocol.

```python
# Picking a protocol is a breeze
remote = pynocchio.RemoteLibrary(protocol=pynocchio.protocols.HTTP)
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
