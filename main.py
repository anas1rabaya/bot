import os
import logging
import uuid
from typing import Dict, List
from datetime import datetime
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import google.generativeai as genai
from supabase import SyncClient
from gotrue import SyncGoTrueClient

# تحميل المتغيرات من ملف .env
load_dotenv()

# إعدادات السجلات
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# معلومات النسخة الرقمية - أنس ربايعة
DIGITAL_SELF = {
    "name": "أنس ربايعة",
    "location": "فلسطين 🇵🇸",
    "education": "بكالوريوس GIS - الجامعة العربية الأمريكية",
    "specialization": "مبرمج AI وحلول ذكاء اصطناعي",
    "services": [
        "بناء مواقع ويب احترافية",
        "تطوير بوتات ذكية مدعومة بالـ AI",
        "حلول الذكاء الاصطناعي المخصصة",
        "أتمتة وحلول تقنية متقدمة",
        "تطوير تطبيقات ويب وموبايل"
    ],
    "skills": [
        "Python & AI Development",
        "Web Development (Frontend & Backend)",
        "Telegram & WhatsApp Bots",
        "Machine Learning & AI Integration",
        "GIS & Spatial Analysis",
        "Cloud Deployment & Automation"
    ],
    "linkedin": "https://www.linkedin.com/in/anas-rabaya"
}

# System Prompt للـ Gemini
SYSTEM_PROMPT = """أنت أنس ربايعة، مبرمج AI من فلسطين، خريج GIS من الجامعة العربية الأمريكية.

تخصصك: حلول الذكاء الاصطناعي، مواقع ويب، بوتات ذكية، وأتمتة.

أسلوبك:
- عفوي وودود
- مختصر ومباشر
- استخدم إيموجي بشكل طبيعي
- رد بالعربية (إلا إذا سألوك بالإنجليزي)

القواعد:
- لا تذكر أسعار محددة أبداً - قل "تواصل معي وبنتفق على أفضل سعر يناسبك"
- كن متحمساً وإيجابياً دائماً
- اسأل عن التفاصيل قبل تقديم الحلول
- وجّه للتواصل عبر LinkedIn للمشاريع الجدية: https://www.linkedin.com/in/anas-rabaya
- اجعل الردود قصيرة (2-4 جمل غالباً)
- استخدم أمثلة عملية عند الشرح

تذكر: أنت نسخة رقمية من أنس، تساعد الناس 24/7"""

# إعداد Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel('gemini-pro')
else:
    model = None
    logger.warning("GEMINI_API_KEY غير موجود!")

# إعداد Supabase بدون create_client
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase: SyncClient = None
auth_client: SyncGoTrueClient = None

if SUPABASE_URL and SUPABASE_KEY:
    try:
        # إنشاء عميل Supabase
        supabase = SyncClient(SUPABASE_URL, SUPABASE_KEY, options={})
        
        # إنشاء Auth Client منفصل
        auth_client = SyncGoTrueClient(SUPABASE_URL, supabase)
        
        logger.info("تم الاتصال بـ Supabase وAuth بنجاح")
    except Exception as e:
        logger.error(f"خطأ أثناء إنشاء عميل Supabase: {e}")
else:
    logger.warning("Supabase credentials غير موجودة!")

# إنشاء جدول المحادثات في Supabase (إذا لم يكن موجوداً)
def init_database():
    """تهيئة قاعدة البيانات"""
    if not supabase:
        return
    
    try:
        logger.info("قاعدة البيانات جاهزة")
    except Exception as e:
        logger.error(f"خطأ في تهيئة قاعدة البيانات: {e}")

# تخزين session_id لكل مستخدم
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
        logger.info(f"تم حفظ المحادثة للمستخدم {user_id}")
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

def handle_special_questions(user_message: str) -> str:
    message_lower = user_message.lower().strip()
    
    if any(word in message_lower for word in ["مين أنت", "من أنت", "شو اسمك", "تعرف نفسك"]):
        return "أنا أنس ربايعة 👨‍💻 مبرمج ذكاء اصطناعي من فلسطين، متخصص ببناء حلول تقنية ذكية. درست GIS وصار عندي خبرة قوية بالـ AI والويب ديفلوبمنت 🚀"
    
    if any(word in message_lower for word in ["كم سعر", "بكم", "السعر", "التكلفة", "الثمن"]):
        return "الأسعار تختلف حسب المشروع والمميزات 💰 لكن أضمنلك أسعار منافسة وجودة عالية. حاب تحكيلي عن مشروعك وبعطيك سعر مناسب؟"
    
    if any(word in message_lower for word in ["كيف أتواصل", "رابط", "لينكد إن", "linkedin", "تواصل"]):
        return f"تواصل معي على LinkedIn للمشاريع الجدية: {DIGITAL_SELF['linkedin']} 💼"
    
    if any(word in message_lower for word in ["أمثلة", "مشاريع", "أعمال", "portfolio", "أعمالك"]):
        return "بشتغل على مشاريع متنوعة: بوتات ذكية للشركات، مواقع ويب تفاعلية، أنظمة أتمتة، وحلول AI مخصصة. حاب تشوف أمثلة لنوع معين؟ 💼"
    
    return None

