import aiogram

# Створюємо об'єкт класу Bot
bot = aiogram.Bot('')
# Створюємо об'єкт класу Dispatcher
dispatcher = aiogram.Dispatcher()   

# Словник з активними тестами та службовою інформацією про них
active_tests = {}

router_join = aiogram.Router()
dispatcher.include_router(router=router_join)

router_command = aiogram.Router()
dispatcher.include_router(router=router_command)

router_start_test = aiogram.Router()
dispatcher.include_router(router=router_start_test)