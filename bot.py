from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext

# ضع هنا التوكن الخاص بالبوت
TOKEN = "7554502855:AAFR5_19Tjb2REX9vw80VHMos_bYJKH2iIc"

# دالة الترحيب عند استخدام /start
async def start(update: Update, context: CallbackContext) -> None:
    bot_username = context.bot.username  # جلب اسم البوت تلقائيًا
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

# إنشاء التطبيق وإضافة الأوامر
def main():
    app = Application.builder().token(TOKEN).build()
    
    # إضافة أمر /start
    app.add_handler(CommandHandler("start", start))

    # إضافة معالج للرسائل النصية العادية
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_separator))

    # تشغيل البوت
    print("البوت يعمل الآن...")
    app.run_polling()

if __name__ == "__main__":
    main()