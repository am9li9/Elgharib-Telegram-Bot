from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, CallbackContext
import json

# --- إعدادات البوت ---
TOKEN = "7554502855:AAFR5_19Tjb2REX9vw80VHMos_bYJKH2iIc"
ADMIN_ID = 634869382  # معرف المشرف الأساسي
DATA_FILE = "bot_data.json"

# --- تحميل البيانات ---
def load_data():
    try:
        with open(DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"users": [], "notify_join": True}

def save_data(data):
    with open(DATA_FILE, "w") as file:
        json.dump(data, file, indent=4)

data = load_data()

# --- دالة الترحيب عند /start ---
async def start(update: Update, context: CallbackContext) -> None:
    user = update.message.from_user
    user_info = {"id": user.id, "name": user.full_name, "username": user.username}

    # التحقق من المستخدم الجديد
    if user_info not in data["users"]:
        data["users"].append(user_info)
        save_data(data)

        # إشعار المشرف بدخول عضو جديد
        if data["notify_join"]:
            admin_message = f"🚀 **عضو جديد انضم للبوت**\n\n👤 الاسم: {user.full_name}\n🔹 يوزر: @{user.username if user.username else 'لا يوجد'}\n🆔 ID: `{user.id}`\n\n📊 إجمالي المستخدمين: {len(data['users'])}"
            await context.bot.send_message(chat_id=ADMIN_ID, text=admin_message, parse_mode="Markdown")

    # لوحة التحكم
    keyboard = [[InlineKeyboardButton("🔧 لوحة التحكم", callback_data="panel")]]
    reply_markup = InlineKeyboardMarkup(keyboard)

    welcome_message = f"""أهلًا وسهلًا بك في بوت {context.bot.username} 🚀  
الغريب للمسطرة —  
يمكنك رفع البوت في مجموعتك وسأعمل على توفيرها بعد كل رسالة يتم إرسالها.  

تم برمجة وتطوير البوت من قبل:  
أحمد الغريب  

📌 @quranbng  @quranfont  @Am9li9  
"""
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

# --- دالة لوحة التحكم ---
async def panel(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id

    if user_id != ADMIN_ID:
        await query.answer("❌ ليس لديك صلاحية لاستخدام هذه الميزة.", show_alert=True)
        return

    keyboard = [
        [InlineKeyboardButton("📢 إرسال إذاعة", callback_data="broadcast")],
        [InlineKeyboardButton("🚀 حالة الإشعارات", callback_data="toggle_notify")],
        [InlineKeyboardButton("📊 عدد المستخدمين", callback_data="users_count")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await query.message.edit_text("🔧 **لوحة التحكم**", reply_markup=reply_markup, parse_mode="Markdown")

# --- دالة إرسال الشرطة الصغيرة بعد كل رسالة ---
async def send_separator(update: Update, context: CallbackContext) -> None:
    if update.message.text.startswith("/"):
        return  # لا نرد على الأوامر
    await update.message.reply_text("-")

# --- تبديل إشعارات دخول المستخدمين ---
async def toggle_notify(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id

    if user_id != ADMIN_ID:
        await query.answer("❌ ليس لديك صلاحية لاستخدام هذه الميزة.", show_alert=True)
        return

    data["notify_join"] = not data["notify_join"]
    save_data(data)

    status = "✅ مفعلة" if data["notify_join"] else "❌ معطلة"
    await query.message.edit_text(f"🚀 إشعارات دخول المستخدمين الآن: {status}")

# --- عرض عدد المستخدمين ---
async def users_count(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id

    if user_id != ADMIN_ID:
        await query.answer("❌ ليس لديك صلاحية لاستخدام هذه الميزة.", show_alert=True)
        return

    count = len(data["users"])
    await query.message.edit_text(f"📊 إجمالي عدد المستخدمين: {count}")

# --- إرسال إذاعة ---
async def broadcast(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    user_id = query.from_user.id

    if user_id != ADMIN_ID:
        await query.answer("❌ ليس لديك صلاحية لاستخدام هذه الميزة.", show_alert=True)
        return

    await query.message.edit_text("✍️ **أرسل الآن نص الإذاعة**")
    context.user_data["waiting_for_broadcast"] = True

async def handle_broadcast(update: Update, context: CallbackContext) -> None:
    if context.user_data.get("waiting_for_broadcast", False) and update.message.from_user.id == ADMIN_ID:
        message_text = update.message.text
        sent_count = 0

        for user in data["users"]:
            try:
                await context.bot.send_message(chat_id=user["id"], text=f"📢 **إعلان جديد:**\n\n{message_text}", parse_mode="Markdown")
                sent_count += 1
            except:
                pass  # إذا فشل الإرسال لبعض المستخدمين

        await update.message.reply_text(f"✅ تم إرسال الإذاعة إلى {sent_count} مستخدم.")
        context.user_data["waiting_for_broadcast"] = False

# --- ربط الأوامر ومعالجات الأحداث ---
def main():
    app = Application.builder().token(TOKEN).build()

    # أوامر
    app.add_handler(CommandHandler("start", start))

    # معالجة الضغط على أزرار لوحة التحكم
    app.add_handler(CallbackQueryHandler(panel, pattern="panel"))
    app.add_handler(CallbackQueryHandler(toggle_notify, pattern="toggle_notify"))
    app.add_handler(CallbackQueryHandler(users_count, pattern="users_count"))
    app.add_handler(CallbackQueryHandler(broadcast, pattern="broadcast"))

    # معالجة الرسائل النصية
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_broadcast))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, send_separator))

    print("🚀 البوت يعمل الآن...")
    app.run_polling()

if __name__ == "__main__":
    main()