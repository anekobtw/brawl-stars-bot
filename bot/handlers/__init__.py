from aiogram import Router

from . import account, common

router = Router()
router.include_router(common.router)
router.include_router(account.router)
