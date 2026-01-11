#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""سكريبت اختبار للبوت"""

import os
import sys
from dotenv import load_dotenv

print("=" * 50)
print("اختبار إعدادات البوت")
print("=" * 50)

# تحميل .env
load_dotenv()
print("\n[1] فحص ملف .env...")
if os.path.exists('.env'):
    print("✓ ملف .env موجود")
else:
    print("✗ ملف .env غير موجود!")
    sys.exit(1)

# فحص التوكن
print("\n[2] فحص TELEGRAM_TOKEN...")
token = os.getenv("TELEGRAM_TOKEN")
if token:
    if token == "your_bot_token_here":
        print("✗ التوكن غير محدد (قيمة افتراضية)")
    else:
        print(f"✓ التوكن موجود: {token[:10]}...")
else:
    print("✗ التوكن غير موجود!")
    sys.exit(1)

# فحص المكتبات
print("\n[3] فحص المكتبات...")
try:
    import telegram
    print("✓ python-telegram-bot مثبت")
except ImportError:
    print("✗ python-telegram-bot غير مثبت")
    print("  قم بتشغيل: python -m pip install -r requirements.txt")
    sys.exit(1)

try:
    import google.generativeai as genai
    print("✓ google-generativeai مثبت")
except ImportError:
    print("⚠ google-generativeai غير مثبت (اختياري)")

try:
    from supabase import create_client
    print("✓ supabase مثبت")
except ImportError:
    print("⚠ supabase غير مثبت (اختياري)")

# اختبار الاتصال
print("\n[4] اختبار الاتصال بـ Telegram...")
try:
    from telegram import Bot
    bot = Bot(token=token)
    bot_info = bot.get_me()
    print(f"✓ الاتصال ناجح!")
    print(f"  اسم البوت: {bot_info.first_name}")
    print(f"  معرف البوت: @{bot_info.username}")
except Exception as e:
    print(f"✗ فشل الاتصال: {e}")
    print("\nالأسباب المحتملة:")
    print("  1. التوكن غير صحيح")
    print("  2. لا يوجد اتصال بالإنترنت")
    print("  3. البوت تم حذفه أو تعطيله")
    sys.exit(1)

print("\n" + "=" * 50)
print("✓ جميع الاختبارات نجحت!")
print("=" * 50)
print("\nيمكنك الآن تشغيل البوت بـ: python main.py")
