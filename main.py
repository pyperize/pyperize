#!/usr/bin/env python3
from contextlib import asynccontextmanager

import flet.fastapi as flet_fastapi
from fastapi import FastAPI
import uvicorn

import packages
from src import ui
from src.manager import Manager
from src.api import API
import sys
import logging

@asynccontextmanager
async def lifespan(app: FastAPI):
    await flet_fastapi.app_manager.start()
    yield
    await flet_fastapi.app_manager.shutdown()

root: FastAPI = FastAPI(lifespan=lifespan)
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
ui_app: FastAPI = flet_fastapi.app(ui.App(manager)) # , assets_dir="./assets/")

root.mount("/api/", api.app)
root.mount("/", ui_app)

if __name__ == "__main__":
    uvicorn.run(
        root,
        host="0.0.0.0",
        port=8000,
        log_level="warning",
    )