def generate_response(user_message: str, user_id: int, session_id: str) -> str:
    special_response = handle_special_questions(user_message)
    if special_response:
        return special_response
    
    if not model:
        logger.warning("Gemini API غير متاح - استخدام رد افتراضي")
        return """مرحباً! 👋

أنا أنس ربايعة - نسخة رقمية ذكية

للأسف، خدمة الذكاء الاصطناعي غير متاحة حالياً. لكن يمكنني مساعدتك:

🤖 حلول الذكاء الاصطناعي
💻 مواقع ويب احترافية
🔧 بوتات ذكية وأتمتة

تواصل معي على LinkedIn للمشاريع الجدية:
https://www.linkedin.com/in/anas-rabaya 💼"""
    
    try:
        history = get_conversation_history(user_id, session_id, limit=5)
        context = SYSTEM_PROMPT
        if history:
            context += "\n\nالمحادثات السابقة في هذه الجلسة:\n"
            for conv in reversed(history):
                context += f"المستخدم: {conv.get('message', '')}\n"
                context += f"أنت: {conv.get('response', '')}\n\n"
        prompt = f"{context}\n\nالمستخدم: {user_message}\nأنت:"
        response = model.generate_content(prompt)
        return response.text.strip()
    
    except Exception as e:
        logger.error(f"خطأ في توليد الرد: {e}")
        import traceback
        traceback.print_exc()
        return "عذراً، حدث خطأ أثناء معالجة رسالتك. لكن يمكنني مساعدتك! تواصل معي على LinkedIn: https://www.linkedin.com/in/anas-rabaya 💼"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    user_sessions[user_id] = str(uuid.uuid4())
    welcome_message = """مرحباً! 👋

أنا أنس ربايعة - نسخة رقمية ذكية

متخصص في:
🤖 حلول الذكاء الاصطناعي
💻 مواقع ويب احترافية
🔧 بوتات ذكية وأتمتة

أي مشروع في بالك، أقدر أساعدك فيه بجودة عالية وأسعار منافسة

كيف أقدر أخدمك؟ 🚀"""
    await update.message.reply_text(welcome_message)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        user = update.effective_user
        user_message = update.message.text
        if not user_message:
            return
        logger.info(f"رسالة من {user.id} ({user.username}): {user_message}")
        session_id = get_or_create_session(user.id)
        await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
        response = generate_response(user_message, user.id, session_id)
        await update.message.reply_text(response)
        save_conversation(
            user_id=user.id,
            username=user.username or user.first_name or "unknown",
            message=user_message,
            response=response,
            session_id=session_id
        )
        logger.info(f"تم إرسال الرد للمستخدم {user.id}")
    except Exception as e:
        logger.error(f"خطأ في معالجة الرسالة: {e}")
        import traceback
        traceback.print_exc()
        try:
            await update.message.reply_text("عذراً، حدث خطأ غير متوقع. حاول مرة أخرى! 😅")
        except:
            pass

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"حدث خطأ: {context.error}")
    if update and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "عذراً، حدث خطأ تقني. جرب مرة أخرى بعد قليل! 😅"
            )
        except:
            pass

def main():
    BOT_TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not BOT_TOKEN or BOT_TOKEN == "your_bot_token_here":
        print("❌ TELEGRAM_TOKEN غير موجود أو غير صالح!")
        return
    try:
        from telegram import Bot
        test_bot = Bot(token=BOT_TOKEN)
        bot_info = test_bot.get_me()
        print(f"✅ تم الاتصال بالبوت: @{bot_info.username}")
    except Exception as e:
        print(f"❌ خطأ في الاتصال بالبوت: {e}")
        return
    init_database()
    try:
        application = Application.builder().token(BOT_TOKEN).build()
        application.add_handler(CommandHandler("start", start))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        application.add_error_handler(error_handler)
        print("\n🚀 جارٍ تشغيل البوت...")
        print(f"ℹ️  Gemini API: {'متاح ✓' if model else 'غير متاح ✗'}")
        print(f"ℹ️  Supabase: {'متاح ✓' if supabase else 'غير متاح ✗'}\n")
        logger.info("جارٍ تشغيل البوت...")
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )
    except KeyboardInterrupt:
        print("\n\n⏹️  تم إيقاف البوت")
    except Exception as e:
        print(f"\n❌ خطأ أثناء تشغيل البوت: {e}")
        logger.error(f"خطأ أثناء تشغيل البوت: {e}")

if __name__ == "__main__":
    main()
