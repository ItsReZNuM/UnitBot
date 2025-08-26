
import telebot
import logging
from datetime import datetime
from pytz import timezone

import config
import database as db
from handlers import register_handlers

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8')
    ]
)
logger = logging.getLogger(__name__)

bot = telebot.TeleBot(config.TOKEN)

commands = [
    telebot.types.BotCommand("start", "شروع ربات"),
    telebot.types.BotCommand("help", "راهنمای استفاده از ربات")
]
bot.set_my_commands(commands)

bot_start_time = datetime.now(timezone('Asia/Tehran')).timestamp()

def main():
    logger.info("Bot is starting...")
    
    db.init_db()
    
    register_handlers(bot, bot_start_time)
    
    try:
        logger.info("Bot polling started.")
        bot.polling(none_stop=True)
    except Exception as e:
        logger.error(f"Error in bot polling: {str(e)}")
    finally:
        logger.info("Bot stopped.")

if __name__ == '__main__':
    main()