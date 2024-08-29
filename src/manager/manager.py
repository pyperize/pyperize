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
import flet as ft
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.api import API
    from src.pipe import Pipe, IO
    from src.package import Package

class GlobalConfig(BaseModel):
    pass

class Console(ft.TextField):
    def write(self, string):
        self.value += string
    
    def isatty(self):
        return False
    
    def flush(self):
        try:
            self.update()
        except:
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
        self.out: Console = Console(
            expand=True,
            bgcolor=ft.colors.GREY_400,
            color=ft.colors.GREY_800,
            # text_style=ft.TextStyle(font_family=ft.),
            text_align=ft.TextAlign.LEFT,
            multiline=True,
            disabled=True,
            content_padding=20,
            min_lines=12,
        )
        # self.background: dict = {}
