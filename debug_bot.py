#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""سكريبت تشخيص للمشاكل"""

import sys
import os

print("=" * 60)
print("تشخيص مشاكل البوت")
print("=" * 60)

# 1. فحص Python
print("\n[1] فحص Python...")
print(f"   Python version: {sys.version}")

# 2. فحص المكتبات
print("\n[2] فحص المكتبات...")
try:
    import telegram
    print("   ✓ python-telegram-bot مثبت")
except ImportError as e:
    print(f"   ✗ python-telegram-bot غير مثبت: {e}")
    print("   الحل: python -m pip install python-telegram-bot")
    sys.exit(1)

try:
    from dotenv import load_dotenv
    print("   ✓ python-dotenv مثبت")
except ImportError as e:
    print(f"   ✗ python-dotenv غير مثبت: {e}")
    print("   الحل: python -m pip install python-dotenv")
    sys.exit(1)

# 3. فحص ملف .env
print("\n[3] فحص ملف .env...")
if os.path.exists('.env'):
    print("   ✓ ملف .env موجود")
    with open('.env', 'r', encoding='utf-8') as f:
        lines = f.readlines()
        for line in lines:
            if line.startswith('TELEGRAM_TOKEN'):
                token_value = line.split('=', 1)[1].strip()
                if token_value and token_value != 'your_bot_token_here':
                    print(f"   ✓ TELEGRAM_TOKEN موجود: {token_value[:20]}...")
                else:
                    print("   ✗ TELEGRAM_TOKEN غير محدد!")
else:
    print("   ✗ ملف .env غير موجود!")
    sys.exit(1)

# 4. تحميل المتغيرات
print("\n[4] تحميل المتغيرات...")
load_dotenv()
token = os.getenv("TELEGRAM_TOKEN")

if not token:
    print("   ✗ لا يمكن قراءة TELEGRAM_TOKEN من .env")
    sys.exit(1)

if token == "your_bot_token_here":
    print("   ✗ التوكن غير محدد (قيمة افتراضية)")
    sys.exit(1)

print(f"   ✓ التوكن محمّل: {token[:20]}...")

# 5. اختبار الاتصال
print("\n[5] اختبار الاتصال بـ Telegram...")
try:
    from telegram import Bot
    bot = Bot(token=token)
    bot_info = bot.get_me()
    print(f"   ✓ الاتصال ناجح!")
    print(f"   ✓ اسم البوت: {bot_info.first_name}")
    print(f"   ✓ معرف البوت: @{bot_info.username}")
except Exception as e:
    print(f"   ✗ فشل الاتصال: {type(e).__name__}: {e}")
    print("\n   الأسباب المحتملة:")
    print("   1. التوكن غير صحيح")
    print("   2. لا يوجد اتصال بالإنترنت")
    print("   3. البوت تم حذفه أو تعطيله")
    sys.exit(1)

# 6. محاولة استيراد main.py
print("\n[6] فحص main.py...")
try:
    import main
    print("   ✓ main.py يمكن استيراده")
except Exception as e:
    print(f"   ✗ خطأ في main.py: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("✓ جميع الاختبارات نجحت!")
print("=" * 60)
print("\nيمكنك الآن تشغيل البوت بـ: python main.py")
print("أو اضغط Enter لتشغيله الآن...")

input()
print("\nجارٍ تشغيل البوت...\n")

if __name__ == "__main__":
    import main
    main.main()
