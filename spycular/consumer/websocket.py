import asyncio
from typing import Any, Dict

import websockets

from ..pointer.graph.abstract import PointerGraph
from ..serde.capnp.deserialize import _deserialize
from ..serde.capnp.serialize import _serialize
from ..store.abstract import AbstractStore
from .abstract import AbstractConsumer


class WebSocketConsumer(AbstractConsumer):
    reply_queue: Dict[Any, Any] = {}
    count = 0

    def __init__(self, storage: AbstractStore, url: str, port: int) -> None:
        super().__init__(storage=storage)
        self.url = url
        self.port = port

    # This coroutine handles the incoming messages
    async def handle_input(self, websocket):
        try:
            WebSocketConsumer.reply_queue[websocket] = []
            reply_callback = WebSocketConsumer.create_user_reply_callback(
                websocket,
            )
            async for message in websocket:
                ptr = _deserialize(message, from_bytes=True)
                self.reflected_module.execute(
                    ptr,
                    self.storage,
                    reply_callback,
                )
        finally:
            # Remove client from dictionary upon disconnection
            WebSocketConsumer.reply_queue.pop(websocket, None)

    # This coroutine sends messages asynchronously
    async def handle_output(self, websocket):
        try:
            while not self.stop_event.is_set():
                await asyncio.sleep(0)
                if (
                    WebSocketConsumer.reply_queue.get(websocket, False)
                    and WebSocketConsumer.reply_queue[websocket]
                ):
                    await websocket.send(
                        _serialize(
                            WebSocketConsumer.reply_queue[websocket].pop(0),
                            to_bytes=True,
                        ),
                    )
        finally:
            # Remove client from dictionary upon disconnection
            WebSocketConsumer.reply_queue.pop(websocket, None)

    @staticmethod
    def create_user_reply_callback(websocket):
        def reply(obj_id: str, obj: Any):
            """Handle replies by storing them in the reply queue with
            the corresponding object ID.

            Args:
                obj_id (str): Unique identifier for the object.
                obj (Any): The object to be stored as a reply.
            """
            WebSocketConsumer.reply_queue[websocket].append(obj)

        return reply

    async def serve(self, websocket):
        # Create tasks for sending and receiving messages
        consumer_task = asyncio.ensure_future(self.handle_input(websocket))
        producer_task = asyncio.ensure_future(self.handle_output(websocket))

        done, pending = await asyncio.wait(
            [consumer_task, producer_task],
            return_when=asyncio.FIRST_COMPLETED,
        )

        for task in pending:
            task.cancel()

    def close(self):
        self.stop_event.set()

    async def execute_graph(self, ptr: PointerGraph) -> None:
        # return await super().execute_graph(ptr)
        pass

    def reply(self, obj_id: str, obj: object) -> Any:
        # return super().reply(obj_id, obj)
        pass

    def start(self):
        try:
            loop = asyncio.get_running_loop()
        except RuntimeError:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
        self.ws = websockets.serve(self.serve, self.url, self.port)

        self.stop_event = asyncio.Event()
        loop.run_until_complete(self.ws)
        return loop

    def listen(self):
        try:
            loop = self.start()
            loop.run_until_complete(self.stop_event.wait())
        except KeyboardInterrupt:
            print("Shutting down Websocket Consumer...")
