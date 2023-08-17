from abc import ABC, abstractclassmethod


class AbstractStore(ABC):
    def __init__(self, store) -> None:
        self.store = store
        super().__init__()

    @abstractclassmethod
    def save(self, obj_id: str, obj):
        pass

    @abstractclassmethod
    def get(self, obj_id):
        pass

    @abstractclassmethod
    async def save(self, obj_id: str, obj):
        pass

    @abstractclassmethod
    async def get(self, obj_id):
        pass
