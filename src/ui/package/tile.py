from __future__ import annotations
import flet as ft
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.manager import Manager
    from src.ui.common import ConfigPage
    from src.package import Package

class PackageTile(ft.Container):
    def __init__(
            self,
            package: Package,
            manager: Manager,
            config_page: ConfigPage,
        ) -> None:
        self.package: str = package
        self.manager: Manager = manager
        self.config_page: ConfigPage = config_page

        super().__init__(
            ft.Row(
                controls=[
                    ft.Container(
                        ft.Text(self.package.name, size=18),
                        padding=ft.padding.symmetric(horizontal=10),
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
            expand=True,
        )
