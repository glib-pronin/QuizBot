from ..settings import dispatcher, router_command
from ..permission import isAdmin
from aiogram.types import Message
from aiogram.filters import CommandStart 

# Хендлер для команди /start
@router_command.message(CommandStart())
async def start_handler(message: Message):
    if isAdmin(message):
        await message.answer(f'Привіт, адміне {message.from_user.full_name}!\nЗа допомогою цього боту ти зможеш проводити тестування для твоїх учнів, щоб перевірити їхній рівень знань із різних тем!\nЩоб обрати тест, скористайтеся командою: /showquizzes')
    else:
        await message.answer(f'Привіт, {message.from_user.full_name}!\nЗа допомогою цього боту ти зможеш проходити тести на різні теми, щоб перевірити свої знання!\nЩоб приєднатися до тесту, скористайся командою: /join')

