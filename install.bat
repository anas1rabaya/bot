@echo off
chcp 65001 >nul
echo ========================================
echo   تثبيت مكتبات البوت
echo ========================================
echo.

echo جاري تثبيت المكتبات...
echo.

python -m pip install python-telegram-bot==20.7
if errorlevel 1 (
    echo [خطأ] فشل تثبيت python-telegram-bot
    pause
    exit /b 1
)
echo [✓] python-telegram-bot مثبت
echo.

python -m pip install google-generativeai==0.3.2
if errorlevel 1 (
    echo [خطأ] فشل تثبيت google-generativeai
    pause
    exit /b 1
)
echo [✓] google-generativeai مثبت
echo.

python -m pip install supabase==2.3.4
if errorlevel 1 (
    echo [خطأ] فشل تثبيت supabase
    pause
    exit /b 1
)
echo [✓] supabase مثبت
echo.

python -m pip install python-dotenv==1.0.0
if errorlevel 1 (
    echo [خطأ] فشل تثبيت python-dotenv
    pause
    exit /b 1
)
echo [✓] python-dotenv مثبت
echo.

echo ========================================
echo   ✓ تم تثبيت جميع المكتبات بنجاح!
echo ========================================
echo.
echo يمكنك الآن تشغيل البوت بـ: python main.py
echo.
pause
