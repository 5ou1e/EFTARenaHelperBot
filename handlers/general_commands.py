from aiogram import types
from aiogram.dispatcher import FSMContext

from loader import dispatcher, bot, Config

from datetime import datetime
import pytz


@dispatcher.message_handler(commands = ['start'], is_admin = True, state = '*')
async def process_start_command(message : types.Message, state : FSMContext) -> None:
    if Config.is_active == False:
        Config.is_active = True
        Config.check_started_time = pytz.timezone('Europe/Moscow').localize(datetime.now())
        await message.answer('Чекер запущен!')
    else:
        await message.answer('Чекер уже запущен!')


@dispatcher.message_handler(commands = ['stop'], is_admin = True, state = '*')
async def process_stop_command(message : types.Message, state : FSMContext) -> None:
    if Config.is_active == True:
        Config.is_active = False
        await message.answer('Чекер остановлен!')
    else:
        await message.answer('Чекер уже остановлен!')
