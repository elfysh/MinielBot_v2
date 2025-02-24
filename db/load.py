import requests
from config.config import THEME_URLS_TEXT
from bot.db import get_session
from bot.models import  TextTemplate
from extract import get_folder_files


def load_phrases():
    session = get_session()

    for theme, folder_url in THEME_URLS_TEXT.items():
        theme_id = int(theme)
        phrases = get_folder_files(folder_url)
        for phrase_name, phrase_url in phrases.items():
            response = requests.get(phrase_url)
            response.encoding = 'utf-8'

            if response.status_code == 200:
                phrases_list = response.text.splitlines()

                for phrase in phrases_list:
                    phrase = phrase.replace('.',' ').strip()
                    existing_phrases = {phrase_obj.message_text for phrase_obj in
                                        session.query(TextTemplate.message_text).filter_by(theme_id=theme_id).all()}
                    if phrase not in existing_phrases:
                        phrase_obj = TextTemplate(theme_id=theme_id, message_text=phrase)
                        session.add(phrase_obj)

    session.commit()
    session.close()

