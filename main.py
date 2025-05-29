from modules import dispatcher, bot
import aiogram

async def main():
    await dispatcher.start_polling(bot)

try:
    aiogram._asyncio.run(main())
except KeyboardInterrupt:
    print("Бот завершив роботу!")