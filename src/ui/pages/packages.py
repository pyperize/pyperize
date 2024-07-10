from __future__ import annotations
import flet as ft
from typing import TYPE_CHECKING

from src.ui.package import PackageTile
if TYPE_CHECKING:
    from src.manager import Manager
    from src.ui.common import ConfigPage

class PackagesPage(ft.Container):
    def __init__(self, manager: Manager, config_page: ConfigPage) -> None:
        self.manager: Manager = manager
        self.config_page: ConfigPage = config_page
        self.packages_list: ft.ListView = ft.ListView(
            expand=True,
            spacing=20,
            padding=ft.padding.symmetric(vertical=20),
            divider_thickness=1,
            auto_scroll=True,
        )
        super().__init__(
            content=ft.Column(
                controls=[
                    self.packages_list,
                ],
                expand=True,
            ),
            padding=ft.padding.all(20),
            expand=True,
        )
        self.refresh_page(False)

    def refresh_page(self, update: bool = True) -> None:
        with self.manager.lock:
            self.packages_list.controls = [
                PackageTile(
                    package,
                    self.manager,
                    self.config_page,
                ) for package in self.manager.packages.values()
            ]
        if update:
            self.update()
