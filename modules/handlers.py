from .settings import *
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from .permission import isAdmin
import os

@dispatcher.message(CommandStart())
async def start_handler(message: Message):
    if isAdmin(message):
        await message.answer(f'Привіт, адміне {message.from_user.full_name}!\nЗа допомогою цього боту ти зможеш проводити тестування для твоїх учнів, щоб перевірити їхній рівень знань із різних тем!\nОсь доступні для тебе команди:\n/showquizzes - список усіх тестів')
    else:
        await message.answer(f'Привіт, {message.from_user.full_name}!\nЗа допомогою цього боту ти зможеш проходити тести на різні теми, щоб перевірити свої знання!\nОсь доступні для тебе команди:')


@dispatcher.message(Command('showquizzes'))
async def showquizzes_handler(message: Message):
    if isAdmin(message):
        files = os.listdir('quizzes')
        filesName = [f.replace('.json', '') for f in files]
        await message.answer(f'Список тестів: \n{str.join('\n', filesName)}')
    else:
        await message.answer('У вас немає прав для цієї команди')


