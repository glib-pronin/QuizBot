from .settings import *
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from .permission import isAdmin
import os, json

# Хендлер для команди /start
@dispatcher.message(CommandStart())
async def start_handler(message: Message):
    if isAdmin(message):
        await message.answer(f'Привіт, адміне {message.from_user.full_name}!\nЗа допомогою цього боту ти зможеш проводити тестування для твоїх учнів, щоб перевірити їхній рівень знань із різних тем!\nОсь доступні для тебе команди:\n/showquizzes - список усіх тестів')
    else:
        await message.answer(f'Привіт, {message.from_user.full_name}!\nЗа допомогою цього боту ти зможеш проходити тести на різні теми, щоб перевірити свої знання!\nОсь доступні для тебе команди:')

# Хендлер для команди /showquizzes (тільки для адмінів)
@dispatcher.message(Command('showquizzes'))
async def showquizzes_handler(message: Message):
    if isAdmin(message):
        files = [f for f in os.listdir('quizzes') if f.endswith('.json')]
        testName = []
        for file in files:
            with open(f'quizzes/{file}', 'r', encoding='utf-8') as f:
                data = json.load(f)
                testName.append(data.get('title'))
        await message.answer(f'Список тестів: \n{'\n'.join(testName)}')
    else:
        await message.answer('У вас немає прав для цієї команди')


        