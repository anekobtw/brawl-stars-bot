from aiogram import F, Router, types
from aiogram.filters import Command

router = Router()


@router.message(F.text, Command("start"))
async def start(message: types.Message) -> None: ...
