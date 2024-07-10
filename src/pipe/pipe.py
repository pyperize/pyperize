from __future__ import annotations
import src.pipe as pipe
from src.ui.common import ConfigPage
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.manager import Manager

class Pipe:
    cls_name: str = "Abstract Pipe"
    cls_config: type[pipe.Config] = pipe.Config
    cls_function: type[pipe.Function] = pipe.Function

    def __init__(self, name: str, manager: Manager, config: pipe.Config) -> None:
        self.name: str = name
        self.config: pipe.Config = config
        self.playing: bool = False
        self.disabled: bool = False

    def config_ui(self, manager: Manager, config_page: ConfigPage) -> pipe.ConfigUI:
        return pipe.ConfigUI(self, manager, config_page)

    def play(self, manager: Manager) -> None:
        if self.playing:
            return
        self.playing = True

    def stop(self, manager: Manager, result) -> None:
        if not self.playing:
            return
        self.playing = False

    def __getstate__(self):
        return {
            "cls_name": self.cls_name,
            "cls_config": self.cls_config,
            "cls_function": self.cls_function,
            "name": self.name,
            "config": self.config,
            "playing": self.playing,
            "disabled": self.disabled,
            "play": self.play,
            "stop": self.stop,
            "__init__": self.__init__,
            "__getstate__": self.__getstate__,
            "__setstate__": self.__setstate__,
        }

    def __setstate__(self, state):
        self.__dict__.update(state)
