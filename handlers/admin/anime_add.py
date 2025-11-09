from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database import load_data, save_data
from keyboards import admin_menu
from config import STORAGE_CHANNEL

async def handle_confirm_episodes_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yangi anime qo'shishni tasdiqlash (KeyboardButton)"""
    user_id = update.effective_user.id
    from handlers.admin_panel import user_states
    
    if user_id not in user_states:
        await update.message.reply_text("❌ Xatolik yuz berdi!")
        return
    
    state_data = user_states[user_id]
    episodes = state_data.get("episodes", [])
    
    if not episodes:
        await update.message.reply_text("❌ Hech qanday qism yuklanmagan!")
        return
    
    episode_count = len(episodes)
    
    # State o'zgartirish
    user_states[user_id]["state"] = "anime_ready"
    
    # Yuborish tugmasi
    keyboard = [
        [KeyboardButton("✅ Yuborish")],
        [KeyboardButton("🔙 Orqaga")]
    ]
    
    await update.message.reply_text(
        f"✅ Jami {episode_count} ta qism saqlandi!\n\n"
        f"Kanalga Post yuborilsinmi ❗️",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def handle_send_new_anime_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yangi animeni kanalga yuborish (KeyboardButton)"""
    user_id = update.effective_user.id
    from handlers.admin_panel import user_states
    
    if user_id not in user_states:
        await update.message.reply_text("❌ Xatolik yuz berdi!")
        return
    
    state_data = user_states[user_id]
    anime_name = state_data.get("anime_name")
    post_message_id = state_data.get("post_message_id")
    episodes = state_data.get("episodes", [])
    is_hentai = state_data.get("is_hentai", False)
    
    # Bazaga qo'shish
    data = load_data()
    
    import time
    anime_id = str(int(time.time()))
    
    anime_info = {
        "name": anime_name,
        "post_id": post_message_id,
        "episodes": episodes,
        "episode_count": len(episodes)
    }
    
    if is_hentai:
        data["hentai"][anime_id] = anime_info
    else:
        data["animes"][anime_id] = anime_info
    
    save_data(data)
    
    # Kanalga yuborish
    try:
        main_channels = data.get("main_channels", [])
        
        bot_me = await context.bot.get_me()
        bot_username = bot_me.username
        
        watch_url = f"https://t.me/{bot_username}?start=watch_{anime_id}" if not is_hentai else f"https://t.me/{bot_username}?start=watchh_{anime_id}"
        
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton("📺 Tomosha qilish", url=watch_url)
        ]])
        
        for channel_id in main_channels:
            await context.bot.copy_message(
                chat_id=channel_id,
                from_chat_id=STORAGE_CHANNEL,
                message_id=post_message_id,
                reply_markup=keyboard
            )
        
        await update.message.reply_text(
            f"✅ {anime_name} muvaffaqiyatli qo'shildi!\n"
            f"📺 Qismlar: {len(episodes)} ta",
            reply_markup=admin_menu()
        )
        
        del user_states[user_id]
        
    except Exception as e:
        await update.message.reply_text(f"❌ Xato: {str(e)}", reply_markup=admin_menu())
