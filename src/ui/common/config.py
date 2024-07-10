import flet as ft
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.pipe.config import ConfigUI

class ConfigPage(ft.BottomSheet):
    def __init__(self) -> None:
        self.title: ft.Text = ft.Text()
        # self.page: ft.Container = ft.Container()
        self.current: ft.Column = ft.Column()
        self.names: list[str] = []
        self.contents: list[ConfigUI] = []
        self.back_btn: ft.IconButton = ft.IconButton(
            icon=ft.icons.ARROW_BACK,
            tooltip="Back",
            on_click=self.pop,
        )
        super().__init__(
            content=ft.ListView(
                controls=[
                    ft.Container(
                        ft.Row([
                                self.back_btn,
                                self.title,
                        ]),
                        padding=ft.padding.symmetric(vertical=20),
                    ),
                    self.current,
                ],
                # width=800,
                padding=40,
            ),
            dismissible=False,
            is_scroll_controlled=True,
            maintain_bottom_view_insets_padding=True,
            use_safe_area=True,
            # enable_drag=True,
        )

    def refresh(self, update: bool = True) -> None:
        if self.names:
            title_len: int = len(self.names[-1])
            idx: int = -1
            total: int = -len(self.names)
            while (idx - 1) >= total and ((title_len + (l := (len(self.names[(idx - 1)]) + (3 if ">" not in self.names[(idx - 1)] else 5)))) <= 70):
                title_len += l
                idx -= 1
            self.title.value = " > ".join([name if ">" not in name else f'"{name}"' for name in self.names[idx:]])[:70]
            # self.page.content = self.contents[-1]
            self.current.controls.clear()
            self.current.controls.append(self.contents[-1])
            self.open = True
        else:
            self.title.value = None
            # self.page.content = None
            self.current.controls.clear()
            self.open = False
        if update:
            self.update()

    def push(self, name: str, control: ft.Control) -> None:
        self.names.append(name)
        self.contents.append(control)
        self.refresh()

    def pop(self, e) -> None:
        v = None
        try:
            self.names.pop()
            v = self.contents.pop()
        except:
            pass
        finally:
            try:
                if v is not None:
                    v.dismiss()
            except:
                raise
            finally:
                self.refresh()

    def on_dismiss(self, e) -> None:
        while self.contents:
            self.contents.pop().dismiss()
        self.names.clear()
        self.refresh(False)
        # self.names.clear()
        # self.contents.clear()
