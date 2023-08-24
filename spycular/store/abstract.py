from abc import ABCMeta, abstractmethod


class AbstractStore(metaclass=ABCMeta):
    def __init__(self, store) -> None:
        self.store = store
        super().__init__()

    @abstractmethod
    def save(self, obj_id: str, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def has(self, obj_id):
        pass
