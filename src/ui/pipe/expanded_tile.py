from __future__ import annotations
import flet as ft
import src.pipe as pipe
from src.ui.pipe.tile import PipeTile
from typing import TYPE_CHECKING, Any, Callable
if TYPE_CHECKING:
    from src.manager import Manager
    from src.ui.common import ConfigPage

class ExpandedPipeTile(ft.Container):
    def __init__(
            self,
            name: str,
            manager: Manager,
            config_page: ConfigPage,
            select_pipe: Callable[[type[pipe.Pipe] | pipe.Pipe], pipe.Pipe],
            delete_pipe: Callable[[Any], None],
            instance: pipe.Pipe | None = None,
        ) -> None:
        self.pipe_tile: PipeTile = PipeTile(
            name,
            manager,
            config_page,
            select_pipe,
            delete_pipe,
            instance,
            self.refresh_status,
        )

        if self.pipe_tile.instance:
            disabled: bool = self.pipe_tile.instance.disabled
        else:
            disabled: bool = True

        self.play_btn: ft.IconButton = ft.IconButton(
            icon=ft.icons.PLAY_ARROW_OUTLINED,
            selected_icon=ft.icons.STOP,
            selected=self.pipe_tile.instance.playing if self.pipe_tile.instance else None,
            disabled=disabled,
            tooltip="Play/Stop",
            on_click=self.play_clicked,
        )
        self.refresh_btn: ft.IconButton = ft.IconButton(
            icon=ft.icons.REFRESH_OUTLINED,
            tooltip="Refresh Status",
            on_click=self.refresh_status,
        )
        self.result = None

        super().__init__(
            ft.Row(
                controls=[
                    ft.Row(
                        [
                            self.play_btn,
                            self.refresh_btn,
                        ],
                        spacing=0,
                    ),
                    self.pipe_tile,
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            )
        )

    def refresh_status(self, e = None) -> None:
        if self.pipe_tile.instance:
            self.play_btn.disabled = self.pipe_tile.instance.disabled
            self.play_btn.selected = self.pipe_tile.instance.playing
        else:
            self.play_btn.disabled = True
            self.play_btn.selected = False
        self.update()

    def play_clicked(self, e) -> None:
        if self.pipe_tile.instance:
            if self.play_btn.selected == self.pipe_tile.instance.playing:
                self.play_btn.selected = not self.pipe_tile.instance.playing
                self.update()
                try:
                    if self.pipe_tile.instance.playing:
                        self.pipe_tile.instance.stop(self.pipe_tile.manager, self.result)
                    else:
                        self.result = None
                        self.pipe_tile.instance.play(self.pipe_tile.manager)
                        self.result = self.pipe_tile.instance.cls_function(self.pipe_tile.instance.config)(pipe.IO())
                except:
                    raise
                finally:
                    try:
                        self.pipe_tile.instance.stop(self.pipe_tile.manager, self.result)
                    except:
                        raise
                    finally:
                        self.refresh_status()
        else:
            self.play_btn.disabled = True
