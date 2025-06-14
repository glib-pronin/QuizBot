from .settings import active_tests, bot, dispatcher
from .filter import StartTest, NextQuestion, CompleteTest
from .db import Session, Student, Result
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.storage.base import StorageKey
from aiogram.fsm.context import FSMContext
from aiogram.utils.keyboard import InlineKeyboardBuilder
import json, random

# Функція, яка завантажує певний json-файл
def load_file(filename: str):
    with open(f'quizzes/{filename}', 'r', encoding='utf-8') as f:
        return json.load(f)

# Функція, яка генерує унікальний код доступуп до тесту
def generate_unique_code():
    while True:
        code = str(random.randint(1000, 9999))
        if not code in active_tests:
            return code
        
# Функція, яка створює інформаційний рядок для створонего тесту, а такаож inline-кнопку
async def get_test_start_msg(code: str):
    test_code = active_tests.get(code)
    if test_code:
        title = test_code.get("test")
        test_id = test_code.get("test_id")
        students = test_code.get("connected_students")
        connected_students = '\n'.join([students[id]['name'] for id in students])
        test_start_msg = f'Тест: {title}\n\nКод підключення: {code}\n\nСписок підключених студентів:\n{connected_students}'
        kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Розпочати тест', callback_data=StartTest(code=code, test_id=test_id).pack())]])
        return test_start_msg, kb

# Функція, яка результати проходження тесту до бд
async def add_student_result(student_id: int, test_name: str, student_name: str, answers: str, result: str, interrupted: bool ):
    with Session() as session:
        student = session.query(Student).filter_by(telegram_id = student_id).first()
        if not student:
            print(f"Помилка: Студента з telegram_id {student_id} не знайдено.")
            return
        result = Result(
            test_name = test_name, answers = answers, grade = result, 
            interrupted = interrupted, student_name = student_name, student = student)
        print(f'Результати студента з id {student_id} додано.')
        session.add(result)
        session.commit()

# Функція, яка показує адміну, хто вже відповів на питання, а хто ні
async def show_answered_student(code: int, question_index: int):
    student_answered = [student['name'] for student in active_tests[code]['connected_students'].values() if student['answered']==True]
    student_not_answered = [student['name'] for student in active_tests[code]['connected_students'].values() if student['answered']==False]
    kb = await get_admin_kb(code, question_index)
    await bot.edit_message_text(
        chat_id=active_tests[code]['admin_id'], message_id=active_tests[code]['admin_msg'], 
        text=f'{question_index+1}) {active_tests[code]['questions'][question_index]['question']}\n☑️Відповіли:\n{'\n'.join(student_answered)}\n\n🤔Не відповіли:\n{'\n'.join(student_not_answered)}',
        reply_markup=kb
        )

# Функція, яка повертає клавіатуру для адміну: з написом "Завершити тест", якщо питання останнє, інакше - "Наступне питання"
async def get_admin_kb(code: str, question_index: int):
    if question_index + 1 < len(active_tests[code]['questions']):
        return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Наступне питання", callback_data=NextQuestion(code=code).pack())]])
    return InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text="Завершити тест", callback_data=CompleteTest(code=code).pack())]])

# Функція, яка повертає клавіатуру з обробленими варіантами відповіді 
async def get_answers_kb(answers: list, selected_answer: str):
    student_kb = InlineKeyboardBuilder()
    for answer in answers:
        student_kb.button(text=f'🟡 {answer} - ваша відповідь' if answer.startswith(selected_answer) else answer, callback_data='double_answer')
    return student_kb.adjust(1).as_markup()

# Функція, яка очищає state, а також видаляє повідомлення (відповідь студента та коментар від бота)
async def clear_state_and_messaages(student_id: int, student: dict):
    context = FSMContext(storage=dispatcher.storage, key=StorageKey(bot_id=bot.id, chat_id=student_id, user_id=student_id))
    await context.clear()
    msg_ids_to_delete = student.get('msg_ids_to_delete')
    if msg_ids_to_delete:
        for msg_id in msg_ids_to_delete:
            await bot.delete_message(chat_id=student_id, message_id=msg_id)
        student['msg_ids_to_delete'].clear()

