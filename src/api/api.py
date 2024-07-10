from __future__ import annotations
from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.responses import Response, PlainTextResponse
from threading import Lock
from typing import TYPE_CHECKING, Callable
import asyncio
if TYPE_CHECKING:
    from src.manager import Manager

async def ws_receive(websocket: WebSocket, function: Callable[[bytes], None]):
    while True:
        try:
            await asyncio.to_thread(function, args=(await websocket.receive_bytes(),))
        except WebSocketDisconnect:
            break
        except:
            websocket.close()
            raise

async def ws_send(websocket: WebSocket, function: Callable[[], bytes]):
    while True:
        try:
            await websocket.send_bytes(await asyncio.to_thread(function))
        except WebSocketDisconnect:
            break
        except:
            websocket.close()
            raise

class API:
    def __init__(self) -> None:
        self.app: FastAPI = FastAPI()
        self.ws_handlers: dict[str, Callable[[Request], tuple[Callable[[bytes], None], Callable[[], bytes]]]] = {}
        self.rest_handlers: dict[str, Callable[[Request], Response]] = {}
        self.ws_lock: Lock = Lock()
        self.rest_lock: Lock = Lock()
        self.manager: Manager = None

        @self.app.websocket("/ws/{channel}")
        async def websocket_endpoint(websocket: WebSocket, channel: str, request: Request):
            if channel in self.ws_handlers:
                receive, send = self.ws_handlers[channel](request)
                await websocket.accept()
                await asyncio.gather(
                    ws_receive(websocket, receive),
                    ws_send(websocket, send),
                )

        @self.app.get("/health")
        async def health_endpoint():
            return PlainTextResponse("OK")

        @self.app.get("/rest/{channel}")
        async def get_endpoint(channel: str, request: Request):
            return self._rest_endpoint(channel, request)

        @self.app.post("/rest/{channel}")
        async def post_endpoint(channel: str, request: Request):
            return self._rest_endpoint(channel, request)

    def _rest_endpoint(self, channel: str, request: Request) -> Response:
        if channel in self.rest_handlers:
            return self.rest_handlers[channel](request)
        else:
            return PlainTextResponse("Not Found", status_code=404)

    def add_ws_handler(self, handler_name: str, handler: Callable[[Request], tuple[Callable[[bytes], None], Callable[[], bytes]]]):
        return self._add_handler(handler_name, handler, self.ws_handlers, self.ws_lock)

    def add_rest_handler(self, handler_name: str, handler: Callable[[Request], Response]):
        return self._add_handler(handler_name, handler, self.rest_handlers, self.rest_lock)

    def _add_handler(self, handler_name: str, handler: Callable[[Request], tuple[Callable[[bytes], None], Callable[[], bytes]] | Response], handlers: dict[str, Callable[[Request], tuple[Callable[[bytes], None], Callable[[], bytes]] | Response]], lock: Lock):
        with lock:
            if handler_name not in handlers:
                handlers[handler_name] = handler
            return handlers[handler_name]

    def remove_ws_handler(self, handler_name: str):
        self._remove_handler(handler_name, self.ws_handlers, self.ws_lock)

    def remove_rest_handler(self, handler_name: str):
        self._remove_handler(handler_name, self.rest_handlers, self.rest_lock)

    def _remove_handler(self, handler_name: str, handlers: dict[str, Callable[[Request], tuple[Callable[[bytes], None], Callable[[], bytes]] | Response]], lock: Lock):
        with lock:
            if handler_name in handlers:
                del handlers[handler_name]
