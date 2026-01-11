import os
from dotenv import load_dotenv

print("Testing...")
load_dotenv()
token = os.getenv("TELEGRAM_TOKEN")
print(f"Token: {token[:30] if token else 'NOT FOUND'}...")

if token:
    try:
        from telegram import Bot
        bot = Bot(token=token)
        info = bot.get_me()
        print(f"Bot name: {info.first_name}")
        print(f"Bot username: @{info.username}")
        print("SUCCESS!")
    except Exception as e:
        print(f"ERROR: {e}")
else:
    print("Token not found in .env")
