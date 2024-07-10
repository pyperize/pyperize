#!/usr/bin/env python3
import flet as ft

import packages
from src import ui
from src.manager import Manager
from src.api import API

api: API = API()
manager: Manager = Manager(api)
api.manager = manager
ft.app(ui.App(manager)) # , assets_dir="./assets/")
