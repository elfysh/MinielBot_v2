from pathlib import Path

api = '7699583281:AAF3eUJtspro9PnezHFempmKgEAgGnA7U2U'
BASE_DIR = Path(__file__).resolve().parent.parent
DATABASE_URL = f"sqlite:///{BASE_DIR}/db/miniel.db"
HELP_TEXT = 'инструкция'
START_MESSAGE = 'старт'

THEMES_IDS = {
    'morning':1,#morning
    'night':2,#night
    'compliment':3,#compliment
    'food':4,#food
    'meme':5#meme
}

THEME_URLS_TEXT = {
    '1':'https://disk.yandex.ru/d/27yDTU3iCjs7yA',#morning
    '2':'https://disk.yandex.ru/d/DAIH1GXp4FkTUw',#night
    '3':'https://disk.yandex.ru/d/-pYAxxlEruTg9Q',#compliment
    '4':'https://disk.yandex.ru/d/m1vSDyTenZf-sQ',#food
    '5':'https://disk.yandex.ru/d/iAmqrUeuAq4QIg'#meme
}

