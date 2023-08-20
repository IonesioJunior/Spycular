from abc import ABCMeta
from types import ModuleType

from ..puppetry.puppet import Puppet


class AbstractConsumer(metaclass=ABCMeta):
    def __init__(self, storage):
        self.storage = storage
        super().__init__()

    def set_module(self, module: ModuleType):
        self.puppet_module = Puppet(module)
