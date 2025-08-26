# main.py

import telebot
import logging
from datetime import datetime
from pytz import timezone

import config
import database as db
from handlers import register_handlers

# تنظیمات لاگ‌گیری
logging.basicConfig(
    level=logging.ERROR, # تغییر به INFO برای دیدن لاگ‌های بیشتر
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

# ایجاد نمونه ربات
bot = telebot.TeleBot(config.TOKEN)

# تنظیم دستورات ربات
commands = [
    telebot.types.BotCommand("start", "شروع ربات"),
    telebot.types.BotCommand("help", "راهنمای استفاده از ربات")
]
bot.set_my_commands(commands)

# زمان شروع به کار ربات
bot_start_time = datetime.now(timezone('Asia/Tehran')).timestamp()

def main():
    logger.info("Bot is starting...")
    
    # مقداردهی اولیه پایگاه داده
    db.init_db()
    
    # ثبت تمام هندلرها
    register_handlers(bot, bot_start_time)
    
    # شروع polling
    try:
        logger.info("Bot polling started.")
        bot.polling(none_stop=True)
    except Exception as e:
        logger.error(f"Error in bot polling: {str(e)}")
    finally:
        logger.info("Bot stopped.")

if __name__ == '__main__':
    main()