from telegram import Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, CallbackContext
import json

# ✅ ضع هنا التوكن الخاص بالبوت
TOKEN = "7554502855:AAFR5_19Tjb2REX9vw80VHMos_bYJKH2iIc"
ADMIN_ID = 634869382  # ✅ ضع هنا ID الأدمن

# ✅ ملف لحفظ بيانات المستخدمين
USERS_DATA_FILE = "users.json"

# ✅ تحميل بيانات المستخدمين من ملف JSON
def load_users():
    try:
        with open(USERS_DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"users": [], "notifications": True}

# ✅ حفظ بيانات المستخدمين
def save_users(data):
    with open(USERS_DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

# ✅ دالة الترحيب عند استخدام /start
async def start(update: Update, context: CallbackContext) -> None:
    user = update.effective_user
    users_data = load_users()

    # ✅ إضافة المستخدم الجديد إلى القائمة إذا لم يكن موجودًا
    if user.id not in users_data["users"]:
        users_data["users"].append(user.id)
        save_users(users_data)

        # ✅ إرسال إشعار دخول مستخدم جديد إذا كان مفعلاً
        if users_data["notifications"]:
            admin_message = f"🚀 مستخدم جديد دخل إلى البوت!\n\n👤 الاسم: {user.full_name}\n🆔 ID: {user.id}\n📌 اليوزر: @{user.username if user.username else 'لا يوجد'}\n👥 العدد الكلي: {len(users_data['users'])}"
            await context.bot.send_message(chat_id=ADMIN_ID, text=admin_message)

    # ✅ إنشاء لوحة التحكم
    keyboard = [
        [InlineKeyboardButton("📊 لوحة التحكم", callback_data="panel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_message = f"""أهلًا وسهلًا بك في بوت {context.bot.username} 🚀  
الغريب للمسطرة —  
يمكنك رفع البوت في مجموعتك وسأعمل على توفيرها بعد كل رسالة يتم إرسالها.  

تم برمجة وتطوير البوت من قبل:  
أحمد الغريب  

حساباتي ↓  
📌 @quranbng  @quranfont  @Am9li9  
"""
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# ✅ دالة لوحة التحكم
async def panel(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id

    if user_id != ADMIN_ID:
        await query.answer("❌ ليس لديك صلاحية لاستخدام هذه الميزة.", show_alert=True)
        return

    users_data = load_users()
    status = "🔔 مفعّل" if users_data["notifications"] else "🔕 معطل"
    
    keyboard = [
        [InlineKeyboardButton("📢 إرسال إذاعة", callback_data="broadcast")],
        [InlineKeyboardButton(f"🔄 إشعارات الدخول: {status}", callback_data="toggle_notifications")],
        [InlineKeyboardButton("🔄 تحديث القائمة", callback_data="panel")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    panel_message = f"""📊 **لوحة التحكم**  
👥 عدد المستخدمين: {len(users_data["users"])}  
⚙️ إعدادات التحكم متاحة أدناه ⬇️"""

    await query.message.edit_text(panel_message, reply_markup=reply_markup)

# ✅ تبديل إشعارات دخول المستخدمين الجدد
async def toggle_notifications(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id

    if user_id != ADMIN_ID:
        await query.answer("❌ ليس لديك صلاحية لاستخدام هذه الميزة.", show_alert=True)
        return

    users_data = load_users()
    users_data["notifications"] = not users_data["notifications"]
    save_users(users_data)

    await panel(update, context)

# ✅ دالة إرسال الإذاعة لكل المستخدمين
async def broadcast(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id

    if user_id != ADMIN_ID:
        await query.answer("❌ ليس لديك صلاحية لاستخدام هذه الميزة.", show_alert=True)
        return

    await query.message.reply_text("✍️ أرسل الآن الرسالة التي تريد بثها لجميع المستخدمين.")
    context.user_data["broadcasting"] = True

# ✅ استقبال رسالة الإذاعة وإرسالها للمستخدمين
async def handle_broadcast(update: Update, context: CallbackContext) -> None:
    if context.user_data.get("broadcasting") and update.message.from_user.id == ADMIN_ID:
        message_text = update.message.text
        users_data = load_users()

        # ✅ إرسال الرسالة لكل المستخدمين
        for user_id in users_data["users"]:
            try:
                await context.bot.send_message(chat_id=user_id, text=f"📢 **رسالة إدارية:**\n\n{message_text}")
            except:
                pass

        await update.message.reply_text("✅ تم إرسال الإذاعة بنجاح!")
        context.user_data["broadcasting"] = False

# ✅ دالة إرسال الشرطة الصغيرة "-" بعد كل رسالة
async def send_separator(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("-")

# ✅ استقبال جميع أنواع الرسائل والرد عليها
async def handle_all_messages(update: Update, context: CallbackContext) -> None:
    message = update.message

    # ✅ التأكد من أن الرسالة ليست أمرًا للبوت
    if not message.text or not message.text.startswith("/"):
        await message.reply_text("-")

# ✅ إنشاء التطبيق وإضافة الأوامر
def main():
    app = Application.builder().token(TOKEN).build()
    
    # ✅ أوامر الإدارة
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(panel, pattern="panel"))
    app.add_handler(CallbackQueryHandler(toggle_notifications, pattern="toggle_notifications"))
    app.add_handler(CallbackQueryHandler(broadcast, pattern="broadcast"))
    
    # ✅ استقبال جميع أنواع الرسائل والرد عليها بـ "-"
    app.add_handler(MessageHandler(filters.ALL, handle_all_messages))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_broadcast))

    # ✅ تشغيل البوت
    print("🤖 البوت يعمل الآن...")
    app.run_polling()

if __name__ == "__main__":
    main()