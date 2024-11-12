import os

import brawlstats
from aiogram import F, Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv
from datetime import datetime

import database
import funcs

router = Router()
load_dotenv()
client = brawlstats.Client(os.getenv("BS_TOKEN"))
um = database.UsersManager()


class LinkingState(StatesGroup):
    tag = State()


@router.message(F.text, Command("link"))
async def link(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    if um.get_user_tag(message.from_user.id) is not None:
        await message.answer("Your account is already linked!")
        return
    await message.answer("Send me your tag in Brawl Stars")
    await state.set_state(LinkingState.tag)


@router.message(LinkingState.tag)
async def process_tag(message: types.Message, state: FSMContext) -> None:
    um.create_user(message.from_user.id, message.text)
    await message.answer("Linked")
    await state.clear()


@router.message(F.text, Command("unlink"))
async def unlink(message: types.Message) -> None:
    um.delete_user(message.from_user.id)
    await message.answer("Unlinked")


@router.message(F.text, Command("account"))
async def account(message: types.Message) -> None:
    tag = um.get_user_tag(message.from_user.id)
    if tag is None:
        await message.answer("Your account is not linked. /link")
        return

    try:
        filename = funcs.generate_profile(client.get_profile(tag))
        await message.answer_photo(photo=types.FSInputFile(filename))
        os.remove(filename)
    except Exception as e:
        await message.answer(f"An error occurred: {e}")


@router.message(F.text, Command("battlelogs"))
async def battlelog(message: types.Message) -> None:
    tag = um.get_user_tag(message.from_user.id)
    if tag is None:
        await message.answer("Your account is not linked. /link")
        return

    res = ""
    wins = 0
    for battle in client.get_battle_logs(tag):
        result = "❌"
        if battle.battle.get("result") == "victory":
            result = "✅"
            wins += 1

        starplayer = ""
        if battle.battle.get("star_player", {}).get("tag", "").lstrip("#") == tag:
            starplayer = "🌟"

        time = datetime.strptime(battle.battle_time, "%Y%m%dT%H%M%S.%fZ").strftime("%d/%m/%Y %H:%M:%S")
        res += f"{time} - {battle.event['mode']} {result} {starplayer}\n"

    res += f"\nWins: {wins}/25\nWinrate: {wins/25*100}%"
    await message.answer(res or "No battle logs found.")
