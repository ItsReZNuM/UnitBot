import telebot
from telebot import types
from telebot.types import InlineQueryResultArticle, InputTextMessageContent
import re
import math
import logging
from datetime import datetime
from pytz import timezone
import json
import os
from time import sleep , time

logging.basicConfig(
    level=logging.ERROR,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log')
    ]
)
logger = logging.getLogger(__name__)

TOKEN = '7962365735:AAEwwWkyOJ5hyOW4toExtZwesceLrRJyXx0'
bot = telebot.TeleBot(TOKEN)
ADMIN_USER_IDS = [6728527154]
message_tracker = {}
user_data = {}
USERS_FILE = "users.json"

commands = [
    telebot.types.BotCommand("start", "شروع ربات"),
    telebot.types.BotCommand("help", "راهنمای استفاده از ربات")
]
bot.set_my_commands(commands)

bot_start_time = datetime.now(timezone('Asia/Tehran')).timestamp()

def save_user(user_id, username):
    if user_id in ADMIN_USER_IDS:
        return
    users = []
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                users = json.load(f)
        except json.JSONDecodeError:
            logger.error("Failed to read users.json, starting with empty list")
    
    if not any(user['id'] == user_id for user in users):
        users.append({"id": user_id, "username": username if username else "ندارد"})
        try:
            with open(USERS_FILE, 'w', encoding='utf-8') as f:
                json.dump(users, f, ensure_ascii=False, indent=4)
            logger.info(f"Saved user {user_id} to users.json")
        except Exception as e:
            logger.error(f"Error saving user {user_id} to users.json: {e}")

def is_message_valid(message):
    message_time = message.date
    logger.info(f"Checking message timestamp: {message_time} vs bot_start_time: {bot_start_time}")
    if message_time < bot_start_time:
        logger.warning(f"Ignoring old message from user {message.chat.id} sent at {message_time}")
        return False
    return True

def check_rate_limit(user_id):
    current_time = time()
    
    if user_id not in message_tracker:
        message_tracker[user_id] = {'count': 0, 'last_time': current_time, 'temp_block_until': 0}
    
    if current_time < message_tracker[user_id]['temp_block_until']:
        remaining = int(message_tracker[user_id]['temp_block_until'] - current_time)
        return False, f"شما به دلیل ارسال پیام زیاد تا {remaining} ثانیه نمی‌تونید پیام بفرستید 😕"
    
    if current_time - message_tracker[user_id]['last_time'] > 1:
        message_tracker[user_id]['count'] = 0
        message_tracker[user_id]['last_time'] = current_time
    
    message_tracker[user_id]['count'] += 1
    
    if message_tracker[user_id]['count'] > 2:
        message_tracker[user_id]['temp_block_until'] = current_time + 30
        return False, "شما بیش از حد پیام فرستادید! تا ۳۰ ثانیه نمی‌تونید پیام بفرستید 😕"
    
    return True, ""

def send_broadcast(message):
    if not is_message_valid(message):
        return
    user_id = message.chat.id
    if user_id not in ADMIN_USER_IDS:
        return
    users = []
    if os.path.exists(USERS_FILE):
        try:
            with open(USERS_FILE, 'r', encoding='utf-8') as f:
                users = json.load(f)
        except json.JSONDecodeError:
            logger.error("Failed to read users.json")
            bot.send_message(user_id, "❌ خطا در خواندن لیست کاربران!")
            return
    success_count = 0
    for user in users:
        try:
            bot.send_message(user["id"], message.text)
            success_count += 1
            sleep(0.5)
        except Exception as e:
            logger.warning(f"Failed to send broadcast to user {user['id']}: {e}")
            continue
    bot.send_message(user_id, f"پیام به {success_count} کاربر ارسال شد 📢")
    logger.info(f"Broadcast sent to {success_count} users by admin {user_id}")

def persian_to_english_number(text):
    persian_digits = '۰۱۲۳۴۵۶۷۸۹'
    english_digits = '0123456789'
    translation_table = str.maketrans(persian_digits, english_digits)
    return text.translate(translation_table)

