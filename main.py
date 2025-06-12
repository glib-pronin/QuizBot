from modules import dispatcher, bot, all_routers
from modules.utils import generate_unique_code
import aiogram



for router in all_routers:
    dispatcher.include_router(router)

async def main():
    await dispatcher.start_polling(bot)

try:
    aiogram._asyncio.run(main())
except KeyboardInterrupt:
    print("Бот завершив роботу!")