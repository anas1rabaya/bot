import os
import logging
import uuid
from typing import Dict, List
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import requests
from supabase import Client, create_client

# تحميل المتغيرات من ملف .env
load_dotenv()

# إعداد السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# النسخة الرقمية
DIGITAL_SELF = {
    "name": "أنس ربايعة",
    "linkedin": "https://www.linkedin.com/in/anas-rabaya"
}

# إعداد Groq API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_API_URL = "https://api.groq.com/v1/generate"  # مثال عام، عدّل حسب مستندات Groq

# إعداد Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = None

try:
    if SUPABASE_URL and SUPABASE_KEY:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("✅ تم الاتصال بـ Supabase بنجاح")
except Exception as e:
    logger.error(f"خطأ أثناء الاتصال بـ Supabase: {e}")

# إدارة الجلسات
user_sessions: Dict[int, str] = {}
def get_or_create_session(user_id: int) -> str:
    if user_id not in user_sessions:
        user_sessions[user_id] = str(uuid.uuid4())
    return user_sessions[user_id]

def save_conversation(user_id: int, username: str, message: str, response: str, session_id: str):
    if not supabase:
        return
    try:
        data = {
            "user_id": user_id,
            "user_name": username or "unknown",
            "message": message,
            "response": response,
            "timestamp": datetime.utcnow().isoformat(),
            "session_id": session_id
        }
        supabase.table("conversations").insert(data).execute()
    except Exception as e:
        logger.error(f"خطأ في حفظ المحادثة: {e}")

def get_conversation_history(user_id: int, session_id: str = None, limit: int = 5) -> List[Dict]:
    if not supabase:
        return []
    try:
        query = supabase.table("conversations").select("*").eq("user_id", user_id)
        if session_id:
            query = query.eq("session_id", session_id)
        response = query.order("timestamp", desc=True).limit(limit).execute()
        return response.data if response.data else []
    except Exception as e:
        logger.error(f"خطأ في جلب تاريخ المحادثات: {e}")
        return []

# التعامل مع الأسئلة الخاصة
def handle_special_questions(user_message: str) -> str:
    msg = user_message.lower()
    if any(word in msg for word in ["مين أنت", "من أنت", "شو اسمك"]):
        return "أنا أنس ربايعة 👨‍💻 مبرمج ذكاء اصطناعي من فلسطين، متخصص ببناء حلول تقنية ذكية 🚀"
    if any(word in msg for word in ["كم سعر", "بكم", "السعر"]):
        return "الأسعار تختلف حسب المشروع 💰 تواصل معي على LinkedIn لتحديد السعر المناسب: " + DIGITAL_SELF["linkedin"]
    if any(word in msg for word in ["كيف أتواصل", "linkedin", "تواصل"]):
        return f"تواصل معي على LinkedIn: {DIGITAL_SELF['linkedin']} 💼"
    return None

# توليد الرد باستخدام Groq API
def generate_response_with_groq(user_message: str, user_id: int, session_id: str) -> str:
    # تحقق من الأسئلة الخاصة أولاً
    special = handle_special_questions(user_message)
    if special:
        return special
    
    history = get_conversation_history(user_id, session_id, limit=5)
    context = "أنت نسخة رقمية من أنس ربايعة، مبرمج AI.\n"
    if history:
        context += "\nالمحادثات السابقة:\n"
        for conv in reversed(history):
            context += f"المستخدم: {conv.get('message')}\nأنت: {conv.get('response')}\n"
    prompt = f"{context}\nالمستخدم: {user_message}\nأنت:"

    try:
        headers = {"Authorization": f"Bearer {GROQ_API_KEY}", "Content-Type": "application/json"}
        payload = {"prompt": prompt, "max_tokens": 200}
        res = requests.post(GROQ_API_URL, json=payload, headers=headers, timeout=15)
        res.raise_for_status()
        data = res.json()
        return data.get("text", "عذراً، لم أستطع توليد رد. حاول مرة أخرى.")
    except Exception as e:
        logger.error(f"خطأ في Groq API: {e}")
        return "حدث خطأ أثناء معالجة رسالتك 😅"

# أوامر Telegram
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_sessions[update.effective_user.id] = str(uuid.uuid4())
    await update.message.reply_text(
        "مرحباً! 👋 أنا النسخة الرقمية من أنس ربايعة. أرسل رسالتك وسأرد عليك!"
    )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    session_id = get_or_create_session(user.id)
    user_message = update.message.text
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    response = generate_response_with_groq(user_message, user.id, session_id)
    await update.message.reply_text(response)
    save_conversation(user.id, user.username or "unknown", user_message, response, session_id)

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"حدث خطأ: {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text("عذراً، حدث خطأ تقني. حاول مرة أخرى 😅")

# تشغيل البوت
def main():
    BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not BOT_TOKEN:
        logger.error("TELEGRAM_TOKEN غير موجود!")
        return

    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)
    logger.info("🚀 جارٍ تشغيل البوت...")
    application.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()
