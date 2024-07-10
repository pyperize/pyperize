from __future__ import annotations
import flet as ft
from typing import TYPE_CHECKING, Any, Callable
from src.ui.data import DataTile
if TYPE_CHECKING:
    from src.manager import Manager
    from src.ui.common import ConfigPage

class DataPage(ft.Container):
    def __init__(self, manager: Manager, config_page: ConfigPage) -> None:
        self.manager: Manager = manager
        self.config_page: ConfigPage = config_page
        self.data_list: ft.ListView = ft.ListView(
            expand=True,
            spacing=20,
            padding=ft.padding.symmetric(vertical=20),
            divider_thickness=1,
            auto_scroll=True,
        )
        super().__init__(
            content=ft.Column(
                controls=[
                    self.data_list,
                ],
                expand=True,
            ),
            padding=ft.padding.all(20),
            expand=True,
        )
        self.refresh_page(False)

    def refresh_page(self, update: bool = True) -> None:
        with self.manager.lock:
            self.data_list.controls = [
                DataTile(
                    name,
                    type(data).__name__,
                    data,
                    self.manager,
                    self.config_page,
                    self.delete_data(name)
                ) for name, data in self.manager.data.items()
            ]
        if update:
            self.update()

    def delete_data(self, name: str) -> Callable[[Any], None]:
        def _delete_data(e: Any | None = None):
            with self.manager.lock:
                if name in self.manager.data:
                    del self.manager.data[name]
            self.refresh_page()
        return _delete_data
