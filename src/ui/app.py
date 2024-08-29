import flet as ft
import src.ui as ui
from src.manager import Manager
import base64

title: str = "pyperize"
logo: str = base64.b64encode(open("./assets/icon.png", "rb").read()).decode("latin-1")

class App:
    def __init__(self, manager: Manager) -> None:
        self.manager: Manager = manager

    def refresh_page(self, e) -> None:
        self.content.controls[0].tabs[self.content.controls[0].selected_index].content.refresh_page()

    def __call__(self, page: ft.Page) -> None:
        self.page: ft.Page = page
        self.page.expand = True
        self.appbar = ft.AppBar(
            title=ft.Row(
                [
                    ft.Image(src_base64=logo, height=40, width=40),
                    ft.Text(title, size=30, weight=ft.FontWeight.W_900),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=20,
            ),
            toolbar_height=90,
            center_title=True,
            bgcolor=ft.colors.SURFACE_VARIANT,
        )
        self.config_page: ui.common.ConfigPage = ui.common.ConfigPage()
        self.content: ft.Column = ft.Column(
            [
                ft.Tabs(
                    selected_index=0,
                    animation_duration=300,
                    tabs=[
                        ft.Tab(
                            text="Pipes",
                            icon=ft.icons.DASHBOARD_OUTLINED,
                            content=ui.pages.PipesPage(self.manager, self.config_page),
                        ),
                        ft.Tab(
                            text="Data",
                            icon=ft.icons.DATA_USAGE_OUTLINED,
                            content=ui.pages.DataPage(self.manager, self.config_page),
                        ),
                        ft.Tab(
                            text="API",
                            icon=ft.icons.LINK_OUTLINED,
                            content=ui.pages.APIPage(self.manager, self.config_page),
                        ),
                        ft.Tab(
                            text="Packages",
                            icon=ft.icons.EXTENSION_OUTLINED,
                            content=ui.pages.PackagesPage(self.manager, self.config_page),
                        ),
                        ft.Tab(
                            text="Settings",
                            icon=ft.icons.SETTINGS_OUTLINED,
                            content=ui.pages.SettingsPage(self.manager, self.config_page),
                        ),
                    ],
                    on_change=self.refresh_page,
                    expand=True,
                ),
                ft.ExpansionTile(
                    title=ft.Text("Console"),
                    initially_expanded=False,
                    maintain_state=True,
                    controls=[
                        ft.Column(
                            [self.manager.out],
                            height=360,
                            expand=True,
                            scroll=ft.ScrollMode.ALWAYS,
                            alignment=ft.MainAxisAlignment.START,
                            horizontal_alignment=ft.CrossAxisAlignment.START,
                        ),
                    ],
                ),
            ],
            expand=True,
        )

        self.page.title = title
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.appbar = self.appbar

        self.page.add(self.config_page)
        self.page.add(self.content)
        self.page.update()
