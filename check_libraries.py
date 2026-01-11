#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""التحقق من المكتبات المثبتة"""

print("=" * 60)
print("التحقق من المكتبات المثبتة")
print("=" * 60)

libraries = {
    "python-telegram-bot": "telegram",
    "google-generativeai": "google.generativeai",
    "supabase": "supabase",
    "python-dotenv": "dotenv"
}

all_installed = True

for lib_name, import_name in libraries.items():
    try:
        __import__(import_name)
        print(f"✓ {lib_name} - مثبت")
    except ImportError:
        print(f"✗ {lib_name} - غير مثبت")
        all_installed = False

print("=" * 60)

if all_installed:
    print("✓ جميع المكتبات مثبتة!")
    print("\nيمكنك الآن تشغيل البوت بـ: python main.py")
else:
    print("✗ بعض المكتبات غير مثبتة")
    print("\nقم بتثبيتها بـ:")
    print("python -m pip install -r requirements.txt")
    print("\nأو شغّل: .\\install.bat")

print("=" * 60)
input("\nاضغط Enter للإغلاق...")
