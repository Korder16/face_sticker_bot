from typing import Callable, Dict, Any, Awaitable
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject


class FaceSwapperMiddleware(BaseMiddleware):
    def __init__(self, swapper, app, loaded_r) -> None:
        super().__init__()
        self.swapper = swapper
        self.app = app
        self.loaded_r = loaded_r

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
    ) -> Any:
        data["swapper"] = self.swapper
        data["app"] = self.app
        data["loaded_r"] = self.loaded_r
        return await handler(event, data)
