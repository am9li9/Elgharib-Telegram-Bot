import json
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, CallbackContext

# ضع هنا التوكن الخاص بالبوت
TOKEN = "7554502855:AAFR5_19Tjb2REX9vw80VHMos_bYJKH2iIc"

# المعرف الخاص بك كمشرف
ADMIN_ID = 123456789  # ضع هنا معرفك في تيليجرام

# اسم ملف تخزين المستخدمين
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

# قائمة المستخدمين
users = load_users()

# حالة البوت (تشغيل/إيقاف)
bot_active = True

# تفعيل/تعطيل المسطرة
send_separator_enabled = True

# دالة الترحيب عند استخدام /start
async def start(update: Update, context: CallbackContext) -> None:
    user_id = update.effective_user.id
    if user_id not in users:
        users.add(user_id)
        save_users()  # حفظ المستخدم الجديد

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
    if send_separator_enabled:
        await update.message.reply_text("—")

# دالة عرض لوحة التحكم للمشرف
async def panel(update: Update, context: CallbackContext) -> None:
    if update.effective_user.id != ADMIN_ID:
        await update.message.reply_text("❌ ليس لديك صلاحية لاستخدام هذه الميزة.")
        return

    keyboard = [
        [InlineKeyboardButton("📊 عرض عدد المستخدمين", callback_data="show_users")],
        [InlineKeyboardButton("🛑 إيقاف البوت" if bot_active else "✅ تشغيل البوت", callback_data="toggle_bot")],
        [InlineKeyboardButton("🔄 تعطيل المسطرة" if send_separator_enabled else "✅ تفعيل المسطرة", callback_data="toggle_separator")],
        [InlineKeyboardButton("📢 إرسال رسالة جماعية", callback_data="broadcast")]
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("🔧 **لوحة تحكم البوت**", reply_markup=reply_markup)

# دالة التعامل مع أزرار لوحة التحكم
async def button_handler(update: Update, context: CallbackContext) -> None:
    global bot_active, send_separator_enabled

    query = update.callback_query
    user_id = query.from_user.id

    if user_id != ADMIN_ID:
        await query.answer("❌ ليس لديك صلاحية لاستخدام هذه الميزة.", show_alert=True)
        return

    if query.data == "show_users":
        await query.answer()
        await query.message.reply_text(f"📊 عدد المستخدمين الذين استخدموا البوت: {len(users)}")

    elif query.data == "toggle_bot":
        bot_active = not bot_active
        new_status = "✅ تم تشغيل البوت" if bot_active else "🛑 تم إيقاف البوت"
        await query.answer(new_status, show_alert=True)
        await query.message.edit_text(new_status)

    elif query.data == "toggle_separator":
        send_separator_enabled = not send_separator_enabled
        new_status = "✅ تم تفعيل المسطرة" if send_separator_enabled else "❌ تم تعطيل المسطرة"
        await query.answer(new_status, show_alert=True)
        await query.message.edit_text(new_status)

    elif query.data == "broadcast":
        await query.answer()
        await query.message.reply_text("✍️ أرسل الآن الرسالة التي تريد إرسالها لجميع المستخدمين.")
        context.user_data["waiting_for_broadcast"] = True

# دالة استقبال الرسائل الجماعية من المشرف
async def broadcast_message(update: Update, context: CallbackContext) -> None:
    if context.user_data.get("waiting_for_broadcast") and update.effective_user.id == ADMIN_ID:
        message = update.message.text
        context.user_data["waiting_for_broadcast"] = False

        sent_count = 0
        for user_id in users:
            try:
                await context.bot.send_message(chat_id=user_id, text=message)
                sent_count += 1
            except:
                continue

        await update.message.reply_text(f"📢 تم إرسال الرسالة إلى {sent_count} مستخدم.")

# إنشاء التطبيق وإضافة الأوامر
def main():
    app = Application.builder().token(TOKEN).build()
    
    # أوامر البوت
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("panel", panel))  # لوحة التحكم

    # استقبال الردود على الأزرار
    app.add_handler(CallbackQueryHandler(button_handler))

    # استقبال الرسائل النصية
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, broadcast_message))

    # إضافة معالج للرسائل النصية العادية لتفعيل المسطرة
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_separator))

    # تشغيل البوت
    print("البوت يعمل الآن...")
    app.run_polling()

if __name__ == "__main__":
    main()