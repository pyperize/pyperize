from __future__ import annotations
import os
from typing import TYPE_CHECKING, Iterable

if TYPE_CHECKING:
    from src.pipe import Pipe

class Package:
    name: str = "Abstract Package"
    _pipes: Iterable[type[Pipe]] = []
    dependencies: dict[str, Package] = {}

    def __init__(self) -> None:
        self.path: str = os.path.dirname(__file__)
        self.pipes: dict[str, type[Pipe]] = {cls.cls_name: cls for cls in self._pipes}
