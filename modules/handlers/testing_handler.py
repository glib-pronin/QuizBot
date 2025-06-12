from ..settings import  active_tests, bot
from ..filter import StartTest, TestAnswer, NextQuestion, CompleteTest
from ..utils import load_file
from ..permission import isAdmin
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from aiogram.filters import Command
from aiogram import F, Router
from aiogram.utils.keyboard import InlineKeyboardBuilder

router_testing = Router()

# Хендлер для натискання кнопки початку тесту
@router_testing.callback_query(StartTest.filter())
async def start_test_handler(callback: CallbackQuery, callback_data: StartTest):
    if not callback_data.code in active_tests: # Перевіряємо, чи є тест з таким кодом
        await callback.answer('Цей тест вже завершено, розпочніть новий!', show_alert=True)
        return
    
    if not active_tests[callback_data.code]['connected_students']: # Перевіряємо, чи під'єдналися до тесту студенти
        await callback.answer('Ви не можете запустити тест без доєднаних студентів!', show_alert=True)
        return
    
    if isAdmin(callback):
        data = load_file(f'{callback_data.test_id}.json')
        active_tests[callback_data.code]['current_question'] = 0
        active_tests[callback_data.code]['questions'] = data.get('questions')

        for student in active_tests[callback_data.code]['connected_students'].values():
            student['answered'] = False
            student['answers'] = {}
        await callback.answer(f'Тест розпочато')
        await send_question(callback_data.code, active_tests[callback_data.code]['current_question'])
    else:
        await callback.message.answer('У вас немає прав для цієї команди')

# Хендлер для натискання кнопки з варіантом відповіді
@router_testing.callback_query(TestAnswer.filter())
async def answer_handler(callback: CallbackQuery, callback_data: TestAnswer):
    # Записуємо обрану відповідь
    code = callback_data.code
    index = callback_data.index # Індекс відповіді
    question_index = active_tests[code]['current_question']
    answer = active_tests[code]['questions'][question_index]['answers'][index]
    active_tests[code]['connected_students'][callback.from_user.id]['answers'][question_index] = answer
    # Оновлюємо стан студента
    active_tests[code]['connected_students'][callback.from_user.id]['answered'] = True
    await callback.answer('Ваша відповідь прийнята')
    # Блокуємо кнопки відповіді
    await bot.edit_message_text(
        chat_id=callback.from_user.id, message_id=active_tests[code]['connected_students'][callback.from_user.id]['message_id'], 
        text=f'{question_index+1}) {active_tests[code]['questions'][question_index]['question']}', 
        reply_markup=await get_answers_kb(answers=active_tests[code]['questions'][question_index]['answers'], selected_answer=callback_data.letter))
    # Повідомляємо адміна, що студент відповів
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

# Хендлер для повторного вибору варіанту - повідомляє, що така дія не можлива
@router_testing.callback_query(F.data == 'double_answer')
async def double_answer_handler(callback: CallbackQuery):
    await callback.answer("Ви вже відповіли на це питання, відповідь змінити не можна!", show_alert=True)

# Хендлер для натискання кнопки наступного питання
@router_testing.callback_query(NextQuestion.filter())
async def next_question_handler(callback: CallbackQuery, callback_data: NextQuestion):
    if isAdmin(callback):
        code = callback_data.code
        for student in active_tests[code]['connected_students'].values():
            student['answered'] = False
        active_tests[code]['current_question'] += 1
        await callback.answer(f'Наступне питання')
        await send_question(code=code, question_index=active_tests[code]['current_question'])
    else:
        await callback.message.answer('У вас немає прав для цієї команди')

# Функція відправки питання студенту
async def send_question(code: str, question_index: int):
    question_data = active_tests[code]['questions'][question_index]
    question = question_data['question']
    student_kb = InlineKeyboardBuilder()
    ind = 0
    for answer in question_data['answers']:
        student_kb.button(text=answer, callback_data=TestAnswer(code=code, index=ind, letter=answer[:1]).pack())
        ind += 1
    students_names = [student['name'] for student in active_tests[code]['connected_students'].values()]
    admin_text = f'{question_index+1}) {question}\n☑️Відповіли:\n\n🤔Не відповіли:\n{'\n'.join(students_names)}'
    # Випадок, якщо питання перше (потрібно зберегти айді повідомлень)
    if question_index == 0:
        for id, student in active_tests[code]['connected_students'].items(): 
            msg = await bot.send_message(chat_id=id, text=f'{question_index+1}) {question}', reply_markup=student_kb.adjust(1).as_markup())
            student['message_id'] = msg.message_id
        admin_msg = await bot.send_message(chat_id=active_tests[code]['admin_id'], text=admin_text, reply_markup=await get_admin_kb(code=code, question_index=question_index))
        active_tests[code]['admin_msg'] = admin_msg.message_id
        return
    # Випадок, якщо питання не є першим
    for id, student in active_tests[code]['connected_students'].items():
        await bot.edit_message_text(chat_id=id, message_id=student['message_id'], text=f'{question_index+1}) {question}', reply_markup=student_kb.adjust(1).as_markup())
    await bot.edit_message_text(
        chat_id=active_tests[code]['admin_id'], message_id=active_tests[code]['admin_msg'], text=admin_text,
        reply_markup=await get_admin_kb(code=code, question_index=question_index)
        )

