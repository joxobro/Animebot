from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database import load_data
from keyboards import admin_menu

async def start_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reklama boshlash"""
    query = update.callback_query if update.callback_query else None
    user_id = update.effective_user.id
    
    from handlers.admin_panel import user_states
    user_states[user_id] = {"state": "waiting_broadcast"}
    
    # Tasdiqlash va Orqaga tugmalari
    keyboard = [
        [KeyboardButton("🔙 Orqaga")]
    ]
    
    text = "📢 Reklama xabaringizni kiriting:\n\nRasm, video, audio, fayl yoki matn yuborishingiz mumkin."
    
    if query:
        await query.answer()
        await query.message.reply_text(
            text,
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )
    else:
        await update.message.reply_text(
            text,
            reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
        )

async def handle_broadcast_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Reklama xabarini qabul qilish"""
    user_id = update.effective_user.id
    
    from handlers.admin_panel import user_states
    user_states[user_id] = {
        "state": "broadcast_ready",
        "message_id": update.message.message_id,
        "chat_id": update.effective_chat.id
    }
    
    # Tasdiqlash tugmasi
    keyboard = [
        [InlineKeyboardButton("✅ Yuborish", callback_data="send_broadcast")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="admin_menu")]
    ]
    
    await update.message.reply_text(
        "✅ Reklama xabari qabul qilindi!\n\n"
        "Barcha foydalanuvchilarga yuborilsinmi?",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def send_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Barcha foydalanuvchilarga yuborish"""
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    from handlers.admin_panel import user_states
    
    if user_id not in user_states:
        await query.message.reply_text("❌ Xatolik yuz berdi!")
        return
    
    state_data = user_states[user_id]
    message_id = state_data.get("message_id")
    chat_id = state_data.get("chat_id")
    
    data = load_data()
    users = list(data["users"].keys())
    
    await query.edit_message_text("📢 Xabar yuborilmoqda...")
    
    success = 0
    failed = 0
    
    for user_id_str in users:
        try:
            await context.bot.copy_message(
                chat_id=int(user_id_str),
                from_chat_id=chat_id,
                message_id=message_id
            )
            success += 1
        except:
            failed += 1
    
    await query.message.reply_text(
        f"✅ Reklama yuborildi!\n\n"
        f"📊 Muvaffaqiyatli: {success}\n"
        f"❌ Xatolik: {failed}",
        reply_markup=admin_menu()
    )
    
    del user_states[user_id]
