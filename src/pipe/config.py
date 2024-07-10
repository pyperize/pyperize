from __future__ import annotations
from pydantic import BaseModel, ConfigDict
import flet as ft
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.manager import Manager
    from src.ui.common import ConfigPage
    import src.pipe as pipe

class Config(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

class ConfigUI(ft.Container):
    def __init__(self, instance: pipe.Pipe, manager: Manager, config_page: ConfigPage, content: ft.Control | None = None) -> None:
        self.instance: pipe.Pipe = instance
        self.manager: Manager = manager
        self.config_page: ConfigPage = config_page
        super().__init__(content)

    def dismiss(self) -> None:
        pass
