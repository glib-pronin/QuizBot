from ..settings import dispatcher, active_tests, bot, router_join
from ..filter import TestConnection
from ..utils import get_test_start_msg
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

# Хендлер для команди /join
@router_join.message(Command('join'))
async def join_hendler(message: Message, state: FSMContext):
    await message.answer('Введіть код підключення до тесту')
    await state.set_state(TestConnection.code)
    await state.update_data(code=3)      


# Хендлер, який реагує на стан студента - code 
@router_join.message(TestConnection.code)
async def entering_code_handler(message: Message, state: FSMContext):
    if message.text in active_tests:
        await message.answer("Код правильний. Введіть ваше ім'я")
        await state.set_state(TestConnection.name)
        await state.update_data(code=message.text)
    else:
        data = await state.get_data()
        attempts = data.get('code')
        attempts -= 1
        await state.update_data(code=attempts)
        if attempts > 0:
            await message.answer(f"Код неправильний, введіть ще раз (кількість спроб: {attempts})") 
        else:
            await message.answer("У вас більше немає спроб!")
            await state.set_state(TestConnection.wrong_code)
            
# Хендлер, який реагує на стан студента - name 
@router_join.message(TestConnection.name)
async def entering_name_handler(message: Message, state: FSMContext):
    student_name = message.text
    id = message.from_user.id
    data = await state.get_data()
    code = data.get('code')
    await state.clear()
    active_tests[code]['connected_students'][id]={"name": student_name}
    admin_msg, kb = get_test_start_msg(code)
    print(active_tests)
    await bot.edit_message_text(
        chat_id=active_tests[code]['admin_id'], message_id=active_tests[code]['message_id'], 
        text=admin_msg, reply_markup=kb)
    await message.answer(f"Вас доєднано до тесту \'{active_tests[code]['test']}\', чекайте, коли адміністратор запустить його")
