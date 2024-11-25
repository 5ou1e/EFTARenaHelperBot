from aiogram import types
from aiogram import Dispatcher, Bot
from aiogram.utils.executor import Executor

from aiogram.dispatcher.filters import BoundFilter
from config import Config

Config.load()

async def set_my_commands(bot : Bot) -> None:
    await bot.set_my_commands(
        commands = [
            types.BotCommand(command = 'start', description = 'Запустить'),
            types.BotCommand(command = 'stop', description = 'Остановить'),
        ]
    )

class AdminFilter(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin):
        self.is_admin = is_admin

    async def check(self, obj):
        if isinstance(obj, types.message.Message):
            if str(obj.from_user.id) == Config.get('Settings', 'admin_id', fallback=None):
                return True
        elif isinstance(obj, types.callback_query.CallbackQuery):
            if str(obj.message.chat.id) == Config.get('Settings', 'admin_id', fallback=None):
                return True
        return False


bot = Bot(token = Config.get('Settings', 'bot_token', fallback=None), parse_mode = 'HTML')

dispatcher = Dispatcher(bot = bot,)

executor = Executor(dispatcher = dispatcher, skip_updates = False)

dispatcher.filters_factory.bind(AdminFilter)
