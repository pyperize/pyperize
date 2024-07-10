from __future__ import annotations
import flet as ft
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.manager import Manager
    from src.ui.common import ConfigPage

class SettingsPage(ft.Container):
    def __init__(self, manager: Manager, config_page: ConfigPage) -> None:
        self.manager: Manager = manager
        self.config_page: ConfigPage = config_page
        super().__init__()
        self.refresh_page(False)

    def refresh_page(self, update: bool = True) -> None:
        if update:
            self.update()
