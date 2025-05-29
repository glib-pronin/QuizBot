from .settings import dispatcher, active_tests, students, bot
from .permission import isAdmin
from .filter import StudentStateFilter
from .utils import get_test_start_msg, load_file, generate_unique_code
from aiogram import F
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os

# Хендлер для команди /start
@dispatcher.message(CommandStart())
async def start_handler(message: Message):
    if isAdmin(message):
        await message.answer(f'Привіт, адміне {message.from_user.full_name}!\nЗа допомогою цього боту ти зможеш проводити тестування для твоїх учнів, щоб перевірити їхній рівень знань із різних тем!\nЩоб обрати тест, скористайтеся командою: /showquizzes')
    else:
        await message.answer(f'Привіт, {message.from_user.full_name}!\nЗа допомогою цього боту ти зможеш проходити тести на різні теми, щоб перевірити свої знання!\nЩоб приєднатися до тесту, скористайся командою: /join')

# Хендлер для команди /showquizzes (тільки для адмінів)
@dispatcher.message(Command('showquizzes'))
async def showquizzes_handler(message: Message):
    if isAdmin(message):
        files = [f for f in os.listdir('quizzes') if f.endswith('.json')]
        kb = InlineKeyboardBuilder()
        for file in files:
            data = load_file(file)
            kb.add(InlineKeyboardButton(text=data.get('title'), callback_data=f'test_{data.get('test_id')}'))
        await message.answer('Натисність на кнопку з назвою потрібного тесту, щоб розпочати підготовку до запуску', reply_markup=kb.adjust(1).as_markup())
    else:
        await message.answer('У вас немає прав для цієї команди')

# Хендлер для команди /join
@dispatcher.message(Command('join'))
async def join_hendler(message: Message):
    students[message.from_user.id] = {
        'state': 'entering_code',
        'attempts': 3
    }
    await message.answer('Введіть код підключення до тесту')

# Хендлер, який реагує на стан студента - entering_code 
@dispatcher.message(StudentStateFilter('entering_code'))
async def entering_code_handler(message: Message):
    if message.text in active_tests:
        students[message.from_user.id] = {
            'state': 'entering_name',
            'code': message.text
        } 
        await message.answer("Код правильний. Введіть ваше ім'я")
    else:
        students[message.from_user.id]['attempts'] -= 1
        attempts = students[message.from_user.id]['attempts']
        if attempts > 0:
            await message.answer(f"Код неправильний, введіть ще раз (кількість спроб: {attempts})") 
        else:
            await message.answer("У вас більше немає спроб!")
            students[message.from_user.id]['state'] = 'wrong_code' 
            
# Хендлер, який реагує на стан студента - entering_name 
@dispatcher.message(StudentStateFilter('entering_name'))
async def entering_name_handler(message: Message):
    student_name = message.text
    id = message.from_user.id
    code = students[id]['code']
    students[id]['state'] = 'joined'
    students[id]['name'] = student_name
    active_tests[code]['connected_students'].append(student_name)
    admin_msg, kb = get_test_start_msg(code)
    print(active_tests)
    await bot.edit_message_text(
        chat_id=active_tests[code]['admin_id'], message_id=active_tests[code]['message_id'], 
        text=admin_msg, reply_markup=kb)
    await message.answer(f"Вас доєднано до тесту \'{active_tests[code]['test']}\', чекайте, коли адміністратор запустить його")

# Хендлер для натискання кнопок вибору тесту
@dispatcher.callback_query(F.data.startswith('test_'))
async def callback_test_handler(callback: CallbackQuery):
    if isAdmin(callback):
        connect_code = generate_unique_code()
        data = load_file(f'{callback.data[5:]}.json')
        title = data.get('title')
        test_id = data.get('test_id')
        active_tests[connect_code] = {
            'test': title,
            'test_id': test_id,
            'admin_id': callback.from_user.id,
            'connected_students': []
        }
        admin_msg, kb = get_test_start_msg(connect_code)
        await callback.answer('')
        msg = await callback.message.answer(admin_msg, reply_markup=kb)
        active_tests[connect_code]['message_id'] = msg.message_id
        print(active_tests)
    else: 
        await callback.message.answer('У вас немає прав для цієї команди')

