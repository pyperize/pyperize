from __future__ import annotations
import flet as ft
from src.ui.pipe import ExpandedPipeTile
from typing import TYPE_CHECKING, Callable, Any
if TYPE_CHECKING:
    from src.manager import Manager
    from src.ui.common import ConfigPage
    import src.pipe as pipe

class PipesPage(ft.Container):
    def __init__(self, manager: Manager, config_page: ConfigPage) -> None:
        self.manager: Manager = manager
        self.config_page: ConfigPage = config_page
        self.new_pipe_name = ft.TextField(
            hint_text="Give the pipe a unique name...",
            expand=True,
            border_color="grey",
            on_submit=self.add_pipe,
            dense=True,
        )
        self.pipes_list: ft.ListView = ft.ListView(
            expand=True,
            spacing=20,
            padding=ft.padding.symmetric(vertical=20),
            divider_thickness=1,
            auto_scroll=True,
        )
        super().__init__(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            self.new_pipe_name,
                            ft.IconButton(
                                icon=ft.icons.ADD,
                                on_click=self.add_pipe,
                            ),
                        ],
                        spacing=10,
                    ),
                    self.pipes_list,
                ],
                expand=True,
            ),
            padding=ft.padding.all(20),
            expand=True,
        )
        self.refresh_page(False)

    def refresh_page(self, update: bool = True) -> None:
        with self.manager.lock:
            self.pipes_list.controls = [
                ExpandedPipeTile(
                    name,
                    self.manager,
                    self.config_page,
                    self.select_pipe(name),
                    self.delete_pipe(name),
                    pipe,
                ) for name, pipe in self.manager.pipes.items()
            ]
        if update:
            self.new_pipe_name.focus()
            self.update()

    def select_pipe(self, name: str) -> Callable[[type[pipe.Pipe] | pipe.Pipe], pipe.Pipe]:
        def _select_pipe(cls: type[pipe.Pipe] | pipe.Pipe) -> pipe.Pipe:
            if isinstance(cls, type):
                cls: pipe.Pipe = cls(name, self.manager, cls.cls_config())
            self.manager.pipes[name] = cls
            return cls
        return _select_pipe

    def add_pipe(self, e) -> None:
        added = None
        with self.manager.lock:
            if self.new_pipe_name.value and (self.new_pipe_name.value not in self.manager.pipes):
                added = self.new_pipe_name.value
                self.manager.pipes[added] = None
        self.new_pipe_name.value = ""
        self.refresh_page()

    def delete_pipe(self, name: str) -> Callable[[Any], None]:
        def _delete_pipe(e: Any | None = None):
            with self.manager.lock:
                if name in self.manager.pipes:
                    del self.manager.pipes[name]
            self.refresh_page()
        return _delete_pipe
