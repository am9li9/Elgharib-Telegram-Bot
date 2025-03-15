from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, CallbackContext

# ✅ معلومات البوت
TOKEN = "7554502855:AAFR5_19Tjb2REX9vw80VHMos_bYJKH2iIc"
ADMIN_ID = 634869382  # ✅ معرف الأدمن

# ✅ متغير لتحديد حالة إشعارات الدخول
notify_new_users = True

# ✅ دالة الترحيب عند استخدام /start
async def start(update: Update, context: CallbackContext) -> None:
    bot_username = context.bot.username
    keyboard = [[InlineKeyboardButton("📊 لوحة التحكم", callback_data="panel")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    welcome_message = f"""أهلًا وسهلًا بك في بوت {bot_username} 🚀  
الغريب للمسطرة —  
يمكنك رفع البوت في مجموعتك وسأعمل على توفيرها بعد كل رسالة يتم إرسالها.  

تم برمجة وتطوير البوت من قبل:  
أحمد الغريب  

📌 حساباتي: @quranbng  @quranfont  @Am9li9  
"""
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# ✅ دالة إرسال المسطرة بعد كل رسالة
async def send_separator(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("—")

# ✅ دالة لوحة التحكم
async def panel(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id if query else update.message.from_user.id

    if user_id != ADMIN_ID:
        await (query.message.reply_text("❌ ليس لديك صلاحية لاستخدام هذه الميزة.") if query else update.message.reply_text("❌ ليس لديك صلاحية لاستخدام هذه الميزة."))
        return

    status = "✅ مفعّل" if notify_new_users else "❌ معطّل"
    keyboard = [
        [InlineKeyboardButton(f"🔔 إشعارات الدخول: {status}", callback_data="toggle_notify")],
        [InlineKeyboardButton("🔄 تحديث القائمة", callback_data="panel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    if query:
        await query.message.edit_text("🔧 **لوحة التحكم**", reply_markup=reply_markup)
    else:
        await update.message.reply_text("🔧 **لوحة التحكم**", reply_markup=reply_markup)

# ✅ دالة تبديل حالة إشعارات الدخول
async def toggle_notify(update: Update, context: CallbackContext) -> None:
    global notify_new_users
    query = update.callback_query

    if query.from_user.id != ADMIN_ID:
        await query.answer("❌ ليس لديك صلاحية لاستخدام هذه الميزة.", show_alert=True)
        return

    notify_new_users = not notify_new_users
    await panel(update, context)

# ✅ دالة إرسال إشعار عند دخول عضو جديد
async def new_member(update: Update, context: CallbackContext) -> None:
    global notify_new_users
    if notify_new_users:
        user = update.effective_user
        total_users = context.bot_data.get('user_count', 0) + 1
        user_info = f"""🚀 **عضو جديد في البوت!**  
👤 الاسم: {user.full_name}  
🔗 المعرف: @{user.username if user.username else 'لا يوجد'}  
🆔 الايدي: `{user.id}`  
👥 إجمالي المستخدمين: {total_users}"""
        
        await context.bot.send_message(chat_id=ADMIN_ID, text=user_info)
    
    context.bot_data['user_count'] = total_users

# ✅ إنشاء التطبيق وإضافة الأوامر
def main():
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_separator))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, new_member))
    app.add_handler(CallbackQueryHandler(panel, pattern="panel"))
    app.add_handler(CallbackQueryHandler(toggle_notify, pattern="toggle_notify"))

    print("✅ البوت يعمل الآن...")
    app.run_polling()

if __name__ == "__main__":
    main()