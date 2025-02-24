from sqlalchemy import func
from bot.models import TextTemplate, Theme
from bot.db import get_session

#генерация текстовых сообщений


def generate_message(theme_id):
    session = get_session()
    message = session.query(TextTemplate.message_text).filter_by(theme_id=int(theme_id)).order_by(func.random()).limit(
        1).scalar()
    session.close()
    return message if message else ''