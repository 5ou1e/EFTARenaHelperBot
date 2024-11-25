from configparser import ConfigParser
import os
from datetime import datetime
import pytz


class Config():

    config_path = "config.ini"
    configparser = ConfigParser(allow_no_value = True)
    configparser.add_section('Settings')

    is_active = True # Статус чекера (True - Включен\ False - Отключен)
    check_started_time = pytz.timezone('Europe/Moscow').localize(datetime.now()) # Время запуска чекера
    latest_match_id = '' # Айди последнего найденного матча
    checker_last_sent_message = None # Последнее отправленное сообщение в телеграм о


    @staticmethod
    def load():
        if not os.path.exists(Config.config_path):
            with open(Config.config_path,"a+") as f:
                f.close()
        Config.configparser.read(Config.config_path)

    @staticmethod
    def get(section, name, fallback=None):

        Config.configparser.read(Config.config_path)
        try:
            result = Config.configparser.get(section, name, fallback=fallback)
            return result
        except:
            return False

    @staticmethod
    def set(section, name, value):
        Config.configparser.read(Config.config_path)
        Config.configparser.set(section, name, value)
        with open(Config.config_path, "w") as file:
            Config.configparser.write(file)



eft_logs_path = 'D:\Battlestate Games\EFT Arena' # Путь к папке с логами (С:\Battlestate Games\EFT Arena\Logs)
