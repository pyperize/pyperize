from __future__ import annotations
import flet as ft
from typing import TYPE_CHECKING, Any, Callable
import src.pipe as pipe
if TYPE_CHECKING:
    from src.manager import Manager
    from src.ui.common import ConfigPage

class PipeTile(ft.Container):
    def __init__(
            self,
            name: str,
            manager: Manager,
            config_page: ConfigPage,
            select_pipe: Callable[[type[pipe.Pipe] | pipe.Pipe], pipe.Pipe],
            delete_pipe: Callable[[Any], None],
            instance: pipe.Pipe | None = None,
            refresh_status: Callable[[Any | None], None] | None = None,
            # io_cls: tuple[type[pipe.IO], type[pipe.IO]] = (pipe.IO, pipe.IO),
        ) -> None:
        self.name: str = name
        self.manager: Manager = manager
        self.config_page: ConfigPage = config_page
        self.select_pipe: Callable[[type[pipe.Pipe] | pipe.Pipe], pipe.Pipe] = select_pipe
        self.delete_pipe: Callable[[Any], None] = delete_pipe
        self.instance: pipe.Pipe | None = instance
        self.options: dict[str, type[pipe.Pipe] | pipe.Pipe] = {}
        self.refresh_status: Callable[[Any | None], None] | None = refresh_status
        # self.io_cls: tuple[type[pipe.IO], type[pipe.IO]] = io_cls

        self.pipe_selector: ft.Dropdown = ft.Dropdown(
            self.instance.cls_name if self.instance else None,
            padding=ft.padding.symmetric(horizontal=10),
            border_color="grey",
            on_change=self.select_changed,
            on_click=self.refresh_options,
            dense=True,
        )
        self.refresh_options(update=False)
        self.config_btn: ft.IconButton = ft.IconButton(
            icon=ft.icons.SETTINGS_OUTLINED,
            disabled=self.instance == None,
            tooltip="Configure",
            on_click=self.config_clicked,
        )
        self.delete_btn: ft.IconButton = ft.IconButton(
            ft.icons.DELETE_OUTLINED,
            tooltip="Delete",
            on_click=self.delete_pipe,
        )

        super().__init__(
            ft.Row(
                controls=[
                    ft.Container(
                        ft.Text(name, size=18),
                        padding=ft.padding.symmetric(horizontal=10),
                    ),
                    ft.Row(
                        controls=[
                            self.pipe_selector,
                            self.config_btn,
                            self.delete_btn,
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

    # def validate(self, cls: pipe.Function) -> bool:
    #     try:
    #         cls.cls_input.model_validate(self.io_cls[0]())
    #         self.io_cls[1].model_validate(cls.cls_output())
    #     except ValidationError:
    #         return False
    #     return True

    def refresh_options(self, e = None, update: bool = True) -> None:
        self.options: dict[str, type[pipe.Pipe] | pipe.Pipe] = {
            name: cls
            for package in self.manager.packages
            for name, cls in self.manager.packages[package].pipes.items()
            # if self.validate(cls.cls_function)
        }
        # self.options.update({
        #     f"Pipe: {name}": instance
        #     for name, instance in self.manager.pipes.items()
        #     if name != self.name
        #     # if instance and self.validate(instance.cls_function)
        # })
        self.pipe_selector.options = [ft.dropdown.Option(name) for name in self.options]
        self.pipe_selector.value = self.instance.cls_name if self.instance else None
        if update:
            self.update()

    def select_changed(self, e) -> None:
        self.instance: pipe.Pipe | None = self.select_pipe(self.options[self.pipe_selector.value]) if self.pipe_selector.value else None
        self.config_btn.disabled = self.instance == None
        self.update()
        if self.refresh_status:
            self.refresh_status()

    def config_clicked(self, e) -> None:
        if self.instance:
            self.config_page.push(self.name, self.instance.config_ui(self.manager, self.config_page))
