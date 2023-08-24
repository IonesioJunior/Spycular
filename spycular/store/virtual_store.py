from .abstract import AbstractStore


class VirtualStore(AbstractStore):
    def __init__(self) -> None:
        super().__init__(store={})

    def get(self, obj_id):
        return self.store.get(obj_id, None)

    def save(self, obj_id, obj):
        self.store[obj_id] = obj

    def delete(self, obj_id):
        del self.store[obj_id]

    def has(self, obj_id):
        return obj_id in self.store.keys()
