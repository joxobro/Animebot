from telegram import Update, InlineQueryResultArticle, InputTextMessageContent, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import load_data
import uuid

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

async def handle_inline_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Inline qidiruv - @AniVoidXbot Naruto"""
    query = update.inline_query.query
    
    if not query or len(query) < 2:
        return
    
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
        
        if ratio >= 60:
            bot_username = context.bot.username
            watch_url = f"https://t.me/{bot_username}?start=watch_{anime_id}"
            
            keyboard = InlineKeyboardMarkup([[
                InlineKeyboardButton("📺 Tomosha qilish", url=watch_url)
            ]])
            
            result = InlineQueryResultArticle(
                id=str(uuid.uuid4()),
                title=f"☘️ {anime_name}",
                description=f"📺 {anime_data.get('episode_count', 0)} ta qism",
                input_message_content=InputTextMessageContent(
                    f"☘️ {anime_name}\n\n📺 Qismlar: {anime_data.get('episode_count', 0)} ta\n\n"
                    f"Tomosha qilish uchun quyidagi tugmani bosing:"
                ),
                reply_markup=keyboard
            )
            
            results.append((result, ratio))
    
    results.sort(key=lambda x: x[1], reverse=True)
    results = [r[0] for r in results[:50]]
    
    await update.inline_query.answer(results, cache_time=10)
