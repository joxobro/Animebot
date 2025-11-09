from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ContextTypes
from database import load_data, save_data
from config import STORAGE_CHANNEL, MAIN_CHANNEL_USERNAME
from keyboards import admin_menu

async def handle_ongoing(update, context, page=1):
    query = update.callback_query if update.callback_query else None
    message = update.callback_query.message if query else update.message
    
    data = load_data()
    animes = list(data["animes"].items())
    
    if not animes:
        text = "📺 Hozircha animelar yo'q"
        if query:
            await query.answer()
            await query.edit_message_text(text)
        else:
            await message.reply_text(text, reply_markup=admin_menu())
        return
    
    # Mavjud animelarni tekshirish
    valid_animes = []
    for anime_id, anime_data in animes:
        try:
            await context.bot.forward_message(
                chat_id=STORAGE_CHANNEL,
                from_chat_id=STORAGE_CHANNEL,
                message_id=anime_data["post_id"]
            )
            valid_animes.append((anime_id, anime_data))
        except:
            del data["animes"][anime_id]
    
    save_data(data)
    
    if not valid_animes:
        text = "📺 Hozircha animelar yo'q"
        if query:
            await query.answer()
            await query.edit_message_text(text)
        else:
            await message.reply_text(text, reply_markup=admin_menu())
        return
    
    # Keyboard yaratish
    keyboard = []
    for anime_id, anime_data in valid_animes[:10]:
        keyboard.append([KeyboardButton(f"☘️ {anime_data['name']}")])
    
    keyboard.append([KeyboardButton("🔙 Orqaga")])
    
    text = f"📺 Animelar ({len(valid_animes)} ta):\n\nQism qo'shish uchun anime nomini tanlang:"
    
    await message.reply_text(
        text,
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def handle_anime_selected(update: Update, context: ContextTypes.DEFAULT_TYPE, anime_name: str):
    """Anime tanlanganda qism qo'shish"""
    user_id = update.effective_user.id
    data = load_data()
    
    found_id = None
    found_anime = None
    
    for anime_id, anime_data in data["animes"].items():
        if f"☘️ {anime_data['name']}" == anime_name:
            found_id = anime_id
            found_anime = anime_data
            break
    
    if not found_anime:
        await update.message.reply_text("❌ Anime topilmadi!", reply_markup=admin_menu())
        return
    
    from handlers.admin_panel import user_states
    user_states[user_id] = {
        "state": "adding_episodes",
        "anime_id": found_id,
        "anime_name": found_anime["name"],
        "new_episodes": [],
        "current_episode_count": len(found_anime["episodes"])
    }
    
    current_count = len(found_anime["episodes"])
    
    # Tasdiqlash va Bekor qilish tugmalari
    keyboard = [
        [KeyboardButton("✅ Tasdiqlash"), KeyboardButton("❌ Bekor qilish")],
        [KeyboardButton("🔙 Orqaga")]
    ]
    
    await update.message.reply_text(
        f"📺 {found_anime['name']}\n\n"
        f"Hozirda {current_count} ta qism mavjud.\n"
        f"{current_count + 1}-qismdan boshlab videolarni yuboring.\n\n"
        f"Barcha qismlarni yuborganingizdan keyin '✅ Tasdiqlash' tugmasini bosing.",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    )

async def handle_confirm_new_episodes_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Yangi qismlarni tasdiqlash (KeyboardButton)"""
    user_id = update.effective_user.id
    from handlers.admin_panel import user_states
    
    if user_id not in user_states:
        await update.message.reply_text("❌ Xatolik yuz berdi!")
        return
    
    state_data = user_states[user_id]
    new_episodes = state_data.get("new_episodes", [])
    
    if not new_episodes:
        await update.message.reply_text("❌ Hech qanday qism yuklanmagan!")
        return
    
    episode_count = len(new_episodes)
    
    # State o'zgartirish
    user_states[user_id]["state"] = "episodes_ready"
    
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

async def handle_send_to_channel_keyboard(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Postni kanalga yuborish (KeyboardButton)"""
    user_id = update.effective_user.id
    from handlers.admin_panel import user_states
    
    if user_id not in user_states:
        await update.message.reply_text("❌ Xatolik yuz berdi!")
        return
    
    state_data = user_states[user_id]
    new_episodes = state_data.get("new_episodes", [])
    anime_id = state_data.get("anime_id")
    
    # Bazaga qo'shish
    data = load_data()
    anime_data = data["animes"][anime_id]
    anime_data["episodes"].extend(new_episodes)
    anime_data["episode_count"] = len(anime_data["episodes"])
    save_data(data)
    
    # Kanalga yuborish
    try:
        main_channels = data.get("main_channels", [])
        
        bot_me = await context.bot.get_me()
        bot_username = bot_me.username
        watch_url = f"https://t.me/{bot_username}?start=watch_{anime_id}"
        
        from telegram import InlineKeyboardButton, InlineKeyboardMarkup
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton("📺 Tomosha qilish", url=watch_url)
        ]])
        
        for channel_id in main_channels:
            await context.bot.copy_message(
                chat_id=channel_id,
                from_chat_id=STORAGE_CHANNEL,
                message_id=anime_data["post_id"],
                reply_markup=keyboard
            )
        
        await update.message.reply_text(
            f"✅ {len(new_episodes)} ta qism muvaffaqiyatli qo'shildi!\n"
            f"📺 Jami qismlar: {anime_data['episode_count']} ta",
            reply_markup=admin_menu()
        )
        
        del user_states[user_id]
        
    except Exception as e:
        await update.message.reply_text(f"❌ Xato: {str(e)}", reply_markup=admin_menu())
