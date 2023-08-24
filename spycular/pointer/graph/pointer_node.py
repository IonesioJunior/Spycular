from typing import List

from ...serde.capnp.recursive import serializable
from ..abstract import Pointer
from .state_enum import PointerState


@serializable
class PointerNode:
    def __init__(
        self,
        pointer: Pointer | None = None,
        count: int = 0,
        sucessor: List[str] | None = None,
    ) -> None:
        self.id = pointer.id if pointer else ""  # type: ignore
        self.pointer = pointer
        self.path = pointer.path if self.pointer else ""  # type: ignore
        self.parents = (
            [
                parent.target_id if parent.target_id else parent.id
                for parent in pointer.parents  # type: ignore
            ]
            if getattr(pointer, "parents", None)
            else []
        )

        self.predecessor = (
            False
            if not getattr(pointer, "parents", False)
            or not pointer.parents  # type: ignore
            else True
        )
        self.count = count
        self.state = PointerState.PENDING
        self.sucessor = sucessor if sucessor else []

    def set_pointer(self, pointer: Pointer):
        self.id = pointer.id
        self.pointer = pointer
        self.path = pointer.path
        self.parents = (
            [
                parent.target_id if parent.target_id else parent.id
                for parent in pointer.parents  # type: ignore
            ]
            if getattr(pointer, "parents", None)
            else []
        )
        self.predecessor = (
            False if not pointer.parents else True  # type: ignore
        )

    def __repr__(self) -> str:
        return f"<PointerNode id={self.id} count={self.count} \
            state={self.state} sucessor={self.sucessor} \
            parents={self.parents} predecessor={self.predecessor}>"