UNITS = {
    'length': {
        'names': {
            'millimeter': 'mm', 'centimeter': 'cm', 'meter': 'm', 'kilometer': 'km', 'decimeter': 'dm',
            'inch': 'in', 'foot': 'ft', 'yard': 'yd', 'mile': 'mi',
            'mm': 'mm', 'cm': 'cm', 'm': 'm', 'km': 'km', 'dm': 'dm',
            'in': 'in', 'ft': 'ft', 'yd': 'yd', 'mi': 'mi'
        },
        'to_base': {
            'mm': 0.001, 'cm': 0.01, 'm': 1, 'km': 1000, 'dm': 0.1,
            'in': 0.0254, 'ft': 0.3048, 'yd': 0.9144, 'mi': 1609.34
        },
        'base_unit': 'm',
        'emoji': '📏'
    },
    'weight': {
        'names': {
            'milligram': 'mg', 'gram': 'g', 'kilogram': 'kg', 'ton': 't', 'pound': 'lb',
            'mg': 'mg', 'g': 'g', 'kg': 'kg', 't': 't', 'lb': 'lb'
        },
        'to_base': {
            'mg': 0.000001, 'g': 0.001, 'kg': 1, 't': 1000, 'lb': 0.453592
        },
        'base_unit': 'kg',
        'emoji': '⚖️'
    },
    'area': {
        'names': {
            'centimeter square': 'cm2', 'meter square': 'm2', 'hectare': 'ha', 'inch square': 'in2', 'foot square': 'ft2', 'acre': 'acre',
            'cm2': 'cm2', 'm2': 'm2', 'ha': 'ha', 'in2': 'in2', 'ft2': 'ft2', 'acre': 'acre'
        },
        'to_base': {
            'cm2': 0.0001, 'm2': 1, 'ha': 10000, 'in2': 0.00064516, 'ft2': 0.092903, 'acre': 4046.86
        },
        'base_unit': 'm2',
        'emoji': '🏞️'
    },
    'volume': {
        'names': {
            'milliliter': 'ml', 'centimeter cubic': 'cm3', 'liter': 'l', 'meter cubic': 'm3', 'gallon': 'gal', 'barrel': 'bbl',
            'ml': 'ml', 'cm3': 'cm3', 'l': 'l', 'm3': 'm3', 'gal': 'gal', 'bbl': 'bbl', 'cc': 'cc'
        },
        'to_base': {
            'ml': 0.001, 'cm3': 0.001, 'l': 1, 'm3': 1000, 'gal': 3.78541, 'bbl': 158.987, 'cc': 0.001
        },
        'base_unit': 'l',
        'emoji': '🧴'
    },
    'time': {
        'names': {
            'second': 's', 'minute': 'min', 'hour': 'h', 'day': 'd', 'week': 'wk', 'month': 'mo', 'year': 'yr',
            's': 's', 'min': 'min', 'h': 'h', 'd': 'd', 'wk': 'wk', 'mo': 'mo', 'yr': 'yr'
        },
        'to_base': {
            's': 1, 'min': 60, 'h': 3600, 'd': 86400, 'wk': 604800, 'mo': 2.628e6, 'yr': 3.156e7
        },
        'base_unit': 's',
        'emoji': '⏱️'
    },
    'temperature': {
        'names': {
            'celsius': 'C', 'fahrenheit': 'F', 'kelvin': 'K',
            'C': 'C', 'F': 'F', 'K': 'K'
        },
        'to_base': {
            'C': lambda x: x, 'F': lambda x: (x - 32) * 5/9, 'K': lambda x: x - 273.15
        },
        'from_base': {
            'C': lambda x: x, 'F': lambda x: x * 9/5 + 32, 'K': lambda x: x + 273.15
        },
        'base_unit': 'C',
        'emoji': '🌡️'
    },
    'speed': {
        'names': {
            'meter per second': 'm/s', 'kilometer per hour': 'km/h', 'mile per hour': 'mph', 'mach': 'mach',
            'm/s': 'm/s', 'km/h': 'km/h', 'mph': 'mph', 'mach': 'mach'
        },
        'to_base': {
            'm/s': 1, 'km/h': 0.277778, 'mph': 0.44704, 'mach': 343
        },
        'base_unit': 'm/s',
        'emoji': '🚀'
    },
    'energy': {
        'names': {
            'joule': 'J', 'kilojoule': 'kJ', 'megajoule': 'MJ', 'watt hour': 'Wh', 'kilowatt hour': 'kWh', 'calorie': 'cal', 'kilocalorie': 'kcal',
            'J': 'J', 'kJ': 'kJ', 'MJ': 'MJ', 'Wh': 'Wh', 'kWh': 'kWh', 'cal': 'cal', 'kcal': 'kcal'
        },
        'to_base': {
            'J': 1, 'kJ': 1000, 'MJ': 1e6, 'Wh': 3600, 'kWh': 3.6e6, 'cal': 4.184, 'kcal': 4184
        },
        'base_unit': 'J',
        'emoji': '⚡️'
    },
    'pressure': {
        'names': {
            'pascal': 'Pa', 'kilopascal': 'kPa', 'atmosphere': 'atm', 'bar': 'bar', 'millimeter mercury': 'mmHg',
            'Pa': 'Pa', 'kPa': 'kPa', 'atm': 'atm', 'bar': 'bar', 'mmHg': 'mmHg'
        },
        'to_base': {
            'Pa': 1, 'kPa': 1000, 'atm': 101325, 'bar': 100000, 'mmHg': 133.322
        },
        'base_unit': 'Pa',
        'emoji': '🌬️'
    },
    'angle': {
        'names': {
            'degree': 'deg', 'radian': 'rad', 'gradian': 'grad',
            'deg': 'deg', 'rad': 'rad', 'grad': 'grad'
        },
        'to_base': {
            'deg': math.pi/180, 'rad': 1, 'grad': math.pi/200
        },
        'base_unit': 'rad',
        'emoji': '📐'
    },
    'digital': {
        'names': {
            'byte': 'B', 'kilobyte': 'KB', 'megabyte': 'MB', 'gigabyte': 'GB', 'terabyte': 'TB', 'petabyte': 'PB', 'exabyte': 'EB',
            'B': 'B', 'KB': 'KB', 'MB': 'MB', 'GB': 'GB', 'TB': 'TB', 'PB': 'PB', 'EB': 'EB'
        },
        'to_base': {
            'B': 1, 'KB': 1024, 'MB': 1024**2, 'GB': 1024**3, 'TB': 1024**4, 'PB': 1024**5, 'EB': 1024**6
        },
        'base_unit': 'B',
        'emoji': '💾'
    }
}

