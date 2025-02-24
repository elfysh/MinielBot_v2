from config.config import api
from apscheduler.schedulers.blocking import BlockingScheduler
from bot.views import start_command, help_command, message_command,acquaintance_command, job
import telebot
import threading

bot = telebot.TeleBot(api)

@bot.message_handler(commands=['start'])
def start(message):
    start_command(message, bot)

@bot.message_handler(commands=['help'])
def help(message):
    help_command(message, bot)

@bot.message_handler(commands=['compliment'])
def compliment(message):
    message_command(message, bot, 'compliment')

@bot.message_handler(commands=['meme'])
def meme(message):
    message_command(message, bot, 'meme')

@bot.message_handler(commands=['food'])
def food(message):
    message_command(message, bot, 'food')

@bot.message_handler(commands=['acquaintance'])
def acquaintance(message):
    acquaintance_command(message.chat.id, bot)


if __name__ == "__main__":
    proc_bot = threading.Thread(target=bot.infinity_polling)
    proc_bot.start()

    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'interval', minutes=1, kwargs={'bot': bot})
    scheduler.start()
