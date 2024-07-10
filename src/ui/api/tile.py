from __future__ import annotations
import flet as ft
from typing import TYPE_CHECKING, Any, Callable
if TYPE_CHECKING:
    from src.manager import Manager
    from src.ui.common import ConfigPage

class APITile(ft.Container):
    def __init__(
            self,
            name: str,
            manager: Manager,
            config_page: ConfigPage,
            delete: Callable[[Any], None],
        ) -> None:
        self.name: str = name
        self.manager: Manager = manager
        self.config_page: ConfigPage = config_page
        # self.config_btn: ft.IconButton = ft.IconButton(
        #     icon=ft.icons.SETTINGS_OUTLINED,
        #     tooltip="Configure",
        #     # on_click=self.config_clicked,
        # )
        self.delete_btn: ft.IconButton = ft.IconButton(
            ft.icons.DELETE_OUTLINED,
            tooltip="Delete",
            on_click=delete,
        )

        super().__init__(
            ft.Row(
                controls=[
                    ft.Container(
                        ft.Text(self.name, size=18),
                        padding=ft.padding.symmetric(horizontal=10),
                    ),
                    ft.Row(
                        controls=[
                            # self.config_btn,
                            self.delete_btn,
                        ],
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
            expand=True,
        )
