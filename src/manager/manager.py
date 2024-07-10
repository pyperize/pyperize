# Manager
# - API
# - Pipes
# - Data
# - Packages
# - Settings

from __future__ import annotations
from pydantic import BaseModel
from threading import Lock
import packages
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.api import API
    from src.pipe import Pipe, IO
    from src.package import Package

class GlobalConfig(BaseModel):
    pass

class Manager:
    cls_config: type[GlobalConfig] = GlobalConfig

    def __init__(self, api: API, config: GlobalConfig | None = None) -> None:
        self.config: GlobalConfig = config if config else self.cls_config()
        self.lock: Lock = Lock()
        self.api: API = api
        self.pipes: dict[str, Pipe | None] = {}
        self.data: dict[str, IO] = {}
        self.packages: dict[str, Package] = packages.PACKAGES
        # self.background: dict = {}
