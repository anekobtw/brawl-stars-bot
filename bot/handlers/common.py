# Write function handlers here, examples are provided below

import os

import brawlstats
from aiogram import F, Router, types
from aiogram.filters import Command
from dotenv import load_dotenv

import funcs

router = Router()
load_dotenv()
client = brawlstats.Client(os.getenv("BS_TOKEN"))


@router.message(F.text, Command("start"))
async def start(message: types.Message) -> None: ...


@router.message(F.text, Command("user"))
async def user(message: types.Message) -> None:
    try:
        player = client.get_profile(message.text.split()[1])
        top_brawler = max(player.brawlers, key=lambda brawler: brawler.trophies)
        funcs.generate_profile(top_brawler.id, player.icon.id, player.name, player.name_color, funcs.generate_description(player))
        await message.answer_photo(photo=types.FSInputFile(f"{player.name}.png"))
        os.remove(f"{player.name}.png")
    except Exception as e:
        await message.answer(f"An error occurred: {e}")
