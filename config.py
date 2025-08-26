import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise ValueError("توکن ربات (TOKEN) در فایل .env تعریف نشده است!")

admin_ids_str = os.getenv("ADMIN_USER_IDS", "")
try:
    ADMIN_USER_IDS = [int(admin_id.strip()) for admin_id in admin_ids_str.split(',') if admin_id.strip()]
except ValueError:
    print("خطا: فرمت ADMIN_USER_IDS در فایل .env صحیح نیست. باید لیستی از اعداد جدا شده با کاما باشد.")
    ADMIN_USER_IDS = []


DATABASE_FILE = "users.db"