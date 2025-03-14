from telegram import Update
from telegram.ext import Application, MessageHandler, filters, CallbackContext

# ضع التوكن الخاص بك هنا
TOKEN = "7554502855:AAFR5_19Tjb2REX9vw80VHMos_bYJKH2iIc"

async def handle_messages(update: Update, context: CallbackContext):
    await update.message.reply_text("—")  # المسطرة بعد كل رسالة

def main():
    # إنشاء التطبيق (بدلاً من Updater)
    app = Application.builder().token(TOKEN).build()

    # إضافة معالج الرسائل
    app.add_handler(MessageHandler(filters.ALL, handle_messages))

    # تشغيل البوت
    app.run_polling()

if __name__ == "__main__":
    main()