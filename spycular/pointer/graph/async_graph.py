import asyncio
from typing import Callable, Set

from ...puppetry.puppet import Puppet
from ...serde.capnp.recursive import serializable
from ...store.abstract import AbstractStore
from ..abstract import Pointer
from .abstract import PointerGraph
from .state_enum import PointerState


@serializable
class AsyncPointerGraph(PointerGraph):
    def __init__(self, pointers: Set[Pointer]) -> None:
        super().__init__(pointers)

    @staticmethod
    async def worker(
        graph_map,
        queue,
        lock,
        puppet,
        storage,
        reply_callback,
        number,
    ):
        while not queue.empty():
            node = await queue.get()
            # graph_map[node].solve(, storage, reply_callback)
            puppet.execute(
                pointer=graph_map[node].pointer,
                storage=storage,
                reply_callback=reply_callback,
            )

            async with lock:
                graph_map[node].state = PointerState.FINISHED

            for parent in graph_map[node].parents:
                async with lock:
                    graph_map[parent].count -= 1
                    if graph_map[parent].count == 0:
                        storage.delete(parent)

            for sucessor in graph_map[node].sucessor:
                to_be_executed = True
                for parent in graph_map[sucessor].parents:
                    if graph_map[parent].state != PointerState.FINISHED:
                        to_be_executed = False

                if to_be_executed:
                    async with lock:
                        graph_map[sucessor].state = PointerState.RUNNING
                        queue.put_nowait(sucessor)
            await asyncio.sleep(0)

    async def async_solve(
        self,
        puppet: Puppet,
        storage: AbstractStore | None = None,
        reply_callback: Callable | None = None,
    ) -> None:
        node_starters = self.root_nodes

        queue: asyncio.Queue = asyncio.Queue(
            maxsize=len(self.graph_map.keys()),
        )
        graph_changes_lock = asyncio.Lock()
        for item in node_starters:
            queue.put_nowait(item)

        consumer_tasks = [
            asyncio.create_task(
                AsyncPointerGraph.worker(
                    graph_map=self.graph_map,
                    queue=queue,
                    lock=graph_changes_lock,
                    number=i,
                    puppet=puppet,
                    storage=storage,
                    reply_callback=reply_callback,
                ),
            )
            for i in range(len(node_starters))
        ]
        await asyncio.gather(*consumer_tasks)
