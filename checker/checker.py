import asyncio
from loader import bot
import os
from dateutil import parser as date_parser
from datetime import datetime, timedelta
import pytz

from loader import Config

async def loop(delay = 1):
    while True:
        if Config.is_active:
            await check()
        await asyncio.sleep(1)

async def check():
    try:
        latest_logs = await find_latest_logs()
        print(latest_logs)
        if not latest_logs:
            return
        latest_match_id, latest_match_date, map, game_mode, ranking_mode, players, players_count_max, players_count_confirmed = await find_latest_match_id(latest_logs)
        if (latest_match_id and latest_match_date >= Config.check_started_time
            and not (pytz.timezone('Europe/Moscow').localize(datetime.now()) - latest_match_date).total_seconds() >= 25):
            message = f"<b>Матч найден!</b>\n——————————————\n<b>Карта:</b> {map}\n<b>Режим:</b> {game_mode} ({ranking_mode})\n"
            if not latest_match_id == Config.latest_match_id:
                latest_match_id == Config.latest_match_id
                Config.latest_match_id = latest_match_id
                Config.checker_last_sent_message = await bot.send_message(int(Config.get('Settings', 'admin_id', fallback=0)), message)
            else:
                message += f'<b>Игроки ({players_count_confirmed}/{players_count_max}):</b> '
                for player in players:
                    message += f'\n ● {player}'
                if Config.checker_last_sent_message:
                    await bot.edit_message_text(message, chat_id=int(Config.get('Settings', 'admin_id', fallback=0)), message_id=Config.checker_last_sent_message.message_id)
                else:
                    await bot.send_message(int(Config.get('Settings', 'admin_id', fallback=0)), message)

    except Exception as e:
        print(e)


async def find_latest_logs():
    # Получаем список всех элементов в директории
    directory = Config.get('Settings', 'eft_path', fallback = '') + '\Logs'
    folders = [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]

    # Если папок нет, возвращаем None
    if not folders:
        return None

    # Находим папку с самой поздней датой создания
    latest_folder = max(folders, key=lambda f: os.path.getctime(os.path.join(directory, f)))

    file_name = f"{latest_folder.removeprefix('log_')} web_socket.log"
    latest_logs = os.path.join(directory, latest_folder, file_name)

    if os.path.exists(latest_logs):
        return latest_logs
    else:
        return None


async def find_latest_match_id(latest_logs):
    with open(latest_logs, 'r') as file:
        lines = file.readlines()
        match_id = None
        for line in reversed(lines):
            if 'request-to-confirm-match' in line:
                date_string = line.split('|')[0]
                date = date_parser.parse(date_string)
                match_id = line.split('"matchId":"')[-1].split('"')[0]
                _map = line.split('"location":"')[-1].split('"')[0]
                map = _map.replace('Arena', '').replace('_', '')
                game_mode = line.split('"gameMode":"')[-1].split('"')[0]
                ranking_mode = line.split('"rankingMode":"')[-1].split('"')[0]
                players_count_max = line.split('"playersCount":')[-1].split(',')[0]
                players = []
                players_count_confirmed = 0
                break
        print(match_id)
        if match_id:
            for line in reversed(lines):
                if ('player-confirmed-notification' in line) and (match_id in line):
                    player = line.split('"nickname":"')[-1].split('"')[0]
                    players.append(player)
                    players_count_confirmed += 1
            players.reverse()
            print(players)
            return match_id, date, map, game_mode, ranking_mode, players, players_count_max, players_count_confirmed
    return None, None, None, None, None, None, None, None
