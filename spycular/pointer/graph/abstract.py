from abc import ABCMeta, abstractmethod
from typing import Callable, Dict, List, Set

from ...puppetry.puppet import Puppet
from ...serde.capnp.recursive import serializable
from ...store.abstract import AbstractStore
from ..abstract import Pointer
from .pointer_node import PointerNode
from .state_enum import PointerState


@serializable
class PointerGraph(metaclass=ABCMeta):
    def __init__(self, pointers: Set[Pointer]) -> None:
        self.graph_map: Dict[str, PointerNode] = {}
        self.__build_execution_graph(pointers)

    @abstractmethod
    async def async_solve(
        self,
        puppet: Puppet,
        storage: AbstractStore | None = None,
        reply_callback: Callable | None = None,
    ) -> None:
        pass

    @property
    def root_nodes(self) -> List[str]:
        node_starters = []
        # Find nodes that start my execution tree
        for key, value in self.graph_map.items():
            if not value.predecessor:
                node_starters.append(key)
                # Executing
                self.graph_map[key].state = PointerState.RUNNING
        return node_starters

    def __build_execution_graph(self, pointers):
        for ptr in pointers:
            node = self.graph_map.get(ptr.id, None)
            if not node:
                self.graph_map[ptr.id] = PointerNode(pointer=ptr)
            else:
                self.graph_map[ptr.id].set_pointer(ptr)

            if getattr(ptr, "parents", None):
                for parent in ptr.parents:
                    parent_id = (
                        parent.target_id if parent.target_id else parent.id
                    )
                    parent_node = self.graph_map.get(parent_id, None)
                    if parent_node:
                        self.graph_map[parent_id].count += 1
                        self.graph_map[parent_id].sucessor.append(ptr.id)
                    else:
                        self.graph_map[ptr.id] = PointerNode(pointer=ptr)

    def __repr__(self) -> str:
        return str(self.graph_map)
