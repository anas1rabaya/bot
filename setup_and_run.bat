@echo off
chcp 65001 >nul
echo ========================================
echo   إعداد وتشغيل Telegram Bot
echo ========================================
echo.

REM التحقق من ملف .env
if not exist .env (
    echo [خطأ] ملف .env غير موجود!
    echo.
    echo يرجى إنشاء ملف .env وإضافة:
    echo TELEGRAM_TOKEN=your_bot_token_here
    echo GEMINI_API_KEY=your_gemini_key_here
    echo SUPABASE_URL=your_supabase_url
    echo SUPABASE_KEY=your_supabase_key
    echo.
    pause
    exit /b 1
)

echo [✓] ملف .env موجود
echo.

REM تثبيت المكتبات
echo [*] جاري تثبيت المكتبات...
pip install -r requirements.txt
if errorlevel 1 (
    echo [خطأ] فشل تثبيت المكتبات!
    pause
    exit /b 1
)

echo [✓] تم تثبيت المكتبات بنجاح
echo.

REM تشغيل البوت
echo [*] جاري تشغيل البوت...
echo.
python main.py

pause
