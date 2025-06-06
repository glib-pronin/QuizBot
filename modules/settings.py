import aiogram

# Створюємо об'єкт класу Bot
bot = aiogram.Bot('')
# Створюємо об'єкт класу Dispatcher
dispatcher = aiogram.Dispatcher()   

# Словник з активними тестами та службовою інформацією про них
""" Структура словника active_tests
active_tests = {
    "код_тесту": {
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

router_join = aiogram.Router()
dispatcher.include_router(router=router_join)

router_command = aiogram.Router()
dispatcher.include_router(router=router_command)

router_start_test = aiogram.Router()
dispatcher.include_router(router=router_start_test)

router_testing = aiogram.Router()
dispatcher.include_router(router=router_testing)