# Хендлер для натискання кнопки завершити тест
@router_testing.callback_query(CompleteTest.filter())
async def complete_test_handler(callback: CallbackQuery, callback_data: CompleteTest):
    if isAdmin(callback):
        code = callback_data.code
        await finish_test(code)
    else: 
        await callback.message.answer('У вас немає прав для цієї команди')

# Хендлер для примусового завершення тесту за допомогою команди /stop
@router_testing.message(Command('stop'))
async def stop_tests_handler(message: Message):
    if isAdmin(message):
        codes = [code for code in active_tests if active_tests[code]['admin_id']==message.from_user.id]
        if len(codes) == 0:
            await message.answer('У вас немає активних тестів!')
            return
        for code in codes:
           await finish_test(code, forced=True)
    else: 
        await message.answer('У вас немає прав для цієї команди')
# Функція для завершення тесту (також враховує варіант передчасного завершення)
async def finish_test(code: str, forced: bool = False):
    questions = active_tests[code].get('questions')
    # Перевіряємо, чи розпочався тест з цим кодом
    if not questions:
        await bot.send_message(
            chat_id=active_tests[code]['admin_id'], 
            text=f"❗️ Тест із кодом <b>{code}</b> було скасовано — він ще не розпочався.", parse_mode='HTML')
        for id in active_tests[code]['connected_students']:
            await bot.send_message(chat_id=id, text=f"❗️ Тест '{active_tests[code]['test']}' було скасовано адміністратором, він ще не встиг розпочатися.")
        del active_tests[code]
        return
    students = active_tests[code]['connected_students']
    current_question = active_tests[code]['current_question']
    total_questions = len(questions)
    student_results = []
    student_results_percentage = []
    # Перевіряємо відповіді кожного студента
    for id, student in students.items():
        score = 0
        student_answers = student['answers']
        answers_analysis = []
        ind = 0
        for question in questions:
            if forced and ind > current_question:
                break 
            correct_answer = question['correct_answer']
            student_answer = student_answers.get(ind)
            # Якщо відповіді збігаються
            if student_answer == correct_answer:
                score += 1
                answers_analysis.append(f'\n{ind+1} {question['question']}\n✅ {student_answer} - ваша відповідь')
            # Якщо студент не надав відповіді
            elif not student_answer:
                answers_analysis.append(f'\n{ind+1} {question['question']}\n❌ Ви не відповіли на це питання\n✅ Правильна відповідь: {correct_answer}')
            # Якщо відповідь не правильна
            else:
                answers_analysis.append(f'\n{ind+1} {question['question']}\n❌ {student_answer} - ваша відповідь\n✅ Правильна відповідь: {correct_answer}')
            ind += 1
        # Формуємо повідомлення студенту та відправляємо
        score_str = f'{score}/{current_question+1 if forced else total_questions}'
        await bot.edit_message_text(
            chat_id=id, message_id=student['message_id'], 
            text=f"{'❗️Тест було достроково завершено адміністратором.' if forced else 'Тест завершено!🎉'}\n\nВаш результат: {score_str}\n\nАналіз відповідей:\n{'\n'.join(answers_analysis)}")
        student_results.append(f'🟢 {student['name']} - {score_str}')
        student_results_percentage.append(round(score / (current_question if forced else total_questions) * 100, 2))
    # Відправляємо повідомлення адміну зі статистикою та результатами кожного студента 
    average_score = round(sum(student_results_percentage)/len(student_results_percentage), 2)
    await bot.edit_message_text(
        chat_id=active_tests[code]['admin_id'], message_id=active_tests[code]['admin_msg'],
        text=f"{'❗️Тест із кодом ' + code + ' було достроково завершено.'if forced else 'Тест завершено!🎉'}\n\nСередній бал: {average_score}%\n\nрезультати студентів:\n{'\n'.join(student_results)}"
    )
    del active_tests[code] # Видаляємо інформацію про тест

