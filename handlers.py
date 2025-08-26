
import logging
from time import sleep

import telebot
from telebot import types
from telebot.types import InlineQueryResultArticle, InputTextMessageContent

import database as db
import conversion as conv
import utils
from config import ADMIN_USER_IDS

logger = logging.getLogger(__name__)

def register_handlers(bot, bot_start_time):
    @bot.message_handler(commands=['start'])
    def handle_start(message):
        if not utils.is_message_valid(message, bot_start_time):
            return
        
        user_id = message.from_user.id
        username = message.from_user.username
        first_name = message.from_user.first_name
        
        allowed, error_message = utils.check_rate_limit(user_id)
        if not allowed:
            bot.send_message(user_id, error_message)
            return
            
        if user_id not in ADMIN_USER_IDS:
            db.add_user(user_id, username, first_name)

        welcome_message = """🌟 *به UnitBot خوش آمدید!* 🌟
با @RezUnitBot به‌راحتی واحدها را تبدیل کنید! 🚀
کافیه توی هر چت بنویسید 
                 `@RezUnitBot 10 km` 
                 تا مقدار به همه واحدها در دسته طول تبدیل بشه.
برای راهنمای کامل، از /help استفاده کنید 📚

🌟 *Welcome to UnitBot!* 🌟
Convert units easily with @RezUnitBot! 🚀
Type something like `@RezUnitBot 10 km` to convert kilometers to all length units.
For a full guide, use /help 📚"""
        
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)

        if user_id in ADMIN_USER_IDS:
            btn_special = types.KeyboardButton("پیام همگانی 📢")
            markup.add(btn_special)
        
        bot.send_message(message.chat.id, welcome_message, parse_mode="Markdown", reply_markup=markup)

    @bot.message_handler(commands=['help'])
    def handle_help(message):
        if not utils.is_message_valid(message, bot_start_time):
            return
        
        user_id = message.from_user.id
        allowed, error_message = utils.check_rate_limit(user_id)
        if not allowed:
            bot.send_message(user_id, error_message)
            return
        
        help_message = """📚 *راهنمای UnitBot* 📚

🔧 *نحوه استفاده*:
توی هر چت بنویسید `@RezUnitBot <عدد> <واحد>` تا مقدار به همه واحدها در دسته مربوطه تبدیل بشه. مثال: 
`@RezUnitBot 10 km`
 یا 
 `@RezUnitBot 10 kilometer`.

✨ *ویژگی‌ها*:
- پشتیبانی از نام کامل واحدها (مثل `kilometer`) و مخفف‌ها (مثل `km`).
- حساس نبودن به حروف بزرگ و کوچک (مثل `KM`, `km`, `KiLoMeTeR`).
- پشتیبانی از اعداد فارسی (مثل ۱۰ یا ۵.۵).
- اعداد بزرگ با کاما جدا می‌شن (مثل 10,000)، اعداد کوچک تا ۶ رقم اعشار برای مقادیر خیلی کوچک و ۲ رقم اعشار برای بقیه (مثل 0.000006 یا 6.21).

📏 *واحدهای پشتیبانی‌شده*:
- *طول* 📏: millimeter (mm), centimeter (cm), meter (m), kilometer (km), decimeter (dm), inch (in), foot (ft), yard (yd), mile (mi)
- *وزن* ⚖️: milligram (mg), gram (g), kilogram (kg), ton (t), pound (lb)
- *مساحت* 🏞️: centimeter square (cm2), meter square (m2), hectare (ha), inch square (in2), foot square (ft2), acre
- *حجم* 🧴: milliliter (ml), centimeter cubic (cm3), cc (cc), liter (l), meter cubic (m3), gallon (gal), barrel (bbl)
- *زمان* ⏱️: second (s), minute (min), hour (h), day (d), week (wk), month (mo), year (yr)
- *دما* 🌡️: celsius (C), fahrenheit (F), kelvin (K)
- *سرعت* 🚀: meter per second (m/s), kilometer per hour (km/h), mile per hour (mph), mach
- *انرژی* ⚡️: joule (J), kilojoule (kJ), megajoule (MJ), watt hour (Wh), kilowatt hour (kWh), calorie (cal), kilocalorie (kcal)
- *فشار* 🌬️: pascal (Pa), kilopascal (kPa), atmosphere (atm), bar, millimeter mercury (mmHg)
- *زاویه* 📐: degree (deg), radian (rad), gradian (grad)
- *دیتا* 💾: byte (B), kilobyte (KB), megabyte (MB), gigabyte (GB), terabyte (TB), petabyte (PB), exabyte (EB)

📝 *مثال‌ها*:
- `@RezUnitBot 10 km` → تبدیل ۱۰ کیلومتر به همه واحدهای طول.
- `@RezUnitBot 5 kg` → تبدیل ۵ کیلوگرم به همه واحدهای وزن.
- `@RezUnitBot 100 C` → تبدیل ۱۰۰ سلسیوس به فارنهایت و کلوین.

🚀 *حالا با `@RezUnitBot 10 km` شروع کنید! تبدیل لذت‌بخش!* 🎉

📚 *UnitBot Help Guide* 📚

🔧 *How to Use*:
Type `@RezUnitBot <number> <unit>` in any chat to convert a value to all units in its category. Example: `@RezUnitBot 10 km` or `@RezUnitBot 10 kilometer`.

✨ *Features*:
- Supports both full unit names (e.g., `kilometer`) and abbreviations (e.g., `km`).
- Case-insensitive (e.g., `KM`, `km`, `KiLoMeTeR` all work).
- Persian numbers (e.g., ۱۰ or ۵.۵) are supported.
- Large numbers are formatted with commas (e.g., 10,000), small numbers up to 6 decimal places for very small values or 2 decimal places otherwise (e.g., 0.000006 or 6.21).

📏 *Supported Units*:
- *Length* 📏: millimeter (mm), centimeter (cm), meter (m), kilometer (km), decimeter (dm), inch (in), foot (ft), yard (yd), mile (mi)
- *Weight* ⚖️: milligram (mg), gram (g), kilogram (kg), ton (t), pound (lb)
- *Area* 🏞️: centimeter square (cm2), meter square (m2), hectare (ha), inch square (in2), foot square (ft2), acre
- *Volume* 🧴: milliliter (ml), centimeter cubic (cm3), cc (cc), liter (l), meter cubic (m3), gallon (gal), barrel (bbl)
- *Time* ⏱️: second (s), minute (min), hour (h), day (d), week (wk), month (mo), year (yr)
- *Temperature* 🌡️: celsius (C), fahrenheit (F), kelvin (K)
- *Speed* 🚀: meter per second (m/s), kilometer per hour (km/h), mile per hour (mph), mach
- *Energy* ⚡️: joule (J), kilojoule (kJ), megajoule (MJ), watt hour (Wh), kilowatt hour (kWh), calorie (cal), kilocalorie (kcal)
- *Pressure* 🌬️: pascal (Pa), kilopascal (kPa), atmosphere (atm), bar, millimeter mercury (mmHg)
- *Angle* 📐: degree (deg), radian (rad), gradian (grad)
- *Digital* 💾: byte (B), kilobyte (KB), megabyte (MB), gigabyte (GB), terabyte (TB), petabyte (PB), exabyte (EB)

📝 *Examples*:
- `@RezUnitBot 10 km` → Converts 10 kilometers to all length units.
- `@RezUnitBot 5 kg` → Converts 5 kilograms to all weight units.
- `@RezUnitBot 100 C` → Converts 100 Celsius to Fahrenheit and Kelvin.

🚀 *Start converting now with `@RezUnitBot 10 km`! Happy converting!* 🎉.
"""
        bot.reply_to(message, help_message, parse_mode="Markdown")

    @bot.message_handler(commands=['alive'])
    def alive_command(message):
        if not utils.is_message_valid(message, bot_start_time):
            return
        user_id = message.from_user.id
        allowed, error_message = utils.check_rate_limit(user_id)
        if not allowed:
            bot.send_message(user_id, error_message)
            return
        bot.send_message(message.chat.id, "I'm alive and kicking! 🤖 DigitIDBot is here!")

    @bot.inline_handler(lambda query: True)
    def inline_query(query):
        results = []
        value, from_unit, category, error_message = conv.parse_query(query.query)
        
        if error_message:
            results.append(InlineQueryResultArticle(
                id='error', title='Input Error ❌',
                input_message_content=InputTextMessageContent(error_message, parse_mode="Markdown")
            ))
            bot.answer_inline_query(query.id, results)
            return

        output = []
        emoji = conv.UNITS[category]['emoji']
        for unit, unit_name in conv.UNITS[category]['names'].items():
            if unit_name != from_unit:
                try:
                    result = conv.convert_unit(value, from_unit, unit_name, category)
                    output.append(f'''{emoji} {conv.format_number(value)} {from_unit} = {result} {unit_name}''')
                except Exception:
                    continue
        output_message = "\n".join(sorted(set(output)))

        if not output_message:
            results.append(InlineQueryResultArticle(
                id='error', title='No Results ❌',
                input_message_content=InputTextMessageContent(
                    f"هیچ نتیجه‌ای برای {query.query} تولید نشد. مثال‌ها:\n@RezUnitBot 10 kilometer\n@RezUnitBot 10 km\n\nNo results for {query.query}. Check your input. Examples:\n@RezUnitBot 10 kilometer\n@RezUnitBot 10 km",
                    parse_mode="Markdown"
                )
            ))
        else:
            results.append(InlineQueryResultArticle(
                id='1', title=f"Convert {from_unit} {emoji}",
                input_message_content=InputTextMessageContent(output_message)
            ))
        bot.answer_inline_query(query.id, results)

    @bot.message_handler(func=lambda message: message.text == "پیام همگانی 📢")
    def handle_broadcast_request(message):
        if not utils.is_message_valid(message, bot_start_time):
            return
        user_id = message.chat.id
        if user_id not in ADMIN_USER_IDS:
            bot.send_message(user_id, "این قابلیت فقط برای ادمین‌ها در دسترسه!")
            return
        logger.info(f"Broadcast initiated by admin {user_id}")
        bot.send_message(user_id, "هر پیامی که می‌خوای بنویس تا برای همه کاربران ارسال بشه 📢")
        bot.register_next_step_handler(message, send_broadcast)

    def send_broadcast(message):
        if not utils.is_message_valid(message, bot_start_time):
            return
        user_id = message.chat.id
        if user_id not in ADMIN_USER_IDS:
            return
            
        user_ids = db.get_all_user_ids()
        if not user_ids:
            bot.send_message(user_id, "❌ هیچ کاربری در پایگاه داده یافت نشد!")
            return

        success_count = 0
        for uid in user_ids:
            try:
                bot.send_message(uid, message.text)
                success_count += 1
                sleep(0.5)
            except Exception as e:
                logger.warning(f"Failed to send broadcast to user {uid}: {e}")
                continue
        bot.send_message(user_id, f"پیام به {success_count} کاربر ارسال شد 📢")
        logger.info(f"Broadcast sent to {success_count} users by admin {user_id}")
        
    @bot.message_handler(content_types=['text'])
    def handle_text(message):
        if not utils.is_message_valid(message, bot_start_time):
            return
        user_id = message.from_user.id
        allowed, error_message = utils.check_rate_limit(user_id)
        if not allowed:
            bot.send_message(user_id, error_message)
            return