def format_number(value):
    if value >= 100000:
        return f"{int(value):,}"
    elif value >= 1000:
        return f"{value:,.0f}"
    elif value < 0.01 and value > 0:
        return f"{value:.6f}".rstrip('0').rstrip('.')
    else:
        return f"{value:.2f}".rstrip('0').rstrip('.')

def convert_unit(value, from_unit, to_unit, category):
    try:
        if category == 'temperature':
            base_value = UNITS[category]['to_base'][from_unit](value)
            result = UNITS[category]['from_base'][to_unit](base_value)
        else:
            base_value = value * UNITS[category]['to_base'][from_unit]
            result = base_value / UNITS[category]['to_base'][to_unit]
        return format_number(result)
    except Exception as e:
        logger.error(f"Error in conversion from {from_unit} to {to_unit}: {str(e)}")
        raise

def find_unit(unit_str):
    if not unit_str:
        return None, None
    unit_str = unit_str.lower().strip()
    if unit_str == 'k':
        return 'K', 'temperature'
    for cat, data in UNITS.items():
        units = {k.lower(): v for k, v in data['names'].items()}
        if unit_str in units:
            return units[unit_str], cat
    return None, None

def parse_query(query):
    query = persian_to_english_number(query.strip())
    pattern = r'^(\d*\.?\d*)\s*([^\s]+)$'
    match = re.match(pattern, query)
    if not match:
        return None, None, None, "فرمت ورودی نادرست است. مثال‌ها:\n@RezUnitBot 10 kilometer\n@RezUnitBot 10 km\n\nInvalid input format. Examples:\n@RezUnitBot 10 kilometer\n@RezUnitBot 10 km"
    value, from_unit_str = match.groups()
    try:
        value = float(value)
        if value == 0 and query.startswith('0'):
            return None, None, None, "عدد صفر معتبر نیست. مثال‌ها:\n@RezUnitBot 10 kilometer\n@RezUnitBot 10 km\n\nZero value is not valid. Examples:\n@RezUnitBot 10 kilometer\n@RezUnitBot 10 km"
    except ValueError:
        return None, None, None, "عدد نامعتبر است. مثال‌ها:\n@RezUnitBot 10 kilometer\n@RezUnitBot 10 km\n\nInvalid number. Examples:\n@RezUnitBot 10 kilometer\n@RezUnitBot 10 km"
    from_unit, category = find_unit(from_unit_str)
    if not from_unit:
        return None, None, None, f"واحد ({from_unit_str}) شناخته نشد. مثال‌ها:\n@RezUnitBot 10 kilometer\n@RezUnitBot 10 km\n\nUnit ({from_unit_str}) not recognized. Examples:\n@RezUnitBot 10 kilometer\n@RezUnitBot 10 km"
    return value, from_unit, category, None

