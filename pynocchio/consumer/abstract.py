from abc import ABCMeta, abstractmethod
from types import ModuleType

from ..pointer.abstract import Pointer
from ..pointer.graph.abstract import PointerGraph
from ..puppetry.puppet import Puppet


class AbstractConsumer(metaclass=ABCMeta):
    def __init__(self, storage):
        self.storage = storage
        super().__init__()

    def set_module(self, module: ModuleType):
        self.puppet_module = Puppet(module)

    @abstractmethod
    def execute(self, ptr: Pointer):
        pass

    @abstractmethod
    def execute_graph(self, ptr: PointerGraph):
        pass

    @abstractmethod
    def reply(self, obj_id: str, obj: object):
        pass
