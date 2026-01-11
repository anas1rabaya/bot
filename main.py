import os
import logging
import uuid
from typing import Dict, List
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai
from supabase import create_client, Client
import asyncio

# تحميل المتغيرات من ملف .env
load_dotenv()

# إعدادات السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# معلومات النسخة الرقمية
DIGITAL_SELF = {
    "name": "أنس ربايعة",
    "linkedin": "https://www.linkedin.com/in/anas-rabaya"
}

# System Prompt للـ Gemini
SYSTEM_PROMPT = """أنت أنس ربايعة، مبرمج AI من فلسطين...
...نسخة رقمية من أنس، تساعد الناس 24/7"""

# إعداد Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None
    logger.warning("GEMINI_API_KEY غير موجود!")

# إعداد Supabase
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: Client = None

if SUPABASE_URL and SUPABASE_KEY:
    try:
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        logger.info("تم الاتصال بـ Supabase بنجاح")
    except Exception as e:
        logger.error(f"خطأ أثناء الاتصال بـ Supabase: {e}")
else:
    logger.warning("Supabase credentials غير موجودة!")

# إدارة جلسات المستخدمين
user_sessions: Dict[int, str] = {}

def get_or_create_session(user_id: int) -> str:
    if user_id not in user_sessions:
        user_sessions[user_id] = str(uuid.uuid4())
    return user_sessions[user_id]

# حفظ المحادثات في Supabase
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

# جلب تاريخ المحادثات
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
    message_lower = user_message.lower().strip()
    if any(word in message_lower for word in ["مين أنت", "من أنت", "شو اسمك", "تعرف نفسك"]):
        return "أنا أنس ربايعة 👨‍💻 مبرمج ذكاء اصطناعي من فلسطين"
    if any(word in message_lower for word in ["كم سعر", "بكم", "السعر", "التكلفة"]):
        return "الأسعار تختلف حسب المشروع 💰 تواصل معي وبنتفق على أفضل سعر"
    if any(word in message_lower for word in ["كيف أتواصل", "لينكد إن", "linkedin", "تواصل"]):
        return f"تواصل معي على LinkedIn: {DIGITAL_SELF['linkedin']}"
    return None

# توليد الردود باستخدام Gemini
def generate_response(user_message: str, user_id: int, session_id: str) -> str:
    special_response = handle_special_questions(user_message)
    if special_response:
        return special_response

    if not model:
        return "مرحباً! 👋 خدمة الذكاء الاصطناعي غير متاحة حالياً."

    try:
        history = get_conversation_history(user_id, session_id, limit=5)
        context = SYSTEM_PROMPT
        if history:
            context += "\n\nالمحادثات السابقة:\n"
            for conv in reversed(history):
                context += f"المستخدم: {conv.get('message', '')}\nأنت: {conv.get('response', '')}\n\n"
        prompt = f"{context}\n\nالمستخدم: {user_message}\nأنت:"
        response = model.generate_content(prompt)
        return response.text.strip()
    except Exception as e:
        logger.error(f"خطأ في توليد الرد: {e}")
        return "عذراً، حدث خطأ أثناء معالجة رسالتك."

# معالج /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_sessions[user_id] = str(uuid.uuid4())
    await update.message.reply_text("مرحباً! 👋 أنا أنس الرقمية 🚀")

# معالج الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_message = update.message.text
    if not user_message:
        return
    session_id = get_or_create_session(user.id)
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    response = generate_response(user_message, user.id, session_id)
    await update.message.reply_text(response)
    save_conversation(user.id, user.username or user.first_name or "unknown", user_message, response, session_id)

# معالج الأخطاء
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"حدث خطأ: {context.error}")
    if update and update.effective_message:
        await update.effective_message.reply_text("حدث خطأ تقني. جرب مرة أخرى 😅")

# تشغيل البوت باستخدام asyncio.run
async def start_bot():
    BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not BOT_TOKEN or BOT_TOKEN == "your_bot_token_here":
        logger.error("TELEGRAM_TOKEN غير موجود أو غير صحيح!")
        return

    application = Application.builder().token(BOT_TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    application.add_error_handler(error_handler)

    logger.info(f"✅ تم الاتصال بالبوت")
    await application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True
    )

if __name__ == "__main__":
    asyncio.run(start_bot())
