# دليل النشر على GitHub - خطوة بخطوة 🚀

## الخطوة 1: تثبيت Git (إذا لم يكن مثبتاً)

### Windows:
1. اذهب إلى: https://git-scm.com/download/win
2. حمّل Git for Windows
3. شغّل المثبت واتبع التعليمات
4. أعد فتح PowerShell بعد التثبيت

### التحقق من التثبيت:
```bash
git --version
```

---

## الخطوة 2: إنشاء Repository على GitHub

1. اذهب إلى [GitHub.com](https://github.com) وسجل الدخول
2. اضغط على **+** في الأعلى → **New repository**
3. اختر اسم للمشروع (مثلاً: `telegram-ai-bot` أو `anas-digital-self`)
4. اختر **Public** أو **Private**
5. **⚠️ لا تضع علامة** على "Initialize with README" (لأن لدينا README بالفعل)
6. اضغط **Create repository**

---

## الخطوة 3: تهيئة Git في المشروع

افتح PowerShell في مجلد المشروع (`C:\Users\ميثلون\Desktop\مجلد جديد`) وشغّل:

```bash
# تهيئة Git
git init

# إضافة جميع الملفات (ملف .env محمي ولن يُرفع)
git add .

# عمل commit أولي
git commit -m "Initial commit: Telegram AI Bot - Digital Self for Anas Rabaya"

# إضافة remote repository
# استبدل YOUR_USERNAME و REPO_NAME بالقيم الحقيقية
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# تعيين الفرع الرئيسي
git branch -M main

# رفع الكود
git push -u origin main
```

---

## الخطوة 4: مثال كامل

إذا كان اسم المستخدم `anasrabaya` واسم المشروع `telegram-ai-bot`:

```bash
git init
git add .
git commit -m "Initial commit: Telegram AI Bot for Anas Rabaya"
git remote add origin https://github.com/anasrabaya/telegram-ai-bot.git
git branch -M main
git push -u origin main
```

**ملاحظة**: سيطلب منك GitHub اسم المستخدم وكلمة المرور (أو Personal Access Token)

---

## ✅ ما تم إعداده مسبقاً:

- ✅ ملف `.gitignore` - يحمي ملف `.env` من الرفع
- ✅ ملف `README.md` - دليل شامل بالعربية
- ✅ ملف `DEPLOY.md` - تعليمات النشر
- ✅ جميع الملفات المهمة جاهزة

---

## 🔒 الأمان:

### ✅ ملف `.env` محمي
- تم إضافته إلى `.gitignore`
- **لن يُرفع** إلى GitHub (آمن!)

### ⚠️ تحذير:
- **لا ترفع ملف .env أبداً!**
- التوكنات والمفاتيح السرية يجب أن تبقى محلية فقط

---

## بعد النشر:

### إضافة ملف .env.example (اختياري):

أنشئ ملف `.env.example` يدوياً:

```env
TELEGRAM_TOKEN=your_bot_token_here
GEMINI_API_KEY=your_gemini_key_here
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

ثم:
```bash
git add .env.example
git commit -m "Add .env.example template"
git push
```

---

## تحديثات مستقبلية:

عند إجراء تغييرات في الكود:

```bash
git add .
git commit -m "وصف التغييرات"
git push
```

---

## استكشاف المشاكل:

### "git: command not found"
→ Git غير مثبت. راجع الخطوة 1

### "fatal: not a git repository"
→ لم تقم بتشغيل `git init`

### "remote origin already exists"
→ قم بحذف الـ remote القديم:
```bash
git remote remove origin
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git
```

### "Authentication failed"
→ استخدم Personal Access Token بدلاً من كلمة المرور:
1. GitHub → Settings → Developer settings → Personal access tokens
2. أنشئ token جديد
3. استخدمه ككلمة مرور

---

## 🎉 بعد النشر:

- ✅ الكود الآن على GitHub
- ✅ يمكن للآخرين استنساخه
- ✅ يمكنك تحديثه في أي وقت
- ✅ ملف `.env` آمن ومحمي

**رابط المشروع**: `https://github.com/YOUR_USERNAME/REPO_NAME`
