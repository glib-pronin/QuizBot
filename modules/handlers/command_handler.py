from ..permission import isAdmin
from ..filter import ShowResults
from ..db import Session, Student, Result
from aiogram import Router
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart, Command
from aiogram.utils.keyboard import InlineKeyboardBuilder

router_command = Router()

# Хендлер для команди /start
@router_command.message(CommandStart())
async def start_handler(message: Message):
    if isAdmin(message):
        await message.answer(f'Привіт, адміне {message.from_user.full_name}!\nЗа допомогою цього боту ти зможеш проводити тестування для твоїх учнів, щоб перевірити їхній рівень знань із різних тем!\nЩоб обрати тест, скористайтеся командою: /showquizzes')
    else:
        await message.answer(f'Привіт, {message.from_user.full_name}!\nЗа допомогою цього боту ти зможеш проходити тести на різні теми, щоб перевірити свої знання!\nЩоб приєднатися до тесту, скористайся командою: /join')

# Хендлер для команди /results
@router_command.message(Command('results'))
async def results_handler(message: Message):
    with Session() as session:
        student = session.query(Student).filter_by(telegram_id = message.from_user.id).first()
        if not student:
            await message.answer(text="На жаль, у нас немає ваших результатів, можливо, Ви ще не проходили жодного тесту.")
            return
        results = session.query(Result).filter_by(student_id=student.id).all()
    if not results:
        await message.answer(text="На жаль, у нас немає ваших результатів, можливо, Ви ще не проходили жодного тесту.")
        return
    kb = InlineKeyboardBuilder()
    for result in results:
        kb.button(text=f"{result.test_name} - {result.end_time}", callback_data=ShowResults(id=result.id).pack())
    await message.answer(
        text="Ось ваші тести з датами проходження. Натисніть на будь-який, щоб переглянути детальний аналіз.", 
        reply_markup=kb.adjust(1).as_markup())

# Хендлер для натискання кнопки, яка показуватиме аналіз пройденного тесту
@router_command.callback_query(ShowResults.filter())
async def show_result_handler(callback: CallbackQuery, callback_data: ShowResults):
    with Session() as session:
        result = session.query(Result).filter_by(id = callback_data.id).first()
    await callback.answer()
    await callback.message.answer(text=f"<b>Тест:</b> {result.test_name}\n\n<b>Дата та час:</b> {result.end_time}\n\n<b>Результат:</b> {result.grade}\n\n<b>Чи був перерваний:</b> {'Так' if result.interrupted else 'Ні'}\n\n<b>Ваші ім'я, під яким проходили тест:</b> {result.student_name}\n\n<b>Аналіз відповідей:</b>\n{result.answers}", parse_mode="HTML")