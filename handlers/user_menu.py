from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from database import load_data
from keyboards import back_to_user
from utils import generate_referral_link

async def handle_search(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    from handlers.admin_panel import user_states
    user_states[user_id] = {"state": "searching_anime"}
    
    await query.edit_message_text(
        "🔍 Anime nomini kiriting:",
        reply_markup=back_to_user()
    )

async def handle_profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = query.from_user.id
    data = load_data()
    
    referral_count = len(data["referrals"].get(str(user_id), []))
    is_vip = user_id in data["vip_users"]
    
    bot = await context.bot.get_me()
    ref_link = generate_referral_link(bot.username, user_id)
    
    profile_text = f"""
👤 Profil

🆔 ID: {user_id}
⭐ Status: {'VIP' if is_vip else 'Oddiy'}
👥 Referal: {referral_count}/6

🎁 6 ta do'stni taklif qiling va 1 oy VIP oling!

🔗 Sizning referral havolangiz:
{ref_link}
"""
    
    keyboard = [
        [InlineKeyboardButton("📤 Ulashish", url=f"https://t.me/share/url?url={ref_link}&text=AniVoid botiga qo'shiling!")],
        [InlineKeyboardButton("🔙 Orqaga", callback_data="user_menu")]
    ]
    
    await query.edit_message_text(
        profile_text,
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def handle_vip_info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = load_data()
    vip_message = data.get("vip_message", "⭐ VIP haqida ma'lumot hali kiritilmagan")
    
    await query.edit_message_text(
        vip_message,
        reply_markup=back_to_user()
    )

async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    data = load_data()
    contact_message = data.get("contact_message", "📞 Bog'lanish ma'lumotlari hali kiritilmagan")
    
    await query.edit_message_text(
        contact_message,
        reply_markup=back_to_user()
    )
