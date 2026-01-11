#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""تثبيت جميع المكتبات المطلوبة"""

import subprocess
import sys

print("=" * 60)
print("تثبيت مكتبات البوت")
print("=" * 60)

# قائمة المكتبات المطلوبة
packages = [
    "python-telegram-bot==20.7",
    "google-generativeai==0.3.2",
    "supabase==2.3.4",
    "python-dotenv==1.0.0"
]

print("\nالمكتبات المطلوبة:")
for pkg in packages:
    print(f"  - {pkg}")

print("\n" + "=" * 60)
print("جارٍ التثبيت...")
print("=" * 60 + "\n")

# تثبيت كل مكتبة
for package in packages:
    print(f"📦 تثبيت {package}...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])
        print(f"✅ تم تثبيت {package}\n")
    except subprocess.CalledProcessError as e:
        print(f"❌ فشل تثبيت {package}: {e}\n")

print("=" * 60)
print("✓ انتهى التثبيت!")
print("=" * 60)

# التحقق من التثبيت
print("\nالتحقق من المكتبات المثبتة:\n")

try:
    import telegram
    print("✅ python-telegram-bot")
except ImportError:
    print("❌ python-telegram-bot")

try:
    import google.generativeai
    print("✅ google-generativeai")
except ImportError:
    print("❌ google-generativeai")

try:
    import supabase
    print("✅ supabase")
except ImportError:
    print("❌ supabase")

try:
    import dotenv
    print("✅ python-dotenv")
except ImportError:
    print("❌ python-dotenv")

print("\n" + "=" * 60)
print("يمكنك الآن تشغيل البوت بـ: python main.py")
print("=" * 60)
