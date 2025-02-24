import datetime
from .models import Image, User, Log, Theme
from sqlalchemy.sql.expression import func
from .db import get_session
from config.config import HELP_TEXT, THEMES_IDS, START_MESSAGE
from .templates import generate_message
import random


def start_command(message, bot):
    bot.send_message(message.chat.id, START_MESSAGE)
    log_event(message.chat.id, 0, "start_command")

def help_command(message, bot):
    bot.send_message(message.chat.id, HELP_TEXT)
    log_event(message.chat.id, 0, "help_command")

def message_command(message, bot, theme):
    session = get_session()
    text_message = generate_message(THEMES_IDS[theme])

    # Логирование
    log_event(message.chat.id, THEMES_IDS.get(theme), "message_command")

    if theme in ["compliment", "meme"]:
        if random.choice([True, False]):
            image = session.query(Image.image_url).filter_by(theme_id=THEMES_IDS[theme]).order_by(func.random()).first()
            if image:
                bot.send_photo(message.chat.id, image.image_url)
            else:
                bot.send_message(message.chat.id, text_message)
        else:
            bot.send_message(message.chat.id, text_message)

    elif theme == "food":
        bot.send_message(message.chat.id, text_message)  # Только текст

    session.close()

def log_event(dialog_id, theme_id, command):
    """ Функция для записи лога в таблицу Logs """
    session = get_session()
    log = Log(dialog_id=dialog_id, theme_id=theme_id, send_time=datetime.datetime.utcnow())
    session.add(log)
    session.commit()

def acquaintance_command(chat_id, bot):
    user_info = {}
    user_info['chat_id'] = chat_id
    msg = bot.send_message(chat_id, 'Как я могу к тебе обращаться?(* ^ ω ^)')
    bot.register_next_step_handler(msg, wake_up_step, user_info, bot)
    log_event(chat_id, 6, "acquaintance_command")

def wake_up_step(message, user_info, bot):
    user_info['name'] = message.text
    msg = bot.send_message(message.chat.id,
                           'Во сколько ты обычно встаешь? Укажи время в формате XX:XX по мск, чтобы я могла запомнить')
    bot.register_next_step_handler(msg, sleep_step, user_info, bot)

def sleep_step(message, user_info, bot):
    try:
        user_info['wake_up_time'] = datetime.datetime.strptime(message.text, "%H:%M").time()
        msg = bot.send_message(message.chat.id,
                               'Во сколько ты обычно ложишься спать? Укажи время в формате XX:XX по мск, чтобы я могла запомнить')
        bot.register_next_step_handler(msg, fix_step, user_info, bot)
    except ValueError:
        bot.send_message(message.chat.id, "Ошибка! Время должно быть в формате XX:XX. Попробуй снова с командой /acquaintance.")
        return

def fix_step(message, user_info, bot):
    session = get_session()
    try:
        user_info['sleep_time'] = datetime.datetime.strptime(message.text, "%H:%M").time()
        user_info['username'] = bot.get_chat_member(user_info['chat_id'], user_info['chat_id']).user.username
        user = session.query(User).filter(User.dialog_id == user_info['chat_id']).first()

        if user:
            user.user_name = user_info['name']
            user.wake_up_time= user_info['wake_up_time']
            user.sleep_time = user_info['sleep_time']
            user.tg_nickname = user_info['username']
        else:
            user = User(
                dialog_id=user_info['chat_id'],
                tg_nickname=user_info['username'],
                user_name=user_info['name'],
                wake_up_time=user_info['wake_up_time'],
                sleep_time=user_info['sleep_time']
            )
            session.add(user)

        session.commit()
        bot.send_message(message.chat.id,
                         f'Ура! {user_info["name"]}, твои данные записаны (*¯︶¯*)')


    except ValueError:
        bot.send_message(message.chat.id, "Ошибка! Время должно быть в формате XX:XX. Попробуй снова с командой /acquaintance.")
        return
    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка, попробуйте позже")
        return

def good_morning(chat_id, bot):
    emoji_morning = ['💌', '💘', '💝', '💖', '💗', '💓', '💞', '💕', '❣', '🧡', '💛', '💚', '💙', '💜', '🤎', '🖤', '🤍', '🫶', '🐱', '🐇',
                     '🐰', '🐞']
    session = get_session()
    theme = 'morning'
    text_message = "Доброе утро" + emoji_morning[random.randint(0, len(emoji_morning) - 1)] + '\n' +generate_message(THEMES_IDS[theme])

    # Логирование
    log_event(chat_id, THEMES_IDS.get(theme), "schedule_command")
    image = session.query(Image.image_url).filter_by(theme_id=THEMES_IDS[theme]).order_by(func.random()).first()
    if image:
        bot.send_photo(chat_id, image.image_url, caption=text_message)
    else:
        bot.send_message(chat_id, text_message)

def good_night(chat_id, bot):
    emoji_night = ['💌', '💘', '💝', '💖', '💗', '💓', '💞', '💕', '❣', '🧡', '💛', '💚', '💙', '💜', '🤎', '♥', '🤍', '🌌', '🐱', '🌛',
                   '🌆',
                   '💤', '🐾']
    session = get_session()
    theme = 'night'
    text_message = "Доброй ночи" + emoji_night[random.randint(0, len(emoji_night) - 1)] + '\n' +generate_message(THEMES_IDS[theme])

    # Логирование
    log_event(chat_id, THEMES_IDS.get(theme), "schedule_command")
    image = session.query(Image.image_url).filter_by(theme_id=THEMES_IDS[theme]).order_by(func.random()).first()
    if image:
        bot.send_photo(chat_id, image.image_url, caption=text_message)
    else:
        bot.send_message(chat_id, text_message)

def job(bot):
    time = datetime.datetime.now()
    current_time = time.strftime("%H:%M")
    session = get_session()

    users = session.query(User).all()
    for user in users:
        if current_time == user.wake_up_time.strftime("%H:%M"):
            good_morning(user.dialog_id, bot)

        if current_time == user.sleep_time.strftime("%H:%M"):
            good_night(user.dialog_id, bot)

    session.close()

