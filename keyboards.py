from telegram import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup

def admin_menu():
    keyboard = [
        [KeyboardButton("➕ Anime qo'shish"), KeyboardButton("📺 Ongoing")],
        [KeyboardButton("📊 Statistika"), KeyboardButton("📢 Reklama")],
        [KeyboardButton("👤 Admin"), KeyboardButton("📱 Kanal")],
        [KeyboardButton("⭐ Vip"), KeyboardButton("🔞 Hentai")],
        [KeyboardButton("⚙️ Sozlamalar")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def user_menu():
    keyboard = [
        [KeyboardButton("🔍 Anime qidirish")],
        [KeyboardButton("⭐ Vip"), KeyboardButton("👤 Profil")],
        [KeyboardButton("📞 Bog'lanish")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def back_to_admin():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Orqaga", callback_data="admin_menu")]])

def back_to_user():
    return InlineKeyboardMarkup([[InlineKeyboardButton("🔙 Orqaga", callback_data="user_menu")]])

def watch_button(anime_id, is_hentai=False):
    """Tomosha qilish tugmasi - URL bilan"""
    # Bot username kerak bo'ladi, shuning uchun bu funksiya async bo'lishi kerak
    # Lekin hozircha static qilib qo'yamiz
    callback = f"watch_hentai_{anime_id}" if is_hentai else f"watch_{anime_id}"
    return InlineKeyboardMarkup([[InlineKeyboardButton("📺 Tomosha qilish", callback_data=callback)]])

def confirm_episodes():
    """Tasdiqlash tugmasi - KeyboardButton"""
    keyboard = [
        [KeyboardButton("✅ Tasdiqlash"), KeyboardButton("❌ Bekor qilish")],
        [KeyboardButton("🔙 Orqaga")]
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

def broadcast_confirm():
    return InlineKeyboardMarkup([[InlineKeyboardButton("✅ Yuborilsin", callback_data="send_broadcast")]])

def anime_manage_buttons(anime_id, is_hentai=False):
    prefix = "hentai" if is_hentai else "anime"
    keyboard = [
        [InlineKeyboardButton("➕ Qism qo'shish", callback_data=f"add_episode_{prefix}_{anime_id}")],
        [InlineKeyboardButton("🗑 O'chirish", callback_data=f"delete_{prefix}_{anime_id}")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="ongoing")]
    ]
    return InlineKeyboardMarkup(keyboard)

def pagination_buttons(page, total_pages, callback_prefix):
    keyboard = []
    nav_buttons = []
    
    if page > 1:
        nav_buttons.append(InlineKeyboardButton("◀️ Orqaga", callback_data=f"{callback_prefix}_page_{page-1}"))
    
    nav_buttons.append(InlineKeyboardButton(f"{page}/{total_pages}", callback_data="page_info"))
    
    if page < total_pages:
        nav_buttons.append(InlineKeyboardButton("Keyingi ▶️", callback_data=f"{callback_prefix}_page_{page+1}"))
    
    keyboard.append(nav_buttons)
    keyboard.append([InlineKeyboardButton("🔙 Orqaga", callback_data="admin_menu")])
    
    return InlineKeyboardMarkup(keyboard)

def settings_menu():
    keyboard = [
        [InlineKeyboardButton("⭐ Vip", callback_data="settings_vip")],
        [InlineKeyboardButton("📞 Bog'lanish", callback_data="settings_contact")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="admin_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def channel_type_menu():
    keyboard = [
        [InlineKeyboardButton("✅ Asosiy kanal", callback_data="main_channel_menu")],
        [InlineKeyboardButton("📱 Kanallar", callback_data="channels_menu")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="admin_menu")]
    ]
    return InlineKeyboardMarkup(keyboard)

def admin_add_menu():
    keyboard = [
        [InlineKeyboardButton("👑 Bot egaligi", callback_data="transfer_ownership")],
        [InlineKeyboardButton("👤 Admin", callback_data="add_admin")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="admin_manage")]
    ]
    return InlineKeyboardMarkup(keyboard)
