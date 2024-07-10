#!/usr/bin/env python3
from contextlib import asynccontextmanager

import flet.fastapi as flet_fastapi
from fastapi import FastAPI
import uvicorn

import packages
from src import ui
from src.manager import Manager
from src.api import API

@asynccontextmanager
async def lifespan(app: FastAPI):
    await flet_fastapi.app_manager.start()
    yield
    await flet_fastapi.app_manager.shutdown()

root: FastAPI = FastAPI(lifespan=lifespan)
api: API = API()
manager: Manager = Manager(api)
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
