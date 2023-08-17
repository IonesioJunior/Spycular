from abc import ABC
from collections.abc import Iterable

from ..pointer import Pointer


class AbstractConsumer(ABC):
    def __init__(self, storage, reverse_lib):
        self.storage = storage
        self.reverse_lib = reverse_lib
        super().__init__()

    def execute(self, msg):
        msg.args, msg.kwargs = self.resolve_pointer_args(msg)
        if isinstance(msg, Pointer):
            if not msg.call:
                obj = self.reverse_lib.call_original(msg)
                self.storage.save(msg.id, obj)
            else:
                obj = self.resolve_action_objects(msg)
                if type(obj) != type(None):
                    self.storage.save(msg.id, obj)
        else:
            store_obj = self.storage.get(msg.ptr_id)
            self.reply(msg.ptr_id, store_obj)  # reply_queue[msg.ptr_id] = store_obj

    def resolve_action_objects(self, msg):
        store_obj = self.storage.get(msg.obj_id)
        try:
            return self.reverse_lib.action_call(
                store_obj, msg.path, msg.args, msg.kwargs
            )
        except Exception as e:
            print("Error message in : ", msg)
            raise e

    def resolve_pointer_local(self, ptr):
        ptr_result = None
        if ptr.is_obj_ptr:
            ptr_result = self.storage.get(ptr.id)
        elif not ptr.call:
            ptr_result = self.reverse_lib.call_original(ptr)
        else:
            ptr_result = self.resolve_action_objects(ptr)
        return ptr_result

    def resolve_pointer_args(self, msg):
        # Resolve Args if they're pointers first
        args = []
        for arg in getattr(msg, "args", []):
            if isinstance(arg, Pointer):
                args.append(self.resolve_pointer_local(arg))
            else:
                if isinstance(arg, Iterable):
                    new_args = []
                    for new_agr in arg:
                        if isinstance(new_agr, Pointer):
                            new_agr.args, new_agr.kwargs = self.resolve_pointer_args(
                                new_agr,
                            )
                            new_agr = self.resolve_pointer_local(new_agr)

                        new_args.append(new_agr)
                    arg = tuple(new_args)
                args.append(arg)
        args = tuple(args)

        # Resolve Kwargs if they're pointers first
        kwargs = {}
        for key, val in getattr(msg, "kwargs", {}).items():
            if isinstance(val, Pointer):
                kwargs[key] = self.resolve_pointer_local(val)
            else:
                kwargs[key] = val

        return args, kwargs
