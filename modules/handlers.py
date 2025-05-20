from .settings import *
from aiogram.types import Message
from aiogram.filters import CommandStart

@dispatcher.message(CommandStart())
async def start_handler(message: Message):
    await message.answer(f'Привіт, {message.from_user.full_name}')
    print(message)