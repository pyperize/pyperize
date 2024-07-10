from __future__ import annotations
from pydantic import BaseModel, ConfigDict
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.pipe.config import Config
    from src.pipe.function import IO

class IO(BaseModel):
    model_config = ConfigDict(from_attributes=True, arbitrary_types_allowed=True)

class Function:
    cls_input: type[IO] = IO
    cls_output: type[IO] = IO

    def __init__(self, config: Config) -> None:
        self.config: Config = config

    def __call__(self, input: IO) -> IO:
        return input
