from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import load_data
from config import STORAGE_CHANNEL
from keyboards import user_menu

try:
    from rapidfuzz import fuzz
    USE_FUZZY = True
except ImportError:
    USE_FUZZY = False

def simple_match(query: str, text: str) -> int:
    """Oddiy matching algoritmi"""
    query = query.lower()
    text = text.lower()
    
    if query == text:
        return 100
    if text.startswith(query):
        return 90
    if query in text:
        return 80
    
    query_words = query.split()
    text_words = text.split()
    
    matches = 0
    for q_word in query_words:
        for t_word in text_words:
            if q_word in t_word or t_word in q_word:
                matches += 1
                break
    
    if matches > 0:
        ratio = (matches / len(query_words)) * 70
        return int(ratio)
    
    return 0

async def search_anime(update: Update, context: ContextTypes.DEFAULT_TYPE, query: str):
    """Anime qidirish"""
    data = load_data()
    animes = data.get("animes", {})
    
    results = []
    
    for anime_id, anime_data in animes.items():
        anime_name = anime_data["name"]
        
        # Fuzzy yoki simple matching
        if USE_FUZZY:
            ratio = fuzz.partial_ratio(query.lower(), anime_name.lower())
        else:
            ratio = simple_match(query, anime_name)
        
        if ratio >= 70:
            results.append((anime_id, anime_data, ratio))
    
    if results:
        results.sort(key=lambda x: x[2], reverse=True)
        best_match = results[0]
        
        anime_id = best_match[0]
        anime_info = best_match[1]
        
        try:
            bot_me = await context.bot.get_me()
            bot_username = bot_me.username
            watch_url = f"https://t.me/{bot_username}?start=watch_{anime_id}"
            
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("📺 Tomosha qilish", url=watch_url)
            ]])
            
            await context.bot.copy_message(
                chat_id=update.effective_user.id,
                from_chat_id=STORAGE_CHANNEL,
                message_id=anime_info["post_id"],
                reply_markup=keyboard
            )
            await update.message.reply_text("✅ Anime topildi!", reply_markup=user_menu())
        except Exception as e:
            await update.message.reply_text(f"❌ Xato: {str(e)}", reply_markup=user_menu())
    else:
        await update.message.reply_text("❌ Anime topilmadi!", reply_markup=user_menu())
