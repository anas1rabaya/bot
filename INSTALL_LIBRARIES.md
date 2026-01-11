# تثبيت المكتبات المطلوبة 📦

## الطريقة السريعة:

### شغّل هذا الأمر في PowerShell:

```bash
python -m pip install -r requirements.txt
```

---

## الطريقة اليدوية (إذا فشلت السريعة):

### شغّل كل أمر على حدة:

```bash
python -m pip install python-telegram-bot==20.7
python -m pip install google-generativeai==0.3.2
python -m pip install supabase==2.3.4
python -m pip install python-dotenv==1.0.0
```

---

## أو استخدم الملف الجاهز:

### شغّل:
```bash
.\install.bat
```

---

## التحقق من التثبيت:

بعد التثبيت، شغّل هذا للتحقق:

```bash
python -c "import telegram; print('✓ telegram OK')"
python -c "from dotenv import load_dotenv; print('✓ dotenv OK')"
python -c "import google.generativeai; print('✓ gemini OK')"
python -c "from supabase import create_client; print('✓ supabase OK')"
```

**يجب أن ترى:**
- ✓ telegram OK
- ✓ dotenv OK
- ✓ gemini OK
- ✓ supabase OK

---

## إذا ظهرت أخطاء:

### خطأ: "pip is not recognized"
**الحل:**
```bash
python -m pip install [اسم_المكتبة]
```

### خطأ: "Permission denied"
**الحل:**
- شغّل PowerShell كمسؤول (Run as Administrator)
- أو استخدم: `python -m pip install --user [اسم_المكتبة]`

### خطأ: "No module named 'pip'"
**الحل:**
- تأكد من تثبيت Python بشكل صحيح
- أعد تثبيت Python من python.org

---

## بعد التثبيت:

شغّل البوت:
```bash
python main.py
```
