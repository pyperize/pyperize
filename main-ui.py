#!/usr/bin/env python3
import flet as ft

import packages
from src import ui
from src.manager import Manager
from src.api import API
import sys
import logging

api: API = API()
manager: Manager = Manager(api)
sys.stdout = manager.out
sys.stderr = manager.out
handler = logging.StreamHandler(manager.out)
handler.setFormatter(logging.Formatter('%(asctime)s | %(name)s |  %(levelname)s: %(message)s'))
logging.getLogger(__name__).addHandler(handler)
logging.getLogger("ray").addHandler(handler)
logging.getLogger("ray.data").addHandler(handler)
logging.getLogger("ray.tune").addHandler(handler)
logging.getLogger("ray.rllib").addHandler(handler)
logging.getLogger("ray.train").addHandler(handler)
logging.getLogger("ray.serve").addHandler(handler)
logging.getLogger("flet").addHandler(handler)
logging.getLogger("flet_core").addHandler(handler)
logging.getLogger("asyncio").addHandler(handler)
api.manager = manager
ft.app(ui.App(manager)) # , assets_dir="./assets/")
