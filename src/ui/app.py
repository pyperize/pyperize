import flet as ft
import src.ui as ui
from src.manager import Manager

class App:
    def __init__(self, manager: Manager) -> None:
        self.manager: Manager = manager

    def refresh_page(self, e) -> None:
        self.content.content.tabs[self.content.content.selected_index].content.refresh_page()

    def __call__(self, page: ft.Page) -> None:
        self.page: ft.Page = page
        self.appbar = ft.AppBar(
            title=ft.Column([
                ft.Text("pyperize", size=30, weight=ft.FontWeight.W_900),
            ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            toolbar_height=90,
            center_title=True,
            bgcolor=ft.colors.SURFACE_VARIANT,
        )
        self.config_page: ui.common.ConfigPage = ui.common.ConfigPage()
        self.content: ft.Container = ft.Container(
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
            expand=True,
        )

        self.page.title = "pyperize"
        self.page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        self.page.appbar = self.appbar

        self.page.add(self.config_page)
        self.page.add(self.content)
        self.page.update()
