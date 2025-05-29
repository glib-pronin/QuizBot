import aiogram

# Створюємо об'єкт класу Bot
bot = aiogram.Bot('')
# Створюємо об'єкт класу Dispatcher
dispatcher = aiogram.Dispatcher()   

# Словник з активними тестами та службовою інформацією про них
active_tests = {}
# Словник з студентами, які підключаються до тесту
students = {}