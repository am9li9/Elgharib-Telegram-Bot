import json
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# ضع هنا التوكن الخاص بالبوت
TOKEN = "7554502855:AAFR5_19Tjb2REX9vw80VHMos_bYJKH2iIc"

# المعرف الخاص بك كمشرف
ADMIN_ID = 123456789  # ضع هنا معرفك في تيليجرام

# اسم الملف الذي سيتم فيه تخزين المستخدمين
USER_DATA_FILE = "users.json"

# تحميل المستخدمين من الملف عند بدء التشغيل
def load_users():
    try:
        with open(USER_DATA_FILE, "r") as file:
            return set(json.load(file))
    except (FileNotFoundError, json.JSONDecodeError):
        return set()

# حفظ المستخدمين إلى الملف
def save_users():
    with open(USER_DATA_FILE, "w") as file:
        json.dump(list(users), file)

# قائمة المستخدمين الذين استخدموا البوت
users = load_users()

# دالة الترحيب عند استخدام /start
async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in users:
        users.add(user_id)
        save_users()  # حفظ المستخدم في الملف عند إضافته

    bot_username = context.bot.username  
    welcome_message = f"""أهلًا وسهلًا بك في بوت {bot_username} 🚀  
الغريب للمسطرة —  
يمكنك رفع البوت في مجموعتك وسأعمل على توفيرها بعد كل رسالة يتم إرسالها.  

تم برمجة وتطوير البوت من قبل:  
أحمد الغريب  

حساباتي ↓ 
📌 @quranbng  @quranfont  @Am9li9  
"""
    await update.message.reply_text(welcome_message)

# دالة إرسال المسطرة بعد كل رسالة
async def send_separator(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("—")

# دالة عرض عدد المستخدمين (للمشرف فقط)
async def stats(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id == ADMIN_ID:
        await update.message.reply_text(f"📊 عدد المستخدمين الذين استخدموا البوت: {len(users)}")
    else:
        await update.message.reply_text("❌ ليس لديك صلاحية لاستخدام هذا الأمر.")

# دالة لإيقاف البوت (للمشرف فقط)
async def stop_bot(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id == ADMIN_ID:
        await update.message.reply_text("🛑 تم إيقاف البوت.")
        await context.application.stop()
    else:
        await update.message.reply_text("❌ ليس لديك صلاحية لاستخدام هذا الأمر.")

# إنشاء التطبيق وإضافة الأوامر
def main():
    app = Application.builder().token(TOKEN).build()
    
    # أوامر البوت
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("stats", stats))  # عرض عدد المستخدمين
    app.add_handler(CommandHandler("stop", stop_bot))  # إيقاف البوت

    # إضافة معالج للرسائل النصية
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_separator))

    # تشغيل البوت
    print("البوت يعمل الآن...")
    app.run_polling()

if __name__ == "__main__":
    main()