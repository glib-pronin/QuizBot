from ..settings import active_tests
from ..permission import isAdmin
from ..filter import ChooseTest
from ..utils import get_test_start_msg, load_file, generate_unique_code
from aiogram import Router
from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from aiogram.filters import Command
from aiogram.utils.keyboard import InlineKeyboardBuilder
import os

router_start_test = Router()

# Хендлер для команди /showquizzes (тільки для адмінів)
@router_start_test.message(Command('showquizzes'))
async def showquizzes_handler(message: Message):
    if isAdmin(message):
        files = [f for f in os.listdir('quizzes') if f.endswith('.json')]
        kb = InlineKeyboardBuilder()
        for file in files:
            data = load_file(file)
            cb_data = ChooseTest(test_id=data.get('test_id')).pack()
            kb.add(InlineKeyboardButton(text=data.get('title'), callback_data=cb_data)) 
        await message.answer('Натисність на кнопку з назвою потрібного тесту, щоб розпочати підготовку до запуску', reply_markup=kb.adjust(1).as_markup())
    else:
        await message.answer('У вас немає прав для цієї команди')

# Хендлер для натискання кнопок вибору тесту
@router_start_test.callback_query(ChooseTest.filter())
async def callback_test_handler(callback: CallbackQuery, callback_data: ChooseTest):
    if isAdmin(callback):
        connect_code = generate_unique_code()
        test_id = callback_data.test_id
        data = load_file(f'{test_id}.json')
        title = data.get('title')
        active_tests[connect_code] = {
            'test': title,
            'test_id': test_id,
            'admin_id': callback.from_user.id,
            'connected_students': {}
        }
        admin_msg, kb = get_test_start_msg(connect_code)
        await callback.answer('')
        msg = await callback.message.answer(admin_msg, reply_markup=kb)
        active_tests[connect_code]['message_id'] = msg.message_id
        print(active_tests)
    else: 
        await callback.message.answer('У вас немає прав для цієї команди')
