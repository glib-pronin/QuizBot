import aiogram

# Створюємо об'єкт класу Bot
bot = aiogram.Bot('')
# Створюємо об'єкт класу Dispatcher
dispatcher = aiogram.Dispatcher()   


# Словник з активними тестами та службовою інформацією про них
""" Структура словника active_tests
active_tests = {
    "code": {
        "test": Назва тесту,
        "test_id": Назва файлу,
        "admin_id": ID адміна,
        "message_id": ID повідомлення для оновлення списку приєднаних студентів,
        "admin_msg": ID повідомлення для керуванням тестом,
        "questions": [...],
        "current_question": Номер питання,
        "connected_students": {
            ID студента: {
                "name": "Ім'я",
                "message_id": ID повідомлення з питанням,
                "answered": False/True,
                "msg_ids_to_delete": []
                "answers": {
                    "question_index": answer
                    ... 
                }
            },
            ...
        }
    },
    ...
}"""
active_tests = {}

