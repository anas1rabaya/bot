# دليل النشر على GitHub 🚀

## الخطوات:

### 1. إنشاء Repository جديد على GitHub
1. اذهب إلى [GitHub](https://github.com)
2. اضغط على **New repository** (أو **+** في الأعلى)
3. اختر اسم للمشروع (مثلاً: `telegram-ai-bot` أو `anas-digital-self`)
4. اختر **Public** أو **Private**
5. **لا** تضع علامة على "Initialize with README" (لأن لدينا README بالفعل)
6. اضغط **Create repository**

### 2. تهيئة Git في المشروع المحلي

افتح PowerShell في مجلد المشروع وشغّل:

```bash
# تهيئة Git
git init

# إضافة جميع الملفات
git add .

# عمل commit أولي
git commit -m "Initial commit: Telegram AI Bot - Digital Self"

# إضافة remote repository (استبدل YOUR_USERNAME و REPO_NAME)
git remote add origin https://github.com/YOUR_USERNAME/REPO_NAME.git

# رفع الكود
git branch -M main
git push -u origin main
```

### 3. مثال كامل:

```bash
git init
git add .
git commit -m "Initial commit: Telegram AI Bot for Anas Rabaya"
git remote add origin https://github.com/anasrabaya/telegram-ai-bot.git
git branch -M main
git push -u origin main
```

---

## ⚠️ تحذيرات مهمة:

### ✅ تم إضافة .gitignore
- ملف `.env` **لن يُرفع** (آمن!)
- ملفات Python المؤقتة لن تُرفع
- ملفات الاختبار لن تُرفع

### 🔒 الأمان:
- **لا ترفع ملف .env أبداً!**
- التوكنات والمفاتيح السرية محمية في `.gitignore`
- يمكنك إضافة ملف `.env.example` بدون القيم الحقيقية

---

## بعد النشر:

### إضافة ملف .env.example (اختياري):

أنشئ ملف `.env.example` في المشروع:

```env
TELEGRAM_TOKEN=your_bot_token_here
GEMINI_API_KEY=your_gemini_key_here
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_supabase_key
```

ثم:
```bash
git add .env.example
git commit -m "Add .env.example"
git push
```

---

## تحديثات مستقبلية:

عند إجراء تغييرات:

```bash
git add .
git commit -m "وصف التغييرات"
git push
```
