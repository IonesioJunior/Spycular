from abc import ABCMeta

from ..puppetry.puppet import Puppet


class AbstractConsumer(metaclass=ABCMeta):
    def __init__(self, storage, module):
        self.storage = storage
        self.puppet_module = Puppet(module)
        super().__init__()
