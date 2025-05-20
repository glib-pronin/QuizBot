from modules import *

async def main():
    await dispatcher.start_polling(bot)

aiogram._asyncio.run(main())