@bot.message_handler(commands=['start'])
    
def handle_start(message):
    if not is_message_valid(message):
        return
    
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    allowed, error_message = check_rate_limit(user_id)
    if not allowed:
        bot.send_message(user_id, error_message)
        return
    save_user(user_id, user_name)

    welcome_message = f"""🌟 *به UnitBot خوش آمدید!* 🌟
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
    
    bot.send_message(message.chat.id, welcome_message, parse_mode="Markdown" , reply_markup=markup)
    

@bot.message_handler(commands=['help'])
def handle_help(message):
    if not is_message_valid(message):
        return
    
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    allowed, error_message = check_rate_limit(user_id)
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

🚀 *Start converting now with `@RezUnitBot 10 km`! Happy converting!* 🎉"""
    bot.reply_to(message, help_message, parse_mode="Markdown")

@bot.message_handler(commands=['alive'])
def alive_command(message):
    """Handles the /alive command."""
    if not is_message_valid(message):
        return
    user_id = message.from_user.id
    allowed, error_message = check_rate_limit(user_id)
    if not allowed:
        bot.send_message(user_id, error_message)
        return
    
    bot.send_message(
        message.chat.id,
        "I'm alive and kicking! 🤖 DigitIDBot is here!"
    )

@bot.inline_handler(lambda query: True)
def inline_query(query):
    results = []
    value, from_unit, category, error_message = parse_query(query.query)
    
    if error_message:
        results.append(InlineQueryResultArticle(
            id='error',
            title='Input Error ❌',
            input_message_content=InputTextMessageContent(error_message, parse_mode="Markdown")
        ))
        bot.answer_inline_query(query.id, results)
        return

    output = []
    emoji = UNITS[category]['emoji']
    for unit, unit_name in UNITS[category]['names'].items():
        if unit_name != from_unit:
            try:
                result = convert_unit(value, from_unit, unit_name, category)
                output.append(f"{emoji} {format_number(value)} {from_unit} = {result} {unit_name}")
            except Exception as e:
                continue
    output_message = "\n".join(sorted(set(output)))

    if not output_message:
        results.append(InlineQueryResultArticle(
            id='error',
            title='No Results ❌',
            input_message_content=InputTextMessageContent(
                f"هیچ نتیجه‌ای برای {query.query} تولید نشد. مثال‌ها:\n@RezUnitBot 10 kilometer\n@RezUnitBot 10 km\n\nNo results for {query.query}. Check your input. Examples:\n@RezUnitBot 10 kilometer\n@RezUnitBot 10 km",
                parse_mode="Markdown"
            )
        ))
    else:
        results.append(InlineQueryResultArticle(
            id='1',
            title=f"Convert {from_unit} {emoji}",
            input_message_content=InputTextMessageContent(output_message)
        ))

    bot.answer_inline_query(query.id, results)

@bot.message_handler(content_types=['text'])
def forwarded_message_handler(message):

    if not is_message_valid(message):
        return
    user_id = message.from_user.id
    allowed, error_message = check_rate_limit(user_id)
    if not allowed:
        bot.send_message(user_id, error_message)
        return
    
@bot.message_handler(func=lambda message: message.text == "پیام همگانی 📢")
def handle_broadcast(message):
    if not is_message_valid(message):
        return
    user_id = message.chat.id
    if user_id not in ADMIN_USER_IDS:
        bot.send_message(user_id, "این قابلیت فقط برای ادمین‌ها در دسترسه!")
        return
    logger.info(f"Broadcast initiated by admin {user_id}")
    bot.send_message(user_id, "هر پیامی که می‌خوای بنویس تا برای همه کاربران ارسال بشه 📢")
    bot.register_next_step_handler(message, send_broadcast)

def main():
    print("Bot is starting...")
    bot.polling(none_stop=True)
    print("Bot stopped.")

if __name__ == '__main__':
    main()

try:
    bot.polling()
except Exception as e:
    logger.error(f"Error in bot polling: {str(e)}")