from .settings import active_tests
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import json, random

# Функція, яка створює інформаційний рядок для створонего тесту, а такаож inline-кнопку
def get_test_start_msg(code: str):
    title = active_tests.get(code).get("test")
    test_id = active_tests.get(code).get("test_id")
    students = active_tests.get(code).get("connected_students")
    connected_students = '\n'.join(students)
    test_start_msg = f'Тест: {title}\n\nКод підключення: {code}\n\nСписок підключених студентів:\n{connected_students}'
    kb = InlineKeyboardMarkup(inline_keyboard=[[InlineKeyboardButton(text='Розпочати тест', callback_data=f'start_{test_id}')]])
    return test_start_msg, kb

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
