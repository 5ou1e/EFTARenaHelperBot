import asyncio
import ssl

from loader import executor, set_my_commands
import handlers

from checker import checker

async def on_startup(_) -> None:
    await set_my_commands(bot = executor.dispatcher.bot)
    asyncio.ensure_future(checker.loop())

async def on_shutdown(_) -> None:
    pass

if __name__ == '__main__':
    executor.on_startup(on_startup)
    executor.on_shutdown(on_shutdown)

    executor.start_polling()
