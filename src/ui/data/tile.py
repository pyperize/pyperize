from __future__ import annotations
import flet as ft
from src.pipe import IO
from typing import TYPE_CHECKING, Any, Callable, Iterable, Mapping
if TYPE_CHECKING:
    from src.manager import Manager
    from src.ui.common import ConfigPage

class DataTile(ft.Container):
    def __init__(
            self,
            name: str,
            data_type: str,
            data: IO | Iterable,
            manager: Manager,
            config_page: ConfigPage,
            delete_data: Callable[[Any], None] | None = None,
        ) -> None:
        self.name: str = name
        self.instance: IO | Iterable = data
        self.manager: Manager = manager
        self.config_page: ConfigPage = config_page
        self.config_btn: ft.IconButton = ft.IconButton(
            icon=ft.icons.MENU_OUTLINED,
            tooltip="Details",
            on_click=self.config_clicked,
        )
        if delete_data is not None:
            self.delete_btn: ft.IconButton = ft.IconButton(
                ft.icons.DELETE_OUTLINED,
                tooltip="Delete",
                on_click=delete_data,
            )

        super().__init__(
            ft.Row(
                controls=[
                    ft.Container(
                        ft.Text(f"{name} ({data_type})", size=18),
                        padding=ft.padding.symmetric(horizontal=10),
                    ),
                    ft.Row(
                        controls=[
                            self.config_btn,
                            self.delete_btn,
                        ] if delete_data is not None else [
                            self.config_btn,
                        ],
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
            expand=True,
            expand_loose=True,
        )
    
    def config_clicked(self, e: Any | None = None):
        self.config_page.push(self.name, DataConfigUI(self.instance, self.manager, self.config_page))


class FieldTile(ft.Container):
    def __init__(
            self,
            name: str,
            data_type: str,
            delete_data: Callable[[Any], None] | None = None,
        ) -> None:
        if delete_data is not None:
            self.delete_btn: ft.IconButton = ft.IconButton(
                ft.icons.DELETE_OUTLINED,
                tooltip="Delete",
                on_click=delete_data,
            )

        super().__init__(
            ft.Row(
                controls=[
                    ft.Container(
                        ft.Text(f"{name} ({data_type})", size=18),
                        padding=ft.padding.symmetric(horizontal=10),
                    ),
                    ft.Row(
                        controls=[
                            self.delete_btn,
                        ] if delete_data is not None else [],
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                expand=True,
            ),
            expand=True,
            expand_loose=True,
        )

class DataConfigUI(ft.Container):
    def __init__(self, data: IO | Iterable, manager: Manager, config_page: ConfigPage) -> None:
        self.instance: IO | Iterable = data
        self.manager: Manager = manager
        self.config_page = config_page
        super().__init__(self.get_contents())

    def get_contents(self):
        if isinstance(self.instance, IO):
            return ft.Column([
                DataTile(key, type(v).__name__, v, self.manager, self.config_page, self.delete_data(key))
                if isinstance(v, IO) or (isinstance(v, Iterable) and not isinstance(v, str))
                else FieldTile((s[:20] + ' ... ' + s[-5:]) if len(s:=str(v)) > 30 else s, type(v).__name__, self.delete_data(key))
                for key, v in self.instance
            ])
        elif isinstance(self.instance, Mapping):
            return ft.Column([
                DataTile(key, type(v).__name__, v, self.manager, self.config_page, self.delete_data(key))
                if isinstance(v := self.instance[key], IO) or (isinstance(v, Iterable) and not isinstance(v, str))
                else FieldTile((s[:20] + ' ... ' + s[-5:]) if len(s:=str(v)) > 30 else s, type(v).__name__, self.delete_data(key))
                for key in self.instance
            ])
        else:
            return ft.Column([
                DataTile((s[:20] + ' ... ' + s[-5:]) if len(s:=str(v)) > 30 else s, type(v).__name__, v, self.manager, self.config_page)
                if isinstance(v, IO) or (isinstance(v, Iterable) and not isinstance(v, str))
                else FieldTile((s[:20] + ' ... ' + s[-5:]) if len(s:=str(v)) > 30 else s, type(v).__name__)
                for v in self.instance
            ])

    def delete_data(self, key):
        def _delete_data(e: Any | None = None):
            with self.manager.lock:
                if isinstance(self.instance, IO) and hasattr(self.instance, key):
                    delattr(self.instance, key)
                elif isinstance(self.instance, Mapping) and (key in self.instance):
                    del self.instance[key]
                self.content = self.get_contents()
            self.update()
        return _delete_data

    def dismiss(self) -> None:
        pass
