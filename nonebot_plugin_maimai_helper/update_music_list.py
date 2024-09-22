import json
import os

import requests
from nonebot.log import logger
from data import root_path


URL = "https://www.diving-fish.com/api/maimaidxprober/music_data"


def update_music_list():
    logger.success("开始更新music_list")
    logger.success("开始删除文件")
    if os.path.isfile(root_path + '/game_data/diving_music_list.json'):
        os.remove(root_path + '/game_data/diving_music_list.json')
    new_data = requests.get(URL)
    new_data.encoding = 'utf-8'
    data = json.loads(new_data.text)
    logger.success("开始更新文件")
    with open(root_path + '/game_data/diving_music_list.json', 'w', encoding='utf-8') as old_data:
        json.dump(data, old_data, ensure_ascii=False, indent=4)

