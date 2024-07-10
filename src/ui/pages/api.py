from __future__ import annotations
import flet as ft
from src.ui.api import APITile
from typing import TYPE_CHECKING, Any, Callable
if TYPE_CHECKING:
    from fastapi import Request, Response
    from src.manager import Manager
    from src.ui.common import ConfigPage

class APIPage(ft.Container):
    def __init__(self, manager: Manager, config_page: ConfigPage) -> None:
        self.manager: Manager = manager
        self.config_page: ConfigPage = config_page
        self.api_list: ft.ListView = ft.ListView(
            expand=True,
            spacing=20,
            padding=ft.padding.symmetric(vertical=20),
            divider_thickness=1,
            auto_scroll=True,
        )
        super().__init__(
            content=ft.Column(
                controls=[
                    self.api_list,
                ],
                expand=True,
            ),
            padding=ft.padding.all(20),
            expand=True,
        )
        self.refresh_page(False)

    def refresh_page(self, update: bool = True) -> None:
        with self.manager.lock:
            self.api_list.controls = [*(
                APITile(
                    f"/api/rest/{name}",
                    self.manager,
                    self.config_page,
                    self.delete_api(name, self.manager.api.rest_handlers),
                ) for name in self.manager.api.rest_handlers.keys()
            ), *(
                APITile(
                    f"/api/ws/{name}",
                    self.manager,
                    self.config_page,
                    self.delete_api(name, self.manager.api.ws_handlers),
                ) for name in self.manager.api.ws_handlers.keys()
            )]
        if update:
            self.update()

    def delete_api(self, name: str, handlers: dict[str, Callable[[Request], tuple[Callable[[bytes], None], Callable[[], bytes]] | Response]]) -> Callable[[Any], None]:
        def _delete_api(e: Any | None = None):
            with self.manager.lock:
                if name in handlers:
                    del handlers[name]
            self.refresh_page()
        return _delete_api
