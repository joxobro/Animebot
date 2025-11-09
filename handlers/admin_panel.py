from telegram import Update
from telegram.ext import ContextTypes
from database import load_data, save_data, is_admin, get_stats
from keyboards import admin_menu, back_to_admin, confirm_episodes, anime_manage_buttons, pagination_buttons
from config import STORAGE_CHANNEL

user_states = {}

async def handle_add_anime(update: Update, context: ContextTypes.DEFAULT_TYPE, is_hentai=False):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_states[user_id] = {
        "state": "waiting_anime_name",
        "is_hentai": is_hentai
    }
    
    await query.edit_message_text(
        "📝 Anime nomini kiriting:",
        reply_markup=back_to_admin()
    )

async def handle_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    stats = get_stats()
    await query.edit_message_text(stats, reply_markup=back_to_admin())

async def handle_ongoing(update: Update, context: ContextTypes.DEFAULT_TYPE, page=1):
    query = update.callback_query
    await query.answer()
    
    data = load_data()
    animes = list(data["animes"].items())
    
    if not animes:
        await query.edit_message_text(
            "📺 Hozircha animelar yo'q",
            reply_markup=back_to_admin()
        )
        return
    
    items_per_page = 10
    total_pages = (len(animes) + items_per_page - 1) // items_per_page
    start_idx = (page - 1) * items_per_page
    end_idx = start_idx + items_per_page
    
    keyboard = []
    for anime_id, anime_data in animes[start_idx:end_idx]:
        keyboard.append([{
            "text": f"☘️ {anime_data['name']}",
            "callback_data": f"view_anime_{anime_id}"
        }])
    
    if total_pages > 1:
        nav_row = []
        if page > 1:
            nav_row.append({"text": "◀️ Orqaga", "callback_data": f"ongoing_page_{page-1}"})
        nav_row.append({"text": f"{page}/{total_pages}", "callback_data": "page_info"})
        if page < total_pages:
            nav_row.append({"text": "Keyingi ▶️", "callback_data": f"ongoing_page_{page+1}"})
        keyboard.append(nav_row)
    
    keyboard.append([{"text": "🔙 Orqaga", "callback_data": "admin_menu"}])
    
    from telegram import InlineKeyboardMarkup
    await query.edit_message_text(
        f"📺 Animelar ({len(animes)} ta):",
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    user_states[user_id] = {"state": "waiting_broadcast"}
    
    await query.edit_message_text(
        "📢 Reklama xabarini yuboring:",
        reply_markup=back_to_admin()
    )
